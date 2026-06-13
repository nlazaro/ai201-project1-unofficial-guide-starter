import os
from groq import Groq
from dotenv import load_dotenv
from embed import embed_and_store, retrieve, model, collection
from ingest import load_pdfs, load_txts, load_html, chunk_text

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def ask(question):
    # Retrieve relevant chunks
    results = retrieve(question, k=5)
    
    chunks = results["documents"][0]
    sources = list(set([m["source"] for m in results["metadatas"][0]]))
    
    # Build context from retrieved chunks
    context = "\n\n---\n\n".join(chunks)
    
    # Grounded prompt
    prompt = f"""You are a helpful assistant for students at Brooklyn College's CS department.
Answer the question using ONLY the information provided in the documents below.
If the documents don't contain enough information to answer, say exactly: "I don't have enough information on that."
Do not use any outside knowledge. Do not make anything up.

Documents:
{context}

Question: {question}

Answer:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    
    answer = response.choices[0].message.content
    
    return {
        "answer": answer,
        "sources": sources
    }