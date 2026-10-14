"""
RAG Search — Гибридный поиск
BM25 + Vector Search с LRU кэшем
"""
import asyncio
import logging
from typing import List, Dict, Optional, Tuple
from collections import OrderedDict
import numpy as np

from rag.chunker import Chunk
from rag.embedder import TextEmbedder

logger = logging.getLogger(__name__)


class LRUCache:
    """LRU Cache для кэширования результатов поиска"""
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.cache = OrderedDict()
    
    def get(self, key: str) -> Optional[List]:
        """Получение из кэша"""
        if key in self.cache:
            # Перемещаем в конец (недавно использованные)
            self.cache.move_to_end(key)
            return self.cache[key]
        return None
    
    def put(self, key: str, value: List) -> None:
        """Добавление в кэш"""
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        
        # Удаляем старые записи
        if len(self.cache) > self.max_size:
            self.cache.popitem(last=False)
    
    @property
    def size(self) -> int:
        """Размер кэша"""
        return len(self.cache)
    
    @property
    def hit_rate(self) -> float:
        """Hit rate кэша (упрощённо)"""
        return 0.0  # Можно добавить счётчик попаданий


class BM25Index:
    """BM25 индекс для текстового поиска"""
    
    def __init__(self):
        self.documents: List[str] = []
        self.doc_lengths: List[int] = []
        self.avg_dl: float = 0.0
        self.doc_freqs: Dict[str, int] = {}
        self.term_freqs: List[Dict[str, int]] = []
        
        # Параметры BM25
        self.k1 = 1.5
        self.b = 0.75
    
    def add_documents(self, texts: List[str]) -> None:
        """Добавление документов в индекс"""
        self.documents = texts
        self.doc_lengths = [len(text.split()) for text in texts]
        self.avg_dl = sum(self.doc_lengths) / len(self.doc_lengths) if self.doc_lengths else 0
        
        # Подсчёт частот терминов
        self.term_freqs = []
        self.doc_freqs = {}
        
        for text in texts:
            terms = text.lower().split()
            tf = {}
            for term in terms:
                tf[term] = tf.get(term, 0) + 1
                self.doc_freqs[term] = self.doc_freqs.get(term, 0) + 1
            self.term_freqs.append(tf)
    
    def search(self, query: str, top_k: int = 5) -> List[Tuple[int, float]]:
        """
        Поиск по BM25
        
        Args:
            query: Поисковый запрос
            top_k: Количество результатов
        
        Returns:
            Список (doc_index, score)
        """
        if not self.documents:
            return []
        
        query_terms = query.lower().split()
        scores = []
        
        for i, doc_tf in enumerate(self.term_freqs):
            score = 0.0
            dl = self.doc_lengths[i]
            
            for term in query_terms:
                if term in doc_tf:
                    tf = doc_tf[term]
                    df = self.doc_freqs.get(term, 0)
                    
                    # BM25 формула
                    idf = np.log((len(self.documents) - df + 0.5) / (df + 0.5) + 1)
                    tf_norm = (tf * (self.k1 + 1)) / (tf + self.k1 * (1 - self.b + self.b * dl / self.avg_dl))
                    score += idf * tf_norm
            
            scores.append((i, score))
        
        # Сортировка по убыванию scores
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]


