"""
prompts/templates.py
--------------------
All PromptTemplate definitions for the Resume Screening pipeline.

Design rules
 - Clear, unambiguous instructions
 - Strict output format to avoid hallucination
 - Constraint: NEVER infer skills not explicitly mentioned in the resume
"""

from langchain.prompts import PromptTemplate

# ------------------------------------------------------------------
# STEP 1 — Skill Extraction
# ------------------------------------------------------------------
SKILL_EXTRACTION_TEMPLATE = """You are a precise resume parser. Your ONLY job is to extract
information that is EXPLICITLY stated in the resume text below.

IMPORTANT RULES:
- Do NOT infer, guess, or assume any skill, tool, or experience not directly written in the resume.
- If a field has no information, output an empty list [].
- Output ONLY valid JSON. No explanation, no markdown fences, no extra text.

Resume Text:
{resume_text}

Extract and return exactly this JSON structure:
{{
  "candidate_name": "<full name or 'Unknown'>",
  "skills": ["<skill1>", "<skill2>"],
  "tools_and_technologies": ["<tool1>", "<tool2>"],
  "experience_years": "<number or 'Not mentioned'>",
  "education": "<highest degree or 'Not mentioned'>",
  "certifications": ["<cert1>"],
  "projects": ["<project title 1>", "<project title 2>"]
}}"""

skill_extraction_prompt = PromptTemplate(
    input_variables=["resume_text"],
    template=SKILL_EXTRACTION_TEMPLATE,
)


# ------------------------------------------------------------------
# STEP 2 — Matching Logic
# ------------------------------------------------------------------
MATCHING_TEMPLATE = """You are a technical recruiter performing a skills-gap analysis.

Job Description Requirements:
{job_description}

Candidate Profile (extracted from resume):
{candidate_profile}

Compare the candidate profile against ONLY the requirements listed in the job description.

RULES:
- Only consider skills/tools explicitly present in the candidate profile.
- Do NOT assume the candidate knows something if it is not listed.
- Output ONLY valid JSON. No markdown, no extra text.

Return exactly this JSON structure:
{{
  "matched_skills": ["<skill present in both JD and candidate>"],
  "missing_skills": ["<skill required by JD but absent in candidate>"],
  "bonus_skills": ["<skill candidate has that JD does not require>"],
  "experience_match": "<'Exceeds' | 'Meets' | 'Below' | 'Unknown'>",
  "education_match": "<'Meets' | 'Does not meet' | 'Unknown'>"
}}"""

matching_prompt = PromptTemplate(
    input_variables=["job_description", "candidate_profile"],
    template=MATCHING_TEMPLATE,
)


# ------------------------------------------------------------------
# STEP 3 — Scoring
# ------------------------------------------------------------------
SCORING_TEMPLATE = """You are an objective hiring evaluator. Assign a fit score using the
weighted rubric below.

Scoring Rubric (total = 100):
  - Skills Match       : 40 points  (matched_skills / total_required_skills * 40)
  - Experience Match   : 25 points  (Exceeds=25, Meets=20, Below=10, Unknown=5)
  - Education Match    : 15 points  (Meets=15, Does not meet=5, Unknown=8)
  - Bonus Skills       : 10 points  (each bonus skill = 2 pts, max 10)
  - Projects / Context : 10 points  (judge from candidate profile)

Matching Analysis:
{matching_result}

Candidate Profile:
{candidate_profile}

Job Description:
{job_description}

RULES:
- Scores must be integers between 0 and 100.
- Show your arithmetic clearly in breakdown.
- Output ONLY valid JSON. No markdown, no extra text.

Return exactly this JSON:
{{
  "total_score": <0-100>,
  "score_breakdown": {{
    "skills_match_score": <0-40>,
    "experience_score": <0-25>,
    "education_score": <0-15>,
    "bonus_skills_score": <0-10>,
    "projects_score": <0-10>
  }},
  "rating": "<'Strong' | 'Average' | 'Weak'>"
}}"""

scoring_prompt = PromptTemplate(
    input_variables=["matching_result", "candidate_profile", "job_description"],
    template=SCORING_TEMPLATE,
)


# ------------------------------------------------------------------
# STEP 4 — Explanation (Few-shot included for bonus marks)
# ------------------------------------------------------------------
EXPLANATION_TEMPLATE = """You are a senior technical recruiter writing a hiring recommendation.

--- FEW-SHOT EXAMPLE ---
Score: 82 | Rating: Strong
Explanation: "The candidate is a strong fit for the Data Scientist role. They demonstrate
solid coverage of the required ML skills (Python, scikit-learn, TensorFlow) and bring 4 years
of hands-on experience. The advanced degree in Statistics further strengthens the application.
Minor gap: no Spark experience, but the bonus proficiency in Kafka and AWS suggests
adaptability. Recommend: Proceed to technical interview."
--- END EXAMPLE ---

Now write an explanation for the following candidate:

Job Title: Data Scientist
Candidate Profile: {candidate_profile}
Matching Analysis: {matching_result}
Score Result: {score_result}

RULES:
- Be factual. Reference only information present in the data above.
- Mention specific matched skills AND specific missing skills.
- End with a clear hiring recommendation: Proceed / Hold / Reject.
- Output ONLY valid JSON. No markdown, no extra text.

Return exactly this JSON:
{{
  "summary": "<2-3 sentence overview>",
  "strengths": ["<strength 1>", "<strength 2>"],
  "weaknesses": ["<gap 1>", "<gap 2>"],
  "recommendation": "<'Proceed to interview' | 'Hold for further review' | 'Reject'>",
  "recommendation_reason": "<one sentence justification>"
}}"""

explanation_prompt = PromptTemplate(
    input_variables=["candidate_profile", "matching_result", "score_result"],
    template=EXPLANATION_TEMPLATE,
)
