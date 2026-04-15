"""
main.py
-------
Entry point for the AI Resume Screening System.

Pipeline: Resume → Extract → Match → Score → Explain → Trace
LLM:      Groq (llama3-8b-8192 by default)
Tracing:  LangSmith (automatic when LANGCHAIN_TRACING_V2=true)

Usage:
    python main.py
"""

import os
import json
import sys
from datetime import datetime
from dotenv import load_dotenv

# ── Load environment variables FIRST (before any LangChain import) ──
load_dotenv()

# Validate required env vars
required_vars = ["GROQ_API_KEY", "LANGCHAIN_API_KEY"]
missing = [v for v in required_vars if not os.getenv(v)]
if missing:
    print(f"\n❌  Missing environment variables: {', '.join(missing)}")
    print("   Please copy .env.example to .env and fill in the values.\n")
    sys.exit(1)

# ── Ensure LangSmith tracing is enabled ──
os.environ["LANGCHAIN_TRACING_V2"] = "true"

from chains import build_pipeline, run_screening
from data.resumes import JOB_DESCRIPTION, RESUMES


def print_result(result: dict) -> None:
    """Pretty-print a single candidate's screening result."""
    label = result["candidate_label"]
    name  = result["candidate_name"]
    score = result["scored"].get("total_score", "N/A")
    rating = result["scored"].get("rating", "N/A")
    rec   = result["explained"].get("recommendation", "N/A")
    breakdown = result["scored"].get("score_breakdown", {})

    print(f"\n{'─'*60}")
    print(f"  🧑 {name}  [{label} Candidate]")
    print(f"{'─'*60}")
    print(f"  📊 Total Score  : {score}/100  ({rating})")
    print(f"  📌 Score Breakdown:")
    for k, v in breakdown.items():
        print(f"       {k:<30}: {v}")
    print(f"\n  ✅ Matched Skills  : {result['matched'].get('matched_skills', [])}")
    print(f"  ❌ Missing Skills  : {result['matched'].get('missing_skills', [])}")
    print(f"\n  💬 Summary:")
    print(f"     {result['explained'].get('summary', '')}")
    print(f"\n  🏆 Strengths : {result['explained'].get('strengths', [])}")
    print(f"  ⚠️  Weaknesses: {result['explained'].get('weaknesses', [])}")
    print(f"\n  📋 Recommendation : {rec}")
    print(f"     {result['explained'].get('recommendation_reason', '')}")


def save_results(results: list[dict], output_path: str) -> None:
    """Save all results to a JSON file."""
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n💾  Results saved to: {output_path}")


def main():
    print("\n" + "="*60)
    print("  AI RESUME SCREENING SYSTEM")
    print("  Powered by: Groq (LLaMA 3) + LangChain + LangSmith")
    print("="*60)
    print(f"  LangSmith Project : {os.getenv('LANGCHAIN_PROJECT', 'resume-screener')}")
    print(f"  Tracing Enabled   : {os.getenv('LANGCHAIN_TRACING_V2', 'false')}")
    print(f"  Timestamp         : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # ── Build pipeline once (shared LLM + chains) ──
    print("\n⚙️   Initialising Groq LLM pipeline...")
    chains = build_pipeline(model_name="llama3-8b-8192", temperature=0.0)
    print("    Pipeline ready ✓")

    all_results = []

    # ── Run 3 candidates (Strong, Average, Weak) ──
    for label, resume_text in RESUMES.items():
        result = run_screening(
            resume_text=resume_text,
            job_description=JOB_DESCRIPTION,
            candidate_label=label,
            chains=chains,
            tags=[label.lower(), "innomatics", "resume-screener"],
        )
        all_results.append(result)
        print_result(result)

    # ── Summary Table ──
    print("\n\n" + "="*60)
    print("  SCREENING SUMMARY")
    print("="*60)
    print(f"  {'Candidate':<20} {'Score':>7}   {'Rating':<10} {'Recommendation'}")
    print(f"  {'-'*58}")
    for r in all_results:
        print(
            f"  {r['candidate_name']:<20} "
            f"{r['scored'].get('total_score', 0):>6}/100  "
            f"{r['scored'].get('rating', ''):<10} "
            f"{r['explained'].get('recommendation', '')}"
        )

    # ── Save results ──
    output_file = f"screening_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    save_results(all_results, output_file)

    print("\n✅  All done! Check LangSmith dashboard for traces:")
    print(f"    https://smith.langchain.com\n")


if __name__ == "__main__":
    main()
