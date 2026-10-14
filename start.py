#!/usr/bin/env python3
"""
Универсальный скрипт запуска Джарвис AI
Работает на Windows, Linux и macOS
"""
import os
import sys
import subprocess
import platform
from pathlib import Path


def print_banner():
    """Вывод баннера"""
    print()
    print("=" * 50)
    print("  🤖 Джарвис AI - Запуск...")
    print("=" * 50)
    print()


def check_python():
    """Проверка Python"""
    try:
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 11):
            print(f"❌ Требуется Python 3.11+, у вас {version.major}.{version.minor}")
            return False
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} найден")
        return True
    except Exception as e:
        print(f"❌ Ошибка проверки Python: {e}")
        return False


def check_node():
    """Проверка Node.js"""
    try:
        result = subprocess.run(
            ["node", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        version = result.stdout.strip()
        print(f"✅ Node.js {version} найден")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Node.js не найден! Установите Node.js 18+")
        return False


def install_python_deps():
    """Установка Python зависимостей"""
    print("📦 Установка Python зависимостей...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-q", "-r", "requirements-backend.txt"],
            check=True
        )
        print("✅ Python зависимости установлены")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Ошибка установки Python зависимостей: {e}")
        return False


def install_node_deps():
    """Установка Node зависимостей"""
    print("📦 Установка Node зависимостей...")
    try:
        npm_cmd = "npm.cmd" if platform.system() == "Windows" else "npm"
        subprocess.run(
            [npm_cmd, "install", "--silent"],
            check=True,
            shell=(platform.system() == "Windows")
        )
        print("✅ Node зависимости установлены")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Ошибка установки Node зависимостей: {e}")
        return False


def build_frontend():
    """Сборка frontend"""
    print("🔨 Сборка frontend...")
    try:
        npm_cmd = "npm.cmd" if platform.system() == "Windows" else "npm"
        subprocess.run(
            [npm_cmd, "run", "build"],
            check=True,
            shell=(platform.system() == "Windows")
        )
        print("✅ Frontend собран")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка сборки frontend: {e}")
        return False


def run_server():
    """Запуск сервера"""
    print()
    print("✅ Сборка завершена")
    print()
    print("🚀 Запуск сервера...")
    print("   Frontend: http://localhost:8000")
    print("   API: http://localhost:8000/api")
    print("   WebSocket: ws://localhost:8000/ws")
    print()
    print("Нажмите Ctrl+C для остановки")
    print("=" * 50)
    print()
    
    try:
        subprocess.run(
            [sys.executable, "server.py"],
            check=True
        )
    except KeyboardInterrupt:
        print("\n\n🛑 Сервер остановлен")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Ошибка запуска сервера: {e}")
        return False
    
    return True


def main():
    """Главная функция"""
    print_banner()
    
    # Проверка зависимостей
    if not check_python():
        sys.exit(1)
    
    if not check_node():
        sys.exit(1)
    
    print()
    
    # Установка зависимостей
    install_python_deps()
    install_node_deps()
    
    # Сборка frontend
    if not build_frontend():
        sys.exit(1)
    
    # Запуск сервера
    if not run_server():
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        sys.exit(1)
