import os
import shutil
import json

from internals.config import (
  PDF_DOCUMENT_PATH,
  CHUNK_SIZE,
  CHUNK_OVERLAP,
  CHROMA_PATH, 
  EMBEDDINGS_NAME)

from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain.schema import Document
from langchain.vectorstores.chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader

def load_documents():
    """
    Load the documents from the PDF_DOCUMENT_PATH. Eventually this will be a list of docs, maybe
    """

    loader = PyMuPDFLoader(PDF_DOCUMENT_PATH)
    docs = loader.load()
    print(docs)
    return docs

def split_text(documents: list[Document]):
    """
    After loading the document, split the text into chunks for the Chroma database.
    """
    print(documents[0].page_content)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        add_start_index=True
    )

    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks")
    document = chunks[10]
    print(document.page_content)
    print(json.dumps(document.metadata, indent=2))
    return chunks

def load_to_chroma(chunks: list[Document]):
    """
    Load the chunks into the Chroma database. The database is deleted if it already exists.
    """
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    embeddings = HuggingFaceEmbeddings(
        show_progress=True,
        model_name=EMBEDDINGS_NAME
    )

    print(f"Loaded {embeddings} embeddings.")
    db = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=CHROMA_PATH,
        collection_metadata={"hnsw:space": "cosine"}
    )
    db.persist()
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")

documents = load_documents()
print(f"Number of documents: {len(documents)}")
chunk_data = split_text(documents)
load_to_chroma(chunk_data)
