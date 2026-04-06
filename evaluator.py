from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from datasets import Dataset
import pandas as pd
from data import FINANCIAL_DOCS, EVAL_DATASET

load_dotenv()

def build_rag_pipeline():
    docs = [Document(page_content=doc) for doc in FINANCIAL_DOCS]
    
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(
        docs,
        embeddings,
        persist_directory="./eval_vector_store"
    )
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    template = """You are a financial assistant specialized in ERP and Dynamics 365.
Answer based only on the provided context. Be precise and concise.

Context: {context}
Question: {question}
Answer:"""
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )
    
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain, retriever

def run_evaluation():
    print("Building RAG pipeline...")
    chain, retriever = build_rag_pipeline()
    
    print("Running questions through RAG agent...")
    questions = []
    answers = []
    contexts = []
    ground_truths = []
    
    for item in EVAL_DATASET:
        question = item["question"]
        ground_truth = item["ground_truth"]
        
        answer = chain.invoke(question)
        retrieved_docs = retriever.invoke(question)
        context = [doc.page_content for doc in retrieved_docs]
        
        questions.append(question)
        answers.append(answer)
        contexts.append(context)
        ground_truths.append(ground_truth)
        
        print(f"Q: {question[:50]}...")
        print(f"A: {answer[:80]}...")
        print("-" * 40)
    
    print("\nRunning RAGAS evaluation...")
    
    dataset = Dataset.from_dict({
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths
    })
    
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    embeddings = OpenAIEmbeddings()
    
    ragas_llm = LangchainLLMWrapper(llm)
    ragas_embeddings = LangchainEmbeddingsWrapper(embeddings)
    
    results = evaluate(
        dataset=dataset,
        metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
        llm=ragas_llm,
        embeddings=ragas_embeddings
    )
    
    df = results.to_pandas()
    df.to_csv("eval_results.csv", index=False)
    
    scores = df
    print(f"Faithfulness:      {scores['faithfulness'].mean():.3f}")
    print(f"Answer Relevancy:  {scores['answer_relevancy'].mean():.3f}")
    print(f"Context Precision: {scores['context_precision'].mean():.3f}")
    print(f"Context Recall:    {scores['context_recall'].mean():.3f}")
    print("\nDetailed results saved to eval_results.csv")
    
    return df, results

if __name__ == "__main__":
    df, results = run_evaluation()