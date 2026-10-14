#!/bin/bash

echo ""
echo "========================================"
echo "  🤖 Джарвис AI - Запуск..."
echo "========================================"
echo ""

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден! Установите Python 3.11+"
    exit 1
fi

# Проверка Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js не найден! Установите Node.js 18+"
    exit 1
fi

echo "✅ Python и Node.js найдены"
echo ""

# Установка Python зависимостей
echo "📦 Установка Python зависимостей..."
pip3 install -q -r requirements-backend.txt 2>/dev/null || pip install -q -r requirements-backend.txt

# Установка Node зависимостей
echo "📦 Установка Node зависимостей..."
npm install --silent

# Сборка frontend
echo "🔨 Сборка frontend..."
npm run build
if [ $? -ne 0 ]; then
    echo "❌ Ошибка сборки frontend"
    exit 1
fi

echo ""
echo "✅ Сборка завершена"
echo ""
echo "🚀 Запуск сервера..."
echo "   Frontend: http://localhost:8000"
echo "   API: http://localhost:8000/api"
echo "   WebSocket: ws://localhost:8000/ws"
echo ""
echo "Нажмите Ctrl+C для остановки"
echo "========================================"
echo ""

# Запуск сервера
python3 server.py
