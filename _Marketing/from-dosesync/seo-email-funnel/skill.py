"""
DoseSync SEO Email Funnel Builder
Entry point: run_skill(questions, config)
"""
import sys
from typing import List, Dict

from input_models import QuestionInput, SkillConfig
from guardrails import apply_guardrails
from seo_analysis import build_seo_outline
from interview_parser import parse_interview
from blog_generator import generate_blog_post
from lead_magnet_generator import generate_lead_magnet
from email_funnel_generator import generate_email_funnel
from analytics_recommender import build_analytics_recommendations
from io_utils import (
    save_blog_post_md,
    save_lead_magnet_md,
    save_email_funnel_json,
    save_analytics_json,
    save_meta_json,
)


def process_single_question(q: QuestionInput, config: SkillConfig) -> Dict:
    print(f"[{q.id}] Applying guardrails...", flush=True)
    safe_transcript = apply_guardrails(q.interview_transcript, language=q.language)

    print(f"[{q.id}] Building SEO outline...", flush=True)
    seo_outline = build_seo_outline(
        raw_question=q.raw_question,
        topic_cluster=q.topic_cluster,
        persona_segment=q.persona_segment,
        language=q.language,
        model=config.model,
        article_length=config.article_length,
    )

    print(f"[{q.id}] Parsing interview transcript...", flush=True)
    interview_blocks = parse_interview(
        transcript=safe_transcript,
        language=q.language,
        model=config.model,
    )

    print(f"[{q.id}] Generating blog post...", flush=True)
    blog_post = generate_blog_post(
        question=q,
        seo_outline=seo_outline,
        interview_blocks=interview_blocks,
        config=config,
    )

    print(f"[{q.id}] Generating lead magnet...", flush=True)
    lead_magnet = generate_lead_magnet(
        question=q,
        seo_outline=seo_outline,
        interview_blocks=interview_blocks,
        config=config,
    )

    print(f"[{q.id}] Generating email funnel ({config.emails_count} emails)...", flush=True)
    email_funnel = generate_email_funnel(
        question=q,
        lead_magnet=lead_magnet,
        config=config,
    )

    print(f"[{q.id}] Building analytics recommendations...", flush=True)
    analytics = build_analytics_recommendations(
        question=q,
        email_funnel=email_funnel,
    )

    print(f"[{q.id}] Saving artifacts...", flush=True)
    blog_md_path = save_blog_post_md(blog_post, base_dir=config.output_dir)
    lead_md_path = save_lead_magnet_md(lead_magnet, question_id=q.id, base_dir=config.output_dir)
    funnel_json_path = save_email_funnel_json(q.id, email_funnel, base_dir=config.output_dir)
    analytics_json_path = save_analytics_json(q.id, analytics, base_dir=config.output_dir)

    print(f"[{q.id}] Done. Blog: {blog_post.get('word_count', '?')} words.", flush=True)

    return {
        "question_id": q.id,
        "blog_post": blog_post,
        "lead_magnet": lead_magnet,
        "email_funnel": email_funnel,
        "analytics": analytics,
        "files": {
            "blog_post_md": blog_md_path,
            "lead_magnet_md": lead_md_path,
            "email_funnel_json": funnel_json_path,
            "analytics_json": analytics_json_path,
        },
    }


def run_skill(questions: List[QuestionInput], config: SkillConfig) -> Dict:
    results = []
    blog_paths, lead_paths, funnel_paths, analytics_paths = [], [], [], []

    for q in questions:
        try:
            r = process_single_question(q, config)
        except Exception as e:
            print(f"[{q.id}] ERROR: {e}", file=sys.stderr)
            raise
        results.append(r)
        blog_paths.append(r["files"]["blog_post_md"])
        lead_paths.append(r["files"]["lead_magnet_md"])
        funnel_paths.append(r["files"]["email_funnel_json"])
        analytics_paths.append(r["files"]["analytics_json"])

    meta_path = save_meta_json(results, base_dir=config.output_dir)

    print(f"\nAll done. {len(results)} question(s) processed. Meta: {meta_path}", flush=True)

    return {
        "results": results,
        "generated_files": {
            "blog_posts": blog_paths,
            "lead_magnets": lead_paths,
            "email_funnels": funnel_paths,
            "analytics": analytics_paths,
            "meta": meta_path,
        },
    }
