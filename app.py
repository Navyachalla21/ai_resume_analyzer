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
@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: #1B2A4A;
}
.stApp {
    background-color: #F4F6FA;
}
h1, h2, h3 {
    font-family: 'Fraunces', serif;
    color: #1B2A4A;
    font-weight: 600;
}

/* ---------- Sidebar (light, not dark) ---------- */
[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E2E8F0;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: #1B2A4A !important;
}

/* ---------- File uploader ---------- */
[data-testid="stFileUploader"] {
    background-color: #F8FAFC;
    border: 1.5px dashed #94A3B8;
    border-radius: 10px;
    padding: 14px;
}
[data-testid="stFileUploaderDropzone"] button {
    background-color: #0F766E !important;
    color: white !important;
    border-radius: 6px !important;
    border: none !important;
    font-weight: 500;
}
[data-testid="stFileUploaderFile"] {
    background-color: #FFFFFF;
    border-radius: 6px;
    padding: 6px 10px;
    border: 1px solid #E2E8F0;
}

/* ---------- Buttons ---------- */
div.stButton > button, .stDownloadButton > button {
    background-color: #0F766E;
    color: white !important;
    border-radius: 8px;
    border: none;
    padding: 0.6em 1.4em;
    font-weight: 600;
    box-shadow: 0 1px 2px rgba(0,0,0,0.08);
    transition: 0.15s ease;
}
div.stButton > button:hover, .stDownloadButton > button:hover {
    background-color: #0B5C55;
    color: white !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.12);
}

/* ---------- Header banner ---------- */
.header-banner {
    background: linear-gradient(135deg, #0F766E 0%, #134E4A 100%);
    border-radius: 14px;
    padding: 28px 32px;
    margin-bottom: 24px;
    color: white;
}
.header-banner h1 {
    color: white !important;
    margin: 0 0 6px 0;
    font-size: 1.9rem;
}
.header-banner p {
    color: #D1FAE5 !important;
    margin: 0;
    font-size: 1rem;
}

/* ---------- Metric cards ---------- */
[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
    padding: 16px 18px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
[data-testid="stMetricValue"] {
    color: #0F766E !important;
    font-family: 'Fraunces', serif;
    font-size: 1.5rem !important;
    white-space: normal !important;
    overflow: visible !important;
}
[data-testid="stMetricLabel"] {
    color: #64748B !important;
    font-weight: 500;
}

/* ---------- Section cards ---------- */
.section-card {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 18px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

/* ---------- Skill badges ---------- */
.skill-badge {
    display: inline-block;
    background-color: #E6F4F1;
    color: #0F766E;
    border: 1px solid #B7E4DC;
    border-radius: 20px;
    padding: 4px 14px;
    margin: 3px 5px 3px 0;
    font-size: 0.85rem;
    font-weight: 500;
}
.skill-badge-missing {
    display: inline-block;
    background-color: #FEF2F2;
    color: #B91C1C;
    border: 1px solid #FCA5A5;
    border-radius: 20px;
    padding: 4px 14px;
    margin: 3px 5px 3px 0;
    font-size: 0.85rem;
    font-weight: 500;
}

/* ---------- Role rank cards ---------- */
.role-card {
    background-color: white;
    border: 1px solid #E2E8F0;
    border-left: 5px solid #C9A15A;
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 10px;
}
.role-card-top {
    border-left: 5px solid #0F766E;
    background-color: #F0FAF8;
}
.rank-badge {
    display: inline-block;
    background-color: #1B2A4A;
    color: white;
    border-radius: 50%;
    width: 26px;
    height: 26px;
    text-align: center;
    line-height: 26px;
    font-size: 0.8rem;
    font-weight: 700;
    margin-right: 10px;
}

/* ---------- Progress bar wrapper ---------- */
.progress-outer {
    background-color: #E2E8F0;
    border-radius: 10px;
    height: 10px;
    width: 100%;
    margin-top: 6px;
}
.progress-inner {
    background-color: #0F766E;
    border-radius: 10px;
    height: 10px;
}

hr {
    border: none;
    border-top: 1px solid #E2E8F0;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 🧭 Resume Analyzer")
    st.write("Upload your resume to see how it matches real job roles, spot skill gaps, and get a learning plan.")
    uploaded_file = st.file_uploader("Upload resume", type=["pdf", "docx"])
    st.markdown("---")
    st.caption("Supported formats: PDF, DOCX")
    st.caption("Your file is processed in-memory only — never saved to disk.")

# ---------- Header ----------
st.markdown("""
<div class="header-banner">
    <h1>AI Resume Analyzer & Job Recommendation System</h1>
    <p>A quick, honest read on how your resume lines up with in-demand roles.</p>
</div>
""", unsafe_allow_html=True)

# ---------- Main area ----------
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
        col1.metric("🎯 Best Match", top_role["job_role"], f"{top_role['match_score']}%")
        col2.metric("🛠 Skills Detected", len(flat_skills))
        col3.metric("📋 Roles Compared", len(results))

        st.markdown("<br>", unsafe_allow_html=True)

        # --- Extracted skills ---
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 🛠 Extracted Skills")
        if found_skills_by_category:
            for category, skills in found_skills_by_category.items():
                badges = "".join([f'<span class="skill-badge">{s}</span>' for s in skills])
                st.markdown(f"**{category.title()}**<br>{badges}", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
        else:
            st.write("No recognizable skills found in this resume.")
        st.markdown('</div>', unsafe_allow_html=True)

        # --- Match scores chart ---
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Job Role Match Scores")
        st.bar_chart(results.set_index("job_role")["match_score"], color="#0F766E")
        st.markdown('</div>', unsafe_allow_html=True)

        # --- Top recommended roles ---
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 🏆 Top Recommended Roles")
        for i, row in results.head(3).iterrows():
            css_class = "role-card role-card-top" if i == 0 else "role-card"
            score = float(row["match_score"])
            st.markdown(
                f"""<div class="{css_class}">
                    <span class="rank-badge">{i+1}</span><b>{row['job_role']}</b> — {row['match_score']}% match
                    <div class="progress-outer"><div class="progress-inner" style="width:{min(score,100)}%;"></div></div>
                </div>""",
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

        # --- Skill gap analysis ---
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 🔍 Skill Gap Analysis")
        target_role = st.selectbox("Select a target role to analyze:", results["job_role"])
        target_row = job_roles_df[job_roles_df["job_role"] == target_role].iloc[0]
        gap = get_skill_gap(flat_skills, target_row["required_skills"])

        gcol1, gcol2 = st.columns(2)
        with gcol1:
            st.markdown("**✅ Skills you have**")
            if gap["present"]:
                st.markdown("".join([f'<span class="skill-badge">{s}</span>' for s in gap["present"]]), unsafe_allow_html=True)
            else:
                st.write("None found")
        with gcol2:
            st.markdown("**❌ Missing skills**")
            if gap["missing"]:
                st.markdown("".join([f'<span class="skill-badge-missing">{s}</span>' for s in gap["missing"]]), unsafe_allow_html=True)
            else:
                st.write("None — great match!")
        st.markdown('</div>', unsafe_allow_html=True)

        # --- Learning roadmap ---
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### 🗺 Suggested Learning Roadmap")
        roadmap = generate_roadmap(gap["missing"])
        if roadmap:
            for step in roadmap:
                st.write(f"• {step}")
        else:
            st.write("No additional learning needed for this role — great job!")
        st.markdown('</div>', unsafe_allow_html=True)

        # --- Download report ---
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