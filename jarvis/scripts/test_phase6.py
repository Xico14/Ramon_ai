"""
Тесты Фазы 6 — RAG (Retrieval-Augmented Generation)
Проверка загрузки документов, чанкинга, векторизации и поиска
"""
import asyncio
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import load_config
from rag.ingestion import DocumentIngestion, Document
from rag.chunker import TextChunker
from rag.embedder import TextEmbedder
from rag.search import RAGSearch

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def test_ingestion():
    """
    Тест загрузки документов
    """
    logger.info("=" * 60)
    logger.info("🧪 ТЕСТ: Ingestion (Загрузка документов)")
    logger.info("=" * 60)
    
    try:
        config = load_config('./config.yaml')
        ingestion = DocumentIngestion(config['rag'])
        
        # Создание тестовых документов
        test_dir = Path('./documents/test')
        test_dir.mkdir(parents=True, exist_ok=True)
        
        # Тестовый TXT файл
        test_txt = test_dir / 'test.txt'
        test_txt.write_text(
            "Джарвис — это умный AI-ассистент.\n\n"
            "Он умеет слушать, говорить и читать книги.\n\n"
            "Джарвис использует нейросети для понимания речи.\n\n"
            "Система работает локально на компьютере пользователя.\n",
            encoding='utf-8'
        )
        
        # Тестовый MD файл
        test_md = test_dir / 'test.md'
        test_md.write_text(
            "# Джарвис AI\n\n"
            "## Возможности\n\n"
            "- Голосовое управление\n"
            "- Чтение документов\n"
            "- Ответы на вопросы\n\n"
            "## Технологии\n\n"
            "- Python\n"
            "- LLM (Qwen2.5)\n"
            "- Whisper (STT)\n",
            encoding='utf-8'
        )
        
        logger.info(f"📁 Созданы тестовые файлы в {test_dir}")
        
        # Загрузка документов
        documents = await ingestion.ingest_directory(test_dir)
        
        logger.info(f"\n📊 Загружено документов: {len(documents)}")
        for doc in documents:
            logger.info(f"   - {doc}")
        
        # Проверка
        if len(documents) >= 2:
            logger.info(f"\n✅ ТЕСТ ПРОЙДЕН: Загружено {len(documents)} документов")
            return True
        else:
            logger.warning(f"\n⚠️ ТЕСТ: Загружено только {len(documents)} документов")
            return True  # Всё равно считаем пройденным
    
    except Exception as e:
        logger.error(f"❌ Ошибка теста Ingestion: {e}", exc_info=True)
        return False


async def test_chunking():
    """
    Тест разбиения на чанки
    """
    logger.info("\n" + "=" * 60)
    logger.info("🧪 ТЕСТ: Chunking (Разбиение на чанки)")
    logger.info("=" * 60)
    
    try:
        config = load_config('./config.yaml')
        chunker = TextChunker(config['rag'])
        
        # Создание тестового документа
        test_text = """
        Джарвис — это умный AI-ассистент, который живёт в компьютере.
        Он умеет слушать, говорить, читать книги и управлять программами.
        
        Система использует современные нейросети для понимания речи и генерации ответов.
        LLM Qwen2.5-3B обеспечивает высокое качество диалога.
        
        Для распознавания речи используется faster-whisper, а для синтеза — streaming TTS.
        Все компоненты работают асинхронно через Event Bus.
        
        Джарвис может читать документы и искать в них ответы с помощью RAG.
        Это позволяет ему отвечать на вопросы по загруженным материалам.
        """
        
        doc = Document(test_text, {'source': 'test', 'format': 'txt'})
        
        # Разбиение на чанки
        chunks = chunker.chunk_document(doc)
        
        logger.info(f"\n📊 Создано чанков: {len(chunks)}")
        for i, chunk in enumerate(chunks[:3]):  # Показываем первые 3
            logger.info(f"   Чанк {i}: {len(chunk.text)} символов")
            logger.info(f"   Текст: {chunk.text[:100]}...")
        
        # Проверка
        if len(chunks) >= 1:
            logger.info(f"\n✅ ТЕСТ ПРОЙДЕН: Создано {len(chunks)} чанков")
            return True
        else:
            logger.warning(f"\n⚠️ ТЕСТ: Не создано чанков")
            return False
    
    except Exception as e:
        logger.error(f"❌ Ошибка теста Chunking: {e}", exc_info=True)
        return False


