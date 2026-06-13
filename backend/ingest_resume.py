import json

from embeddings import get_embedding
from vector_store import collection


def store_resume(file_path):

    with open(file_path, "r") as f:
        resume = json.load(f)

    candidate_name = resume["name"]

    skills_text = ", ".join(
        resume.get("skills", [])
    )

    resume_text = f"""
    Candidate: {candidate_name}

    Skills:
    {skills_text}
    """

    embedding = get_embedding(
        resume_text
    )

    candidate_id = (
        candidate_name
        .lower()
        .replace(" ", "_")
    )

    collection.add(
        ids=[candidate_id],
        documents=[resume_text],
        embeddings=[embedding]
    )

    print(
        f"Stored {candidate_name}"
    )
if __name__ == "__main__":

    store_resume(
        "data/candidate_1.json"
    )

    store_resume(
        "data/candidate_2.json"
    )

    store_resume(
        "data/candidate_3.json"
    )

    store_resume(
        "data/candidate_4.json"
    )