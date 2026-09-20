import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from text_cleaner import clean_text

def load_job_roles(csv_path="data/job_roles.csv") -> pd.DataFrame:
    """Loads the job roles and their required skills."""
    return pd.read_csv(csv_path)

def match_resume_to_roles(resume_text: str, job_roles_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compares the resume against every job role's required skills using
    TF-IDF vectors and cosine similarity. Returns roles ranked by match score.
    """
    cleaned_resume = clean_text(resume_text)

    # Build the list of documents: resume first, then each job role's skills
    documents = [cleaned_resume] + job_roles_df["required_skills"].tolist()

    # Convert all documents into TF-IDF vectors
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Compare the resume vector (row 0) against every job role vector (rows 1+)
    resume_vector = tfidf_matrix[0:1]
    role_vectors = tfidf_matrix[1:]
    similarity_scores = cosine_similarity(resume_vector, role_vectors)[0]

    results = job_roles_df.copy()
    results["match_score"] = (similarity_scores * 100).round(1)
    results = results.sort_values(by="match_score", ascending=False).reset_index(drop=True)

    return results

def get_skill_gap(found_skills: list, required_skills_str: str) -> dict:
    """
    Compares the skills found in a resume against a job role's required skills.
    Returns which required skills are present and which are missing.
    """
    required_skills = [s.strip().lower() for s in required_skills_str.split(",")]
    found_skills_lower = [s.lower() for s in found_skills]

    present = [skill for skill in required_skills if skill in found_skills_lower]
    missing = [skill for skill in required_skills if skill not in found_skills_lower]

    return {
        "present": present,
        "missing": missing
    }