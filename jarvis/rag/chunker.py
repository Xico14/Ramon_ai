"""
Text Chunker — Разбиение текста на чанки
С перекрытием для сохранения контекста
"""
import logging
from typing import List, Dict
from dataclasses import dataclass

from rag.ingestion import Document

logger = logging.getLogger(__name__)


@dataclass
class Chunk:
    """Представление чанка текста"""
    text: str
    metadata: Dict
    chunk_id: str
    document_id: str
    chunk_index: int
    
    def __repr__(self):
        return f"Chunk(id={self.chunk_id}, doc={self.document_id}, index={self.chunk_index}, length={len(self.text)})"


class TextChunker:
    """
    Разбиение текста на чанки
    С перекрытием для сохранения контекста между чанками
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.chunk_size = config.get('chunk_size', 500)  # символов
        self.chunk_overlap = config.get('chunk_overlap', 50)  # символов
        
        logger.info(f"TextChunker инициализирован (size={self.chunk_size}, overlap={self.chunk_overlap})")
    
    def chunk_document(self, document: Document) -> List[Chunk]:
        """
        Разбиение документа на чанки
        
        Args:
            document: Документ для разбиения
        
        Returns:
            Список чанков
        """
        text = document.content
        chunks = []
        
        # Если текст меньше chunk_size, возвращаем один чанк
        if len(text) <= self.chunk_size:
            chunk = Chunk(
                text=text,
                metadata=document.metadata.copy(),
                chunk_id=f"{document.id}_chunk_0",
                document_id=document.id,
                chunk_index=0,
            )
            chunks.append(chunk)
            return chunks
        
        # Разбиение с перекрытием
        start = 0
        chunk_index = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            # Попытка разбить по предложениям или абзацам
            if end < len(text):
                # Ищем конец предложения или абзаца
                sentence_end = self._find_sentence_end(text, start, end)
                if sentence_end > start:
                    end = sentence_end
            
            chunk_text = text[start:end].strip()
            
            if chunk_text:
                chunk = Chunk(
                    text=chunk_text,
                    metadata=document.metadata.copy(),
                    chunk_id=f"{document.id}_chunk_{chunk_index}",
                    document_id=document.id,
                    chunk_index=chunk_index,
                )
                chunks.append(chunk)
                chunk_index += 1
            
            # Следующий чанк с перекрытием
            start = end - self.chunk_overlap
            
            # Защита от бесконечного цикла
            if start >= len(text):
                break
        
        logger.debug(f"Документ {document.id} разбит на {len(chunks)} чанков")
        return chunks
    
    def chunk_documents(self, documents: List[Document]) -> List[Chunk]:
        """
        Разбиение списка документов на чанки
        
        Args:
            documents: Список документов
        
        Returns:
            Список всех чанков
        """
        all_chunks = []
        
        for doc in documents:
            chunks = self.chunk_document(doc)
            all_chunks.extend(chunks)
        
        logger.info(f"📦 Создано {len(all_chunks)} чанков из {len(documents)} документов")
        return all_chunks
    
    def _find_sentence_end(self, text: str, start: int, end: int) -> int:
        """
        Поиск конца предложения в диапазоне
        
        Args:
            text: Полный текст
            start: Начальная позиция
            end: Конечная позиция
        
        Returns:
            Позиция конца предложения или end
        """
        # Ищем конец предложения (., !, ?) в последних 20% чанка
        search_start = int(end - (end - start) * 0.2)
        search_region = text[search_start:end]
        
        # Приоритет: абзац > предложение
        for separator in ['\n\n', '\n', '. ', '! ', '? ']:
            pos = search_region.rfind(separator)
            if pos != -1:
                return search_start + pos + len(separator)
        
        return end
    
    def chunk_by_paragraphs(self, document: Document) -> List[Chunk]:
        """
        Разбиение по абзацам (альтернативный метод)
        
        Args:
            document: Документ для разбиения
        
        Returns:
            Список чанков (по одному на абзац)
        """
        paragraphs = document.content.split('\n\n')
        chunks = []
        
        for i, paragraph in enumerate(paragraphs):
            paragraph = paragraph.strip()
            if paragraph:
                chunk = Chunk(
                    text=paragraph,
                    metadata=document.metadata.copy(),
                    chunk_id=f"{document.id}_para_{i}",
                    document_id=document.id,
                    chunk_index=i,
                )
                chunks.append(chunk)
        
        logger.debug(f"Документ {document.id} разбит на {len(chunks)} абзацев")
        return chunks
