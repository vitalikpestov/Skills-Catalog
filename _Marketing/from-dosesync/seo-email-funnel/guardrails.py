import re

DISCLAIMER_EN = (
    "\n\n---\n*DoseSync is a coordination and reminder tool, not a medical recommendation. "
    "Always consult a healthcare professional before changing any medication schedule.*"
)
DISCLAIMER_RU = (
    "\n\n---\n*DoseSync — инструмент напоминания и координации, не медицинская рекомендация. "
    "Всегда консультируйтесь с врачом перед изменением режима приёма лекарств.*"
)

FORBIDDEN_EN = [
    "clinically proven", "prevents complications", "cures", "treats",
    "medical advice", "diagnosis", "guaranteed results", "proven to heal",
    "clinical trial", "FDA approved", "no side effects",
]
FORBIDDEN_RU = [
    "клинически доказано", "предотвращает осложнения", "лечит", "вылечивает",
    "медицинская рекомендация", "диагноз", "гарантированный результат",
    "клинические испытания", "одобрено", "без побочных эффектов",
]

DRUG_PATTERN = re.compile(
    r'\b(Aspirin|Warfarin|Metformin|Lisinopril|Amoxicillin|Ibuprofen|Omeprazole|'
    r'Atorvastatin|Levothyroxine|Amlodipine|[A-Z][a-z]+(ix|in|ol|um|ide|ine))\b'
)


def apply_guardrails(text: str, language: str = "en") -> str:
    forbidden = FORBIDDEN_RU if language == "ru" else FORBIDDEN_EN
    for phrase in forbidden:
        text = re.sub(re.escape(phrase), "", text, flags=re.IGNORECASE)

    text = DRUG_PATTERN.sub("[medication]", text)

    text = re.sub(r'[ \t]{2,}', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def add_disclaimer(text: str, language: str = "en") -> str:
    disclaimer = DISCLAIMER_RU if language == "ru" else DISCLAIMER_EN
    if disclaimer.strip() not in text:
        return text + disclaimer
    return text


def get_disclaimer(language: str = "en") -> str:
    return DISCLAIMER_RU if language == "ru" else DISCLAIMER_EN
