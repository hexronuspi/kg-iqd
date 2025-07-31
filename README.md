## Knowledge Graph-Informed Query Decomposition(KG-IQD): Hybrid KG-RAG Reasoning in Noisy Contexts

This repository contains code, data and other materials which were used in the paper, Knowledge Graph-Informed Query Decomposition(KG-IQD): Hybrid KG-RAG Reasoning in Noisy Contexts.

### KG-IQD: A Hybrid KG-RAG Framework

> **KG-IQD** is a hybrid KG-RAG framework that uses a Knowledge Graph (KG) to strategically guide query decomposition for improved reasoning in complex, noisy domains like disaster response.

---

#### The Problem

Standard QA systems struggle with complex queries over noisy, heterogeneous data:

*   **RAG (Retrieval-Augmented Generation):** Good at retrieving contextual text but lacks the structural awareness needed for comparative or multi-hop questions.
*   **KGs (Knowledge Graphs):** Excel at representing relational facts but are often sparse and lack the rich context found in source documents.

#### Our Solution: KG-IQD

**KG-IQD** combines the strengths of KGs and RAG. It uses the structured knowledge in a KG to break down a complex query into simple, targeted sub-queries.

These sub-queries then guide a precise RAG process, ensuring the final answer is grounded in both:
*   Factual KG triples.
*   Relevant textual evidence from source documents.
