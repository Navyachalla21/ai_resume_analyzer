import streamlit as st
import pandas as pd

from resume_parser import extract_resume_text
from skill_extractor import load_skill_dictionary, extract_skills, get_flat_skill_list
from job_matcher import load_job_roles, match_resume_to_roles, get_skill_gap
from roadmap_generator import generate_roadmap
from report_builder import build_report_pdf

st.set_page_config(page_title="Resume Analyzer", page_icon="🧭", layout="wide")

# ---------- Custom styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@500;600&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
    color: #1B2A4A;
    line-height: 1.6;
}
.stApp {
    background-color: #F6F8FB;
}
h1, h2, h3 {
    font-family: 'Fraunces', serif;
    color: #1B2A4A;
    font-weight: 600;
    margin-top: 0.6em;
}
p, li, span, label {
    line-height: 1.6;
}

/* Sidebar background + only the text we control directly */
[data-testid="stSidebar"] {
    background-color: #1B2A4A;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] .stCaption {
    color: #F6F8FB !important;
}

/* File uploader: force readable colors regardless of sidebar theme */
[data-testid="stFileUploader"] {
    background-color: #FFFFFF;
    border-radius: 6px;
    padding: 10px;
}
[data-testid="stFileUploader"] * {
    color: #1B2A4A !important;
}
[data-testid="stFileUploaderDropzone"] button {
    background-color: #0F766E !important;
    color: white !important;
    border-radius: 4px !important;
    border: none !important;
}
[data-testid="stFileUploaderDropzone"] button * {
    color: white !important;
}

/* Uploaded file name row (appears below the dropzone) */
[data-testid="stFileUploaderFile"] {
    background-color: #FFFFFF;
    border-radius: 4px;
    padding: 4px 8px;
}
[data-testid="stFileUploaderFile"] * {
    color: #1B2A4A !important;
}

div.stButton > button, .stDownloadButton > button {
    background-color: #0F766E;
    color: white;
    border-radius: 4px;
    border: none;
    padding: 0.5em 1.2em;
    font-weight: 500;
}
div.stButton > button:hover, .stDownloadButton > button:hover {
    background-color: #0B5C55;
    color: white;
}

.role-card {
    background-color: white;
    border: 1px solid #E2E8F0;
    border-left: 4px solid #C9A15A;
    border-radius: 4px;
    padding: 14px 18px;
    margin-bottom: 10px;
    line-height: 1.5;
}
.gap-card {
    background-color: white;
    border: 1px solid #E2E8F0;
    border-radius: 4px;
    padding: 16px 20px;
    line-height: 1.7;
}

/* Tables/dataframes */
[data-testid="stTable"], [data-testid="stDataFrame"] {
    border: 1px solid #E2E8F0;
    border-radius: 4px;
}
/* Metric cards (Best Match / Skills Detected / Roles Compared) */
[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 4px;
    padding: 12px 16px;
    overflow: visible !important;
}
[data-testid="stMetricValue"] {
    color: #1B2A4A !important;
    font-family: 'Fraunces', serif;
    font-size: 1.1rem !important;
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: unset !important;
    line-height: 1.3 !important;
}
[data-testid="stMetricValue"] > div {
    white-space: normal !important;
    overflow: visible !important;
    text-overflow: unset !important;
}

}
[data-testid="stMetricDelta"] {
    color: #0F766E !important;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
    color: #F6F8FB !important;
    [data-testid="stMetricValue"] {
    color: #1B2A4A !important;
    font-family: 'Fraunces', serif;
    font-size: 1.3rem !important;
    white-space: normal !important;
    overflow-wrap: break-word !important;
}
}
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 🧭 Resume Analyzer")
    st.write("Upload your resume to see how it matches real job roles, spot skill gaps, and get a learning plan.")
    uploaded_file = st.file_uploader("Upload resume")
    st.markdown("---")

# ---------- Main area ----------
st.title("AI Resume Analyzer & Job Recommendation System")
st.write("A quick, honest read on how your resume lines up with in-demand roles.")

if uploaded_file is not None:
    st.success(f"Analyzing: **{uploaded_file.name}**")

    try:
        resume_text = extract_resume_text(uploaded_file)

        skill_df = load_skill_dictionary()
        found_skills_by_category = extract_skills(resume_text, skill_df)
        flat_skills = get_flat_skill_list(found_skills_by_category)

        job_roles_df = load_job_roles()
        skills_text = ", ".join(flat_skills)
        results = match_resume_to_roles(skills_text, job_roles_df)

        # --- Top match highlight ---
        top_role = results.iloc[0]
        col1, col2, col3 = st.columns(3)
        col1.metric("Best Match", top_role["job_role"], f"{top_role['match_score']}%")
        col2.metric("Skills Detected", len(flat_skills))
        col3.metric("Roles Compared", len(results))

        st.markdown("### 🛠 Extracted Skills")
        for category, skills in found_skills_by_category.items():
            st.markdown(f"**{category.title()}:** {', '.join(skills)}")

        st.markdown("### 📊 Job Role Match Scores")
        st.bar_chart(results.set_index("job_role")["match_score"])

        st.markdown("### 🏆 Top Recommended Roles")
        for i, row in results.head(3).iterrows():
            st.markdown(
                f"<div class='role-card'><b>{i+1}. {row['job_role']}</b> — {row['match_score']}% match</div>",
                unsafe_allow_html=True
            )

        st.markdown("### 🔍 Skill Gap Analysis")
        target_role = st.selectbox("Select a target role to analyze:", results["job_role"])
        target_row = job_roles_df[job_roles_df["job_role"] == target_role].iloc[0]
        gap = get_skill_gap(flat_skills, target_row["required_skills"])

        gcol1, gcol2 = st.columns(2)
        with gcol1:
            st.markdown(
                f"<div class='gap-card'><b>✅ Skills you have</b><br>{', '.join(gap['present']) or 'None found'}</div>",
                unsafe_allow_html=True
            )
        with gcol2:
            st.markdown(
                f"<div class='gap-card'><b>❌ Missing skills</b><br>{', '.join(gap['missing']) or 'None — great match!'}</div>",
                unsafe_allow_html=True
            )

        st.markdown("### 🗺 Suggested Learning Roadmap")
        roadmap = generate_roadmap(gap["missing"])
        if roadmap:
            for step in roadmap:
                st.write(f"• {step}")
        else:
            st.write("No additional learning needed for this role — great job!")

        st.markdown("### ⬇️ Download Report")
        pdf_buffer = build_report_pdf(uploaded_file, found_skills_by_category, results, target_role, gap, roadmap)
        st.download_button(
            label="Download Report as PDF",
            data=pdf_buffer,
            file_name="resume_analysis_report.pdf",
            mime="application/pdf"
        )

    except Exception as e:
        st.error(f"Something went wrong while processing your resume: {e}")

else:
    st.info("👈 Upload a resume from the sidebar to get started.")