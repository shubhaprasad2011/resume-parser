import streamlit as st
import pdfplumber
import re
import spacy
@st.cache_resource
def load_model():
    return spacy.load("en_core_web_sm")

nlp = load_model()

nlp = spacy.load("en_core_web_sm")

# -------- PDF TEXT --------
def extract_text(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
    return text

# -------- EMAIL --------
def get_email(text):
    return re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)

# -------- PHONE --------
def get_phone(text):
    return re.findall(r"\b\d{10}\b", text)

# -------- NAME --------
def get_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return "Not Found"

# -------- SKILLS (Improved with N-grams idea) --------
def get_skills(text):
    skills_db = [
    # Programming Languages
    "python", "java", "c", "c++", "c#", "go", "rust", "kotlin", "swift",

    # Microsoft Stack
    ".net", "asp.net", "asp.net core", "entity framework", "linq",
    "azure", "azure functions", "azure devops", "power bi", "power apps","ssis", "ssrs",

    # Web Development
    "javascript", "typescript", "html", "css", "sass", "bootstrap",
    "react", "angular", "vue.js", "next.js", "node.js", "express.js",

    # Databases
    "sql", "mysql", "postgresql", "sql server", "oracle",
    "mongodb", "redis", "cassandra", "dynamodb",

    # Data & AI
    "data science", "data analysis", "machine learning", "deep learning",
    "nlp", "computer vision", "tensorflow", "pytorch", "scikit-learn",
    "pandas", "numpy",

    # Cloud & DevOps
    "aws", "azure", "google cloud", "cloud computing",
    "docker", "kubernetes", "jenkins", "terraform", "ansible",
    "ci/cd", "devops",

    # APIs & Architecture
    "rest api", "graphql", "microservices", "system design",
    "design patterns",

    # Testing
    "unit testing", "integration testing", "selenium", "cypress", "junit",

    # OS & Networking
    "linux", "unix", "networking", "shell scripting",

    # Security
    "cybersecurity", "ethical hacking", "oauth", "jwt",

    # Big Data
    "hadoop", "spark", "kafka", "hive",

    # Tools
    "git", "github", "gitlab", "bitbucket", "jira",

    # Other
    "agile", "scrum", "problem solving", "data structures", "algorithms"
    ]
    
    text_lower = text.lower()
    found = [skill for skill in skills_db if skill in text_lower]
    return list(set(found))


# -------- STREAMLIT UI --------
st.title("📄 Resume Parser (NLP Project)")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file:
    text = extract_text(uploaded_file)
    
    st.subheader("📌 Extracted Information")
    
    st.write("**Name:**", get_name(text))
    st.write("**Email:**", get_email(text))
    st.write("**Phone:**", get_phone(text))
    st.write("**Skills:**", get_skills(text))