from app.retriever import retriever

results = retriever.search(
    "Java developer assessment",
    top_k=5,
)

for i, result in enumerate(results, start=1):

    print("=" * 50)

    print(f"Rank {i}")

    print(result["metadata"]["name"])

    print(result["score"])

    print(result["metadata"]["url"])