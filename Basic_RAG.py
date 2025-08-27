import requests
from qdrant_client import QdrantClient # type: ignore
from qdrant_client.models import Distance, VectorParams, PointStruct # type: ignore

client = QdrantClient(url="http://localhost:6333")

if not client.collection_exists(collection_name="demo"):
    client.create_collection(
        collection_name="demo",
        vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
    )

dummy_data = [
    "My name is David",
    "I love programming",
    "Python is my favorite language",
    "I enjoy hiking and outdoor activities",
    "Artificial Intelligence is the future",
    "Machine Learning is a subset of AI",
    "Data Science involves statistics and programming",
    "My name is Alice"
]

def insert_data():
    for idx, text in enumerate(dummy_data):
        response = requests.post("http://localhost:11434/api/embed",
                                 json={
                                     "model": "mxbai-embed-large",
                                     "input": text
                                     }
                                )

        data = response.json()
        embedding = data['embeddings'][0]
        client.upsert(
            collection_name="demo",
            wait=True,
            points=[PointStruct(id=idx, vector=embedding, payload={"text": text})],
        )

def prompt_gen():
    user_data = input("Enter your question: ")
    prompt_data = f"Represent this sentence for searching relevant documents: {user_data}"

    response = requests.post("http://localhost:11434/api/embed",
                             json={
                                 "model": "mxbai-embed-large",
                                 "input": prompt_data
                                 }
                            )
    data = response.json()
    query_embedding = data['embeddings'][0]

    search_result = client.query_points(
        collection_name="demo",
        query=query_embedding,
        limit=3,
        with_payload=True
    )

    print("Search Results:")
    for hit in search_result.points:
        print(hit.payload['text'])

def generate_response():
    prompt = input("Enter your prompt for response generation: ")
    response = requests.post("http://localhost:11434/api/generate",
                             json={
                                 "model": "gemma3:4b",
                                 "prompt": prompt,
                                 "stream": False
                                 }
                            )

    #return response.json()['response']
    response_text = response.json()['response']
    print("Generated Response:", response_text)

def actual_prompt():
    user_input = input("Enter your question: ")
    prompt_data = f"Represent this sentence for searching relevant documents: {user_input}"
    
    response = requests.post("http://localhost:11434/api/embed",
                             json={
                                 "model": "mxbai-embed-large",
                                 "input": prompt_data
                                 }
                            )
    data = response.json()
    query_embedding = data['embeddings'][0]

    search_result = client.query_points(
        collection_name="demo",
        query=query_embedding,
        limit=3,
        with_payload=True
    )

    relevent_passages = "\n".join([f"- {hit.payload['text']}" for hit in search_result.points])

    augmented_prompt = f"""
      The following are relevant passages:
      <retrieved-data>{relevent_passages}</retrieved-data>

      Here's the original user prompt, answer with help of the retrieved passages:
      <user-prompt>{user_input}</user-prompt>"""

    response = requests.post("http://localhost:11434/api/generate",
                             json={
                                 "model": "mistral:7b",
                                 "prompt": augmented_prompt,
                                 "stream": False
                                 }
                            )

    response_text = response.json()['response']
    print("Generated Response:", response_text)

def main():
    #insert_data()
    #prompt_gen()
    #generate_response()
    actual_prompt()

if __name__ == "__main__":
    main()
