from rag.vectorstore.faiss_store import build_faiss_index

if __name__ == "__main__":
    index, chunks = build_faiss_index(
        chunk_size=800,
        chunk_overlap=100,
    )

    print()
    print("=" * 70)
    print("FAISS INDEX BUILT")
    print("=" * 70)

    print(f"Number of vectors: {index.ntotal}")
    print(f"Number of chunks: {len(chunks)}")
    print(f"Vector dimension: {index.d}")
