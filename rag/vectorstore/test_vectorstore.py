from rag.vectorstore.faiss_store import (
    INDEX_PATH,
    build_faiss_index,
)

index, chunks = build_faiss_index()

print("FAISS index created successfully.")
print("Number of vectors:", index.ntotal)
print("Vector dimension:", index.d)
print("Number of chunks:", len(chunks))
print("Index path:", INDEX_PATH)
