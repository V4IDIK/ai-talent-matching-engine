import json
from typing import TypedDict

from langgraph.graph import StateGraph, END
from langfuse import observe

from retrieve import get_top_candidates
from evaluate_candidate import evaluate_candidate


class GraphState(TypedDict):
    candidates: list
    rankings: list


@observe(name="retrieve_candidates_node")
def retrieve_candidates_node(state):

    candidates = get_top_candidates(5)

    return {
        "candidates": candidates
    }


@observe(name="rank_candidates_node")
def rank_candidates_node(state):

    rankings = []

    for candidate in state["candidates"]:

        evaluation = evaluate_candidate(candidate)

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

    return {
        "rankings": rankings
    }


@observe(name="save_rankings_node")
def save_rankings_node(state):

    with open(
        "data/rankings.json",
        "w"
    ) as f:
        json.dump(
            state["rankings"],
            f,
            indent=4
        )

    print("\nRankings saved to data/rankings.json")

    return state


workflow = StateGraph(GraphState)

workflow.add_node(
    "retrieve_candidates",
    retrieve_candidates_node
)

workflow.add_node(
    "rank_candidates",
    rank_candidates_node
)

workflow.add_node(
    "save_rankings",
    save_rankings_node
)

workflow.set_entry_point(
    "retrieve_candidates"
)

workflow.add_edge(
    "retrieve_candidates",
    "rank_candidates"
)

workflow.add_edge(
    "rank_candidates",
    "save_rankings"
)

workflow.add_edge(
    "save_rankings",
    END
)

app = workflow.compile()

result = app.invoke({})

print("\nLANGGRAPH RANKING RESULT\n")
print(
    json.dumps(
        result["rankings"],
        indent=4
    )
)