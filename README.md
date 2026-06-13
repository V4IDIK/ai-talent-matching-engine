# AI Talent Matching Engine

An AI-powered talent matching system that uses semantic search, RAG (Retrieval-Augmented Generation), and Gemini to match candidates with job descriptions.

## Features

* Semantic candidate retrieval using ChromaDB
* BGE embeddings with Sentence Transformers
* Gemini-powered candidate evaluation
* Multi-candidate ranking
* LangGraph workflow orchestration
* Langfuse observability and tracing

## Tech Stack

* Python
* Gemini 2.5 Flash
* LangChain
* LangGraph
* Langfuse
* ChromaDB
* Sentence Transformers (BGE)

## Workflow

```text
Candidate Profiles
        ↓
     Embeddings
        ↓
      ChromaDB
        ↓
 Semantic Retrieval
        ↓
      Gemini
        ↓
 Candidate Evaluation
        ↓
 Candidate Ranking
```

## Run

```bash
pip install -r requirements.txt

python backend/graph_ranking.py
```

## Concepts Demonstrated

* Retrieval-Augmented Generation (RAG)
* Semantic Search
* Vector Databases
* LLM-based Evaluation
* Workflow Orchestration
* AI Observability

```
```
