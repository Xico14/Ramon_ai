"""
Проверка структуры проекта Джарвис
Убеждается, что все необходимые файлы и директории на месте
"""
import sys
from pathlib import Path


def check_structure():
    """Проверка структуры проекта"""
    
    print("=" * 60)
    print("🔍 ПРОВЕРКА СТРУКТУРЫ ПРОЕКТА")
    print("=" * 60)
    
    # Директории
    directories = [
        'logs',
        'data',
        'models',
        'documents',
        'core',
        'brain',
        'audio',
        'ui',
        'scripts',
        'grammars',
    ]
    
    print("\n📁 Проверка директорий:")
    for dir_name in directories:
        path = Path(dir_name)
        if path.exists() and path.is_dir():
            print(f"  ✅ {dir_name}/")
        else:
            print(f"  ❌ {dir_name}/ — отсутствует")
            path.mkdir(parents=True, exist_ok=True)
            print(f"     → Создано автоматически")
    
    # Файлы
    files = [
        ('main.py', 'Точка входа'),
        ('config.yaml', 'Конфигурация'),
        ('requirements.txt', 'Зависимости'),
        ('README.md', 'Документация'),
        ('core/__init__.py', 'Core package'),
        ('core/event_bus.py', 'Event Bus'),
        ('core/fsm.py', 'FSM'),
        ('core/orchestrator.py', 'Orchestrator'),
        ('core/config.py', 'Config loader'),
        ('brain/__init__.py', 'Brain package'),
        ('brain/llm.py', 'LLM'),
        ('audio/__init__.py', 'Audio package'),
        ('audio/capture.py', 'Audio Capture'),
        ('audio/vad.py', 'VAD'),
        ('audio/stt.py', 'STT'),
        ('audio/tts.py', 'TTS'),
        ('audio/wake_word.py', 'Wake Word'),
        ('ui/__init__.py', 'UI package'),
        ('ui/main_window.py', 'Main Window'),
        ('grammars/response.gbnf', 'GBNF Grammar'),
        ('scripts/test_phase0.py', 'Тесты Фазы 0'),
        ('scripts/demo.py', 'Демо-режим'),
    ]
    
    print("\n📄 Проверка файлов:")
    missing_files = []
    for file_name, description in files:
        path = Path(file_name)
        if path.exists() and path.is_file():
            print(f"  ✅ {file_name:30} — {description}")
        else:
            print(f"  ❌ {file_name:30} — ОТСУТСТВУЕТ")
            missing_files.append(file_name)
    
    # Модели
    print("\n🧠 Проверка моделей:")
    model_path = Path('models/qwen2.5-3b-q4_k_m.gguf')
    if model_path.exists():
        size_gb = model_path.stat().st_size / (1024 ** 3)
        print(f"  ✅ qwen2.5-3b-q4_k_m.gguf ({size_gb:.2f} GB)")
    else:
        print(f"  ❌ qwen2.5-3b-q4_k_m.gguf — ОТСУТСТВУЕТ")
        print(f"     → Скачайте модель:")
        print(f"       curl -L -o models/qwen2.5-3b-q4_k_m.gguf \\")
        print(f"         https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF/resolve/main/qwen2.5-3b-instruct-q4_k_m.gguf")
    
    # Итоги
    print("\n" + "=" * 60)
    if missing_files:
        print(f"⚠️  Отсутствует {len(missing_files)} файл(ов)")
        print("\nВозможные причины:")
        print("  1. Файлы не были созданы")
        print("  2. Неправильная структура проекта")
        print("  3. Файлы удалены")
    else:
        print("✅ Все файлы на месте!")
        
        if not model_path.exists():
            print("\n⚠️  Не хватает только модели LLM")
            print("   Скачайте её перед запуском")
        else:
            print("\n🚀 Проект готов к запуску!")
            print("   python main.py")
    
    print("=" * 60)
    
    return len(missing_files) == 0


def check_dependencies():
    """Проверка установленных зависимостей"""
    
    print("\n" + "=" * 60)
    print("📦 ПРОВЕРКА ЗАВИСИМОСТЕЙ")
    print("=" * 60)
    
    dependencies = [
        ('pydantic', 'Core'),
        ('yaml', 'Core'),
        ('psutil', 'Core'),
        ('aiosqlite', 'Database'),
        ('numpy', 'Audio'),
        ('PyQt6', 'UI'),
        ('qasync', 'UI'),
        ('faster_whisper', 'STT'),
        ('llama_cpp', 'LLM'),
        ('openwakeword', 'Wake Word'),
    ]
    
    print("\nПроверка пакетов:")
    missing = []
    
    for package, category in dependencies:
        try:
            __import__(package)
            print(f"  ✅ {package:20} — {category}")
        except ImportError:
            print(f"  ❌ {package:20} — НЕ УСТАНОВЛЕН")
            missing.append(package)
    
    print("\n" + "=" * 60)
    if missing:
        print(f"⚠️  Отсутствует {len(missing)} пакет(ов)")
        print("\nУстановите:")
        print("  pip install -r requirements.txt")
    else:
        print("✅ Все зависимости установлены!")
    print("=" * 60)
    
    return len(missing) == 0


if __name__ == '__main__':
    structure_ok = check_structure()
    deps_ok = check_dependencies()
    
    print("\n" + "=" * 60)
    print("📊 ИТОГОВАЯ ПРОВЕРКА")
    print("=" * 60)
    
    if structure_ok and deps_ok:
        print("✅ Проект готов к запуску!")
        print("\nСледующие шаги:")
        print("  1. python scripts/demo.py  — демо-режим")
        print("  2. python main.py          — полный режим")
    else:
        print("⚠️  Есть проблемы, которые нужно решить")
        
        if not structure_ok:
            print("\n📁 Проблемы со структурой:")
            print("   Проверьте, что все файлы на месте")
        
        if not deps_ok:
            print("\n📦 Проблемы с зависимостями:")
            print("   pip install -r requirements.txt")
    
    print("=" * 60)
