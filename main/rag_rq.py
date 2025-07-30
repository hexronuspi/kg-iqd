"""
rag_rq.py

Implements a RQ Retrieval-Augmented Generation (RQ-RAG) system that:
1. Decomposes a complex query into sub-questions.
2. Retrieves relevant chunks for each sub-query.
3. Reranks and combines them for final answering.
"""

import numpy as np
import pandas as pd
import torch
from sentence_transformers.util import cos_sim

from .llm_client import give_answer
from .embedding_generator import embedding_model, reranker

def give_query_answer_rag_multihop(query: str, embedding_csv: str = "embedding.csv") -> str:
    """
    Answers a complex query using a multi-hop RAG pipeline by decomposing it into sub-questions.

    Args:
        query (str): User's original complex query.
        embedding_csv (str): Path to CSV file with text chunks and their embeddings.

    Returns:
        str: Final answer generated using retrieved and reranked passages.
    """
    # --- Step 1: Decompose query into sub-queries ---
    sub_query_instruction = f"""You are a helpful assistant. Break the user's question into independent sub-queries to better search for information.

User query: {query}

Respond with clearly numbered sub-questions like:
1. ...
2. ...
"""
    sub_queries_text = give_answer(sub_query_instruction)

    # Parse numbered sub-questions from model output
    sub_queries = []
    for line in sub_queries_text.splitlines():
        if line.strip().startswith(tuple("1234567890")) and '.' in line:
            _, sub_q = line.split('.', 1)
            sub_queries.append(sub_q.strip())

    if not sub_queries:
        raise ValueError("Failed to extract sub-queries. Model output:\n" + sub_queries_text)

    # --- Step 2: Load embeddings from CSV ---
    df = pd.read_csv(embedding_csv)
    if 'embedding' not in df.columns or 'text' not in df.columns:
        raise ValueError("CSV must contain 'embedding' and 'text' columns.")

    embeddings = np.array([
        np.fromstring(emb, sep=',', dtype=np.float32) for emb in df['embedding']
    ])
    embedding_tensor = torch.tensor(embeddings)

    # --- Step 3: For each sub-query, retrieve top-k, rerank top-m ---
    all_retrieved_texts = []

    for sub_q in sub_queries:
        prompt = "Represent this sentence for searching relevant passages: "
        query_with_prompt = prompt + sub_q
        query_embedding = embedding_model.encode([query_with_prompt], normalize_embeddings=True)[0].astype(np.float32)
        query_tensor = torch.tensor(query_embedding).unsqueeze(0)

        similarities = cos_sim(query_tensor, embedding_tensor)[0].numpy()
        top_k_indices = np.argsort(similarities)[::-1][:5]
        top_k_texts = df.iloc[top_k_indices]['text'].tolist()

        # Rerank using cross-encoder
        pairs = [(sub_q, passage) for passage in top_k_texts]
        scores = reranker.predict(pairs)
        sorted_indices = np.argsort(scores)[::-1]
        top_texts = [top_k_texts[i] for i in sorted_indices[:3]]

        all_retrieved_texts.extend(top_texts)

    # --- Step 4: Compose final answer using retrieved data only ---
    combined_data = " ".join(all_retrieved_texts)

    final_prompt = f"""You are an expert assistant.
Only use the information provided in the data block to craft your answer. Do NOT bring in any outside knowledge or assumptions.

data:
{combined_data}
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