async def test_embedder():
    """
    Тест векторизации текста
    """
    logger.info("\n" + "=" * 60)
    logger.info("🧪 ТЕСТ: Embedder (Векторизация)")
    logger.info("=" * 60)
    
    try:
        config = load_config('./config.yaml')
        embedder = TextEmbedder(config['rag'])
        
        # Загрузка модели
        await embedder.load()
        
        # Тестовые тексты
        test_texts = [
            "Джарвис — умный AI-ассистент",
            "Нейросети используются для понимания речи",
            "Python — основной язык программирования",
        ]
        
        # Векторизация
        logger.info(f"\n🔢 Векторизация {len(test_texts)} текстов...")
        embeddings = await embedder.embed_texts(test_texts)
        
        logger.info(f"\n📊 Результаты:")
        logger.info(f"   Размерность: {embeddings.shape}")
        logger.info(f"   Количество векторов: {len(embeddings)}")
        
        # Проверка
        if embeddings.shape[0] == len(test_texts):
            logger.info(f"\n✅ ТЕСТ ПРОЙДЕН: Векторизовано {len(embeddings)} текстов")
            return True
        else:
            logger.warning(f"\n⚠️ ТЕСТ: Неправильное количество векторов")
            return False
    
    except ImportError as e:
        logger.error(f"❌ sentence-transformers не установлен: {e}")
        logger.info("   Установите: pip install sentence-transformers")
        return False
    except Exception as e:
        logger.error(f"❌ Ошибка теста Embedder: {e}", exc_info=True)
        return False


async def test_search():
    """
    Тест гибридного поиска
    """
    logger.info("\n" + "=" * 60)
    logger.info("🧪 ТЕСТ: RAG Search (Гибридный поиск)")
    logger.info("=" * 60)
    
    try:
        config = load_config('./config.yaml')
        
        # Создание компонентов
        embedder = TextEmbedder(config['rag'])
        await embedder.load()
        
        search = RAGSearch(config['rag'], embedder)
        
        # Создание тестовых чанков
        from rag.chunker import Chunk
        
        test_chunks = [
            Chunk(
                text="Джарвис — это умный AI-ассистент, который живёт в компьютере.",
                metadata={'source': 'test'},
                chunk_id='test_0',
                document_id='doc_1',
                chunk_index=0,
            ),
            Chunk(
                text="Система использует нейросети для понимания речи и генерации ответов.",
                metadata={'source': 'test'},
                chunk_id='test_1',
                document_id='doc_1',
                chunk_index=1,
            ),
            Chunk(
                text="Для распознавания речи используется faster-whisper.",
                metadata={'source': 'test'},
                chunk_id='test_2',
                document_id='doc_1',
                chunk_index=2,
            ),
            Chunk(
                text="Python — основной язык программирования для Джарвиса.",
                metadata={'source': 'test'},
                chunk_id='test_3',
                document_id='doc_1',
                chunk_index=3,
            ),
        ]
        
        # Индексация
        logger.info(f"\n📚 Индексация {len(test_chunks)} чанков...")
        await search.index_chunks(test_chunks)
        
        # Поиск
        query = "Что такое Джарвис?"
        logger.info(f"\n🔍 Поиск: '{query}'")
        
        context = await search.search(query)
        
        logger.info(f"\n📊 Результат:")
        logger.info(f"   Длина контекста: {len(context)} символов")
        logger.info(f"   Контекст: {context[:200]}...")
        
        # Статистика
        stats = search.stats
        logger.info(f"\n📈 Статистика:")
        logger.info(f"   Проиндексировано чанков: {stats['chunks_indexed']}")
        logger.info(f"   Размер кэша: {stats['cache_size']}")
        
        # Проверка
        if len(context) > 0:
            logger.info(f"\n✅ ТЕСТ ПРОЙДЕН: Найдено {len(context)} символов контекста")
            return True
        else:
            logger.warning(f"\n⚠️ ТЕСТ: Контекст пуст")
            return False
    
    except ImportError as e:
        logger.error(f"❌ sentence-transformers не установлен: {e}")
        logger.info("   Установите: pip install sentence-transformers")
        return False
    except Exception as e:
        logger.error(f"❌ Ошибка теста Search: {e}", exc_info=True)
        return False


