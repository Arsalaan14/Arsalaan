"""Central configuration for MedNova."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
JSON_DATA_PATH = Path(os.getenv("JSON_DATA_PATH", str(DATA_DIR / "patient_records_50.json")))
NORMALIZED_DATA_PATH = Path(os.getenv("NORMALIZED_DATA_PATH", str(DATA_DIR / "patient_records_normalized.json")))

CHROMA_DB_DIR = Path(os.getenv("CHROMA_DB_DIR", str(BASE_DIR / "vector_embedding" / "chroma_db")))
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "patient_records")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
TOP_K_RETRIEVAL = int(os.getenv("TOP_K_RETRIEVAL", "5"))

# LLM provider: "offline" (default, no external credentials), "bedrock", or "lmstudio".
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "offline").lower()
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "us.meta.llama3-3-70b-instruct-v1:0")
LLM_MODEL_NAME = BEDROCK_MODEL_ID
LM_STUDIO_BASE_URL = os.getenv("LM_STUDIO_BASE_URL", "http://127.0.0.1:1234/v1")
LM_STUDIO_MODEL_NAME = os.getenv("LM_STUDIO_MODEL_NAME", "local-model")

MAX_NEW_TOKENS = int(os.getenv("MAX_NEW_TOKENS", "1024"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.1"))
TOP_P = float(os.getenv("TOP_P", "0.9"))

JWT_SECRET = os.getenv("JWT_SECRET", "change-this-secret-before-production")
JWT_EXPIRY_HOURS = int(os.getenv("JWT_EXPIRY_HOURS", "8"))
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
AUDIT_LOG_PATH = os.getenv("AUDIT_LOG_PATH", str(BASE_DIR / "runtime" / "audit_log.json"))

# Demo accounts are intentionally documented for an academic/demo deployment.
DEMO_USERS = {
    "admin": {"password": os.getenv("ADMIN_PASSWORD", "Admin@123"), "role": "admin", "name": "System Administrator"},
    "provider": {"password": os.getenv("PROVIDER_PASSWORD", "Provider@123"), "role": "provider", "name": "Dr. Olivia"},
    "patient9": {"password": os.getenv("PATIENT_PASSWORD", "Patient@123"), "role": "patient", "name": "Patient 9", "patient_id": "P009"},
    "insurer": {"password": os.getenv("INSURER_PASSWORD", "Insurer@123"), "role": "insurer", "name": "INS Mutual Agent"},
}
