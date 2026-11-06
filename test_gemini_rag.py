import os
import sys
import json
import urllib.request
import urllib.error

# Add current dir to path to resolve imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from retrieval.retriever import get_retriever
from retrieval.retrieval_utils import build_context

def load_env():
    """Load variables from .env file into os.environ"""
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip()

def query_gemini(prompt: str) -> str:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment.")

    # List models to see what's available
    list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    try:
        req = urllib.request.Request(list_url)
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            available_models = [m["name"] for m in res_data.get("models", []) if "generateContent" in m.get("supportedGenerationMethods", [])]
            print(f"Available models for generateContent: {available_models}")
            if not available_models:
                raise RuntimeError("No models available for generateContent.")
            model_name = available_models[0].split("/")[-1] # pick first available
            print(f"Using model: {model_name}")
    except urllib.error.HTTPError as error:
        error_body = error.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Failed to list models HTTP {error.code}: {error_body}") from error

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
    
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.2
        }
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            return res_data["candidates"][0]["content"]["parts"][0]["text"]
    except urllib.error.HTTPError as error:
        error_body = error.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Gemini API failed with HTTP {error.code}: {error_body}") from error

def test_gemini_rag():
    load_env()
    print("========================================")
    print("Testing RAG Pipeline with Gemini API")
    print("========================================")
    
    # 1. Initialize retriever
    print("\n1. Initializing ChromaDB Retriever...")
    retriever = get_retriever(top_k=2)
    
    # 2. Define a test query
    query = "What are the patients conditions?"
    print(f"\n2. Querying for: '{query}'")
    
    # 3. Retrieve context
    results = retriever.retrieve_documents(query)
    context = build_context(results)
    print(f"   Successfully retrieved {len(results.get('ids', [[]])[0])} patient documents.")
    
    # 4. Build prompt
    prompt = f"""
    You are a medical assistant. Use the following patient records to answer the question.
    If the answer is not in the context, say "I cannot find the answer in the records."
    
    Context:
    {context}
    
    Question: {query}
    
    Answer clearly and concisely:
    """
    
    # 5. Call Gemini
    print("\n3. Sending RAG prompt to Gemini API...")
    try:
        answer = query_gemini(prompt)
        print("\n================ GEMINI ANSWER ================\n")
        print(answer.strip())
        print("\n===============================================\n")
    except Exception as e:
        print(f"\nFailed to get answer from Gemini: {e}")

if __name__ == "__main__":
    test_gemini_rag()
