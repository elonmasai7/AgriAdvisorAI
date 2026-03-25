import json
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from openai import OpenAI

load_dotenv()

ROOT = Path(__file__).resolve().parents[1]
KB_PATH = ROOT / "disease_db" / "knowledge_base.json"
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_store")
EMBED_MODEL = os.getenv("EMBED_MODEL", "oxlo-embed")
COLLECTION_NAME = "agri_disease_knowledge"


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


def main() -> None:
    with KB_PATH.open("r", encoding="utf-8") as file:
        entries = json.load(file)

    docs: list[Document] = []
    for entry in entries:
        page_content = f"{entry['disease_name']} on {entry['crop']}: {entry['symptoms']}"
        docs.append(Document(page_content=page_content, metadata=entry))

    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DB_PATH,
        embedding_function=OxloEmbeddings(),
    )

    try:
        vectorstore.delete_collection()
    except Exception:  # noqa: BLE001
        pass

    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=OxloEmbeddings(),
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DB_PATH,
    )

    _ = vectorstore
    print(f"Seeded {len(docs)} diseases into ChromaDB at {CHROMA_DB_PATH}")


if __name__ == "__main__":
    main()
