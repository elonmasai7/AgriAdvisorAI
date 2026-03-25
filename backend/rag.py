import json
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from openai import OpenAI

load_dotenv()

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
KB_PATH = BASE_DIR / "disease_db" / "knowledge_base.json"
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_store")
CHROMA_COLLECTION = "agri_disease_knowledge"
EMBED_MODEL = os.getenv("EMBED_MODEL", "oxlo-embed")


class OxloEmbeddings(Embeddings):
    def __init__(self) -> None:
        self.client = OpenAI(
            api_key=os.getenv("OXLO_API_KEY"),
            base_url=os.getenv("OXLO_BASE_URL", "https://api.oxlo.ai/v1"),
        )

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        response = self.client.embeddings.create(model=EMBED_MODEL, input=texts)
        return [item.embedding for item in response.data]

    def embed_query(self, text: str) -> list[float]:
        response = self.client.embeddings.create(model=EMBED_MODEL, input=[text])
        return response.data[0].embedding


def _load_knowledge_base() -> list[dict]:
    with KB_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def _build_documents(entries: list[dict]) -> list[Document]:
    docs: list[Document] = []
    for entry in entries:
        page_content = f"{entry['disease_name']} on {entry['crop']}: {entry['symptoms']}"
        docs.append(Document(page_content=page_content, metadata=entry))
    return docs


def initialize_vector_store() -> Chroma:
    embeddings = OxloEmbeddings()
    vectorstore = Chroma(
        collection_name=CHROMA_COLLECTION,
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embeddings,
    )

    try:
        count = vectorstore._collection.count()  # pylint: disable=protected-access
    except Exception:  # noqa: BLE001
        count = 0

    if count > 0:
        logger.info("Loaded existing Chroma collection with %s entries", count)
        return vectorstore

    entries = _load_knowledge_base()
    docs = _build_documents(entries)

    if docs:
        vectorstore.add_documents(docs)
        logger.info("Seeded vector store with %s entries", len(docs))

    return vectorstore


def retrieve_relevant_diseases(query: str, top_k: int = 3) -> list[dict]:
    try:
        vectorstore = initialize_vector_store()
        results = vectorstore.similarity_search(query, k=top_k)
        return [doc.metadata for doc in results]
    except Exception as exc:  # noqa: BLE001
        logger.exception("RAG retrieval failed: %s", exc)
        return []
