import { type Skill, frontmatter } from '@android-skills/core';

/** Body + flattened references appended as `## <relPath>` sections. */
export function flattenWithReferences(skill: Skill): string {
  let out = skill.body.trimEnd();
  if (skill.references.length > 0) {
    out += '\n\n---\n\n# Inlined references\n';
    for (const ref of skill.references) {
      out += `\n## ${ref.relPath}\n\n${(ref.content ?? '').trimEnd()}\n`;
    }
  }
  return out;
}

/** Single-line, no leading/trailing whitespace, collapsed internal whitespace. */
export function singleLine(s: string): string {
  return s.replace(/\s+/g, ' ').trim();
}
