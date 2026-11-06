# Patient Vector Embedding Pipeline

This document explains the architecture of the Patient Data Embedding Pipeline and the capabilities of the normalization engine.

## 1. Supported JSON Capabilities
The data ingestion and normalization system is designed to handle extremely complex and messy real-world clinical datasets.

- **Deep and Arbitrary Nesting**: The system uses a recursive normalization engine. It can automatically detect and extract entities no matter how deeply they are nested. For example, if a `condition` is nested inside a `medication`, which is itself nested inside an `allergy`, the engine will successfully untangle it and map it to the patient's global `conditions` array.
- **Inconsistent/Messy Key Variations**: Real-world data rarely adheres to a strict schema. The engine includes a Key Normalization Map that standardizes dozens of aliases on the fly. For instance, `cond`, `con`, `dx`, and `condition` are all resolved to the canonical `conditions` key. Similar logic exists for medications (`rx`, `meds`), encounters, and demographic fields.
- **Multi-Gigabyte File Scaling**: The system handles massive (e.g., 100GB+) JSON files without throwing Out-of-Memory (OOM) errors. It uses **Streaming JSON Processing (`ijson`)** to process exact one patient record at a time, keeping the RAM footprint well under 100MB at all times.

## 2. Pipeline Architecture (From JSON to ChromaDB)

The embedding pipeline (`vector_embedding/embed_patients.py`) is designed as a direct memory-to-memory stream. Intermediate normalization steps are **never** saved to disk as huge JSON files, resulting in significantly faster processing.

Here is the step-by-step pipeline workflow:

### Step 1: Streaming Ingestion
The pipeline starts by opening the raw, messy JSON file using the `ijson` library. Instead of loading the entire file, it yields a generator that extracts exactly one raw patient record into memory at a time.

### Step 2: Dynamic Normalization
Each raw patient record is passed into the `normalize_single_patient` recursive function. 
- The function walks the entire nested dictionary tree.
- Keys are canonicalized.
- Complex entities (like medications or lab results) are extracted into standard lists.
- **Data Provenance**: Every single extracted value is tagged with a `source_path` (e.g., `patients[0].alrg[0].meds[0].dx`) so you always know exactly where a data point came from in the raw JSON.

### Step 3: Document Conversion
The normalized structured patient dict is passed to `normalized_patient_to_document`. This function translates the structured data into a human-readable text document containing all demographic, clinical, and temporal information. This text representation is what the embedding model will "read".

### Step 4: Batch Accumulation
To maximize GPU/CPU efficiency during the embedding phase, the pipeline accumulates these generated text documents in memory until it hits a configured `batch_size` (e.g., 32 patients).

### Step 5: Vector Encoding
Once a batch is filled, the raw text documents are passed into the `sentence-transformers/all-MiniLM-L6-v2` embedding model. The model computes semantic embeddings (dense vectors) representing the clinical meaning of the patient's record.

### Step 6: ChromaDB Upsert
The generated vectors, along with the raw text documents and extracted metadata (like age, gender, and condition summaries for exact filtering), are upserted into the persistent ChromaDB collection. 
The batch is then wiped from memory, and the system continues pulling the next patient from the raw JSON stream.
