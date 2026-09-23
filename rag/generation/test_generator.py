from rag.generation.rag_generator import RAGGenerator
from rag.retrieval.retriever import SemanticRetriever

retriever = SemanticRetriever()
generator = RAGGenerator()


question = "What factors increase customer churn?"


# ------------------------------------------------------------
# Retrieve relevant documents
# ------------------------------------------------------------

results = retriever.search(
    query=question,
    top_k=3,
)


print("\n==============================")
print("RETRIEVED DOCUMENTS")
print("==============================")


for i, result in enumerate(results, start=1):
    document = result["document"]
    distance = result["distance"]

    print(f"\nRESULT {i}")
    print(f"Distance: {distance}")
    print(f"Source: {document.metadata.get('source')}")
    print(f"Content:\n{document.page_content}")


# ------------------------------------------------------------
# Build context
# ------------------------------------------------------------

context_parts = []

for result in results:
    document = result["document"]

    source = document.metadata.get(
        "source",
        "Unknown source",
    )

    context_parts.append(f"Source: {source}\n" f"{document.page_content}")


context = "\n\n---\n\n".join(context_parts)


# ------------------------------------------------------------
# Generate grounded answer
# ------------------------------------------------------------

answer = generator.generate(
    question=question,
    context=context,
)

sources = []

for result in results:
    source = result["document"].metadata.get(
        "source",
        "Unknown source",
    )

    if source not in sources:
        sources.append(source)


answer_with_sources = answer + "\n\nSources:\n"

for source in sources:
    answer_with_sources += f"- {source}\n"

print("\n==============================")
print("RAG ANSWER")
print("==============================")

print(answer_with_sources)
