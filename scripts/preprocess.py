"""
preprocess.py

Converts the raw SHL catalog into RAG-friendly documents.

Output:
    data/processed_documents.json
"""

import json
from pathlib import Path

from app.load_catalog import load_catalog

OUTPUT_PATH = Path("data/catalog_processed.json")


def clean_text(text: str) -> str:
    """
    Clean whitespace from text.
    """
    if not text:
        return ""

    return " ".join(text.split())


def build_document(assessment: dict) -> dict:
    """
    Convert one assessment into a searchable document.
    """

    name = clean_text(assessment.get("name", ""))

    description = clean_text(
        assessment.get("description", "")
    )

    job_levels = assessment.get("job_levels", [])

    keys = assessment.get("keys", [])

    languages = assessment.get("languages", [])

    duration = assessment.get("duration", "")

    remote = assessment.get("remote", "")

    adaptive = assessment.get("adaptive", "")

    text = f"""
Assessment Name:
{name}

Description:
{description}

Job Levels:
{", ".join(job_levels)}

Categories:
{", ".join(keys)}

Languages:
{", ".join(languages)}

Duration:
{duration}

Remote Testing:
{remote}

Adaptive:
{adaptive}
""".strip()

    return {
        "text": text,
        "metadata": {
            "entity_id": assessment.get("entity_id"),
            "name": name,
            "url": assessment.get("link"),
            "job_levels": job_levels,
            "keys": keys,
            "languages": languages,
            "duration": duration,
            "remote": remote,
            "adaptive": adaptive,
        },
    }


def preprocess_catalog():
    """
    Convert entire catalog into searchable documents.
    """

    catalog = load_catalog()

    documents = []

    for assessment in catalog:
        documents.append(
            build_document(assessment)
        )

    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            documents,
            f,
            indent=2,
            ensure_ascii=False,
        )


if __name__ == "__main__":
    preprocess_catalog()