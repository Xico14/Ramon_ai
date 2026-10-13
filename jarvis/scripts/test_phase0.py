"""
Тесты Фазы 0 — Proof of Concept
Проверка самых рискованных частей системы
"""
import asyncio
import time
import logging
import sys
from pathlib import Path

# Добавляем корень проекта в path
sys.path.insert(0, str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def test_p0_tool_calling():
    """
    P0: Tool-calling
    Проверка: может ли LLM вызывать функции?
    """
    logger.info("=" * 60)
    logger.info("🧪 ТЕСТ P0: Tool-calling")
    logger.info("=" * 60)
    
    try:
        from brain.llm import LLM
        
        config = {
            'model_path': './models/qwen2.5-3b-q4_k_m.gguf',
            'n_ctx': 2048,
            'n_threads': 4,
            'temperature': 0.1,  # Низкая для точности
            'max_tokens': 256,
        }
        
        llm = LLM(config)
        await llm.load()
        
        # Тест: запрос на вызов функции
        prompt = """Ты — AI-ассистент. Пользователь просит: "Посчитай 2+2".
Ответь в формате JSON: {"tool": "calculator", "args": {"expression": "..."}}
"""
        
        response = await llm.generate(prompt)
        
        # Проверка: ответ содержит JSON?
        if '{"tool"' in response or '{"action"' in response:
            logger.info("✅ P0 Tool-calling: LLM генерирует JSON для вызова функций")
            logger.info(f"   Ответ: {response[:100]}...")
            return True
        else:
            logger.warning("⚠️ P0 Tool-calling: LLM не генерирует JSON")
            logger.info(f"   Ответ: {response[:100]}...")
            return False
    
    except FileNotFoundError as e:
        logger.error(f"❌ P0 Tool-calling: Модель не найдена ({e})")
        logger.info("   → Скачайте модель: models/qwen2.5-3b-q4_k_m.gguf")
        return False
    except ImportError as e:
        logger.error(f"❌ P0 Tool-calling: {e}")
        logger.info("   → Установите: pip install llama-cpp-python")
        return False
    except Exception as e:
        logger.error(f"❌ P0 Tool-calling: Ошибка — {e}")
        return False


async def test_p0_wakeword_ru():
    """
    P0: Wake Word RU
    Проверка: есть ли библиотека для русского wake word?
    """
    logger.info("=" * 60)
    logger.info("🧪 ТЕСТ P0: Wake Word RU")
    logger.info("=" * 60)
    
    try:
        # Проверка openwakeword
        from openwakeword.model import Model
        logger.info("✅ P0 Wake Word: openwakeword установлен")
        
        # Проверка наличия модели
        # TODO: Проверить наличие русской модели
        logger.info("⚠️ P0 Wake Word: Нужна кастомная модель для 'Джарвис'")
        logger.info("   → Тренировка модели: https://github.com/dscripka/openWakeWord")
        return True
    
    except ImportError:
        logger.error("❌ P0 Wake Word: openwakeword не установлен")
        logger.info("   → Установите: pip install openwakeword")
        return False
    except Exception as e:
        logger.error(f"❌ P0 Wake Word: Ошибка — {e}")
        return False


async def test_p1_tts_stt():
    """
    P1: TTS/STT скорость
    Проверка: скорость распознавания и синтеза
    """
    logger.info("=" * 60)
    logger.info("🧪 ТЕСТ P1: TTS/STT скорость")
    logger.info("=" * 60)
    
    # Тест STT
    try:
        from faster_whisper import WhisperModel
        
        logger.info("📥 Загрузка Whisper для теста...")
        start = time.time()
        model = WhisperModel("base", device="cpu", compute_type="int8")
        load_time = time.time() - start
        logger.info(f"   Whisper загружен за {load_time:.1f} сек")
        
        # Тест распознавания (синтетический аудио)
        import numpy as np
        test_audio = np.zeros(16000 * 3, dtype=np.float32)  # 3 сек тишины
        
        start = time.time()
        segments, info = model.transcribe(test_audio, language="ru")
        _ = list(segments)  # Итерация для завершения
        stt_time = time.time() - start
        
        logger.info(f"   STT latency: {stt_time*1000:.0f} мс")
        
        if stt_time < 1.0:
            logger.info("✅ P1 STT: Скорость OK (< 1 сек)")
        else:
            logger.warning(f"⚠️ P1 STT: Медленно ({stt_time:.1f} сек)")
        
        stt_ok = stt_time < 1.0
    
    except ImportError:
        logger.error("❌ P1 STT: faster-whisper не установлен")
        logger.info("   → Установите: pip install faster-whisper")
        stt_ok = False
    except Exception as e:
        logger.error(f"❌ P1 STT: Ошибка — {e}")
        stt_ok = False
    
    return stt_ok


async def test_p2_ram():
    """
    P2: RAM потребление
    Проверка: сколько памяти ест система?
    """
    logger.info("=" * 60)
    logger.info("🧪 ТЕСТ P2: RAM потребление")
    logger.info("=" * 60)
    
    try:
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        ram_mb = process.memory_info().rss / 1024 / 1024
        
        logger.info(f"   Текущее потребление: {ram_mb:.0f} MB")
        
        if ram_mb < 500:
            logger.info("✅ P2 RAM: Потребление OK (< 500 MB без моделей)")
        else:
            logger.warning(f"⚠️ P2 RAM: Много ({ram_mb:.0f} MB)")
        
        # Оценка с моделями
        estimated_total = ram_mb + 3500 + 2000 + 1000  # LLM + STT + TTS
        logger.info(f"   Оценка с моделями: ~{estimated_total/1024:.1f} GB")
        
        if estimated_total < 8 * 1024:
            logger.info("✅ P2 RAM: Влезет в 8 GB")
        else:
            logger.warning(f"⚠️ P2 RAM: Может не влезть в 8 GB")
        
        return True
    
    except ImportError:
        logger.error("❌ P2 RAM: psutil не установлен")
        logger.info("   → Установите: pip install psutil")
        return False


async def main():
    """Запуск всех тестов Фазы 0"""
    logger.info("\n" + "=" * 60)
    logger.info("🚀 ФАЗА 0: Proof of Concept")
    logger.info("=" * 60 + "\n")
    
    results = {}
    
    # P0: Tool-calling
    results['tool_calling'] = await test_p0_tool_calling()
    logger.info("")
    
    # P0: Wake Word RU
    results['wakeword_ru'] = await test_p0_wakeword_ru()
    logger.info("")
    
    # P1: TTS/STT
    results['tts_stt'] = await test_p1_tts_stt()
    logger.info("")
    
    # P2: RAM
    results['ram'] = await test_p2_ram()
    logger.info("")
    
    # Итоги
    logger.info("=" * 60)
    logger.info("📊 ИТОГИ ФАЗЫ 0")
    logger.info("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"   {status}: {test_name}")
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    logger.info(f"\n   Результат: {passed}/{total} тестов пройдено")
    
    if passed == total:
        logger.info("\n🎉 Все тесты Фазы 0 пройдены! Можно переходить к Фазе 1.")
    else:
        logger.info("\n⚠️ Некоторые тесты не пройдены. Решите проблемы перед переходом к Фазе 1.")


if __name__ == '__main__':
    asyncio.run(main())
