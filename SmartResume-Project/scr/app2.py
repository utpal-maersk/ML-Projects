import streamlit as st
import numpy as np
import pickle
from PyPDF2 import PdfReader
import matplotlib.pyplot as plt

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="AI Resume Screener", layout="wide")

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
.card {
    padding: 20px;
    border-radius: 15px;
    background: #1c1f26;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
}
.big-font {
    font-size: 40px !important;
    font-weight: bold;
}
.green {color: #00ffae;}
.red {color: #ff4b4b;}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------
st.markdown("<h1 style='text-align:center; color:#00ffae;'>AI Resume Screener</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Smart Hiring Assistant</p>", unsafe_allow_html=True)

# -----------------------------
# LOAD MODEL
# -----------------------------
with open("../models/model.pkl", "rb") as f:
    model = pickle.load(f)

# -----------------------------
# LAYOUT
# -----------------------------
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📄 Upload Resume")
    uploaded_file = st.file_uploader("", type=["txt", "pdf"])

with col2:
    st.markdown("### 💼 Job Requirements")
    required_exp = st.slider("Experience", 0, 10, 3)
    job_domain = st.text_input("Domain", "data science")
    jd_skills = st.text_input("Skills", "python, sql").split(",")

# -----------------------------
# PDF READER
# -----------------------------
def read_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# -----------------------------
# SKILL EXTRACTION
# -----------------------------
def extract_skills(text):
    skills_list = ["python", "sql", "java", "aws", "machine learning"]
    text = text.lower()
    return [s for s in skills_list if s in text]


domain_map = {
    "data science": ["data science", "data analyst", "machine learning", "ai"],
    "finance": ["finance", "accounting", "banking"],
    "law": ["law", "legal", "advocate"],
    "java developer": ["java", "spring", "backend"]
}

education_map = [
    "computer science",
    "data science",
    "information technology",
    "it",
    "artificial intelligence",
    "ai",
    "software engineering"
]


def domain_match_func(job_domain, resume_text):
    resume_text = resume_text.lower()
    job_domain = job_domain.lower()

    if job_domain in domain_map:
        keywords = domain_map[job_domain]
        matches = sum([1 for k in keywords if k in resume_text])
        return matches / len(keywords)

    return 0

def education_match_func(resume_text):
    resume_text = resume_text.lower()

    matches = sum([1 for edu in education_map if edu in resume_text])

    return matches / len(education_map)

# -----------------------------
# BUTTON
# -----------------------------
if st.button(" Analyze Resume"):

    if uploaded_file is None:
        st.warning(" Upload resume first!")
    else:

        # -----------------------------
        # READ FILE
        # -----------------------------
        if uploaded_file.type == "text/plain":
            resume_text = uploaded_file.read().decode("utf-8")
        else:
            resume_text = read_pdf(uploaded_file)

        # -----------------------------
        # FEATURES
        # -----------------------------
        skills = extract_skills(resume_text)

        skill_score = len([s for s in jd_skills if s.strip().lower() in skills]) / len(jd_skills)
        exp_score = 1
        domain_score = domain_match_func(job_domain, resume_text)
        education_score = education_match_func(resume_text)

        flag_score = 0.5
        keyword_score = 0.5
        profile_score = 0.5
        length_score = len(resume_text.split()) / 1000

        # -----------------------------
        # MODEL INPUT
        # -----------------------------
        input_data = np.array([[
            skill_score, exp_score, domain_score,
            education_score, flag_score,
            keyword_score, profile_score, length_score
        ]])

        prediction = model.predict(input_data)[0]

        # -----------------------------
        # FINAL SCORE
        # -----------------------------
        final_score = (
        0.25 * skill_score +
        0.25 * exp_score +
        0.15 * domain_score +
        0.15 * education_score +
        0.1 * flag_score +
        0.05 * keyword_score +
        0.05 * profile_score
    )

        # -----------------------------
        # RESULT
        # -----------------------------
        st.markdown("---")
        st.markdown("##  Result")

        if prediction == 1:
            st.success(f"{round(final_score*100)}% Match - Selected")
        else:
            st.error(f"{round(final_score*100)}% Match - Not Selected")

        # -----------------------------
        # METRICS
        # -----------------------------
        st.markdown("## 📊 Key Metrics")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Skill", f"{int(skill_score*100)}%")
        col2.metric("Experience", f"{int(exp_score*100)}%")
        col3.metric("Domain", f"{int(domain_score*100)}%")
        col4.metric("Education", f"{int(education_score*100)}%")

        # -----------------------------
        # PROGRESS BARS
        # -----------------------------
        st.markdown("### 📊 Score Breakdown")
        

        def show_score(label, score):
            percent = int(score * 100)

            if percent > 70:
                color = "🟢"
            elif percent > 40:
                color = "🟡"
            else:
                color = "🔴"

            st.markdown(f"**{label} {color}**")
            st.progress(min(score + 0.01, 1.0))
            st.caption(f"{percent}% match")

        show_score("Skill Match", skill_score)
        show_score("Experience", exp_score)
        show_score("Domain Match", domain_score)
        show_score("Education Match", education_score)

        # -----------------------------
        # RADAR CHART
        # -----------------------------
        st.markdown("### 📊 Visual Analysis")

        labels = ['Skill', 'Experience', 'Domain', 'Education']
        scores = [skill_score, exp_score, domain_score, education_score]

        scores += scores[:1]
        angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(subplot_kw=dict(polar=True))
        ax.plot(angles, scores)
        ax.fill(angles, scores, alpha=0.3)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)

        st.pyplot(fig)

        # -----------------------------
        # SKILLS
        # -----------------------------
        st.markdown("### 🧠 Detected Skills")
        st.write(" ".join([f"`{s}`" for s in skills]))

        # -----------------------------
        # EXPLANATION
        # -----------------------------
        st.markdown("### 🧠 Why this score?")

        reasons = []

        if skill_score > 0.7:
            reasons.append("Strong skill match")
        elif skill_score > 0.4:
            reasons.append("Moderate skill match")
        else:
            reasons.append("Low skill alignment")

        if domain_score == 1:
            reasons.append("Relevant domain experience")

        if education_score == 1:
            reasons.append("Relevant education background")

        for r in reasons:
            st.write(f"✔️ {r}")

        # -----------------------------
        # RECOMMENDATION
        # -----------------------------
        st.markdown("### 💼 Recommendation")

        if final_score > 0.75:
            st.success("🔥 Strong candidate – shortlist immediately")
        elif final_score > 0.5:
            st.info("👍 Moderate match – consider for interview")
        else:
            st.warning("❌ Not recommended")

        # -----------------------------
        # RESUME PREVIEW
        # -----------------------------
        with st.expander("📄 View Resume"):
            st.write(resume_text[:1000])