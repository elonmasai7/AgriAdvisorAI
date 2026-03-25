import json
import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_store")
EMBED_MODEL = os.getenv("EMBED_MODEL")


def main():
    embeddings = OpenAIEmbeddings(
        openai_api_base=os.getenv("OXLO_BASE_URL"),
        openai_api_key=os.getenv("OXLO_API_KEY"),
        model=EMBED_MODEL
    )
    
    with open("disease_db/knowledge_base.json", "r") as f:
        data = json.load(f)
    
    documents = []
    for entry in data:
        page_content = f"{entry['disease_name']} on {entry['crop']}: {entry['symptoms']}"
        doc = Document(page_content=page_content, metadata=entry)
        documents.append(doc)
    
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=CHROMA_DB_PATH
    )
    
    print(f"Seeded {len(documents)} diseases into ChromaDB at {CHROMA_DB_PATH}")


if __name__ == "__main__":
    main()
