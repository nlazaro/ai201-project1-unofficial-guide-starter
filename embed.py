import chromadb
from sentence_transformers import SentenceTransformer
from ingest import load_pdfs, load_txts, load_html, chunk_text
import os

# Load embedding model
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Set up ChromaDB with persistent storage
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="bc_cs_docs")

def embed_and_store(all_chunks):
    """Embed all chunks and store in ChromaDB with metadata."""
    print(f"Embedding {len(all_chunks)} chunks...")
    texts = [chunk["text"] for chunk in all_chunks]
    ids = [chunk["chunk_id"] for chunk in all_chunks]
    metadatas = [{"source": chunk["source"]} for chunk in all_chunks]
    embeddings = model.encode(texts, show_progress_bar=True).tolist()
    collection.add(
        documents=texts,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas
    )
    print(f"Stored {len(all_chunks)} chunks in ChromaDB!")

def retrieve(query, k=5):
    """Retrieve top-k relevant chunks for a query."""
    query_embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )
    return results

if __name__ == "__main__":
    # Only embed if database is empty
    if collection.count() == 0:
        documents = load_pdfs() + load_txts() + load_html()
        all_chunks = []
        for doc in documents:
            chunks = chunk_text(doc["text"], doc["source"])
            all_chunks.extend(chunks)
        embed_and_store(all_chunks)
    else:
        print(f"Database already has {collection.count()} chunks, skipping embedding.")