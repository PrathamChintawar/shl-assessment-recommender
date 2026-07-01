"""
embeddings.py

Loads the embedding model and provides helper functions
to embed documents and user queries.
"""

from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


class EmbeddingModel:
    """
    Singleton wrapper around SentenceTransformer.
    """

    def __init__(self):
        print(f"Loading embedding model: {MODEL_NAME}")
        self.model = SentenceTransformer(MODEL_NAME)

    def embed_documents(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for multiple documents.
        """
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=True,
        )

        return embeddings

    def embed_query(self, query: str) -> np.ndarray:
        """
        Generate embedding for a user query.
        """
        embedding = self.model.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embedding


# Global singleton
embedding_model = EmbeddingModel()