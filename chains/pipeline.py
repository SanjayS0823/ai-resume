"""
chains/pipeline.py
------------------
Builds the 4-step Resume Screening pipeline using LCEL
(LangChain Expression Language).

Pipeline: Extract → Match → Score → Explain
Each step uses .invoke() and feeds its output to the next.
All steps are automatically traced by LangSmith when
LANGCHAIN_TRACING_V2=true is set in the environment.
"""

import json
import re
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain.callbacks.tracers import LangChainTracer

from prompts import (
    skill_extraction_prompt,
    matching_prompt,
    scoring_prompt,
    explanation_prompt,
)


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------

def _safe_json(raw: str) -> dict:
    """
    Parse LLM output as JSON.
    Strips markdown fences (```json ... ```) if present,
    then raises a clear error if parsing fails.
    """
    # Remove optional markdown fences
    cleaned = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`").strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"LLM returned non-JSON output.\n"
            f"Raw output:\n{raw}\n"
            f"Parse error: {exc}"
        )


# ------------------------------------------------------------------
# Build individual LCEL chains
# ------------------------------------------------------------------

def build_pipeline(model_name: str = "llama3-8b-8192", temperature: float = 0.0) -> dict:
    """
    Instantiate the Groq LLM and return the four LCEL chains.

    Each chain follows the pattern:
        prompt | llm | StrOutputParser()

    Args:
        model_name:  Groq model ID (default: llama3-8b-8192)
        temperature: 0.0 for deterministic, reproducible outputs

    Returns:
        dict with keys: extraction_chain, matching_chain,
                        scoring_chain, explanation_chain, llm
    """
    llm = ChatGroq(
        model=model_name,
        temperature=temperature,
    )

    # LCEL chains — each is a Runnable
    extraction_chain  = skill_extraction_prompt  | llm | StrOutputParser()
    matching_chain    = matching_prompt           | llm | StrOutputParser()
    scoring_chain     = scoring_prompt            | llm | StrOutputParser()
    explanation_chain = explanation_prompt        | llm | StrOutputParser()

    return {
        "extraction_chain":  extraction_chain,
        "matching_chain":    matching_chain,
        "scoring_chain":     scoring_chain,
        "explanation_chain": explanation_chain,
        "llm": llm,
    }


# ------------------------------------------------------------------
# Full pipeline runner
# ------------------------------------------------------------------

def run_screening(
    resume_text: str,
    job_description: str,
    candidate_label: str,
    chains: dict,
    tags: list[str] | None = None,
) -> dict:
    """
    Run the full 4-step screening pipeline for a single resume.

    Args:
        resume_text:      Raw resume string
        job_description:  Job description string
        candidate_label:  e.g. 'Strong', 'Average', 'Weak'
        chains:           dict returned by build_pipeline()
        tags:             Optional LangSmith tags list

    Returns:
        dict with keys: candidate_label, extracted, matched, scored, explained
    """
    run_config = {"tags": tags or [candidate_label, "resume-screener"]}

    print(f"\n{'='*60}")
    print(f"  Processing: {candidate_label} Candidate")
    print(f"{'='*60}")

    # ── STEP 1: Skill Extraction ──────────────────────────────────
    print("  [1/4] Extracting skills...")
    raw_extracted = chains["extraction_chain"].invoke(
        {"resume_text": resume_text},
        config=run_config,
    )
    extracted = _safe_json(raw_extracted)
    print(f"        → Found {len(extracted.get('skills', []))} skills, "
          f"{len(extracted.get('tools_and_technologies', []))} tools")

    # ── STEP 2: Matching Logic ────────────────────────────────────
    print("  [2/4] Matching against job description...")
    raw_matched = chains["matching_chain"].invoke(
        {
            "job_description":   job_description,
            "candidate_profile": json.dumps(extracted, indent=2),
        },
        config=run_config,
    )
    matched = _safe_json(raw_matched)
    print(f"        → Matched: {len(matched.get('matched_skills', []))} | "
          f"Missing: {len(matched.get('missing_skills', []))}")

    # ── STEP 3: Scoring ───────────────────────────────────────────
    print("  [3/4] Computing score...")
    raw_scored = chains["scoring_chain"].invoke(
        {
            "matching_result":   json.dumps(matched, indent=2),
            "candidate_profile": json.dumps(extracted, indent=2),
            "job_description":   job_description,
        },
        config=run_config,
    )
    scored = _safe_json(raw_scored)
    print(f"        → Score: {scored.get('total_score')}/100 "
          f"({scored.get('rating')})")

    # ── STEP 4: Explanation ───────────────────────────────────────
    print("  [4/4] Generating explanation...")
    raw_explained = chains["explanation_chain"].invoke(
        {
            "candidate_profile": json.dumps(extracted, indent=2),
            "matching_result":   json.dumps(matched, indent=2),
            "score_result":      json.dumps(scored, indent=2),
        },
        config=run_config,
    )
    explained = _safe_json(raw_explained)
    print(f"        → Recommendation: {explained.get('recommendation')}")

    return {
        "candidate_label": candidate_label,
        "candidate_name":  extracted.get("candidate_name", "Unknown"),
        "extracted":       extracted,
        "matched":         matched,
        "scored":          scored,
        "explained":       explained,
    }
