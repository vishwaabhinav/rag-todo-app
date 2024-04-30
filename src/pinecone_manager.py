from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import os

load_dotenv()
index_name = os.getenv('PINECONE_INDEX_NAME')
dimension = int(os.getenv('PINECONE_INDEX_DIMENSION'))
pinecone_api_key = os.getenv('PINECONE_API_KEY')

def setup_pinecone():
    """Setup Pinecone environment and index."""
    """Setup Pinecone environment and index using the new Pinecone client."""
    # Create a Pinecone instance
    pc = Pinecone(api_key=pinecone_api_key)

    # Check if the index exists, and create it if it does not
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric='cosine',  # Use 'cosine' or 'euclidean' as per your use case
            spec=ServerlessSpec(
                cloud='aws',  # Choose the cloud provider
                region='us-east-1'  # Choose the region that best suits your location
            )
        )

    # Get the index
    index = pc.Index(name=index_name)
    return index

def store_embeddings(index, embeddings, ids):
    """Store the given embeddings into the specified Pinecone index only if they don't already exist."""
    vectors = [{"id": str(id_), "values": vec} for id_, vec in zip(ids, embeddings)]
    index.upsert(vectors)

def search_embeddings(index, query_embedding, top_k=5):
    """Query the Pinecone index for the top k most semantically relevant embeddings."""
    # Using Pinecone's query method to find the nearest vectors
    query_results = index.query(vector=query_embedding, top_k=top_k)
    return query_results
