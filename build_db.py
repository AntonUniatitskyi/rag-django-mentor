from loader import get_chunked_documents
from vector_db import build_database


def main():
    print("Начинаем сборку базы знаний...")

    try:
        docs = get_chunked_documents()
        print(f"✂️ Документация нарезана на {len(docs)} чанков.")
        build_database(docs)
        print("✅ Векторная база успешно создана!")
    except Exception as e:
        print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    main()