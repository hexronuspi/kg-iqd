"""
main/hybrid.py

Implements a Hybrid KG-RAG pipeline using structured knowledge graphs and RAG-based retrieval.
The core function `hybrid_kg_rag_pipeline` synthesizes answers from both sources.
"""

import json
import re
from .llm_client import give_answer

# These will be injected later from run.py after loading
usedataNEP = None
usedataKER = None
embedding_model = None
reranker = None

def flatten_kg(d, parent_key='', sep='.'):  # used to flatten JSON KGs
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_kg(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def retrieve_from_rag(query: str, df, k: int = 10, m: int = 3):
    embeddings = df['embedding'].apply(lambda emb: np.array(emb.split(','), dtype=np.float32)).tolist()
    embeddings = np.stack(embeddings)

    query_embedding = embedding_model.encode([query], normalize_embeddings=True)[0]
    similarities = np.dot(embeddings, query_embedding)

    top_k_indices = np.argsort(similarities)[::-1][:k]
    top_k_texts = df.iloc[top_k_indices]['text'].tolist()

    pairs = [(query, text) for text in top_k_texts]
    scores = reranker.predict(pairs)

    sorted_indices = np.argsort(scores)[::-1]
    top_m_texts = [top_k_texts[i] for i in sorted_indices[:m]]

    return top_m_texts

def extract_json_from_llm_output(llm_output_str: str):
    match = re.search(r"```(?:json)?\s*([\s\S]+?)\s*```", llm_output_str)
    clean_str = match.group(1) if match else llm_output_str

    try:
        start_brace = clean_str.find('{')
        start_bracket = clean_str.find('[')

        if start_brace == -1 and start_bracket == -1:
            return None

        if start_brace != -1 and (start_brace < start_bracket or start_bracket == -1):
            start_index = start_brace
            end_char = '}'
        else:
            start_index = start_bracket
            end_char = ']'

        end_index = clean_str.rfind(end_char)
        if end_index == -1:
            return None

        json_str = clean_str[start_index : end_index + 1]
        return json.loads(json_str)

    except (json.JSONDecodeError, IndexError):
        return None

def hybrid_kg_rag_pipeline(initial_query: str, df_embeddings):
    print("--- PIPELINE START ---")
    print(f"Initial Query: '{initial_query}'\n")

    target_kg_data = None
    query_lower = initial_query.lower()

    if "nepal" in query_lower and "kerala" in query_lower:
        print("✅ KG Selected: Combined Nepal & Kerala KGs for comparison")
        target_kg_data = {
            "nepal_earthquake_2015": usedataNEP,
            "kerala_floods_2018": usedataKER
        }
    elif "nepal" in query_lower:
        print("✅ KG Selected: Nepal Earthquake KG")
        target_kg_data = usedataNEP
    elif "kerala" in query_lower:
        print("✅ KG Selected: Kerala Floods KG")
        target_kg_data = usedataKER
    else:
        print("❌ Could not determine target KG from query. Aborting.")
        return

    flat_kg = flatten_kg(target_kg_data)

    kg_extraction_prompt = f"""
    You are a data analyst specializing in knowledge graphs. Your task is to identify the 10 most relevant key-value pairs (triples) from the provided JSON data to answer the user's query.

    Return ONLY a valid JSON object containing the 10 selected key-value pairs. Do not add explanations, conversational text, or markdown code fences like ```json. The output format must be a raw, valid JSON object. Example: {{"key1": "value1", "key2": "value2"}}

    USER_QUERY:
    "{initial_query}"

    FLATTENED_KG_DATA:
    {json.dumps(flat_kg, indent=2)}
    """
    extracted_triples_str = give_answer(kg_extraction_prompt)
    extracted_triples = extract_json_from_llm_output(extracted_triples_str)

    if extracted_triples is None:
        print("\n❌ ERROR: Failed to parse/extract JSON from the LLM's KG extraction step.")
        print("\n--- Raw LLM Output that caused the error ---")
        print(extracted_triples_str)
        print("------------------------------------------")
        return

    print("\n--- Step 1: KG Triple Extraction ---")
    print("✅ Top 10 relevant triples extracted from KG:")
    print(json.dumps(extracted_triples, indent=2))

    sub_query_generation_prompt = f"""
    You are a research assistant tasked with breaking down a complex question into smaller, searchable parts. Based on the original query and the key facts extracted from a knowledge graph, generate 15 specific, independent, and self-contained questions designed for a semantic search engine.

    The questions should be granular and directly related to the facts. Each question must be a full, standalone sentence. Return ONLY a Python list of strings.
    Example: ["What was the damage to schools in Nepal?", "How many people were displaced by the earthquake?"]

    ORIGINAL_QUERY:
    "{initial_query}"

    KEY_KG_FACTS:
    {json.dumps(extracted_triples, indent=2)}
    """
    sub_queries_str = give_answer(sub_query_generation_prompt)
    sub_queries = extract_json_from_llm_output(sub_queries_str)

    if sub_queries is None:
        print("\n❌ ERROR: Failed to parse/extract a list from the LLM's sub-query generation step.")
        print("\n--- Raw LLM Output that caused the error ---")
        print(sub_queries_str)
        print("------------------------------------------")
        return

    print("\n--- Step 2: Sub-Query Generation ---")
    print(f"✅ Generated {len(sub_queries)} independent sub-queries:")
    for i, sq in enumerate(sub_queries):
        print(f"  {i+1}. {sq}")

    print("\n--- Step 3: Hybrid Retrieval ---")
    print(f"✅ Performing RAG search for {len(sub_queries)} sub-queries to gather context...")

    all_retrieved_context = set()
    for sq in sub_queries:
        retrieved_texts = retrieve_from_rag(sq, df_embeddings, k=10, m=5)
        all_retrieved_context.update(retrieved_texts)

    final_rag_context = "\n".join(all_retrieved_context)
    print(f"✅ Retrieved {len(all_retrieved_context)} unique context chunks.")

    final_synthesis_prompt = f"""
    You are an expert intelligence analyst and report writer. Your mission is to synthesize information from two sources—a structured Knowledge Graph (KG) and unstructured text from a Retrieval-Augmented Generation (RAG) system—to provide a comprehensive, detailed, and accurate answer to the user's question.

    **CRUCIAL INSTRUCTIONS:**
    1.  **Prioritize KG Data:** Treat the STRUCTURED_KG_DATA as the primary source of truth for specific numbers, dates, and official figures.
    2.  **Use RAG for Context:** Use the UNSTRUCTURED_RAG_CONTEXT to provide narrative, explanations, supporting evidence, and real-world examples for the facts found in the KG.
    3.  **Synthesize, Don't Just List:** Do not simply list facts from both sources. Weave them together into a coherent, well-organized response.
    4.  **Answer the User Directly:** Ensure your final output directly answers the USER_QUESTION.

    ---
    **USER_QUESTION:**
    {initial_query}
    ---
    **STRUCTURED_KG_DATA (Ground Truth Facts):**
    {json.dumps(extracted_triples, indent=2)}
    ---
    **UNSTRUCTURED_RAG_CONTEXT (Narrative & Detail):**
    {final_rag_context}
    ---

    Now, generate your expert, synthesized response.
    """
    final_answer = give_answer(final_synthesis_prompt)

    print("\n--- Step 4: Final Answer Synthesis ---")
    print("✅ Final answer generated.")
    print("\n--- FINAL HYBRID KG-RAG RESPONSE ---")
    print(final_answer)