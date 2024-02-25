import argparse
import json

from internals.config import (
  CHROMA_PATH,
  EMBEDDINGS_NAME,
  MODEL_NAME)

from langchain.vectorstores.chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama


def main():
    """
    Take the search query as an argument and return the search results from the vector database
    """
    ollama = Ollama(base_url='http://localhost:11434', model=MODEL_NAME)
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    embedding_function = HuggingFaceEmbeddings(
        model_name=EMBEDDINGS_NAME
    )
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    qachain=RetrievalQA.from_chain_type(ollama, retriever=db.as_retriever())
    user_query = qachain.invoke(query_text)
    print(json.dumps(user_query))

if __name__ == "__main__":
    main()
    