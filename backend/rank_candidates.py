import json

from retrieve import get_top_candidates
from evaluate_candidate import evaluate_candidate


candidates = get_top_candidates(5)

rankings = []

for candidate in candidates:

    evaluation = evaluate_candidate(
        candidate
    )

    candidate_name = "Unknown"

    for line in candidate.split("\n"):
        if line.strip().startswith("Candidate:"):
            candidate_name = (
                line.replace("Candidate:", "")
                .strip()
            )
            break
    
    rankings.append({
        "candidate": candidate_name,
        "score": evaluation["match_score"],
        "evaluation": evaluation
    })

rankings.sort(
    key=lambda x: x["score"],
    reverse=True
)

with open(
    "data/rankings.json",
    "w"
) as f:
    json.dump(
        rankings,
        f,
        indent=4
    )