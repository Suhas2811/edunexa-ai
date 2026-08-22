import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from document_processing.pdf_processor import extract_text_from_pdf
from document_processing.docx_processor import extract_text_from_docx
from document_processing.pptx_processor import extract_text_from_pptx

from rag.chunking import chunk_text
from rag.embeddings import create_embeddings
from rag.vector_store import store_embeddings, get_collection_count
from rag.retrieval import retrieve_relevant_chunks


st.set_page_config(
    page_title="VidyānVaya AI",
    page_icon="📚",
    layout="wide"
)


st.title("📚 VidyānVaya AI")
st.subheader("A Subject-Agnostic Academic Learning Assistant")

st.write(
    "Upload your academic materials and use AI to "
    "learn, solve questions, practice, and improve."
)

st.divider()

st.header("📂 Upload Academic Materials")


uploaded_files = st.file_uploader(
    "Upload your notes, textbooks, question papers, or presentations",
    type=["pdf", "docx", "pptx"],
    accept_multiple_files=True
)


if uploaded_files:

    st.success(f"{len(uploaded_files)} file(s) uploaded.")

    for file in uploaded_files:

        st.write(f"📄 {file.name}")

        extracted_text = ""


        if file.name.lower().endswith(".pdf"):

            try:

                pages = extract_text_from_pdf(file)

                extracted_text = "\n".join(
                    page["text"]
                    for page in pages
                )

                total_characters = len(extracted_text)

                st.success(
                    f"PDF processed successfully — "
                    f"{len(pages)} pages, "
                    f"{total_characters:,} characters extracted."
                )

                with st.expander("Preview extracted text"):

                    for page in pages[:3]:

                        st.markdown(
                            f"**Page {page['page_number']}**"
                        )

                        st.write(page["text"][:1500])

            except Exception as e:

                st.error(
                    f"Could not process PDF: {e}"
                )

                continue


        elif file.name.lower().endswith(".docx"):

            try:

                paragraphs = extract_text_from_docx(file)

                extracted_text = "\n".join(
                    paragraph["text"]
                    for paragraph in paragraphs
                )

                total_characters = len(extracted_text)

                st.success(
                    f"DOCX processed successfully — "
                    f"{len(paragraphs)} paragraphs, "
                    f"{total_characters:,} characters extracted."
                )

                with st.expander("Preview extracted text"):

                    for paragraph in paragraphs[:20]:

                        st.write(paragraph["text"])

            except Exception as e:

                st.error(
                    f"Could not process DOCX: {e}"
                )

                continue


        elif file.name.lower().endswith(".pptx"):

            try:

                slides = extract_text_from_pptx(file)

                extracted_text = "\n".join(
                    slide["text"]
                    for slide in slides
                )

                total_characters = len(extracted_text)

                st.success(
                    f"PPTX processed successfully — "
                    f"{len(slides)} slides, "
                    f"{total_characters:,} characters extracted."
                )

                with st.expander("Preview extracted text"):

                    for slide in slides[:5]:

                        st.markdown(
                            f"**Slide {slide['slide_number']}**"
                        )

                        st.write(slide["text"][:1500])

            except Exception as e:

                st.error(
                    f"Could not process PPTX: {e}"
                )

                continue


        if extracted_text:

            chunks = chunk_text(extracted_text)

            st.info(
                f"🧩 {len(chunks)} text chunks created."
            )

            with st.expander("Preview text chunks"):

                for index, chunk in enumerate(
                    chunks[:5],
                    start=1
                ):

                    st.markdown(
                        f"**Chunk {index}**"
                    )

                    st.write(chunk)


            try:

                with st.spinner(
                    "Creating embeddings..."
                ):

                    embeddings = create_embeddings(
                        chunks
                    )

                st.success(
                    f"🧠 {len(embeddings)} embeddings "
                    f"created successfully."
                )

                st.write(
                    f"Embedding dimension: "
                    f"{len(embeddings[0])}"
                )


                with st.spinner(
                    "Storing embeddings in vector database..."
                ):

                    store_embeddings(
                        chunks,
                        embeddings,
                        file.name
                    )


                st.success(
                    f"💾 Embeddings from "
                    f"{file.name} stored successfully."
                )


            except Exception as e:

                st.error(
                    f"Could not create or store embeddings: {e}"
                )


    st.divider()

    total_embeddings = get_collection_count()

    st.info(
        f"📊 Total embeddings stored in the "
        f"vector database: {total_embeddings}"
    )


else:

    st.info(
        "Upload your academic materials to get started."
    )
st.divider()

st.header("🔍 Search Your Academic Materials")

query = st.text_input(
    "Ask a question based on your uploaded materials"
)

if query:

    try:

        with st.spinner(
            "Searching for relevant information..."
        ):

            results = retrieve_relevant_chunks(
                query
            )

        st.success(
            "Relevant information found."
        )

        documents = results["documents"][0]

        distances = results["distances"][0]

        for index, document in enumerate(
            documents,
            start=1
        ):

            st.markdown(
                f"### Result {index}"
            )

            st.write(document)

            st.caption(
                f"Similarity distance: "
                f"{distances[index - 1]:.4f}"
            )

    except Exception as e:

        st.error(
            f"Could not retrieve information: {e}"
        )