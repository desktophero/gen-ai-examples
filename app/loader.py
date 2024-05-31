import argparse
import os
import glob
import shutil
import json
import sys

from internals.config import (
  PDF_DOCUMENT_PATH,
  FILE_DOCUMENT_PATH,
  CHUNK_SIZE,
  CHUNK_OVERLAP,
  CHROMA_PATH, 
  EMBEDDINGS_NAME)

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import UnstructuredMarkdownLoader

def list_documents(folder: str) -> list:
    files = glob.glob(folder + "/*.md")
    if len(files) > 0:
        print(f"Found {len(files)} files in {folder}")
    return files

def load_documents(doc_type: str = "pdf", files: list = None):
    """
    Load the documents from the PDF_DOCUMENT_PATH. Eventually this will be a list of docs, maybe
    """

    if doc_type == "pdf":
        loader = PyMuPDFLoader(PDF_DOCUMENT_PATH)
    else:
        loader = UnstructuredMarkdownLoader(files)
    docs = loader.load()
    # print(docs)
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
    # document = chunks[10]
    # print(document.page_content)
    # print(json.dumps(document.metadata, indent=2))
    return chunks

def load_to_chroma(chunks: list[Document]):
    """
    Load the chunks into the Chroma database. The database is deleted if it already exists.
    """
    embeddings = HuggingFaceEmbeddings(
        show_progress=True,
        model_name=EMBEDDINGS_NAME
    )

    # print(f"Loaded {embeddings} embeddings.")
    db = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=CHROMA_PATH,
        collection_metadata={"hnsw:space": "cosine"}
    )
    db.persist()
    # print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")

def clear_vector() -> bool:
    try:
        if os.path.exists(CHROMA_PATH):
            shutil.rmtree(CHROMA_PATH)
        return True
    except Exception as e:
        print(f"Exception: {e}")
        return Fale
    
parser = argparse.ArgumentParser(description="Process some file type")
parser.add_argument("-t", "--type", help="Specify a type: pdf or md")

args = parser.parse_args()
if not clear_vector():
    print("Error!")

if args.type != "pdf":
    files = list_documents(FILE_DOCUMENT_PATH)
else:
    files = [PDF_DOCUMENT_PATH]

for file in files:
    documents = load_documents(args.type, file)
    # print(f"Document len: {len(documents)}")
    chunk_data = split_text(documents)
    load_to_chroma(chunk_data)
