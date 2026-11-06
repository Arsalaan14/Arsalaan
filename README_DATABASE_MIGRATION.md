# Database / Vector Index Migration

MediQueryNow uses ChromaDB for the semantic retrieval index. The source of truth for the academic demo is `data/patient_records_50.json`.

To rebuild the index:

```bash
python -m vector_embedding.embed_patients
```

The application also initializes the index automatically in Docker when the persistent Chroma collection is empty.

For a production migration, move patient metadata/authentication/audit data to a transactional database such as PostgreSQL and retain ChromaDB (or a managed vector store) for embeddings.
