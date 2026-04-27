"""GetSales API tools — LinkedIn outreach flows with node tree builder."""
import re
from typing import Optional

import httpx

BASE_URL = "https://api.getsales.io/api/v1"

# ---------------------------------------------------------------------------
# Timing presets (seconds) — from top-performing flows across 414 live flows
# ---------------------------------------------------------------------------

TIMING_STANDARD = {
    "accept_wait": 1 * 3600,          # 1h after accept before MSG1
    "msg2_delay": 2 * 86400,          # 2d after MSG1
    "msg3_delay": 5 * 86400,          # 5d after MSG2
    "non_accept_timeout": 3 * 86400,  # 3d before non-accept branch
    "withdraw_delay": 15 * 86400,     # 15d before withdraw
}

TIMING_NETWORKING = {
    "accept_wait": 1 * 86400,         # 1d (softer)
    "msg2_delay": 3 * 86400,
    "msg3_delay": 5 * 86400,
    "non_accept_timeout": 3 * 86400,
    "withdraw_delay": 10 * 86400,
}

TIMING_VOLUME = {
    "accept_wait": 1 * 3600,          # 1h
    "msg2_delay": 1 * 86400,          # 1d — faster cadence
    "msg3_delay": 2 * 86400,
    "non_accept_timeout": 21 * 86400, # 21d — long acceptance window
    "withdraw_delay": 15 * 86400,
}

FLOW_TYPE_TIMING = {
    "standard": TIMING_STANDARD,
    "networking": TIMING_NETWORKING,
    "product": TIMING_STANDARD,
    "volume": TIMING_VOLUME,
    "event": TIMING_NETWORKING,
}


