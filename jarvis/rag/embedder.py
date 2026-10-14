"""
Text Embedder — Векторизация текста
Превращение текста в числовые векторы для поиска
"""
import asyncio
import logging
from typing import List, Optional
import numpy as np

from rag.chunker import Chunk

logger = logging.getLogger(__name__)


class TextEmbedder:
    """
    Векторизация текста
    Использует sentence-transformers для создания эмбеддингов
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.model_name = config.get('embedding_model', 'sentence-transformers/all-MiniLM-L6-v2')
        self._model = None
        self._loaded = False
        
        logger.info(f"TextEmbedder инициализирован (модель: {self.model_name})")
    
    async def load(self) -> None:
        """Загрузка модели эмбеддингов"""
        if self._loaded:
            return
        
        logger.info(f"📥 Загрузка модели эмбеддингов: {self.model_name}")
        
        try:
            from sentence_transformers import SentenceTransformer
            
            # Загрузка в отдельном потоке
            loop = asyncio.get_event_loop()
            self._model = await loop.run_in_executor(
                None,
                lambda: SentenceTransformer(self.model_name)
            )
            
            self._loaded = True
            logger.info("✅ Модель эмбеддингов загружена")
        
        except ImportError:
            logger.error("sentence-transformers не установлен. Установите: pip install sentence-transformers")
            raise
        except Exception as e:
            logger.error(f"Ошибка загрузки модели: {e}")
            raise
    
    async def embed_text(self, text: str) -> np.ndarray:
        """
        Векторизация одного текста
        
        Args:
            text: Текст для векторизации
        
        Returns:
            Вектор (numpy array)
        """
        if not self._loaded:
            await self.load()
        
        loop = asyncio.get_event_loop()
        embedding = await loop.run_in_executor(
            None,
            lambda: self._model.encode(text, convert_to_numpy=True)
        )
        
        return embedding
    
    async def embed_texts(self, texts: List[str]) -> np.ndarray:
        """
        Векторизация списка текстов (батч)
        
        Args:
            texts: Список текстов
        
        Returns:
            Матрица векторов (numpy array)
        """
        if not self._loaded:
            await self.load()
        
        loop = asyncio.get_event_loop()
        embeddings = await loop.run_in_executor(
            None,
            lambda: self._model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        )
        
        return embeddings
    
    async def embed_chunks(self, chunks: List[Chunk]) -> List[tuple[Chunk, np.ndarray]]:
        """
        Векторизация списка чанков
        
        Args:
            chunks: Список чанков
        
        Returns:
            Список пар (chunk, embedding)
        """
        if not chunks:
            return []
        
        # Извлечение текстов
        texts = [chunk.text for chunk in chunks]
        
        # Векторизация батчем
        logger.info(f"🔢 Векторизация {len(chunks)} чанков...")
        embeddings = await self.embed_texts(texts)
        
        # Создание пар
        result = list(zip(chunks, embeddings))
        
        logger.info(f"✅ Векторизовано {len(result)} чанков")
        return result
    
    async def embed_query(self, query: str) -> np.ndarray:
        """
        Векторизация запроса для поиска
        
        Args:
            query: Поисковый запрос
        
        Returns:
            Вектор запроса
        """
        return await self.embed_text(query)
    
    @property
    def embedding_dim(self) -> int:
        """Размерность эмбеддингов"""
        if self._model:
            return self._model.get_sentence_embedding_dimension()
        return 384  # По умолчанию для all-MiniLM-L6-v2
    
    @property
    def is_loaded(self) -> bool:
        """Загружена ли модель"""
        return self._loaded
