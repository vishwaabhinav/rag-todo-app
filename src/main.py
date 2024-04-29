import hashlib
from src.data_manager import read_text_file, create_chunks
from src.embeddings import generate_embeddings
from src.pinecone_manager import setup_pinecone, store_embeddings, search_embeddings
from src.llm_manager import generate_conversational_output

CHUNK_MAPPING = {}

def generate_id(text):
    """Generate a unique ID for the given text using SHA-256 hashing."""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def run_query(index, query):
    """Run a query on the Pinecone index and return the results."""
    
    query_embedding = generate_embeddings(query)[0].embedding
    
    results = search_embeddings(index, query_embedding, top_k=2)
    
    # 
    results.matches = [result for result in results.matches if result.score >= 0.1 and result.id in CHUNK_MAPPING]
    return [{"text": CHUNK_MAPPING[result.id], "id": result.id, "score": result.score} for result in results.matches]

def main():
    # Configuration and setup
    file_path = 'data/raw/notes.txt'

    # Read data
    notes_content = read_text_file(file_path)
    
    chunks = create_chunks(notes_content, max_length=1024)

    # Generate embeddings
    embeddings = generate_embeddings(chunks)

    # Setup Pinecone
    index = setup_pinecone()

    # Store embeddings
    ids = [generate_id(chunk) for chunk in chunks]  # Assuming each embedding corresponds to a segment of the text
    
    [CHUNK_MAPPING.update({id_: chunk}) for id_, chunk in zip(ids, chunks)]
    
    store_embeddings(index, embeddings, ids)
    
    # generate and query embeddings
    query = input("Enter your query: ")
    results = run_query(index, query)
    response = generate_conversational_output(results, query)
    print("Results:", response)

if __name__ == '__main__':
    main()
