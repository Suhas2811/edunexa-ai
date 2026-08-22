from rag.embeddings import create_embeddings
from rag.vector_store import collection


def retrieve_relevant_chunks(query, n_results=5):

    query_embedding = create_embeddings(
        [query]
    )

    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=n_results
    )

    return results