import pandas as pd
from text_cleaner import clean_text

def load_skill_dictionary(csv_path="data/skill_dictionary.csv") -> pd.DataFrame:
    """Loads the master list of known skills and their categories."""
    return pd.read_csv(csv_path)

def extract_skills(resume_text: str, skill_df: pd.DataFrame) -> dict:
    """
    Searches the cleaned resume text for every skill in the skill dictionary.
    Returns a dictionary grouping found skills by category.
    """
    cleaned_text = clean_text(resume_text)
    found_skills = {}

    for _, row in skill_df.iterrows():
        skill = row["skill"].lower().strip()
        category = row["category"]

        # Check if the skill appears as a whole word/phrase in the resume text
        if skill in cleaned_text:
            found_skills.setdefault(category, []).append(skill)

    return found_skills

def get_flat_skill_list(found_skills: dict) -> list:
    """Flattens the categorized skills dict into a single list of skill names."""
    flat_list = []
    for skills in found_skills.values():
        flat_list.extend(skills)
    return flat_list