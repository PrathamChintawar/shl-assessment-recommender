"""
load_catalog.py

Loads the SHL assessment catalog from a JSON file.

This module is responsible ONLY for reading and validating
the catalog. It does not modify or preprocess the data.
"""

from pathlib import Path
import json
from typing import List, Dict


DEFAULT_CATALOG_PATH = Path("data/catalog.json")


def load_catalog(catalog_path: Path = DEFAULT_CATALOG_PATH) -> List[Dict]:
    """
    Load the SHL catalog from a JSON file.

    Args:
        catalog_path (Path):
            Path to catalog.json

    Returns:
        List[Dict]:
            List containing assessment dictionaries.

    Raises:
        FileNotFoundError:
            If catalog file doesn't exist.

        ValueError:
            If catalog is empty or invalid JSON.
    """

    if not catalog_path.exists():
        raise FileNotFoundError(
            f"Catalog file not found: {catalog_path}"
        )

    try:
        with open(catalog_path, "r", encoding="utf-8") as f:
            catalog = json.load(f)

    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON file.\n{e}")

    if not isinstance(catalog, list):
        raise ValueError("Expected catalog.json to contain a list of assessments.")

    if len(catalog) == 0:
        raise ValueError("Catalog is empty.")

    return catalog


def get_assessment_by_name(
    catalog: List[Dict],
    name: str,
) -> Dict | None:
    """
    Search assessment by exact name.

    Returns:
        Assessment dictionary or None.
    """

    for assessment in catalog:
        if assessment.get("name", "").lower() == name.lower():
            return assessment

    return None





if __name__ == "__main__":

    catalog = load_catalog()
