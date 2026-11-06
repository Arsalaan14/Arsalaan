#!/bin/sh
set -eu
echo "== MediQueryNow backend startup =="
mkdir -p /app/vector_embedding/chroma_db /app/data /app/runtime
python - <<'PY'
import os
import config
from vector_embedding.normalization import normalize_dataset
from vector_embedding.embed_patients import build_embeddings
if not os.path.exists(config.NORMALIZED_DATA_PATH):
    print("Creating normalized dataset...")
    normalize_dataset(str(config.JSON_DATA_PATH), str(config.NORMALIZED_DATA_PATH))
try:
    import chromadb
    client = chromadb.PersistentClient(path=str(config.CHROMA_DB_DIR))
    col = client.get_or_create_collection(config.COLLECTION_NAME)
    if col.count() == 0:
        print("Building vector index (first startup may take a few minutes)...")
        build_embeddings(str(config.JSON_DATA_PATH), str(config.CHROMA_DB_DIR))
    else:
        print(f"Vector index ready: {col.count()} documents")
except Exception as exc:
    print(f"Index initialization warning: {exc}")
PY
exec gunicorn --bind 0.0.0.0:${PORT:-5000} --workers ${WEB_CONCURRENCY:-1} --timeout 180 backend.app:app
