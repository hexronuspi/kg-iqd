# never used, as we already defined the limitations for RAG, we only use KG and RQ-RAG

"""
rag_answer.py

This module implements a full Retrieval-Augmented Generation (RAG) pipeline:
1. Embedding-based similarity search (using SentenceTransformer).
2. Cross-encoder reranking of top-k similar passages.
3. Final answer generation using context-limited prompting.
"""

import numpy as np
import pandas as pd
import torch
from sentence_transformers.util import cos_sim
from .llm_client import give_answer
from .embedding_generator import embedding_model, reranker


def give_query_answer_rag(query: str, embedding_csv: str = "embedding.csv",
                          k: int = 10, m: int = 3) -> str:
    """
    Answers a query using a RAG pipeline based on dense vector search + reranking.

    Args:
        query (str): The user's question.
        embedding_csv (str): Path to the CSV containing precomputed embeddings.
        k (int): Number of top similar chunks to retrieve.
        m (int): Number of top reranked chunks to include in final context.

    Returns:
        str: The answer generated using only the retrieved and reranked data.
    """
    # Load the embedded document chunks
    df = pd.read_csv(embedding_csv)
    if 'embedding' not in df.columns or 'text' not in df.columns:
        raise ValueError("CSV must contain 'embedding' and 'text' columns.")

    embeddings = np.array([
        np.fromstring(emb, sep=',', dtype=np.float32) for emb in df['embedding']
    ])

    # Encode the query with the special instruction prompt
    prompt = "Represent this sentence for searching relevant passages: "
    query_embedding = embedding_model.encode(
        [prompt + query], normalize_embeddings=True
    )[0].astype(np.float32)

    # Compute cosine similarity with all document embeddings
    query_tensor = torch.tensor(query_embedding).unsqueeze(0)
    embedding_tensor = torch.tensor(embeddings)
    similarities = cos_sim(query_tensor, embedding_tensor)[0].numpy()

    # Retrieve top-k most similar chunks
    top_k_indices = np.argsort(similarities)[::-1][:k]
    top_k_texts = df.iloc[top_k_indices]['text'].tolist()

    # Rerank using cross-encoder
    pairs = [(query, passage) for passage in top_k_texts]
    scores = reranker.predict(pairs)
    sorted_indices = np.argsort(scores)[::-1]
    top_m_texts = [top_k_texts[i] for i in sorted_indices[:m]]

    # Concatenate final context
    data = " ".join(top_m_texts)

    # Create a strict instruction prompt and get the answer
    final_prompt = f"""You are an expert assistant.
Only use the information provided in the data block to craft your answer. Do NOT bring in any outside knowledge or assumptions.

data:
{data}
————

User’s question:
{query}

Your task:
– Read the context carefully.
– Answer the user’s question ({query}) using only that data.
– Be precise, comprehensive, and perfectly organized.
– Explain each point in detail, using examples or references to the data where helpful.
– Do not mention or infer anything that isn’t explicitly in the data.
"""
    return give_answer(final_prompt)
