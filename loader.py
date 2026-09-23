from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import config


def get_chunked_documents() -> list[Document]:
    documents = []
    folders = config.TARGET_FOLDERS or [""]

    for folder in folders:
        folder_path = config.DOCS_DIR / folder
        if not folder_path.exists():
            print(f"⚠️ Папка не найдена: {folder_path}")
            continue

        for file_path in folder_path.rglob("*.txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                documents.append({
                    "source": str(file_path.relative_to(config.DOCS_DIR)),
                    "text": f.read()
                })

    if not documents:
        raise FileNotFoundError("Документы не найдены. Проверь пути в config.py")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        length_function=len,
    )

    lc_documents = []
    for doc in documents:
        chunks = text_splitter.split_text(doc["text"])
        for i, chunk in enumerate(chunks):
            lc_documents.append(
                Document(
                    page_content=chunk,
                    metadata={"source": doc["source"], "chunk_id": i}
                )
            )

    return lc_documents