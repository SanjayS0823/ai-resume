<div align="center">

```
██████╗ ███████╗███████╗██╗   ██╗███╗   ███╗███████╗
██╔══██╗██╔════╝██╔════╝██║   ██║████╗ ████║██╔════╝
██████╔╝█████╗  ███████╗██║   ██║██╔████╔██║█████╗  
██╔══██╗██╔══╝  ╚════██║██║   ██║██║╚██╔╝██║██╔══╝  
██║  ██║███████╗███████║╚██████╔╝██║ ╚═╝ ██║███████╗
╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝
        AI RESUME SCREENING SYSTEM
```

**Drop a resume. Get a verdict.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.3-1C3C3C?style=flat-square&logo=chainlink&logoColor=white)](https://langchain.com)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.1-F55036?style=flat-square)](https://groq.com)
[![LangSmith](https://img.shields.io/badge/LangSmith-Traced-FF6B35?style=flat-square)](https://smith.langchain.com)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=flat-square)](LICENSE)

</div>

---

## What is this?

**RESUME** is a production-grade LLM pipeline that reads resumes the way a senior engineer would — not just keyword matching, but genuine reasoning about fit.

Feed it a job description and a resume. It extracts, matches, scores, and explains. Every step is traced in LangSmith so you can see exactly what the model thought and why.

```
Resume Text ──▶ Extract ──▶ Match ──▶ Score ──▶ Explain ──▶ Verdict
                  │           │         │          │
                  ▼           ▼         ▼          ▼
               skills      gaps      0–100     hire/hold/
               tools       hits    weighted     reject
               exp.       bonus    breakdown
```

---

## Architecture

```
resume_screener/
│
├── prompts/
│   ├── __init__.py
│   └── templates.py        ← 4 PromptTemplates (extract · match · score · explain)
│
├── chains/
│   ├── __init__.py
│   └── pipeline.py         ← LCEL pipeline — prompt | llm | parser
│
├── data/
│   └── resumes.py          ← 3 test resumes (Strong / Average / Weak) + JD
│
├── resume_screening.ipynb  ← Jupyter notebook (run this)
├── main.py                 ← CLI entry point
└── requirements.txt
```

---

## The Pipeline — 4 Steps, Zero Hallucination

### Step 1 · Skill Extraction
Parses the resume for skills, tools, years of experience, education, certifications, and projects. Hard rule: **never infer what isn't written**.

### Step 2 · Matching Logic
Compares extracted profile against job requirements. Returns matched skills, missing skills, bonus skills, and experience/education alignment.

### Step 3 · Scoring (0–100)
Weighted rubric — no vibes, just math:

| Dimension | Weight |
|---|---|
| Skills Match | 40 pts |
| Experience | 25 pts |
| Education | 15 pts |
| Bonus Skills | 10 pts |
| Projects | 10 pts |

### Step 4 · Explanation
Few-shot prompted explanation with explicit strengths, gaps, and a clear hiring recommendation: **Proceed / Hold / Reject**.

---

## Sample Output

```
══════════════════════════════════════════════════════════
  Arjun Mehta  [Strong Candidate]
══════════════════════════════════════════════════════════
  Score     : 88/100  (Strong)
  Matched   : ['Python', 'scikit-learn', 'XGBoost', 'TensorFlow', 'SQL', ...]
  Missing   : ['Apache Spark']
  
  Summary   : Strong fit for the Data Scientist role with 4 years of
              hands-on ML experience and full coverage of core requirements.
              
  Verdict   : ✅ Proceed to interview

──────────────────────────────────────────────────────────
  Priya Sharma  [Average Candidate]
══════════════════════════════════════════════════════════
  Score     : 54/100  (Average)
  Missing   : ['TensorFlow', 'PyTorch', 'XGBoost', 'Apache Spark']
  Verdict   : ⏸  Hold for further review

──────────────────────────────────────────────────────────
  Rahul Verma  [Weak Candidate]
══════════════════════════════════════════════════════════
  Score     : 11/100  (Weak)
  Verdict   : ❌ Reject
```

---

## Quickstart

### 1. Get API Keys

| Service | URL | Free? |
|---|---|---|
| Groq | [console.groq.com/keys](https://console.groq.com/keys) | ✅ Yes |
| LangSmith | [smith.langchain.com](https://smith.langchain.com) | ✅ Yes |

### 2. Install

```bash
git clone https://github.com/Aadithyaar22/resume-screener.git
cd resume-screener
pip install -r requirements.txt
```

### 3. Set Keys (in notebook — never hardcode)

```python
from getpass import getpass
import os

os.environ["GROQ_API_KEY"]         = getpass("Groq API Key: ")
os.environ["LANGCHAIN_API_KEY"]    = getpass("LangSmith API Key: ")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"]    = "resume-screener"
```

### 4. Run

```bash
# Notebook
jupyter notebook resume_screening.ipynb

# Or CLI
python main.py
```

---

## LangSmith Tracing

Every run is automatically traced. Open your project at [smith.langchain.com](https://smith.langchain.com) and you'll see:

- 3 parent runs tagged `strong` / `average` / `weak`
- 4 child spans per run showing each pipeline step
- Full input/output at every stage
- Token usage and latency per call

No `LANGCHAIN_TRACING_V2=true` → no traces. Keep it on.

---

## Tech Stack

| Layer | Tool |
|---|---|
| LLM | Groq · LLaMA 3.1 8B Instant |
| Orchestration | LangChain LCEL |
| Observability | LangSmith |
| Output Parsing | JSON mode + regex fallback |
| Notebook | Jupyter |

---

## Prompt Engineering Decisions

- **JSON mode enforced** at the LLM level (`response_format: json_object`) — eliminates malformed output
- **Explicit non-hallucination constraint** in every prompt: *"Do NOT infer skills not present in the resume"*
- **Few-shot example** in the explanation prompt to anchor output style
- **Weighted rubric** in scoring prompt so the model shows its arithmetic

---
