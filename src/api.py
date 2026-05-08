from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib
import logging
import json
from datetime import datetime
import sys
from pathlib import Path

try:
    # Package import for `python -m src.api` or WSGI entrypoints.
    from src.redis_client import get_redis_client
except ImportError:
    try:
        # Local import for `python src/api.py`.
        from redis_client import get_redis_client
    except ImportError:
        # Allow the API to run even when the Redis wrapper module is absent.
        def get_redis_client():
            return None

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

app = Flask(__name__)
CORS(app)

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/api.log')
    ]
)
logger = logging.getLogger(__name__)

def call_llm(prompt: str) -> str:
    # Temporary placeholder until your real LLM API is ready
    return "LLM integration pending. RAG retrieval is working."


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/ask", methods=["POST"])
def ask():
    request_id = request.headers.get('X-Request-ID', f"req_{datetime.now().timestamp()}")
    
    try:
        try:
            # Try relative import (for gunicorn with src.api:app)
            from .rag import build_rag_prompt
        except ImportError:
            # Fall back to direct import (for python src/api.py)
            from rag import build_rag_prompt
        
        # Log incoming request
        logger.info(f"[{request_id}] Incoming /ask request from {request.remote_addr}")
        
        data = request.get_json()
        user_query = data.get("question", "").strip()

        # Log received question
        if user_query:
            logger.info(f"[{request_id}] Question received: {user_query[:100]}")
        else:
            logger.warning(f"[{request_id}] Empty question provided")
            return jsonify({"error": "Question is required"}), 400

        redis_client = get_redis_client()
        cache_key = None

        if redis_client and user_query:
            try:
                normalized_query = user_query.strip().lower()
                query_hash = hashlib.md5(normalized_query.encode()).hexdigest()
                cache_key = f"rag:ask:{query_hash}"

                cached = redis_client.get(cache_key)
                if cached:
                    logger.info(f"[{request_id}] Cache hit for query")
                    cached_response = json.loads(cached)
                    if isinstance(cached_response, dict) and "question" in cached_response:
                        cached_response["question"] = user_query
                    return jsonify(cached_response)
            except Exception as e:
                logger.warning(f"[{request_id}] Redis cache read failed: {e}")

        # Build RAG prompt and retrieve chunks
        prompt, chunks = build_rag_prompt(user_query, top_k=3)
        
        # Log chunk retrieval
        chunk_count = len(chunks)
        logger.info(f"[{request_id}] Retrieved {chunk_count} chunks for query")
        if chunk_count > 0:
            for i, chunk in enumerate(chunks, 1):
                logger.debug(f"[{request_id}] Chunk {i}: source={chunk.get('source_name')}, page={chunk.get('page_number')}")
        
        answer = call_llm(prompt)

        sources = [
            {
                "source_name": c["source_name"],
                "page_number": c["page_number"],
                "chunk_id": c["chunk_id"]
            }
            for c in chunks
        ]

        response = {
            "question": user_query,
            "answer": answer,
            "sources": sources,
            "prompt_preview": prompt[:2000]
        }
        
        # Log success response
        logger.info(f"[{request_id}] /ask request completed successfully. Chunks: {chunk_count}, Response size: {len(json.dumps(response))} bytes")

        if redis_client and cache_key:
            try:
                redis_client.setex(cache_key, 300, json.dumps(response))
                logger.info(f"[{request_id}] Response cached for 300s")
            except Exception as e:
                logger.warning(f"[{request_id}] Redis cache write failed: {e}")
        
        return jsonify(response)
        
    except Exception as e:
        # Log exceptions with full error details
        logger.error(f"[{request_id}] Exception in /ask endpoint: {type(e).__name__}: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
