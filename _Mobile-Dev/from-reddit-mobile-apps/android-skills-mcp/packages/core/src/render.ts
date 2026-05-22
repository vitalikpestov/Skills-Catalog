/** Emit a YAML plain scalar, double-quoting when the value would otherwise be misparsed. */
export function yamlScalar(s: string): string {
  if (s === '') return '""';
  if (/^[*&!@%>|`#?-]/.test(s)) return jsonQuote(s);
  if (s.includes('*')) return jsonQuote(s);
  if (s.includes(': ') || s.endsWith(':')) return jsonQuote(s);
  if (/^(true|false|null|yes|no|on|off|~)$/i.test(s)) return jsonQuote(s);
  if (/^-?\d/.test(s)) return jsonQuote(s);
  return s;
}

function jsonQuote(s: string): string {
  return `"${s.replace(/\\/g, '\\\\').replace(/"/g, '\\"')}"`;
}

/** Emit a YAML frontmatter block for the given key/value pairs. */
export function frontmatter(obj: Record<string, unknown>, indent = 0): string {
  const lines: string[] = indent === 0 ? ['---'] : [];
  const prefix = ' '.repeat(indent);
  for (const [k, v] of Object.entries(obj)) {
    if (v === undefined || v === null) continue;
    if (Array.isArray(v)) {
      if (v.length === 0) continue;
      lines.push(`${prefix}${k}:`);
      for (const item of v) lines.push(`${prefix}  - ${yamlScalar(String(item))}`);
    } else if (typeof v === 'boolean' || typeof v === 'number') {
      lines.push(`${prefix}${k}: ${v}`);
    } else if (typeof v === 'string' && (v.includes('\n') || v.length > 80)) {
      lines.push(`${prefix}${k}: |-`);
      for (const line of v.split('\n')) lines.push(`${prefix}  ${line}`);
    } else if (typeof v === 'string') {
      lines.push(`${prefix}${k}: ${yamlScalar(v)}`);
    } else if (typeof v === 'object') {
      const inner = frontmatter(v as Record<string, unknown>, indent + 2);
      if (inner) {
        lines.push(`${prefix}${k}:`);
        lines.push(inner);
      }
    }
  }
  if (indent === 0) lines.push('---');
  return lines.join('\n');
}
