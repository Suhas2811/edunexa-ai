import chromadb
import uuid


client = chromadb.PersistentClient(
    path="data/chroma_db"
)


collection = client.get_or_create_collection(
    name="academic_materials"
)


def store_embeddings(chunks, embeddings, source_name):

    ids = [
        str(uuid.uuid4())
        for _ in chunks
    ]

    metadatas = [
        {
            "source": source_name,
            "chunk_number": index + 1
        }
        for index in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )


def get_collection_count():

    return collection.count()