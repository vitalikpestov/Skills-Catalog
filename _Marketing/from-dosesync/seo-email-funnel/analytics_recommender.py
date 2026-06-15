from typing import Dict, List

PERSONA_SEGMENTS_MAP = {
    "sandwich_caregiver": {
        "resend_tag": "sandwich_caregiver",
        "posthog_property": "persona_sandwich_caregiver",
        "persona_label": "Sandwich Generation Caregiver",
    },
    "young_parent": {
        "resend_tag": "young_parent",
        "posthog_property": "persona_young_parent",
        "persona_label": "Young Parent",
    },
    "grandparent": {
        "resend_tag": "grandparent",
        "posthog_property": "persona_grandparent",
        "persona_label": "Grandparent",
    },
    "professional_caregiver": {
        "resend_tag": "professional_caregiver",
        "posthog_property": "persona_professional_caregiver",
        "persona_label": "Professional Caregiver",
    },
    "other": {
        "resend_tag": "caregiver_general",
        "posthog_property": "persona_general",
        "persona_label": "General Caregiver",
    },
}

CLUSTER_UTM_MAP = {
    "double_dosing":  "double-dosing",
    "grandparents":   "grandparents",
    "adhd_kids":      "adhd-kids",
    "burnout":        "caregiver-burnout",
    "other":          "medication-coordination",
}


def build_analytics_recommendations(question, email_funnel: Dict) -> Dict:
    persona_meta = PERSONA_SEGMENTS_MAP.get(
        question.persona_segment,
        PERSONA_SEGMENTS_MAP["other"]
    )
    utm_content = CLUSTER_UTM_MAP.get(question.topic_cluster, question.topic_cluster)

    segments = _build_segments(question, persona_meta)
    events = _build_events(question, email_funnel)
    utm_recs = _build_utm_recommendations(question, utm_content)

    return {
        "segments": segments,
        "events": events,
        "utm_recommendations": utm_recs,
        "resend_tags": [
            persona_meta["resend_tag"],
            f"cluster_{question.topic_cluster}",
            f"lang_{question.language}",
            "pre_launch_waitlist",
        ],
        "posthog_person_properties": {
            persona_meta["posthog_property"]: True,
            "lead_magnet_cluster": question.topic_cluster,
            "lead_magnet_language": question.language,
            "waitlist_source": f"blog_{question.id}",
        },
    }


def _build_segments(question, persona_meta: Dict) -> List[Dict]:
    return [
        {
            "name": f"Blog Opt-in — {persona_meta['persona_label']}",
            "platform": "Resend",
            "filter": f"tag = '{persona_meta['resend_tag']}' AND tag = 'pre_launch_waitlist'",
            "use_case": "Pre-launch nurture sequence targeting this specific persona",
        },
        {
            "name": f"Cluster — {question.topic_cluster}",
            "platform": "Resend",
            "filter": f"tag = 'cluster_{question.topic_cluster}'",
            "use_case": "Send cluster-specific content and launch broadcast",
        },
        {
            "name": f"Language — {question.language.upper()}",
            "platform": "Resend",
            "filter": f"tag = 'lang_{question.language}'",
            "use_case": "Locale-specific broadcasts and launch announcements",
        },
        {
            "name": "All Pre-Launch Waitlist",
            "platform": "Resend",
            "filter": "tag = 'pre_launch_waitlist'",
            "use_case": "Launch day broadcast to all subscribers regardless of persona",
        },
    ]


def _build_events(question, email_funnel: Dict) -> List[Dict]:
    trigger = email_funnel.get("trigger", f"optin_{question.id}")
    events = [
        {
            "event": "lead_magnet_optin",
            "platform": "PostHog",
            "properties": {
                "question_id": question.id,
                "topic_cluster": question.topic_cluster,
                "persona_segment": question.persona_segment,
                "language": question.language,
            },
            "trigger": "User submits opt-in form on blog article",
        },
        {
            "event": "email_sequence_started",
            "platform": "PostHog + Resend webhook",
            "properties": {"funnel_trigger": trigger},
            "trigger": "First email in sequence delivered",
        },
        {
            "event": "lead_magnet_downloaded",
            "platform": "PostHog",
            "properties": {"question_id": question.id},
            "trigger": "User clicks download link in delivery email",
        },
        {
            "event": "launch_email_opened",
            "platform": "Resend",
            "properties": {"campaign": "launch_2026_07_07"},
            "trigger": "User opens the launch broadcast email",
        },
        {
            "event": "launch_email_cta_clicked",
            "platform": "Resend + PostHog",
            "properties": {
                "campaign": "launch_2026_07_07",
                "persona": question.persona_segment,
                "cluster": question.topic_cluster,
            },
            "trigger": "User clicks App Store CTA in launch email",
        },
    ]
    return events


def _build_utm_recommendations(question, utm_content: str) -> List[Dict]:
    base = {
        "utm_source": "blog",
        "utm_medium": "organic",
        "utm_campaign": f"pre_launch_{question.topic_cluster}",
        "utm_content": utm_content,
    }
    return [
        {
            "placement": "Blog article — in-text DoseSync link",
            **base,
            "utm_term": question.id,
            "example": (
                f"https://dosesync.app?utm_source=blog&utm_medium=organic"
                f"&utm_campaign=pre_launch_{question.topic_cluster}"
                f"&utm_content={utm_content}&utm_term={question.id}"
            ),
        },
        {
            "placement": "Lead magnet delivery email — App Store CTA",
            "utm_source": "email",
            "utm_medium": "nurture",
            "utm_campaign": f"waitlist_{question.topic_cluster}",
            "utm_content": "lead_magnet_delivery",
            "utm_term": question.id,
        },
        {
            "placement": "Launch broadcast email — primary CTA",
            "utm_source": "email",
            "utm_medium": "launch",
            "utm_campaign": "launch_2026_07_07",
            "utm_content": f"broadcast_{question.topic_cluster}",
            "utm_term": question.persona_segment,
        },
    ]
