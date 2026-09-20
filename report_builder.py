from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def build_report_pdf(uploaded_file, found_skills_by_category, results, target_role, gap, roadmap):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                             topMargin=0.7*inch, bottomMargin=0.7*inch,
                             leftMargin=0.7*inch, rightMargin=0.7*inch)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("AI Resume Analyzer — Analysis Report", styles["Title"]))
    story.append(Paragraph(f"Resume File: {uploaded_file.name}", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Extracted Skills", styles["Heading2"]))
    for category, skills in found_skills_by_category.items():
        story.append(Paragraph(f"<b>{category.title()}:</b> {', '.join(skills)}", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Job Role Match Scores", styles["Heading2"]))
    for _, row in results.iterrows():
        story.append(Paragraph(f"{row['job_role']}: {row['match_score']}%", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Top 3 Recommended Roles", styles["Heading2"]))
    for i, row in results.head(3).iterrows():
        story.append(Paragraph(f"{i+1}. {row['job_role']} — {row['match_score']}%", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph(f"Skill Gap Analysis (Target Role: {target_role})", styles["Heading2"]))
    present_text = ', '.join(gap['present']) if gap['present'] else 'None found'
    missing_text = ', '.join(gap['missing']) if gap['missing'] else 'None — great match!'
    story.append(Paragraph(f"<b>Skills you have:</b> {present_text}", styles["Normal"]))
    story.append(Paragraph(f"<b>Missing skills:</b> {missing_text}", styles["Normal"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Suggested Learning Roadmap", styles["Heading2"]))
    if roadmap:
        for step in roadmap:
            story.append(Paragraph(step, styles["Normal"]))
    else:
        story.append(Paragraph("No additional learning needed for this role.", styles["Normal"]))

    doc.build(story)
    buffer.seek(0)
    return buffer