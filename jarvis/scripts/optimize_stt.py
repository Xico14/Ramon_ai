"""
Оптимизация STT для ускорения распознавания
"""
import asyncio
import time
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def test_stt_optimization():
    """Тест различных оптимизаций STT"""
    
    logger.info("=" * 60)
    logger.info("🚀 ОПТИМИЗАЦИЯ STT")
    logger.info("=" * 60)
    
    import numpy as np
    from faster_whisper import WhisperModel
    
    # Тестовое аудио (3 секунды тишины)
    test_audio = np.zeros(16000 * 3, dtype=np.float32)
    
    # Тестируем разные модели
    models_to_test = [
        ("tiny", "int8", "Самая быстрая, низкое качество"),
        ("base", "int8", "Базовая (текущая)"),
        ("small", "int8", "Хороший баланс"),
    ]
    
    results = []
    
    for model_size, compute_type, description in models_to_test:
        logger.info(f"\n📊 Тестирование модели: {model_size} ({compute_type})")
        logger.info(f"   {description}")
        
        try:
            # Загрузка модели
            start = time.time()
            model = WhisperModel(model_size, device="cpu", compute_type=compute_type)
            load_time = time.time() - start
            logger.info(f"   Загрузка: {load_time:.1f} сек")
            
            # Тест распознавания
            start = time.time()
            segments, info = model.transcribe(
                test_audio,
                language="ru",
                beam_size=1,  # Уменьшаем для скорости
                vad_filter=True,
                vad_parameters=dict(min_silence_duration_ms=500),
            )
            _ = list(segments)
            latency = time.time() - start
            
            logger.info(f"   Latency: {latency*1000:.0f} мс")
            
            results.append({
                'model': model_size,
                'compute_type': compute_type,
                'latency_ms': latency * 1000,
                'load_time': load_time,
                'description': description,
            })
            
            # Освобождаем память
            del model
            
        except Exception as e:
            logger.error(f"   Ошибка: {e}")
    
    # Итоги
    logger.info("\n" + "=" * 60)
    logger.info("📊 РЕЗУЛЬТАТЫ ОПТИМИЗАЦИИ")
    logger.info("=" * 60)
    
    for result in results:
        status = "✅" if result['latency_ms'] < 1000 else "⚠️"
        logger.info(f"{status} {result['model']:8} | {result['latency_ms']:6.0f} мс | {result['description']}")
    
    # Рекомендация
    fastest = min(results, key=lambda x: x['latency_ms'])
    logger.info(f"\n💡 Рекомендация: используйте модель '{fastest['model']}'")
    logger.info(f"   Latency: {fastest['latency_ms']:.0f} мс")
    
    if fastest['latency_ms'] < 1000:
        logger.info("✅ Цель достигнута! Latency < 1000 мс")
    else:
        logger.info("⚠️  Попробуйте GPU для ускорения")
    
    return results


async def test_gpu_availability():
    """Проверка доступности GPU"""
    
    logger.info("\n" + "=" * 60)
    logger.info("🎮 ПРОВЕРКА GPU")
    logger.info("=" * 60)
    
    try:
        import torch
        
        if torch.cuda.is_available():
            logger.info("✅ CUDA доступна!")
            logger.info(f"   GPU: {torch.cuda.get_device_name(0)}")
            logger.info(f"   Память: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
            
            # Тест с GPU
            logger.info("\n📊 Тест STT с GPU...")
            from faster_whisper import WhisperModel
            import numpy as np
            
            test_audio = np.zeros(16000 * 3, dtype=np.float32)
            
            start = time.time()
            model = WhisperModel("base", device="cuda", compute_type="float16")
            segments, info = model.transcribe(test_audio, language="ru", beam_size=5)
            _ = list(segments)
            latency = time.time() - start
            
            logger.info(f"   GPU Latency: {latency*1000:.0f} мс")
            
            if latency * 1000 < 500:
                logger.info("✅ GPU значительно быстрее! Используйте GPU.")
            
        else:
            logger.info("❌ CUDA недоступна")
            logger.info("   Используется CPU")
            logger.info("\n💡 Для ускорения:")
            logger.info("   1. Установите NVIDIA GPU с CUDA")
            logger.info("   2. Установите CUDA Toolkit: https://developer.nvidia.com/cuda-downloads")
            logger.info("   3. Переустановите llama-cpp-python с поддержкой CUDA:")
            logger.info("      pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121")
    
    except ImportError:
        logger.info("❌ PyTorch не установлен")
        logger.info("   Установите: pip install torch")


async def main():
    """Главная функция"""
    
    # Тест оптимизаций
    await test_stt_optimization()
    
    # Проверка GPU
    await test_gpu_availability()
    
    logger.info("\n" + "=" * 60)
    logger.info("📝 РЕКОМЕНДАЦИИ")
    logger.info("=" * 60)
    logger.info("\n1. Для быстрого старта:")
    logger.info("   - Используйте модель 'tiny' (самая быстрая)")
    logger.info("   - Уменьшите beam_size до 1")
    logger.info("   - Включите VAD filter")
    
    logger.info("\n2. Для лучшего качества:")
    logger.info("   - Используйте модель 'small' или 'base'")
    logger.info("   - Увеличьте beam_size до 5")
    logger.info("   - Используйте GPU если доступен")
    
    logger.info("\n3. Обновите config.yaml:")
    logger.info("   stt:")
    logger.info("     model_size: 'tiny'  # или 'base', 'small'")
    logger.info("     beam_size: 1  # для скорости")
    logger.info("     device: 'cpu'  # или 'cuda' для GPU")


if __name__ == '__main__':
    asyncio.run(main())