def build_node_tree(
    connection_note: str,
    messages: list[str],
    timing: dict[str, int] | None = None,
) -> list[dict]:
    """Build a GetSales flow node tree from messages and timing.

    Implements the "God Level" flow:
      Trigger → connection_request → acceptance_trigger (with timeout)
      ACCEPTED: tag → wait → MSG1 → engagement → wait → MSG2 → ... → end
      NOT-ACCEPTED: wait → like → visit → endorse → withdraw → tag → end
    """
    if timing is None:
        timing = TIMING_STANDARD

    nodes: list[dict] = []
    next_id = 1
    end_id = next_id
    next_id += 1

    nodes.append({"id": end_id, "before": [], "after": [], "type": "end",
                   "automation": "auto", "payload": [], "delay_in_seconds": 0})

    trigger1_id = next_id + 1
    conn_req_id = next_id + 2
    trigger2_id = next_id + 3
    next_id += 4

    # ── ACCEPTED branch ──
    accepted_nodes: list[dict] = []
    current_id = next_id

    tag_id = current_id
    accepted_nodes.append({"id": tag_id, "before": [], "after": [{"node_id": current_id + 1, "branch_id": 1}],
                            "type": "gs_add_tag", "automation": "auto", "payload": {"tag_uuid": "auto_accepted"}, "delay_in_seconds": 0})
    current_id += 1

    wait1_id = current_id
    accepted_nodes.append({"id": wait1_id, "before": [{"node_id": tag_id, "branch_id": 1}],
                            "after": [{"node_id": current_id + 1, "branch_id": 1}],
                            "type": "util_timer", "automation": "auto", "payload": {"wait_time": timing["accept_wait"]}, "delay_in_seconds": 0})
    current_id += 1

    msg_delays = [timing.get("msg2_delay", 2 * 86400), timing.get("msg3_delay", 5 * 86400)]
    engagement_actions = ["linkedin_visit_profile", "linkedin_like_latest_post", "linkedin_endorse_skills"]

    prev_id = wait1_id
    for i, msg_text in enumerate(messages):
        is_last = i == len(messages) - 1
        msg_id = current_id
        accepted_nodes.append({"id": msg_id, "before": [{"node_id": prev_id, "branch_id": 1}],
                                "after": [{"node_id": end_id, "branch_id": 1}] if is_last else [{"node_id": current_id + 1, "branch_id": 1}],
                                "type": "linkedin_send_message", "automation": "auto", "payload": {"template": msg_text}, "delay_in_seconds": 0})
        current_id += 1
        if is_last:
            break
        engage_type = engagement_actions[i % len(engagement_actions)]
        engage_id = current_id
        accepted_nodes.append({"id": engage_id, "before": [{"node_id": msg_id, "branch_id": 1}],
                                "after": [{"node_id": current_id + 1, "branch_id": 1}],
                                "type": engage_type, "automation": "auto", "payload": [], "delay_in_seconds": 0})
        current_id += 1
        if i < len(msg_delays):
            delay_id = current_id
            accepted_nodes.append({"id": delay_id, "before": [{"node_id": engage_id, "branch_id": 1}],
                                    "after": [{"node_id": current_id + 1, "branch_id": 1}],
                                    "type": "util_timer", "automation": "auto", "payload": {"wait_time": msg_delays[i]}, "delay_in_seconds": 0})
            current_id += 1
            prev_id = delay_id
        else:
            prev_id = engage_id

    # ── NOT-ACCEPTED branch ──
    non_accept_nodes: list[dict] = []
    na_start = current_id
    na_steps = [
        ("util_timer", {"wait_time": 86400}),
        ("linkedin_like_latest_post", []),
        ("util_timer", {"wait_time": 2 * 86400}),
        ("linkedin_visit_profile", []),
        ("util_timer", {"wait_time": 3 * 86400}),
        ("linkedin_endorse_skills", []),
        ("util_timer", {"wait_time": timing["withdraw_delay"]}),
        ("linkedin_withdraw_connection_request", []),
        ("gs_add_tag", {"tag_uuid": "auto_not_accepted"}),
        ("end", []),
    ]
    for j, (ntype, payload) in enumerate(na_steps):
        nid = current_id
        before = [{"node_id": current_id - 1, "branch_id": 1}] if j > 0 else []
        after = [{"node_id": current_id + 1, "branch_id": 1}] if j < len(na_steps) - 1 else []
        non_accept_nodes.append({"id": nid, "before": before, "after": after, "type": ntype,
                                  "automation": "auto", "payload": payload, "delay_in_seconds": 0})
        current_id += 1

    # ── Assemble triggers ──
    first_accepted = tag_id
    trigger1 = {"id": trigger1_id, "before": [], "after": [{"node_id": conn_req_id, "branch_id": 1}, {"node_id": end_id, "branch_id": 2}],
                 "type": "trigger_linkedin_connection_request_accepted", "automation": "auto",
                 "payload": {"subtasks": [{"id": trigger1_id + 100, "type": "util_timer", "after": [], "before": [], "payload": {"wait_time": 60}, "automation": "auto"}]},
                 "delay_in_seconds": 0}
    conn_req = {"id": conn_req_id, "before": [{"node_id": trigger1_id, "branch_id": 1}], "after": [{"node_id": trigger2_id, "branch_id": 1}],
                 "type": "linkedin_send_connection_request", "automation": "auto",
                 "payload": {"template": connection_note, "note": connection_note, "fallback_send": False}, "delay_in_seconds": 0}
    trigger2 = {"id": trigger2_id, "before": [{"node_id": conn_req_id, "branch_id": 1}],
                 "after": [{"node_id": first_accepted, "branch_id": 1}, {"node_id": na_start, "branch_id": 2}],
                 "type": "trigger_linkedin_connection_request_accepted", "automation": "auto",
                 "payload": {"subtasks": [{"id": trigger2_id + 100, "type": "util_timer", "after": [], "before": [], "payload": {"wait_time": timing["non_accept_timeout"]}, "automation": "auto"}]},
                 "delay_in_seconds": 0}

    accepted_nodes[0]["before"] = [{"node_id": trigger2_id, "branch_id": 1}]
    non_accept_nodes[0]["before"] = [{"node_id": trigger2_id, "branch_id": 2}]

    all_nodes = [trigger1, conn_req, trigger2] + accepted_nodes + non_accept_nodes
    end_before = []
    for n in all_nodes:
        for a in n.get("after", []):
            if a["node_id"] == end_id:
                end_before.append({"node_id": n["id"], "branch_id": a["branch_id"]})
    nodes[0]["before"] = end_before
    return [nodes[0]] + all_nodes


