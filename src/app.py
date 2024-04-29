from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from .data_manager import read_text_file, create_chunks
from .embeddings import generate_embeddings
from .pinecone_manager import setup_pinecone, search_embeddings, store_embeddings
from .llm_manager import generate_conversational_output
from .db_manager import initialize_db, store_chunk, get_chunk
import hashlib
import os

app = FastAPI()

class Query(BaseModel):
    query: str

index = setup_pinecone()

def generate_id(text):
    """Generate a unique ID for the given text using SHA-256 hashing."""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

@app.on_event("startup")
async def initialize():
    """Load and index documents in Pinecone at startup."""
    print("Initializing server and indexing documents...")
    await initialize_db()
    await index_files()

async def index_files():
    directory = 'data/raw/'
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            notes_content = read_text_file(file_path)
            chunks = create_chunks(notes_content, max_length=1024)
            embeddings = generate_embeddings(chunks)
            ids = [generate_id(chunk) for chunk in chunks]
            for id_, chunk in zip(ids, chunks):
                await store_chunk(id_, chunk)
            store_embeddings(index, embeddings, ids)


@app.get("/query")
async def handle_query(query: str):
    """Handle incoming query and return the conversational response."""
    # Generate query embedding and query Pinecone
    query_embedding = generate_embeddings(query)[0].embedding
    raw_results = search_embeddings(index, query_embedding, top_k=2).matches
    
    # Retrieve and enrich text data for each result
    enriched_results = []
    for result in raw_results:
        id_ = result['id']
        text = await get_chunk(id_)  # Fetch the text associated with the ID
        if text:
            enriched_results.append({
                'id': id_,
                'text': text,
                'score': result['score']
            })
        else:
            print(f"No text found for ID {id_}, this ID will be excluded from conversational output.")

    # Generate conversational output
    conversational_response = generate_conversational_output(enriched_results, query)

    return {"response": conversational_response}

