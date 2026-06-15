"""
Quick-start example for DoseSync SEO Email Funnel Builder.
Run from this directory: python3 example_usage.py
Requires: pip install anthropic
Requires: ANTHROPIC_API_KEY env var set
"""
from input_models import QuestionInput, SkillConfig
from skill import run_skill

SAMPLE_TRANSCRIPT = """
So, I was coordinating meds for my mom and also for my kid with ADHD.
Every morning it's this whole chaos — did someone give it already?
I'd text my husband, he'd text me back, sometimes we'd both give the dose.
We started using a whiteboard. It worked for like two weeks.
Then my husband forgot to check it. My mom got a double dose of her blood pressure medication.
Nothing bad happened thank God, but I was terrified.
The scariest part is you don't know until hours later.
Now we use a shared log. Real-time. If my husband confirms, I see it instantly.
That peace of mind — knowing without having to text — that's everything.
I'd say this happens to a lot of families. The problem isn't caring, it's communication.
"""

questions = [
    QuestionInput(
        id="q001",
        raw_question="How do I prevent double-dosing when multiple caregivers share medication duties?",
        topic_cluster="double_dosing",
        persona_segment="sandwich_caregiver",
        interview_transcript=SAMPLE_TRANSCRIPT,
        language="en",
    ),
]

config = SkillConfig(
    launch_date="2026-07-07",
    article_length="medium",
    emails_count=3,
    product_integration_level="medium",
    output_dir="output",
)

if __name__ == "__main__":
    result = run_skill(questions, config)
    print("\n=== Generated Files ===")
    for category, paths in result["generated_files"].items():
        if isinstance(paths, list):
            for p in paths:
                print(f"  {category}: {p}")
        else:
            print(f"  {category}: {paths}")
