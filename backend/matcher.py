import json

from sklearn.metrics.pairwise import cosine_similarity

from embeddings import get_embedding

with open("data/candidate_1.json") as f:
    resume = json.load(f)

with open("data/jd.json") as f:
    jd = json.load(f)

resume_text = " ".join(
    resume["skills"]
)

jd_text = " ".join(
    jd["required_skills"]
)

resume_embedding = get_embedding(
    resume_text
)

jd_embedding = get_embedding(
    jd_text
)

score = cosine_similarity(
    [resume_embedding],
    [jd_embedding]
)[0][0]

print(
    f"Semantic Match Score: {score*100:.2f}%"
)