from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)

def generate_embeddings(text):
    """Generate embeddings for the given text using OpenAI's API."""
    response = client.embeddings.create(input=text, 
    model="text-embedding-ada-002")
    return response.data
