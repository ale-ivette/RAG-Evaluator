# RAG Evaluator

Automated quality evaluation system for RAG (Retrieval-Augmented Generation) pipelines using RAGAS metrics — applied to Dynamics 365 Finance data.

## Why this matters
Most AI engineers build RAG systems. Few can prove they work well. This tool provides quantitative evidence of RAG quality across 4 dimensions, bridging the gap between prototype and production-ready system.

## Evaluation metrics

| Metric | What it measures |
|---|---|
| Faithfulness | Does the answer stay true to the retrieved context? Detects hallucinations. |
| Answer Relevancy | Does the answer actually address the question asked? |
| Context Precision | Were the right document chunks retrieved? |
| Context Recall | Was all necessary information retrieved? |

## Results on D365 Finance dataset

| Metric | Score |
|---|---|
| Faithfulness | 1.000 |
| Answer Relevancy | 0.953 |
| Context Precision | 1.000 |
| Context Recall | 1.000 |

## Architecture
- **RAGAS** — evaluation framework using LLM-as-judge methodology
- **LangChain** — RAG pipeline orchestration
- **ChromaDB** — vector store for semantic retrieval
- **OpenAI GPT-3.5** — language model for generation and evaluation
- **Streamlit + Plotly** — interactive dashboard with score