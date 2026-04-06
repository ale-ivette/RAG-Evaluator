import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from evaluator import build_rag_pipeline, run_evaluation

st.set_page_config(
    page_title="RAG Evaluator",
    page_icon="📊",
    layout="wide"
)

st.title("RAG Quality Evaluator")
st.caption("Powered by RAGAS · Dynamics 365 Finance")

st.markdown("""
This tool evaluates the quality of a RAG system across 4 dimensions:
- **Faithfulness** — does the answer stay true to the retrieved context?
- **Answer Relevancy** — does the answer actually address the question?
- **Context Precision** — were the right chunks retrieved?
- **Context Recall** — was all necessary information retrieved?
""")

if st.button("Run Evaluation", type="primary"):
    with st.spinner("Running RAGAS evaluation... this takes ~30 seconds"):
        df, results = run_evaluation()
        st.session_state.df = df

if "df" in st.session_state:
    df = st.session_state.df

    scores = {
        "Faithfulness": df["faithfulness"].mean(),
        "Answer Relevancy": df["answer_relevancy"].mean(),
        "Context Precision": df["context_precision"].mean(),
        "Context Recall": df["context_recall"].mean()
    }

    st.subheader("Overall Scores")
    cols = st.columns(4)
    for col, (metric, score) in zip(cols, scores.items()):
        with col:
            color = "normal" if score >= 0.8 else "inverse"
            st.metric(metric, f"{score:.3f}")

    st.subheader("Score Visualization")
    fig = go.Figure(go.Bar(
        x=list(scores.keys()),
        y=list(scores.values()),
        marker_color=["#2ecc71" if v >= 0.9 else "#f39c12" if v >= 0.7 else "#e74c3c" 
                      for v in scores.values()],
        text=[f"{v:.3f}" for v in scores.values()],
        textposition="outside"
    ))
    fig.update_layout(
        yaxis=dict(range=[0, 1.1]),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Per-Question Results")
    st.dataframe(df, use_container_width=True)