from app.embeddings import embedding_model

query = "I need a Java developer assessment"

vector = embedding_model.embed_query(query)

print(vector.shape)
print(vector[:10])