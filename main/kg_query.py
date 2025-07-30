"""
kg_query.py

This module provides a utility to query knowledge graphs using strict
context from pre-supplied data. It ensures no outside knowledge is introduced.
"""

from .llm_client import give_answer

def give_query_answer_kg(query: str = "", data: str = "") -> str:
    """
    Answers a user query using only the provided data context.

    Args:
        query (str): The user's question.
        data (str): Contextual data, such as a chunk from a knowledge graph or document.

    Returns:
        str: The model's response strictly based on the given data.
    """
    prompt = f"""You are an expert assistant.
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
    return give_answer(prompt)
