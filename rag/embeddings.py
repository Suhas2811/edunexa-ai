from sentence_transformers import SentenceTransformer


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def create_embeddings(chunks):

    embeddings = model.encode(
        chunks,
        show_progress_bar=False
    )

    return embeddings