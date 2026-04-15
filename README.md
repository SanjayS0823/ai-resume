# AI Resume Screening System

This project demonstrates a simple **AI-powered Resume Screening System** built using **LangChain and OpenAI**.

The system analyzes resumes and compares them with a job description to determine how well a candidate matches the role.

## Project Objective

The goal of this project is to build an AI pipeline that can:

- Extract important information from resumes
- Compare candidate profiles with job requirements
- Generate a **Fit Score (0–100)**
- Provide an explanation for the evaluation

This helps simulate how AI can assist recruiters in the hiring process.

---

## Pipeline Flow

Resume → Skill Extraction → Matching → Scoring → Explanation

1. **Skill Extraction**
   - Extract skills, tools, and experience from the resume.

2. **Matching**
   - Compare extracted information with the job description.

3. **Scoring**
   - Assign a Fit Score between **0 and 100**.

4. **Explanation**
   - Generate reasoning for the score.

---

## Technologies Used

- Python
- LangChain
- OpenAI API
- Jupyter Notebook
- Prompt Engineering

---

## Project Structure


resume-screening/
│
├── prompts/
│ ├── skill_extraction_prompt.py
│ └── scoring_prompt.py
│
├── chains/
│ ├── extraction_chain.py
│ └── scoring_chain.py
│
├── data/
│ ├── strong_resume.txt
│ ├── average_resume.txt
│ ├── weak_resume.txt
│ └── job_description.txt
│
├── main.py
├── AI_Resume_Screening_System.ipynb
└── requirements.txt


---

## Example Output

Strong Candidate  
Fit Score: 90  
Explanation: Candidate matches most required skills and has relevant experience.

Average Candidate  
Fit Score: 60  
Explanation: Candidate has some matching skills but lacks several required technologies.

Weak Candidate  
Fit Score: 20  
Explanation: Candidate does not meet the core requirements of the role.

---

## How to Run

### 1. Install Dependencies


pip install -r requirements.txt


### 2. Add API Key

Create a `.env` file:


OPENAI_API_KEY=your_api_key_here


### 3. Run the Project


python main.py


or open the notebook:


AI_Resume_Screening_System.ipynb


---

## Learning Outcome

This project helped me understand:

- LangChain pipelines
- Prompt engineering
- LLM-based evaluation systems
- AI-assisted recruitment workflows

---

## Author

Sanjay  
Computer Science Engineering (AI & ML)
