"""
retriever.py

Loads the FAISS index and retrieves
the most relevant SHL assessments.
"""

from pathlib import Path
import pickle

import faiss
import numpy as np

from app.embeddings import embedding_model


PROJECT_ROOT = Path(__file__).resolve().parent.parent

INDEX_PATH = PROJECT_ROOT / "vectorstore" / "faiss.index"

METADATA_PATH = PROJECT_ROOT / "vectorstore" / "metadata.pkl"


class Retriever:

    def __init__(self):

        self.index = faiss.read_index(str(INDEX_PATH))

        with open(METADATA_PATH, "rb") as f:
            self.metadata = pickle.load(f)

    def search(self, query: str, top_k: int = 5):

        query_embedding = embedding_model.embed_query(query)

        query_embedding = np.array([query_embedding]).astype(np.float32)

        scores, indices = self.index.search(query_embedding, top_k)

        results = []

        for score, idx in zip(scores[0], indices[0]):

            if idx == -1:
                continue

            item = self.metadata[idx]

            results.append(
                {
                "score": float(score),
                **item
            }
    )

        return results


retriever = Retriever()