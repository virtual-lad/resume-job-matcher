"""
ChromaDB helper module.

Handles:
- Initializing the ChromaDB client (persistent, stored on disk)
- Getting/creating the "jobs" collection
- Embedding text using sentence-transformers
- Querying for the top N similar jobs
"""

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from django.conf import settings as django_settings

# Load the embedding model once at module level (cached after first load)
_model = SentenceTransformer("all-MiniLM-L6-v2")


def get_chroma_client():
    """Return a persistent ChromaDB client that saves data to disk."""
    client = chromadb.PersistentClient(path=str(django_settings.CHROMA_DB_PATH))
    return client


def get_jobs_collection():
    """Get or create the 'jobs' collection in ChromaDB."""
    client = get_chroma_client()
    collection = client.get_or_create_collection(
        name="jobs",
        metadata={"hnsw:space": "cosine"},  # use cosine similarity
    )
    return collection


def embed_text(text: str):
    """Convert a text string into an embedding vector."""
    vector = _model.encode(text)
    return vector.tolist()


def search_jobs(query_text: str, n_results: int = 5):
    """
    Search ChromaDB for the top N jobs matching the query text.

    Returns a list of dicts:
    [
        {
            "title": "...",
            "company": "...",
            "field": "...",
            "description": "...",
            "skills": "...",
            "score": 0.87,   # similarity 0.0 – 1.0
        },
        ...
    ]
    """
    collection = get_jobs_collection()
    query_vector = embed_text(query_text)

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )

    jobs = []
    for i in range(len(results["ids"][0])):
        metadata = results["metadatas"][0][i]
        distance = results["distances"][0][i]
        # Cosine distance → similarity: similarity = 1 - distance
        similarity = round((1 - distance) * 100, 1)

        jobs.append(
            {
                "title": metadata.get("title", "N/A"),
                "company": metadata.get("company", "N/A"),
                "field": metadata.get("field", "N/A"),
                "description": metadata.get("description", ""),
                "skills": metadata.get("skills", ""),
                "score": similarity,
            }
        )

    return jobs


def get_job_count():
    """Return number of jobs currently stored in ChromaDB."""
    try:
        collection = get_jobs_collection()
        return collection.count()
    except Exception:
        return 0
