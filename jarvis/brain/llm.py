"""
LLM — Мозг Джарвиса
Обёртка над llama-cpp-python для работы с Qwen2.5-3B
"""
import asyncio
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class LLM:
    """
    Large Language Model
    Использует llama-cpp-python для локального запуска Qwen2.5-3B
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.model_path = config.get('model_path', './models/qwen2.5-3b-q4_k_m.gguf')
        self.n_ctx = config.get('n_ctx', 4096)
        self.n_threads = config.get('n_threads', 4)
        self.n_gpu_layers = config.get('n_gpu_layers', 0)
        self.temperature = config.get('temperature', 0.7)
        self.max_tokens = config.get('max_tokens', 512)
        self.grammar_path = config.get('grammar_path')
        
        self._model = None
        self._loaded = False
        
        logger.info(f"LLM инициализирован (модель: {self.model_path})")
    
    async def load(self) -> None:
        """Загрузка модели"""
        if self._loaded:
            return
        
        model_file = Path(self.model_path)
        if not model_file.exists():
            raise FileNotFoundError(f"Модель не найдена: {self.model_path}")
        
        logger.info(f"📥 Загрузка модели из {self.model_path}...")
        
        # Импорт llama-cpp-python
        try:
            from llama_cpp import Llama
        except ImportError:
            raise ImportError("llama-cpp-python не установлен. Запустите: pip install llama-cpp-python")
        
        # Загрузка модели (в отдельном потоке, чтобы не блокировать event loop)
        loop = asyncio.get_event_loop()
        self._model = await loop.run_in_executor(None, self._load_model_sync)
        
        self._loaded = True
        logger.info("✅ Модель загружена")
    
    def _load_model_sync(self):
        """Синхронная загрузка модели"""
        from llama_cpp import Llama
        
        # Загрузка GBNF grammar (если есть)
        grammar = None
        if self.grammar_path and Path(self.grammar_path).exists():
            from llama_cpp import LlamaGrammar
            grammar = LlamaGrammar.from_file(self.grammar_path)
            logger.info(f"✅ GBNF grammar загружен: {self.grammar_path}")
        
        model = Llama(
            model_path=self.model_path,
            n_ctx=self.n_ctx,
            n_threads=self.n_threads,
            n_gpu_layers=self.n_gpu_layers,
            verbose=False,
        )
        
        return model, grammar
    
    async def generate(
        self,
        user_text: str,
        context: str = "",
        history: list[dict] | None = None,
    ) -> str:
        """
        Генерация ответа
        """
        if not self._loaded:
            await self.load()
        
        model, grammar = self._model
        
        # Формирование промпта
        prompt = self._build_prompt(user_text, context, history or [])
        
        logger.debug(f"Промпт:\n{prompt}")
        
        # Генерация (в отдельном потоке)
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: model(
                prompt,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                grammar=grammar,
                stop=["</s>", "User:", "Пользователь:"],
            )
        )
        
        answer = response['choices'][0]['text'].strip()
        
        logger.debug(f"Ответ LLM: {answer[:100]}...")
        
        return answer
    
    def _build_prompt(
        self,
        user_text: str,
        context: str,
        history: list[dict],
    ) -> str:
        """Построение промпта"""
        system_prompt = """Ты — Джарвис, умный AI-ассистент. Ты помогаешь пользователю с различными задачами.
Отвечай кратко, по делу и дружелюбно. Если не знаешь ответа — честно скажи об этом.
"""
        
        if context:
            system_prompt += f"\n\nКонтекст из документов:\n{context}\n"
        
        # Формирование диалога
        messages = [f"System: {system_prompt}"]
        
        for msg in history[-6:]:  # Последние 6 сообщений
            role = "User" if msg['role'] == 'user' else "Assistant"
            messages.append(f"{role}: {msg['content']}")
        
        messages.append(f"User: {user_text}")
        messages.append("Assistant:")
        
        prompt = "\n".join(messages)
        
        return prompt
    
    async def generate_stream(
        self,
        user_text: str,
        context: str = "",
        history: list[dict] | None = None,
    ):
        """
        Стриминг генерации (yield токены)
        """
        if not self._loaded:
            await self.load()
        
        model, grammar = self._model
        prompt = self._build_prompt(user_text, context, history or [])
        
        loop = asyncio.get_event_loop()
        
        # Стриминг в отдельном потоке
        def stream_generator():
            for chunk in model(
                prompt,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                grammar=grammar,
                stream=True,
                stop=["</s>", "User:", "Пользователь:"],
            ):
                token = chunk['choices'][0]['text']
                if token:
                    yield token
        
        # Конвертация синхронного генератора в асинхронный
        for token in stream_generator():
            yield token
            await asyncio.sleep(0)  # Даём шанс event loop
    
    async def stop(self) -> None:
        """Остановка LLM"""
        if self._model:
            self._model = None
            self._loaded = False
            logger.info("🛑 LLM остановлен")
    
    @property
    def is_loaded(self) -> bool:
        """Загружена ли модель"""
        return self._loaded
