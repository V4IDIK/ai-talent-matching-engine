import json
from typing import TypedDict
from langgraph.graph import StateGraph, END
from retrieve import get_top_candidate
from evaluate_candidate import evaluate_candidate
from langfuse import observe


class GraphState(TypedDict):
    candidate: str
    evaluation: dict

@observe(name="retrieve_node")
def retrieve_node(state):

    candidate = get_top_candidate()

    return {
        "candidate": candidate
    }

@observe(name="evaluate_node")
def evaluate_node(state):

    evaluation = evaluate_candidate(
        state["candidate"]
    )

    return {
        "evaluation": evaluation
    }

@observe(name="save_node")
def save_node(state):

    with open(
        "data/evaluation.json",
        "w"
    ) as f:
        json.dump(
            state["evaluation"],
            f,
            indent=4
        )

    return state


workflow = StateGraph(GraphState)

workflow.add_node(
    "retrieve",
    retrieve_node
)

workflow.add_node(
    "evaluate",
    evaluate_node
)

workflow.set_entry_point(
    "retrieve"
)

workflow.add_edge(
    "retrieve",
    "evaluate"
)

workflow.add_node(
    "save",
    save_node
)

workflow.add_edge(
    "evaluate",
    "save"
)

workflow.add_edge(
    "save",
    END
)

app = workflow.compile()

result = app.invoke({})

print("\nLANGGRAPH RESULT\n")
print(result)