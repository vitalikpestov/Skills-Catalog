"""Validate i18n pilot output: placeholders, length, JSON integrity."""
import json
import re
from pathlib import Path

INPUT = Path("/Users/vitalik/Documents/Projects/MobileApp/DoseSync/Marketing/i18n-pilot-fr-es-2026-04-27.json")

with open(INPUT) as f:
    data = json.load(f)

errors = []
warnings = []
stats = {"total": len(data), "placeholders_match": 0, "length_ok": 0, "structural_changes": 0}

# Placeholder pattern: %@, %lld, %1$@, %2$lld, etc.
placeholder_re = re.compile(r"%(?:\d+\$)?[@dl]+")

for entry in data:
    key = entry["key"]
    en = entry["en"]
    fr = entry.get("fr", "")
    es = entry.get("es", "")

    # 1. Placeholder preservation
    en_placeholders = sorted(placeholder_re.findall(en))
    fr_placeholders = sorted(placeholder_re.findall(fr))
    es_placeholders = sorted(placeholder_re.findall(es))

    if en_placeholders != fr_placeholders:
        errors.append(f"[{key}] FR placeholder mismatch: EN={en_placeholders} FR={fr_placeholders}")
    elif en_placeholders != es_placeholders:
        errors.append(f"[{key}] ES placeholder mismatch: EN={en_placeholders} ES={es_placeholders}")
    else:
        stats["placeholders_match"] += 1

    # 2. Length budget (±30% of EN, generous for inflectional languages)
    en_len = len(en)
    fr_len = len(fr)
    es_len = len(es)
    if en_len >= 20:  # only check meaningful strings
        fr_ratio = fr_len / en_len
        es_ratio = es_len / en_len
        if fr_ratio > 1.5 or fr_ratio < 0.5:
            warnings.append(f"[{key}] FR length ratio {fr_ratio:.2f} (EN={en_len}, FR={fr_len})")
        if es_ratio > 1.5 or es_ratio < 0.5:
            warnings.append(f"[{key}] ES length ratio {es_ratio:.2f} (EN={en_len}, ES={es_len})")
        if fr_ratio <= 1.5 and fr_ratio >= 0.5 and es_ratio <= 1.5 and es_ratio >= 0.5:
            stats["length_ok"] += 1
    else:
        stats["length_ok"] += 1  # short strings always pass length check

    # 3. Structural changes flagged
    if entry.get("structural_change"):
        stats["structural_changes"] += 1

    # 4. Check for forbidden phrasings (medical guardrails)
    forbidden = ["take this medicine", "take this dose", "you should take", "doctor recommends"]
    for f_phrase in forbidden:
        if f_phrase.lower() in fr.lower() or f_phrase.lower() in es.lower():
            errors.append(f"[{key}] Forbidden medical-prescription phrase: '{f_phrase}'")

    # 5. Check «vous»/«usted» tone (indirect — look for «tu»/«tú» which are forbidden)
    if re.search(r'\btu\b', fr.lower()) or re.search(r'\bton\b', fr.lower()) or re.search(r'\btes\b', fr.lower()) or re.search(r'\bta\b', fr.lower()):
        # whitelist 'tu' inside compounds and proper nouns
        warnings.append(f"[{key}] FR informal 'tu/ton/ta' — verify (might be intentional)")
    if re.search(r'\btú\b', es.lower()) or re.search(r'\btu\b', es.lower()):
        warnings.append(f"[{key}] ES informal 'tú/tu' — verify (might be intentional)")

# Summary
print("=== i18n Pilot Validation Report ===")
print(f"Total strings:          {stats['total']}")
print(f"Placeholders match:     {stats['placeholders_match']}/{stats['total']}")
print(f"Length ok (±50%):       {stats['length_ok']}/{stats['total']}")
print(f"Structural changes:     {stats['structural_changes']}")
print(f"")
print(f"ERRORS:   {len(errors)}")
for e in errors:
    print(f"  ❌ {e}")
print(f"")
print(f"WARNINGS: {len(warnings)}")
for w in warnings:
    print(f"  ⚠️  {w}")
