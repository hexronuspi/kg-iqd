"""
embedding_generator.py

This module provides utilities for generating embeddings from raw text using
a SentenceTransformer model and saving the results into a CSV file.

The generated CSV includes:
- `text`: the original chunk of text
- `embedding`: a stringified list of the embedding vector

Models used:
- Embedding model: mixedbread-ai/mxbai-embed-large-v1
- Reranker: cross-encoder/ms-marco-MiniLM-L-6-v2
"""

import torch
import pandas as pd
from tqdm import tqdm
from sentence_transformers import SentenceTransformer, CrossEncoder

# Select GPU if available
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"[EmbeddingGenerator] Using device: {device}")

# Load models
embedding_model = SentenceTransformer('mixedbread-ai/mxbai-embed-large-v1', device=device)
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2', device=device)

def generate_embeddings_csv(text_file: str, csv_file: str, chunk_size: int = 1000, batch_size: int = 32) -> None:
    """
    Generates sentence embeddings from a text file and saves them into a CSV.

    Args:
        text_file (str): Path to the input `.txt` file.
        csv_file (str): Path to the output `.csv` file.
        chunk_size (int): Number of words per text chunk. Default is 1000.
        batch_size (int): Batch size for embedding computation. Default is 32.
    """
    # Read text from file
    with open(text_file, 'r', encoding='utf-8') as f:
        text = f.read()

    # Split text into chunks
    words = text.split()
    chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

    embeddings = []
    for i in tqdm(range(0, len(chunks), batch_size), desc="Encoding chunks"):
        batch = chunks[i:i + batch_size]
        batch_emb = embedding_model.encode(batch, normalize_embeddings=True, show_progress_bar=False)
        embeddings.extend(batch_emb)

    # Prepare data for CSV
    data = [
        {'text': chunk, 'embedding': ','.join(map(str, emb))}
        for chunk, emb in zip(chunks, embeddings)
    ]

    # Write to CSV
    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)