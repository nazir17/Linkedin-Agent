from app.configs.pinecone_config import pinecone_index



def upsert_vectors(vectors: list):
    try:
        pinecone_index.upsert(vectors=vectors)
        print(f"{len(vectors)} vectors upserted successfully.")
    except Exception as e:
        print(f"Pinecone upsert failed: {e}")
        raise


def query_similar(vector, top_k=5):
    try:
        res = pinecone_index.query(vector=vector, top_k=top_k, include_metadata=True)
        return res
    except Exception as e:
        print(f"Pinecone query failed: {e}")
        raise