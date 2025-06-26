"""Embedding utilities using sentence-transformers."""

from typing import List

# Placeholder import for actual sentence-transformers usage
try:
    from sentence_transformers import SentenceTransformer
except ImportError:  # pragma: no cover - not installed in all environments
    SentenceTransformer = None  # type: ignore


def embed_sentences(sentences: List[str], model_name: str) -> List[List[float]]:
    """Return embeddings for a list of sentences."""
    if SentenceTransformer is None:
        raise ImportError("sentence-transformers is not installed")

    model = SentenceTransformer(model_name)
    embeddings = model.encode(sentences)
    return embeddings.tolist()