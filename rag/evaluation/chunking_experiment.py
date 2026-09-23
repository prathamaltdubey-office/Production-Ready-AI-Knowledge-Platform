import faiss
import numpy as np

from rag.chunking.text_chunker import chunk_documents
from rag.embeddings.embedder import DocumentEmbedder
from rag.ingestion.document_loader import load_all_documents

DOCUMENTS_PATH = "documents"


EVALUATION_QUERIES = [
    {
        "query": "What factors are associated with customer churn?",
        "expected_source": "documents\\sample.txt",
        "expected_keywords": [
            "customer tenure",
            "contract type",
            "monthly charges",
            "internet service",
            "additional services",
        ],
    },
    {
        "query": "Which customers generally have higher churn risk?",
        "expected_source": "documents\\sample.txt",
        "expected_keywords": [
            "month-to-month",
            "higher churn risk",
            "long-term contracts",
        ],
    },
    {
        "query": "How can companies reduce customer churn?",
        "expected_source": "documents\\sample.md",
        "expected_keywords": [
            "customer retention",
            "retention programs",
        ],
    },
    {
        "query": "What are the key features of the SmartHome Hub?",
        "expected_source": "documents\\sample.pdf",
        "expected_keywords": [
            "Universal Compatibility",
            "AI-Powered Assistant",
            "Enhanced Security",
        ],
    },
    {
        "query": "What is the projected smart home market size?",
        "expected_source": "documents\\sample.pdf",
        "expected_keywords": [
            "$135.3 billion",
            "11.6%",
        ],
    },
    {
        "query": "What is SmartTech's market share?",
        "expected_source": "documents\\sample.pdf",
        "expected_keywords": [
            "SmartTech Co.",
            "35%",
        ],
    },
    {
        "query": "What is the marketing strategy for the SmartHome Hub?",
        "expected_source": "documents\\sample.pdf",
        "expected_keywords": [
            "Digital Marketing",
            "Trade Shows",
            "Retail Partnerships",
        ],
    },
    {
        "query": "What are the next steps for the SmartHome Hub?",
        "expected_source": "documents\\sample.pdf",
        "expected_keywords": [
            "Finalize production agreements",
            "pre-order website",
            "official launch event",
        ],
    },
]

EXPERIMENTS = [
    {
        "name": "Small",
        "chunk_size": 200,
        "chunk_overlap": 30,
    },
    {
        "name": "Medium",
        "chunk_size": 300,
        "chunk_overlap": 50,
    },
    {
        "name": "Large",
        "chunk_size": 500,
        "chunk_overlap": 50,
    },
    {
        "name": "Large-Overlap",
        "chunk_size": 500,
        "chunk_overlap": 100,
    },
    {
        "name": "XL",
        "chunk_size": 600,
        "chunk_overlap": 100,
    },
    {
        "name": "XXL",
        "chunk_size": 800,
        "chunk_overlap": 100,
    },
]


def build_index(embeddings):
    """Build a temporary FAISS index."""

    embeddings = np.asarray(
        embeddings,
        dtype="float32",
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    return index


def evaluate_experiment(
    index,
    chunks,
    embedder,
    top_k=3,
):
    """
    Calculate content-aware Recall@K.

    A query is successful when:
    1. The expected source appears in the top K.
    2. At least one expected keyword appears
       in the retrieved content.
    """

    successful_queries = 0

    print("\n" + "-" * 70)
    print(f"CONTENT-AWARE RECALL@{top_k}")
    print("-" * 70)

    for query_number, item in enumerate(
        EVALUATION_QUERIES,
        start=1,
    ):
        query = item["query"]
        expected_source = item["expected_source"]
        expected_keywords = item["expected_keywords"]

        # Create query embedding.
        query_embedding = embedder.embed_query(query)

        query_embedding = np.asarray(
            [query_embedding],
            dtype="float32",
        )

        # Search FAISS.
        distances, indices = index.search(
            query_embedding,
            top_k,
        )

        retrieved_sources = []
        retrieved_text = ""

        for index_value in indices[0]:

            if index_value == -1:
                continue

            document = chunks[index_value]

            source = document.metadata.get("source")

            retrieved_sources.append(source)

            retrieved_text += " " + document.page_content

        # Check source.
        source_hit = expected_source in retrieved_sources

        # Check content.
        retrieved_text = retrieved_text.lower()

        matched_keywords = [
            keyword
            for keyword in expected_keywords
            if keyword.lower() in retrieved_text
        ]

        content_hit = len(matched_keywords) > 0

        # Final hit.
        hit = source_hit and content_hit

        if hit:
            successful_queries += 1

        print()
        print(f"Query {query_number}: {query}")
        print(f"Expected source: {expected_source}")
        print(f"Retrieved sources: {retrieved_sources}")
        print(f"Matched keywords: {matched_keywords}")
        print(f"Source hit: " f"{'YES' if source_hit else 'NO'}")
        print(f"Content hit: " f"{'YES' if content_hit else 'NO'}")
        print(f"Hit@{top_k}: " f"{'YES' if hit else 'NO'}")

    recall = successful_queries / len(EVALUATION_QUERIES)

    print()
    print(f"Successful queries: " f"{successful_queries}")
    print(f"Total queries: " f"{len(EVALUATION_QUERIES)}")
    print(f"Content Recall@{top_k}: " f"{recall:.4f}")
    print(f"Content Recall@{top_k}: " f"{recall * 100:.2f}%")

    return recall


def main():
    """Run all chunking experiments."""

    print("=" * 70)
    print("CHUNKING STRATEGY EXPERIMENT")
    print("=" * 70)

    documents = load_all_documents(DOCUMENTS_PATH)

    embedder = DocumentEmbedder()

    results = []

    for experiment in EXPERIMENTS:

        name = experiment["name"]
        chunk_size = experiment["chunk_size"]
        chunk_overlap = experiment["chunk_overlap"]

        print("\n" + "-" * 70)
        print(f"Experiment: {name}")
        print(f"Chunk size: {chunk_size}")
        print(f"Chunk overlap: {chunk_overlap}")
        print("-" * 70)

        # Create chunks.
        chunks = chunk_documents(
            documents,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

        print(f"Documents: {len(documents)}")
        print(f"Chunks: {len(chunks)}")

        # Generate embeddings.
        embeddings = embedder.embed_documents(chunks)

        # Build temporary index.
        index = build_index(embeddings)

        # Evaluate.
        recall = evaluate_experiment(
            index,
            chunks,
            embedder,
            top_k=3,
        )

        results.append(
            {
                "name": name,
                "chunk_size": chunk_size,
                "chunk_overlap": chunk_overlap,
                "chunks": len(chunks),
                "recall": recall,
            }
        )

    # Final comparison.
    print("\n")
    print("=" * 70)
    print("FINAL COMPARISON")
    print("=" * 70)

    print(
        f"{'Strategy':<15}"
        f"{'Size':<10}"
        f"{'Overlap':<10}"
        f"{'Chunks':<10}"
        f"{'Recall@3':<12}"
    )

    print("-" * 70)

    for result in results:

        print(
            f"{result['name']:<15}"
            f"{result['chunk_size']:<10}"
            f"{result['chunk_overlap']:<10}"
            f"{result['chunks']:<10}"
            f"{result['recall'] * 100:.2f}%"
        )


if __name__ == "__main__":
    main()
