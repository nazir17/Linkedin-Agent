import os
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "chat-agent")

EMBEDDING_DIMENSION = 768

pc = Pinecone(api_key=PINECONE_API_KEY)

def init_pinecone_index():
    existing_indexes = [idx["name"] for idx in pc.list_indexes()]

    if INDEX_NAME not in existing_indexes:
        print(f"Creating new Pinecone index '{INDEX_NAME}' with dimension {EMBEDDING_DIMENSION}")
        pc.create_index(
            name=INDEX_NAME,
            dimension=EMBEDDING_DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region=PINECONE_ENVIRONMENT),
        )
    else:
        idx_info = pc.describe_index(INDEX_NAME)
        if idx_info["dimension"] != EMBEDDING_DIMENSION:
            print(f"Deleting index '{INDEX_NAME}' with incorrect dimension {idx_info['dimension']}")
            pc.delete_index(INDEX_NAME)
            
            print(f"Creating new index '{INDEX_NAME}' with dimension {EMBEDDING_DIMENSION}")
            pc.create_index(
                name=INDEX_NAME,
                dimension=EMBEDDING_DIMENSION,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region=PINECONE_ENVIRONMENT),
            )

    return pc.Index(INDEX_NAME)

pinecone_index = init_pinecone_index()