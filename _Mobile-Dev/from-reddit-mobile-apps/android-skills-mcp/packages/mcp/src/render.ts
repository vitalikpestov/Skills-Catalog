import { type Skill, frontmatter } from '@android-skills/core';

// Re-emit a SKILL.md from the parsed Skill object. Manual YAML to avoid an extra dep.
export function rebuildSkillMarkdown(
  skill: Skill,
  opts: { includeReferences?: boolean } = {},
): string {
  const fm = skill.frontmatter;
  const head = frontmatter({
    name: fm.name,
    description: fm.description,
    license: fm.license,
    compatibility: fm.compatibility,
    'allowed-tools': fm.allowedTools,
    metadata: fm.metadata,
  });

  const lines: string[] = [head];
  lines.push('');
  lines.push(skill.body.trimEnd());

  if (opts.includeReferences && skill.references.length > 0) {
    lines.push('');
    lines.push('---');
    lines.push('');
    lines.push('# Inlined references');
    for (const ref of skill.references) {
      lines.push('');
      lines.push(`## ${ref.relPath}`);
      lines.push('');
      lines.push((ref.content ?? '').trimEnd());
    }
  }
  return `${lines.join('\n')}\n`;
}
