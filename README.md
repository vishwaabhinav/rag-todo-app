- place your data under /data/raw/ as txt files
- create an account on https://www.pinecone.io and get the api key
- get the openai api key
- clone .env.example and create .env
- create a venv
- ```python -r requirements.txt```
- ```uvicorn src.app:app --reload```


Once server is up and running, query your data,

```http://127.0.0.1:8000/query?query=what%20are%20my%20todos```