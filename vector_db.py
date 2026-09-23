from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import config

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )

def build_database(documents):
    print(f"Создаем локальную базу из {len(documents)} чанков в {config.CHROMA_DB_DIR}...")
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=get_embeddings(),
        persist_directory=str(config.CHROMA_DB_DIR)
    )
    return vectorstore

def get_database():
    return Chroma(
        persist_directory=str(config.CHROMA_DB_DIR),
        embedding_function=get_embeddings()
    )