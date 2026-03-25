import os
import json
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_store")
EMBED_MODEL = os.getenv("EMBED_MODEL")

embeddings = OpenAIEmbeddings(
    openai_api_base=os.getenv("OXLO_BASE_URL"),
    openai_api_key=os.getenv("OXLO_API_KEY"),
    model=EMBED_MODEL
)


def initialize_vector_store() -> Chroma:
    if os.path.exists(CHROMA_DB_PATH):
        # Load existing
        vectorstore = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)
    else:
        # Create new
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
    
    return vectorstore


def retrieve_relevant_diseases(query: str, top_k: int=3) -> list[dict]:
    vectorstore = initialize_vector_store()
    results = vectorstore.similarity_search(query, k=top_k)
    return [doc.metadata for doc in results]
