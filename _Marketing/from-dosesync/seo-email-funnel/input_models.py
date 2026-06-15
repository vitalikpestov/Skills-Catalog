from dataclasses import dataclass, field
from typing import Literal, Optional

TopicCluster = Literal["double_dosing", "grandparents", "adhd_kids", "burnout", "other"]
PersonaSegment = Literal[
    "sandwich_caregiver", "young_parent", "grandparent",
    "professional_caregiver", "other"
]


@dataclass
class QuestionInput:
    id: str
    raw_question: str
    topic_cluster: TopicCluster
    persona_segment: PersonaSegment
    interview_transcript: str
    language: Literal["en", "ru"] = "en"


@dataclass
class SkillConfig:
    launch_date: str = "2026-07-07"
    article_length: Literal["short", "medium", "long"] = "medium"
    emails_count: int = 5
    product_integration_level: Literal["light", "medium", "strong"] = "medium"
    model: str = "claude-sonnet-4-6"
    output_dir: str = "output"
