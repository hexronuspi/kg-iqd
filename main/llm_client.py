"""
llm_client.py

This module provides a wrapper function to query the Gemini 2.5 Pro model using LiteLLM.
"""

from litellm
import os

# Load API key securely (can be set in your environment or .env)
GEMINI_KEY = os.getenv("GEMINI_KEY")

def give_answer(query: str) -> str:
    """
    Sends a query to the Gemini 2.5 Pro LLM via LiteLLM and returns the model's response.

    Args:
        query (str): The prompt or question to send to the model.

    Returns:
        str: The content of the model's response.

    Raises:
        ValueError: If API key is missing or the response structure is invalid.
    """
    if not GEMINI_KEY:
        raise ValueError("GEMINI_KEY is not set in the environment variables.")

    response = completion(
        model="gemini/gemini-2.5-pro",
        messages=[{"role": "user", "content": query}],
        api_key=GEMINI_KEY
    )

    try:
        return response['choices'][0]['message']['content']
    except (KeyError, IndexError) as e:
        raise ValueError(f"Unexpected response format: {response}") from e
