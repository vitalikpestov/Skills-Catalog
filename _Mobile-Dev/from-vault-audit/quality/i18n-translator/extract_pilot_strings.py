"""Extract 50 representative strings for FR+ES pilot translation."""
import json, re
from pathlib import Path

XCSTRINGS = Path("/Users/vitalik/Documents/Projects/MobileApp/DoseSync/DoseSync/Localizable.xcstrings")

with open(XCSTRINGS) as f:
    data = json.load(f)

strings = data["strings"]
candidates = []

for key, val in strings.items():
    locs = val.get("localizations", {})
    if "en" not in locs:
        continue
    en_unit = locs["en"].get("stringUnit", {})
    en_val = en_unit.get("value", "")
    if not en_val.strip():
        continue
    # Skip super-short symbolic strings
    if len(en_val) < 3 and not en_val.isalnum():
        continue
    # Already fully translated to both → skip (no calibration value)
    if "fr" in locs and "es" in locs:
        fr_state = locs["fr"]["stringUnit"].get("state", "")
        es_state = locs["es"]["stringUnit"].get("state", "")
        if fr_state == "translated" and es_state == "translated":
            continue
    candidates.append({
        "key": key,
        "en": en_val,
        "comment": val.get("comment", ""),
        "has_fr": "fr" in locs,
        "has_es": "es" in locs,
        "len_en": len(en_val),
    })

# Categorize
def categorize(c):
    k, en, cmt = c["key"].lower(), c["en"].lower(), c["comment"].lower()
    haystack = f"{k} {cmt}".lower()
    # CTA
    if any(w in haystack for w in ["button", "cta", "primary action"]) or \
       k.startswith(("button_","btn_","cta_")) or \
       en in ["confirm","skip","cancel","save","done","continue","next","back","get started","add","delete"] or \
       any(en.startswith(w + " ") for w in ["confirm","add","skip","save","get","start","tap","try"]):
        return "CTA"
    # Push
    if any(w in haystack for w in ["push", "notification body", "notification title", "alert body"]) or \
       k.startswith(("push_","notification_","notif_")):
        return "PUSH"
    # Onboarding
    if any(w in haystack for w in ["onboard", "welcome", "trust message", "step ", "scenario"]) or \
       k.startswith(("welcome_","onboarding_","ob_","step_","trust_")):
        return "ONBOARDING"
    # Error
    if any(w in haystack for w in ["error", "failed", "retry", "offline", "connection", "sync error"]) or \
       k.startswith(("error_","err_")) or \
       any(en.startswith(w) for w in ["Couldn't","Could not","Failed","Unable","Sorry"]):
        return "ERROR"
    # Edge case (empty, paywall CTA, legal, a11y)
    if any(w in haystack for w in ["empty", "paywall", "legal", "accessibility", "voiceover", "subscription", "trial"]) or \
       k.startswith(("empty_","paywall_","legal_","a11y_","accessibility_")):
        return "EDGE"
    return "OTHER"

for c in candidates:
    c["cat"] = categorize(c)

# Group by category
by_cat = {"CTA": [], "ONBOARDING": [], "PUSH": [], "ERROR": [], "EDGE": []}
for c in candidates:
    if c["cat"] in by_cat:
        by_cat[c["cat"]].append(c)

print("=== Candidate counts per category ===")
for cat, items in by_cat.items():
    print(f"  {cat}: {len(items)}")
print(f"  TOTAL eligible: {sum(len(v) for v in by_cat.values())}")
print(f"  OTHER (uncategorized eligible): {sum(1 for c in candidates if c['cat']=='OTHER')}")
print(f"  Total candidates (en exists, fr or es missing): {len(candidates)}")

# Sort each category by length (mid-length strings = most representative — too short = trivial, too long = edge case)
import statistics
for cat in by_cat:
    items = by_cat[cat]
    if not items:
        continue
    items.sort(key=lambda x: x["len_en"])
    # Pick 10: mix of short, medium, long for representativeness
    if len(items) >= 10:
        # 3 short, 4 medium, 3 long
        n = len(items)
        picks = items[:3] + items[n//2-2:n//2+2] + items[-3:]
        # Dedup
        seen = set()
        unique = []
        for p in picks:
            if p["key"] not in seen:
                seen.add(p["key"])
                unique.append(p)
        by_cat[cat] = unique[:10]
    # else take all

# Output 50-string JSON
out = []
for cat in ["CTA","ONBOARDING","PUSH","ERROR","EDGE"]:
    for c in by_cat[cat]:
        out.append({
            "key": c["key"],
            "category": cat,
            "en": c["en"],
            "comment": c["comment"],
            "has_existing_fr": c["has_fr"],
            "has_existing_es": c["has_es"],
        })

print(f"\n=== Final pilot selection: {len(out)} strings ===")
for cat in ["CTA","ONBOARDING","PUSH","ERROR","EDGE"]:
    n = sum(1 for o in out if o["category"]==cat)
    print(f"  {cat}: {n}")

OUT_FILE = Path("/tmp/i18n-pilot-50-input.json")
with open(OUT_FILE, "w") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print(f"\nWrote {OUT_FILE}")
