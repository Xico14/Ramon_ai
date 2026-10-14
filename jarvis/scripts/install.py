"""
Скрипт установки зависимостей для Джарвиса
Поэтапная установка с обработкой ошибок
"""
import subprocess
import sys
import platform


def run_command(cmd, description):
    """Выполняет команду и выводит результат"""
    print(f"\n{'='*60}")
    print(f"📦 {description}")
    print(f"{'='*60}")
    print(f"Команда: {cmd}\n")
    
    result = subprocess.run(cmd, shell=True, capture_output=False)
    
    if result.returncode == 0:
        print(f"✅ Успешно: {description}")
        return True
    else:
        print(f"❌ Ошибка: {description}")
        return False


def install_step_by_step():
    """Поэтапная установка зависимостей"""
    
    print("\n" + "="*60)
    print("🤖 Установка зависимостей для Джарвиса")
    print("="*60)
    print(f"Python: {sys.version}")
    print(f"Платформа: {platform.system()} {platform.machine()}")
    print("="*60)
    
    steps = [
        # Шаг 1: Базовые зависимости
        (
            "pip install --upgrade pip setuptools wheel",
            "Обновление pip и инструментов сборки"
        ),
        
        # Шаг 2: Core зависимости
        (
            "pip install pydantic pyyaml psutil",
            "Core: pydantic, pyyaml, psutil"
        ),
        
        # Шаг 3: Database
        (
            "pip install aiosqlite",
            "Database: aiosqlite"
        ),
        
        # Шаг 4: NumPy (важно установить первым)
        (
            "pip install numpy",
            "Audio: numpy"
        ),
        
        # Шаг 5: PyAudio (на Windows может потребовать special wheel)
        (
            "pip install pyaudio",
            "Audio: pyaudio (может потребовать Visual C++ Build Tools на Windows)"
        ),
        
        # Шаг 6: UI
        (
            "pip install PyQt6 qasync",
            "UI: PyQt6, qasync"
        ),
        
        # Шаг 7: STT
        (
            "pip install faster-whisper",
            "STT: faster-whisper"
        ),
        
        # Шаг 8: LLM
        (
            "pip install llama-cpp-python",
            "LLM: llama-cpp-python (может компилироваться несколько минут)"
        ),
        
        # Шаг 9: Wake Word
        (
            "pip install openwakeword",
            "Wake Word: openwakeword"
        ),
        
        # Шаг 10: RAG (опционально, может быть тяжелым)
        (
            "pip install sentence-transformers rank-bm25",
            "RAG: sentence-transformers, rank-bm25 (опционально)"
        ),
        
        # Шаг 11: Security
        (
            "pip install cryptography",
            "Security: cryptography"
        ),
        
        # Шаг 12: Testing
        (
            "pip install pytest pytest-asyncio",
            "Testing: pytest, pytest-asyncio"
        ),
    ]
    
    results = []
    
    for cmd, description in steps:
        success = run_command(cmd, description)
        results.append((description, success))
        
        if not success:
            print(f"\n⚠️  Предупреждение: {description} не установлен")
            print("   Продолжаем установку остальных пакетов...\n")
    
    # Итоги
    print("\n" + "="*60)
    print("📊 ИТОГИ УСТАНОВКИ")
    print("="*60)
    
    for description, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {description}")
    
    success_count = sum(1 for _, s in results if s)
    total_count = len(results)
    
    print(f"\nРезультат: {success_count}/{total_count} пакетов установлено")
    
    if success_count == total_count:
        print("\n🎉 Все зависимости установлены успешно!")
        print("\nСледующие шаги:")
        print("1. Скачайте модель LLM:")
        print("   mkdir models")
        print("   curl -L -o models/qwen2.5-3b-q4_k_m.gguf https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF/resolve/main/qwen2.5-3b-instruct-q4_k_m.gguf")
        print("\n2. Запустите тесты:")
        print("   python scripts/test_phase0.py")
        print("\n3. Запустите Джарвиса:")
        print("   python main.py")
    else:
        print("\n⚠️  Некоторые пакеты не установлены.")
        print("\nРешение проблем:")
        print("\n1. PyAudio на Windows:")
        print("   - Установите Visual C++ Build Tools:")
        print("     https://visualstudio.microsoft.com/visual-cpp-build-tools/")
        print("   - Или скачайте pre-compiled wheel:")
        print("     https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio")
        print("   - Установите: pip install PyAudio-X.XX-cp3XX-cp3XX-win_amd64.whl")
        
        print("\n2. llama-cpp-python:")
        print("   - Может требовать компиляции (5-10 минут)")
        print("   - Убедитесь, что установлен C++ компилятор")
        print("   - Для GPU: pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121")
        
        print("\n3. sentence-transformers:")
        print("   - Тяжелый пакет (~2 GB с моделями)")
        print("   - Можно пропустить, если не нужен RAG")
    
    return success_count == total_count


if __name__ == "__main__":
    success = install_step_by_step()
    sys.exit(0 if success else 1)
