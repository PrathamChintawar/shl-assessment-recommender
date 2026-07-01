"""
build_index.py

Creates a FAISS vector index from the processed SHL documents.

Outputs:
    vectorstore/faiss.index
    vectorstore/metadata.pkl
"""

import json
import pickle
from pathlib import Path

import faiss
import numpy as np

from app.embeddings import embedding_model

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DOCUMENT_PATH = PROJECT_ROOT / "data" / "catalog_processed.json"

VECTORSTORE_DIR = PROJECT_ROOT / "vectorstore"

INDEX_PATH = VECTORSTORE_DIR / "faiss.index"

METADATA_PATH = VECTORSTORE_DIR / "metadata.pkl"


def load_documents():
    with open(DOCUMENT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build_index():

    documents = load_documents()

    texts = [doc["text"] for doc in documents]

    metadata = []

    for doc in documents:
        metadata.append({
            "text": doc["text"],
            **doc["metadata"]
        })

    print(f"Embedding {len(texts)} documents...")

    embeddings = embedding_model.embed_documents(texts)

    embeddings = embeddings.astype(np.float32)

    dimension = embeddings.shape[1]

    print(f"Embedding dimension : {dimension}")

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    VECTORSTORE_DIR.mkdir(exist_ok=True)

    faiss.write_index(index, str(INDEX_PATH))

    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)

    print("=" * 60)
    print("Vector Store Created Successfully")
    print(f"Documents Indexed : {index.ntotal}")
    print(f"Index Saved To    : {INDEX_PATH}")
    print(f"Metadata Saved To : {METADATA_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    build_index()