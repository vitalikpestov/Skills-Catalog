import json
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path("output")


def ensure_output_dir(base: str = "output"):
    path = Path(base)
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_blog_post_md(blog_post: dict, base_dir: str = "output") -> str:
    out = ensure_output_dir(base_dir)
    slug = _slugify(blog_post.get("seo_title", blog_post["id"]))
    path = out / f"blog_{blog_post['id']}_{slug}.md"

    header = "\n".join([
        f"<!-- id: {blog_post['id']} -->",
        f"<!-- primary_keyword: {blog_post.get('primary_keyword', '')} -->",
        f"<!-- meta_description: {blog_post.get('meta_description', '')} -->",
        f"<!-- word_count: {blog_post.get('word_count', '?')} -->",
        f"<!-- generated: {_now()} -->",
        "",
    ])

    path.write_text(header + blog_post["content_markdown"], encoding="utf-8")
    return str(path)


def save_lead_magnet_md(lead_magnet: dict, question_id: str, base_dir: str = "output") -> str:
    out = ensure_output_dir(base_dir)
    slug = _slugify(lead_magnet.get("title", question_id))
    path = out / f"lead_magnet_{question_id}_{slug}.md"

    lines = [
        f"# {lead_magnet.get('title', 'Lead Magnet')}",
        "",
        f"> {lead_magnet.get('promise', '')}",
        "",
        "## Contents",
        "",
    ]
    for item in lead_magnet.get("format_outline", []):
        lines.append(f"- {item}")

    lines += [
        "",
        "---",
        "",
        "## Opt-in Copy",
        "",
        f"**Short CTA:** {lead_magnet.get('optin_copy_short', '')}",
        "",
        f"**Long copy:**",
        "",
        lead_magnet.get("optin_copy_long", ""),
        "",
        "---",
        "",
        "## Email Delivery",
        "",
        f"**Subject:** {lead_magnet.get('delivery_subject_line', '')}",
        f"**Thank-you headline:** {lead_magnet.get('thank_you_headline', '')}",
        "",
        f"<!-- generated: {_now()} -->",
    ]

    path.write_text("\n".join(lines), encoding="utf-8")
    return str(path)


def save_email_funnel_json(question_id: str, funnel: dict, base_dir: str = "output") -> str:
    out = ensure_output_dir(base_dir)
    path = out / f"email_funnel_{question_id}.json"
    path.write_text(json.dumps(funnel, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(path)


def save_analytics_json(question_id: str, analytics: dict, base_dir: str = "output") -> str:
    out = ensure_output_dir(base_dir)
    path = out / f"analytics_{question_id}.json"
    path.write_text(json.dumps(analytics, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(path)


def save_meta_json(results: list, base_dir: str = "output") -> str:
    out = ensure_output_dir(base_dir)
    path = out / "meta.json"
    meta = {
        "generated_at": _now(),
        "total_questions": len(results),
        "results": [
            {
                "question_id": r["question_id"],
                "blog_title": r["blog_post"].get("seo_title", ""),
                "word_count": r["blog_post"].get("word_count", 0),
                "lead_magnet_title": r["lead_magnet"].get("title", ""),
                "email_steps": len(r["email_funnel"].get("sequence", [])),
                "files": r.get("files", {}),
            }
            for r in results
        ],
    }
    path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(path)


def _slugify(text: str, max_len: int = 40) -> str:
    import re
    slug = re.sub(r"[^\w\s-]", "", text.lower())
    slug = re.sub(r"[\s_-]+", "-", slug).strip("-")
    return slug[:max_len]


def _now() -> str:
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
