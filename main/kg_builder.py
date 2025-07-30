"""
kg_builder.py

This module builds a knowledge graph prompt by injecting an input string
into a template prompt and querying the Gemini model using give_answer.
"""

import os

from .llm_client import give_answer

def build_kg_from_input(input_str: str, prompt_path: str = "prompts/buildkg.txt") -> str:
    """
    Reads the prompt template, replaces the placeholder with input text,
    and gets the response from the LLM.

    Args:
        input_str (str): The actual input to substitute in the prompt.
        prompt_path (str): Path to the prompt template with `inputStr` placeholder.

    Returns:
        str: The response from the LLM.
    """
    if not os.path.exists(prompt_path):
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

    with open(prompt_path, 'r', encoding='utf-8') as f:
        prompt_template = f.read()

    # Replace the placeholder with the input
    filled_prompt = prompt_template.replace("inputStr", input_str)

    # Call the LLM and return response
    return give_answer(filled_prompt)
