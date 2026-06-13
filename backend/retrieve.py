import json

from embeddings import get_embedding
from vector_store import collection
from langfuse import observe
with open("data/jd.json", "r") as f:
    jd = json.load(f)

query_text = f"""
Job Title:
{jd.get("job_title", "")}

Required Skills:
{", ".join(jd.get("required_skills", []))}

Responsibilities:
{" ".join(jd.get("responsibilities", []))}
"""

query_embedding = get_embedding(query_text)

@observe(name="get_top_candidate")
def get_top_candidate():
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=1
    )

    candidate_profile = results["documents"][0][0]

    return candidate_profile

def get_top_candidates(k=5):

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    return results["documents"][0]

if __name__ == "__main__":
    print(get_top_candidate())