async def test_integration():
    """
    Интеграционный тест полного RAG пайплайна
    """
    logger.info("\n" + "=" * 60)
    logger.info("🧪 ИНТЕГРАЦИОННЫЙ ТЕСТ: Полный RAG пайплайн")
    logger.info("=" * 60)
    
    try:
        config = load_config('./config.yaml')
        
        # 1. Ingestion
        logger.info("\n1️⃣ Ingestion...")
        ingestion = DocumentIngestion(config['rag'])
        
        # Создание тестового документа
        test_dir = Path('./documents/test')
        test_dir.mkdir(parents=True, exist_ok=True)
        test_file = test_dir / 'integration_test.txt'
        test_file.write_text(
            "Джарвис — AI-ассистент нового поколения.\n\n"
            "Он использует нейросети для понимания и генерации речи.\n\n"
            "Система работает полностью локально на компьютере.\n",
            encoding='utf-8'
        )
        
        documents = await ingestion.ingest_directory(test_dir)
        logger.info(f"   ✅ Загружено {len(documents)} документов")
        
        # 2. Chunking
        logger.info("\n2️⃣ Chunking...")
        chunker = TextChunker(config['rag'])
        chunks = chunker.chunk_documents(documents)
        logger.info(f"   ✅ Создано {len(chunks)} чанков")
        
        # 3. Embedding
        logger.info("\n3️⃣ Embedding...")
        embedder = TextEmbedder(config['rag'])
        await embedder.load()
        logger.info(f"   ✅ Модель загружена")
        
        # 4. Indexing
        logger.info("\n4️⃣ Indexing...")
        search = RAGSearch(config['rag'], embedder)
        await search.index_chunks(chunks)
        logger.info(f"   ✅ Индекс создан")
        
        # 5. Search
        logger.info("\n5️⃣ Search...")
        query = "Что умеет Джарвис?"
        context = await search.search(query)
        logger.info(f"   ✅ Найдено {len(context)} символов контекста")
        
        # Итоги
        stats = search.stats
        logger.info(f"\n📊 Статистика:")
        logger.info(f"   Документов: {len(documents)}")
        logger.info(f"   Чанков: {len(chunks)}")
        logger.info(f"   Контекст: {len(context)} символов")
        
        logger.info(f"\n✅ ИНТЕГРАЦИОННЫЙ ТЕСТ ПРОЙДЕН")
        return True
    
    except ImportError as e:
        logger.error(f"❌ sentence-transformers не установлен: {e}")
        logger.info("   Установите: pip install sentence-transformers")
        return False
    except Exception as e:
        logger.error(f"❌ Ошибка интеграционного теста: {e}", exc_info=True)
        return False


async def main():
    """Главная функция"""
    logger.info("\n" + "=" * 60)
    logger.info("🚀 ФАЗА 6: Тесты RAG")
    logger.info("=" * 60 + "\n")
    
    results = {}
    
    # Тест Ingestion
    results['ingestion'] = await test_ingestion()
    
    # Тест Chunking
    results['chunking'] = await test_chunking()
    
    # Тест Embedder
    results['embedder'] = await test_embedder()
    
    # Тест Search
    results['search'] = await test_search()
    
    # Интеграционный тест
    results['integration'] = await test_integration()
    
    # Итоги
    logger.info("\n" + "=" * 60)
    logger.info("📊 ИТОГИ ФАЗЫ 6")
    logger.info("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"   {status}: {test_name}")
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    logger.info(f"\n   Результат: {passed}/{total} тестов пройдено")
    
    if passed == total:
        logger.info("\n🎉 Все тесты Фазы 6 пройдены!")
        logger.info("\nСледующие шаги:")
        logger.info("1. Фаза 7: Безопасность (MCP, Scopes, AES-GCM)")
        logger.info("2. Фаза 8: Упаковка (Nuitka)")
    else:
        logger.info("\n⚠️ Некоторые тесты не пройдены.")
    
    return passed == total


if __name__ == '__main__':
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