class RAGSearch:
    """
    Гибридный поиск: BM25 + Vector Search
    С LRU кэшем для частых запросов
    """
    
    def __init__(self, config: dict, embedder: TextEmbedder):
        self.config = config
        self.embedder = embedder
        self.top_k = config.get('top_k', 5)
        self.cache_size = config.get('cache_size', 1000)
        
        # Компоненты поиска
        self.bm25 = BM25Index()
        self.cache = LRUCache(self.cache_size)
        
        # Векторное хранилище
        self.chunks: List[Chunk] = []
        self.vectors: Optional[np.ndarray] = None
        
        # Статистика
        self._cache_hits = 0
        self._cache_misses = 0
        
        logger.info(f"RAGSearch инициализирован (top_k={self.top_k}, cache_size={self.cache_size})")
    
    async def index_chunks(self, chunks: List[Chunk]) -> None:
        """
        Индексация чанков
        
        Args:
            chunks: Список чанков для индексации
        """
        if not chunks:
            logger.warning("Нет чанков для индексации")
            return
        
        self.chunks = chunks
        
        # BM25 индекс
        texts = [chunk.text for chunk in chunks]
        self.bm25.add_documents(texts)
        logger.info(f"✅ BM25 индекс создан ({len(chunks)} документов)")
        
        # Векторный индекс
        logger.info("🔢 Создание векторного индекса...")
        chunk_embeddings = await self.embedder.embed_chunks(chunks)
        
        # Извлечение векторов
        self.vectors = np.array([emb for _, emb in chunk_embeddings])
        logger.info(f"✅ Векторный индекс создан ({self.vectors.shape})")
    
    async def search(self, query: str) -> str:
        """
        Гибридный поиск
        
        Args:
            query: Поисковый запрос
        
        Returns:
            Контекст из найденных чанков
        """
        # Проверка кэша
        cached_result = self.cache.get(query)
        if cached_result is not None:
            self._cache_hits += 1
            logger.debug(f"📦 Кэш: {query[:50]}...")
            return cached_result
        
        self._cache_misses += 1
        
        if not self.chunks:
            logger.warning("Индекс пуст")
            return ""
        
        # BM25 поиск
        bm25_results = self.bm25.search(query, top_k=self.top_k)
        bm25_scores = {idx: score for idx, score in bm25_results}
        
        # Vector поиск
        query_vector = await self.embedder.embed_query(query)
        vector_results = self._vector_search(query_vector, top_k=self.top_k)
        vector_scores = {idx: score for idx, score in vector_results}
        
        # Комбинирование результатов (RRF - Reciprocal Rank Fusion)
        combined_scores = self._combine_scores(bm25_scores, vector_scores)
        
        # Получение топ-K результатов
        top_indices = sorted(combined_scores.keys(), key=lambda x: combined_scores[x], reverse=True)[:self.top_k]
        
        # Формирование контекста
        context_parts = []
        for idx in top_indices:
            if idx < len(self.chunks):
                chunk = self.chunks[idx]
                context_parts.append(chunk.text)
        
        context = "\n\n".join(context_parts)
        
        # Сохранение в кэш
        self.cache.put(query, context)
        
        logger.info(f"🔍 Найдено {len(top_indices)} чанков для запроса: {query[:50]}...")
        return context
    
    def _vector_search(self, query_vector: np.ndarray, top_k: int) -> List[Tuple[int, float]]:
        """
        Векторный поиск (cosine similarity)
        
        Args:
            query_vector: Вектор запроса
            top_k: Количество результатов
        
        Returns:
            Список (chunk_index, similarity_score)
        """
        if self.vectors is None or len(self.vectors) == 0:
            return []
        
        # Нормализация векторов
        query_norm = query_vector / (np.linalg.norm(query_vector) + 1e-10)
        vectors_norm = self.vectors / (np.linalg.norm(self.vectors, axis=1, keepdims=True) + 1e-10)
        
        # Cosine similarity
        similarities = np.dot(vectors_norm, query_norm)
        
        # Получение топ-K
        top_indices = np.argsort(similarities)[::-1][:top_k]
        results = [(int(idx), float(similarities[idx])) for idx in top_indices]
        
        return results
    
    def _combine_scores(
        self,
        bm25_scores: Dict[int, float],
        vector_scores: Dict[int, float],
        k: int = 60
    ) -> Dict[int, float]:
        """
        Комбинирование scores с помощью RRF (Reciprocal Rank Fusion)
        
        RRF(d) = Σ 1 / (k + rank_i(d))
        """
        # Получение рангов
        bm25_ranked = sorted(bm25_scores.items(), key=lambda x: x[1], reverse=True)
        vector_ranked = sorted(vector_scores.items(), key=lambda x: x[1], reverse=True)
        
        bm25_ranks = {idx: rank + 1 for rank, (idx, _) in enumerate(bm25_ranked)}
        vector_ranks = {idx: rank + 1 for rank, (idx, _) in enumerate(vector_ranked)}
        
        # Комбинирование
        all_indices = set(bm25_ranks.keys()) | set(vector_ranks.keys())
        combined = {}
        
        for idx in all_indices:
            score = 0.0
            if idx in bm25_ranks:
                score += 1.0 / (k + bm25_ranks[idx])
            if idx in vector_ranks:
                score += 1.0 / (k + vector_ranks[idx])
            combined[idx] = score
        
        return combined
    
    @property
    def stats(self) -> Dict:
        """Статистика поиска"""
        total = self._cache_hits + self._cache_misses
        hit_rate = self._cache_hits / total if total > 0 else 0.0
        
        return {
            'chunks_indexed': len(self.chunks),
            'cache_size': self.cache.size,
            'cache_hits': self._cache_hits,
            'cache_misses': self._cache_misses,
            'cache_hit_rate': hit_rate,
        }
    
    async def clear_cache(self) -> None:
        """Очистка кэша"""
        self.cache = LRUCache(self.cache_size)
        self._cache_hits = 0
        self._cache_misses = 0
        logger.info("🗑️ Кэш очищен")
