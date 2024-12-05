import argparse
import os
import shutil
from langchain.schema.document import Document
from getEmbedding import get_embedding_function
from langchain.vectorstores.chroma import Chroma

CHROMA_PATH = "chroma"
DATA_PATH = "/Users/krishnasuresh/Desktop/Projects/Vigil_Dev/server/embeddedvector"


def main():

    # Check if the database should be cleared (using the --clear flag).
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print("✨ Clearing Database")
        clear_database()

    # Create (or update) the data store.
    documents = load_documents()
    add_to_chroma(documents)


def load_documents():
    documents = []
    for filename in os.listdir(DATA_PATH):
        if filename.endswith(".txt"):
            file_path = os.path.join(DATA_PATH, filename)
            with open(file_path, "r") as file:
                content = file.read()
                metadata = {"source": filename}
                documents.append(Document(page_content=content, metadata=metadata))
    return documents


def add_to_chroma(documents: list[Document]):
    # Load the existing database.
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
    )

    # Calculate Document IDs.
    documents_with_ids = calculate_document_ids(documents)

    # Add or Update the documents.
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Only add documents that don't exist in the DB.
    new_documents = []
    for document in documents_with_ids:
        if document.metadata["id"] not in existing_ids:
            new_documents.append(document)

    if len(new_documents):
        print(f"👉 Adding new documents: {len(new_documents)}")
        new_document_ids = [doc.metadata["id"] for doc in new_documents]
        db.add_documents(new_documents, ids=new_document_ids)
    else:
        print("✅ No new documents to add")


def calculate_document_ids(documents):
    for document in documents:
        source = document.metadata.get("source")
        document_id = f"{source}"
        document.metadata["id"] = document_id

    return documents


def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)


if __name__ == "__main__":
    main()