async def _gs_request(method: str, path: str, api_key: str, team_id: str, data: dict | None = None) -> dict | None:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Team-Id": team_id,
        "Content-Type": "application/json",
    }
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            if method == "GET":
                resp = await client.get(f"{BASE_URL}{path}", headers=headers)
            else:
                resp = await client.post(f"{BASE_URL}{path}", headers=headers, json=data or {})
            resp.raise_for_status()
            return resp.json()
    except httpx.HTTPStatusError as exc:
        return {"_error": True, "status_code": exc.response.status_code,
                "detail": exc.response.text[:300]}
    except Exception as exc:
        return {"_error": True, "detail": str(exc)}


def _gs_failed(data: dict | None) -> dict | None:
    """Return error dict if request failed, None if ok."""
    if data is None:
        return {"success": False, "error": "GetSales API returned no data"}
    if isinstance(data, dict) and data.get("_error"):
        return {"success": False, "error": f"GetSales API error: {data.get('detail', 'unknown')}"}
    return None


async def getsales_list_profiles(api_key: str, team_id: str) -> dict:
    data = await _gs_request("GET", "/linkedin-profiles", api_key, team_id)
    if err := _gs_failed(data):
        return err
    profiles = []
    for p in (data.get("data", []) if isinstance(data, dict) else []):
        profiles.append({
            "id": p.get("id"),
            "name": p.get("name", ""),
            "linkedin_url": p.get("linkedin_url", ""),
        })
    return {"success": True, "profiles": profiles}


async def getsales_create_flow(api_key: str, team_id: str, name: str, nodes: list[dict]) -> dict:
    data = await _gs_request("POST", "/flows", api_key, team_id, {"name": name, "nodes": nodes})
    if err := _gs_failed(data):
        return err
    return {"success": True, "flow_id": data.get("data", {}).get("id"), "name": name}


def _validate_linkedin_url(url: str) -> bool:
    """Check that a LinkedIn URL looks valid (profile or company)."""
    if not url:
        return False
    return bool(re.match(
        r"https?://(www\.)?linkedin\.com/(in|company|pub)/[a-zA-Z0-9\-_%]+",
        url.strip(),
    ))


async def getsales_add_leads(api_key: str, team_id: str, flow_id: int, leads: list[dict]) -> dict:
    invalid = [l for l in leads if not _validate_linkedin_url(l.get("linkedin_url", ""))]
    if invalid:
        bad_urls = [l.get("linkedin_url", "<empty>") for l in invalid[:5]]
        return {
            "success": False,
            "error": f"{len(invalid)} lead(s) have invalid LinkedIn URLs: {bad_urls}. "
                     "Each lead must have a valid linkedin_url (https://linkedin.com/in/...).",
        }
    data = await _gs_request("POST", f"/flows/{flow_id}/leads", api_key, team_id, {"leads": leads})
    if err := _gs_failed(data):
        return err
    return {"success": True, "flow_id": flow_id, "leads_added": len(leads)}


async def getsales_activate_flow(api_key: str, team_id: str, flow_id: int, confirm: str) -> dict:
    if confirm != "I confirm":
        return {"success": False, "error": "Must pass confirm='I confirm' to activate"}
    data = await _gs_request("POST", f"/flows/{flow_id}/activate", api_key, team_id)
    if err := _gs_failed(data):
        return err
    return {"success": True, "flow_id": flow_id, "status": "ACTIVE"}
