# A simple rule-based mapping of skills to suggested learning topics/resources.
# This is the "beginner approach" your PDF specifies (rule-based roadmap).
LEARNING_SUGGESTIONS = {
    "fastapi": "Learn FastAPI basics — build a simple REST API endpoint.",
    "docker": "Learn Docker fundamentals — containerize a small Python app.",
    "sql": "Practice SQL queries — joins, aggregations, and subqueries.",
    "power bi": "Build a sample dashboard in Power BI using public datasets.",
    "machine learning": "Complete a beginner ML course covering regression and classification.",
    "scikit-learn": "Practice building models with scikit-learn on a Kaggle dataset.",
    "pytorch": "Follow the official PyTorch tutorials to build a basic neural network.",
    "tensorflow": "Complete a TensorFlow/Keras beginner course.",
    "nlp": "Learn NLP basics — tokenization, embeddings, and simple text classification.",
    "transformers": "Learn how to use Hugging Face Transformers for a simple NLP task.",
    "opencv": "Practice basic image processing tasks using OpenCV.",
    "cnn": "Learn Convolutional Neural Network fundamentals for image tasks.",
    "cloud deployment": "Deploy a small app to a free-tier cloud platform (e.g., Render, Streamlit Cloud).",
}

DEFAULT_SUGGESTION = "Explore introductory tutorials and hands-on projects for this skill."

def generate_roadmap(missing_skills: list) -> list:
    """
    Generates a simple learning roadmap: one suggestion per missing skill,
    in the order they appear (roughly simulating a week-by-week plan).
    """
    roadmap = []
    for week, skill in enumerate(missing_skills, start=1):
        suggestion = LEARNING_SUGGESTIONS.get(skill, DEFAULT_SUGGESTION)
        roadmap.append(f"Week {week}: {skill.title()} — {suggestion}")
    return roadmap