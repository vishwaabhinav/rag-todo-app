from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)

def generate_conversational_output(raw_data, query):
    prompt = "DOCUMENT:"
    for item in raw_data:
        prompt += f"ID: {item['id']}, Text: {item['text']}, Score: {item['score']}\n"
    prompt += "\n\nQUESTION:\n""" + query +  "\n\n"
    
    prompt += """INSTRUCTIONS:
                Answer the users QUESTION using the DOCUMENT text above.
                Keep your answer ground in the facts of the DOCUMENT.
                If the DOCUMENT doesn\’t contain the facts to answer the QUESTION return No Answer found. """
                
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an AI trained to convert raw data into conversational responses."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
