from typing import TypedDict

from langgraph.graph import StateGraph, END


class GraphState(TypedDict):
    candidate: str
    evaluation: dict