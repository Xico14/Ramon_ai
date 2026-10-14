@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   🤖 Джарвис AI - Запуск...
echo ========================================
echo.

REM Проверка Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден! Установите Python 3.11+
    pause
    exit /b 1
)

REM Проверка Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js не найден! Установите Node.js 18+
    pause
    exit /b 1
)

echo ✅ Python и Node.js найдены
echo.

REM Установка Python зависимостей
echo 📦 Установка Python зависимостей...
pip install -q -r requirements-backend.txt
if errorlevel 1 (
    echo ⚠️  Ошибка установки Python зависимостей
)

REM Установка Node зависимостей
echo 📦 Установка Node зависимостей...
call npm install --silent
if errorlevel 1 (
    echo ⚠️  Ошибка установки Node зависимостей
)

REM Сборка frontend
echo 🔨 Сборка frontend...
call npm run build
if errorlevel 1 (
    echo ❌ Ошибка сборки frontend
    pause
    exit /b 1
)

echo.
echo ✅ Сборка завершена
echo.
echo 🚀 Запуск сервера...
echo    Frontend: http://localhost:8000
echo    API: http://localhost:8000/api
echo    WebSocket: ws://localhost:8000/ws
echo.
echo Нажмите Ctrl+C для остановки
echo ========================================
echo.

REM Запуск сервера
python server.py

pause
