import json

from embeddings import get_embedding
from vector_store import collection

with open("data/jd.json", "r") as f:
    jd = json.load(f)

# Build a rich query from the JD
query_text = f"""
Job Title:
{jd.get("job_title", "")}

Required Skills:
{", ".join(jd.get("required_skills", []))}

Responsibilities:
{" ".join(jd.get("responsibilities", []))}
"""

query_embedding = get_embedding(query_text)

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=5
)

print("\nTop Matching Candidates:\n")

for i, doc in enumerate(results["documents"][0], start=1):
    print(f"\nCandidate #{i}")
    print("")
    print(doc[:500])