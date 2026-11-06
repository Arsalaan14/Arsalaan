import os
import sys
import logging
from config import CHROMA_DB_DIR, JSON_DATA_PATH, LLM_MODEL_NAME

# 1. Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("main")

def print_banner():
    print("=" * 80)
    print(" " * 20 + "Patient Health Record Assistant")
    print("=" * 80)
    print("Type your question.")
    print("\nExamples:")
    print("  * Who has HbA1c above 7%?")
    print("  * Show cardiac patients.")
    print("  * Summarize Patient P009.")
    print("  * What medications is Patient 5 taking?")
    print("\nType 'exit' to quit.")
    print("=" * 80)

def health_check():
    print("\n[INFO] Checking project structure...")
    
    # 2. Verify required folders
    required_dirs = ["data", "vector_embedding", "retrieval", "rag_engine"]
    all_dirs_ok = True
    for d in required_dirs:
        if not os.path.isdir(d):
            print(f"[ERROR] Missing required directory: {d}/")
            all_dirs_ok = False
            
    if not all_dirs_ok:
        sys.exit(1)
        
    print(f"[{'✓' if os.path.isfile(JSON_DATA_PATH) else 'x'}] JSON Dataset Found")
    print(f"[{'✓' if os.path.isdir(CHROMA_DB_DIR) else 'x'}] ChromaDB Found")
    
    if not os.path.isdir(CHROMA_DB_DIR):
        print("\n[ERROR] Vector database not found.")
        print("Options:")
        print("1. Build embeddings now")
        print("2. Exit")
        choice = input("Enter choice (1/2): ").strip()
        if choice == '1':
            print("\n[INFO] Building embeddings...")
            from vector_embedding.embed_patients import build_embeddings
            build_embeddings(JSON_DATA_PATH, CHROMA_DB_DIR)
            print("[✓] ChromaDB Built Successfully")
        else:
            print("Exiting.")
            sys.exit(0)

    print("[✓] Collection Found")

    print("\n[INFO] Loading vector database...")
    from retrieval.retriever import get_retriever
    
    print("\n[INFO] Loading LLM...")
    from rag_engine.rag_pipeline import RAGPipeline
    
    print("[✓] Embedding Model Available")
    print("[✓] LLM Available")
    print("[✓] Retrieval Layer Loaded")
    
    return RAGPipeline()

def main():
    try:
        pipeline = health_check()
    except Exception as e:
        logger.error(f"Initialization failed: {e}")
        sys.exit(1)
        
    print("\n[INFO] Starting Patient Health Record Assistant...")
    print("\n[INFO] Warming up LLM...")
    pipeline.generator.generate("Hello", "Context: None")
    print("[✓] LLM Warm-Up Completed\n")
    
    print_banner()

    # Interactive Loop
    while True:
        try:
            query = input("\nUser: ").strip()
            if not query:
                continue
                
            if query.lower() in ['exit', 'quit']:
                print("\nShutting down gracefully... Goodbye!")
                break
                
            print("\nProcessing...\n")
            result = pipeline.run(query)
            
            print("=" * 80)
            print(result["answer"])
            print("=" * 80)
            print("\nRAG Diagnostics:")
            print(f"Retrieved Documents: {result['retrieved_docs']}")
            print(f"Document IDs: {', '.join(result['doc_ids'])}")
            print(f"Retrieval Time: {result['retrieval_time']:.2f} sec")
            print(f"Generation Time: {result['generation_time']:.2f} sec")
            print(f"Total Time: {result['retrieval_time'] + result['generation_time']:.2f} sec")
            print("=" * 80)
            
        except KeyboardInterrupt:
            print("\nShutting down gracefully... Goodbye!")
            break
        except Exception as e:
            logger.error(f"Error during query execution: {e}")
            print("\nAn error occurred while processing your request. Please try again.")

if __name__ == "__main__":
    main()
