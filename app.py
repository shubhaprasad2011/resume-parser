import streamlit as st
import pdfplumber
import re
import spacy
import os
# os.system("python -m spacy download en_core_web_sm")

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
        "python", "java", "c++", "machine learning",
        "nlp", "sql", "data science", "tensorflow"
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