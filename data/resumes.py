"""
data/resumes.py
---------------
Sample resumes (Strong / Average / Weak) and a Data Scientist
job description used for testing the pipeline.
"""

JOB_DESCRIPTION = """
Position: Data Scientist
Company: TechCorp Analytics

Required Skills:
- Python (3+ years)
- Machine Learning (scikit-learn, XGBoost)
- Deep Learning (TensorFlow or PyTorch)
- SQL and database querying
- Data visualization (Matplotlib, Seaborn, or Tableau)
- Feature engineering and model evaluation
- Statistics and probability
- Pandas, NumPy

Nice-to-Have:
- Apache Spark / big data tools
- Cloud platforms (AWS, GCP, or Azure)
- MLflow or experiment tracking
- NLP experience

Experience Required: 2+ years in a data science or ML role
Education: Bachelor's or Master's in CS, Statistics, Math, or related field

Responsibilities:
- Build and deploy ML models for business problems
- Analyze large datasets and derive actionable insights
- Collaborate with engineering teams to productionize models
- Write clean, reproducible code
"""

# ── Resume 1: Strong Candidate ────────────────────────────────────
RESUME_STRONG = """
Name: Arjun Mehta
Email: arjun.mehta@email.com
Phone: +91-9876543210

SUMMARY
Senior Data Scientist with 4 years of experience building and deploying machine learning
solutions at scale. Proficient in the full ML lifecycle from data ingestion to model serving.

SKILLS
Programming: Python, SQL, R, Bash
ML Frameworks: scikit-learn, XGBoost, TensorFlow, PyTorch
Data Tools: Pandas, NumPy, Matplotlib, Seaborn, Tableau
Big Data: Apache Spark, Hadoop
Cloud: AWS (SageMaker, S3, EC2), GCP (BigQuery, Vertex AI)
MLOps: MLflow, Docker, Kubernetes
NLP: Hugging Face Transformers, spaCy

EXPERIENCE
Data Scientist — DataDriven Inc. (2021 – Present, 3 years)
- Designed and deployed 10+ production ML models using scikit-learn and XGBoost
- Built a demand forecasting system using LSTM (TensorFlow) reducing errors by 23%
- Performed feature engineering on 50M-row datasets using Spark
- Tracked experiments with MLflow; automated retraining pipelines on AWS SageMaker

Junior Data Analyst — Analytics Hub (2020 – 2021, 1 year)
- Conducted SQL-based analysis on customer behavior data
- Created dashboards in Tableau for business stakeholders

EDUCATION
M.Sc. Data Science — IIT Bombay (2020)
B.Tech Computer Science — VIT University (2018)

CERTIFICATIONS
- AWS Certified Machine Learning – Specialty
- Google Professional Data Engineer

PROJECTS
- Real-time Fraud Detection System (XGBoost + Kafka + AWS Lambda)
- Sentiment Analysis API (BERT fine-tuning, HuggingFace + FastAPI)
- Customer Churn Prediction (scikit-learn, Pandas, Tableau dashboard)
"""

# ── Resume 2: Average Candidate ───────────────────────────────────
RESUME_AVERAGE = """
Name: Priya Sharma
Email: priya.sharma@email.com

SUMMARY
Data Science enthusiast with 2 years of experience in analytics and basic machine learning.
Comfortable with Python and SQL for data analysis tasks.

SKILLS
Programming: Python, SQL
Libraries: Pandas, NumPy, Matplotlib, scikit-learn
Databases: MySQL, PostgreSQL
Tools: Jupyter Notebook, Excel, Power BI

EXPERIENCE
Data Analyst — InfoSoft Solutions (2022 – Present, 2 years)
- Performed exploratory data analysis using Pandas and Matplotlib
- Built a customer segmentation model using K-Means (scikit-learn)
- Wrote complex SQL queries to extract insights from relational databases
- Created monthly reports using Power BI

Intern — StartupX (2021 – 2022, 6 months)
- Assisted in cleaning datasets and building basic regression models
- Visualized sales trends using Matplotlib and Seaborn

EDUCATION
B.Tech Information Technology — Anna University (2021)

PROJECTS
- House Price Prediction (Linear Regression, scikit-learn, Pandas)
- Sales Dashboard (SQL + Power BI)
"""

# ── Resume 3: Weak Candidate ──────────────────────────────────────
RESUME_WEAK = """
Name: Rahul Verma
Email: rahul.v@email.com

SUMMARY
Recent graduate interested in data science. I have completed online courses in Python
and data analysis and am eager to learn.

SKILLS
Programming: Python (basic), HTML, CSS
Tools: Microsoft Excel, Google Sheets
Other: MS Word, PowerPoint

EDUCATION
B.Com — Delhi University (2023)
Online Courses:
- Python for Beginners (Udemy)
- Excel for Data Analysis (Coursera)

PROJECTS
- Student Grade Calculator (Python script)
- Monthly Expense Tracker (Excel)

EXPERIENCE
No professional experience in data science or machine learning.
"""

RESUMES = {
    "Strong":  RESUME_STRONG,
    "Average": RESUME_AVERAGE,
    "Weak":    RESUME_WEAK,
}
