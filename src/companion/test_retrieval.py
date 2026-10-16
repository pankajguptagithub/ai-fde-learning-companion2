from companion.retrieval import retrieve

query = "What is reranking in RAG?"

results = retrieve(query)

print("Query:", query)
print("\nRetrieved documents:")

for result in results:
    print(
        result["source"],
        "->",
        result["id"]
    )
