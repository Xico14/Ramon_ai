"""
FastAPI Backend Server для Джарвис AI
Обслуживает frontend и предоставляет API
"""
import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Добавляем путь к jarvis модулям
sys.path.insert(0, str(Path(__file__).parent / 'jarvis'))

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Создание FastAPI приложения
app = FastAPI(
    title="Джарвис AI Backend",
    description="Backend API для AI-ассистента Джарвис",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модели данных
class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None

class DocumentUpload(BaseModel):
    title: str
    content: str
    format: str

class ToolExecution(BaseModel):
    tool_id: str
    arguments: dict

# Глобальное состояние
class AppState:
    def __init__(self):
        self.fsm_state = "IDLE"
        self.messages = []
        self.documents = []
        self.metrics = {
            "cpu": 15.0,
            "ram": 234.0,
            "ram_total": 8192.0,
            "events_published": 0,
            "events_delivered": 0,
            "events_failed": 0,
            "uptime": 0,
        }
        self.websocket_connections = []
        
    def add_message(self, role: str, content: str):
        message = {
            "id": str(len(self.messages) + 1),
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.messages.append(message)
        return message
    
    def update_metrics(self):
        import random
        self.metrics["cpu"] = max(5, min(95, self.metrics["cpu"] + random.uniform(-5, 5)))
        self.metrics["ram"] = max(200, min(800, self.metrics["ram"] + random.uniform(-10, 10)))
        self.metrics["events_published"] += random.randint(0, 5)
        self.metrics["events_delivered"] += random.randint(0, 5)
        self.metrics["uptime"] += 1

state = AppState()

# Mock LLM для демонстрации
async def mock_llm_response(message: str) -> str:
    """Имитация ответа от LLM"""
    await asyncio.sleep(1.5)  # Имитация задержки
    
    message_lower = message.lower()
    
    if "привет" in message_lower or "здравствуй" in message_lower:
        return "Привет! Я Джарвис, ваш AI-ассистент. Чем могу помочь?"
    
    if "как дела" in message_lower:
        return "У меня всё отлично! Все системы работают нормально. А у вас?"
    
    if "что ты умеешь" in message_lower or "возможности" in message_lower:
        return "Я умею:\n- Отвечать на вопросы\n- Искать информацию в документах\n- Выполнять математические вычисления\n- Управлять файлами\n- Отвечать на голосовые команды"
    
    if "время" in message_lower or "час" in message_lower:
        now = datetime.now()
        return f"Сейчас {now.strftime('%H:%M')}"
    
    if "дата" in message_lower or "сегодня" in message_lower:
        now = datetime.now()
        return f"Сегодня {now.strftime('%d.%m.%Y')}"
    
    if "посчитай" in message_lower or "сколько" in message_lower:
        import re
        match = re.search(r'(\d+)\s*([+\-*/])\s*(\d+)', message)
        if match:
            num1 = float(match.group(1))
            op = match.group(2)
            num2 = float(match.group(3))
            
            if op == '+': result = num1 + num2
            elif op == '-': result = num1 - num2
            elif op == '*': result = num1 * num2
            elif op == '/': result = num1 / num2 if num2 != 0 else 0
            else: result = 0
            
            return f"{int(num1)} {op} {int(num2)} = {int(result)}"
        return "Не смог распознать математическое выражение"
    
    return "Понял ваш вопрос. В полной версии я использую нейросеть Qwen2.5-3B для генерации ответов и могу искать информацию в ваших документах."

# API Endpoints

@app.get("/")
async def root():
    """Главная страница - обслуживает frontend"""
    index_path = Path(__file__).parent / "dist" / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return JSONResponse({"message": "Frontend not built. Run 'npm run build' first."})

@app.get("/api/health")
async def health_check():
    """Проверка здоровья сервера"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.get("/api/metrics")
async def get_metrics():
    """Получение системных метрик"""
    state.update_metrics()
    return state.metrics

@app.get("/api/fsm")
async def get_fsm_state():
    """Получение состояния FSM"""
    return {"state": state.fsm_state}

@app.post("/api/chat")
async def chat(message: ChatMessage):
    """Отправка сообщения в чат"""
    try:
        # Добавляем сообщение пользователя
        user_msg = state.add_message("user", message.message)
        
        # Изменяем состояние FSM
        state.fsm_state = "THINK"
        
        # Получаем ответ от LLM
        response = await mock_llm_response(message.message)
        
        # Добавляем ответ ассистента
        assistant_msg = state.add_message("assistant", response)
        
        # Возвращаем в IDLE
        state.fsm_state = "IDLE"
        
        return {
            "user_message": user_msg,
            "assistant_message": assistant_msg,
            "fsm_state": state.fsm_state
        }
    
    except Exception as e:
        logger.error(f"Error in chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/messages")
async def get_messages():
    """Получение истории сообщений"""
    return {"messages": state.messages}

@app.delete("/api/messages")
async def clear_messages():
    """Очистка истории сообщений"""
    state.messages.clear()
    return {"status": "cleared"}

@app.get("/api/documents")
async def get_documents():
    """Получение списка документов"""
    return {"documents": state.documents}

@app.post("/api/documents")
async def upload_document(doc: DocumentUpload):
    """Загрузка нового документа"""
    import random
    
    document = {
        "id": str(len(state.documents) + 1),
        "title": doc.title,
        "source": "upload",
        "format": doc.format,
        "size": len(doc.content) * 2,  # Примерный размер
        "chunks": random.randint(10, 50),
        "uploadedAt": datetime.now().isoformat()
    }
    
    state.documents.append(document)
    return document

@app.delete("/api/documents/{doc_id}")
async def delete_document(doc_id: str):
    """Удаление документа"""
    state.documents = [d for d in state.documents if d["id"] != doc_id]
    return {"status": "deleted"}

@app.get("/api/tools")
async def get_tools():
    """Получение списка инструментов"""
    tools = [
        {
            "id": "calculator",
            "name": "Калькулятор",
            "description": "Математические вычисления",
            "scope": "math",
            "risk": "low",
            "requiresConfirmation": False,
            "enabled": True,
            "usageCount": 0
        },
        {
            "id": "web_search",
            "name": "Поиск в интернете",
            "description": "Поиск информации в интернете",
            "scope": "web",
            "risk": "low",
            "requiresConfirmation": False,
            "enabled": True,
            "usageCount": 0
        },
        {
            "id": "read_file",
            "name": "Чтение файла",
            "description": "Чтение содержимого файла",
            "scope": "files.local",
            "risk": "low",
            "requiresConfirmation": False,
            "enabled": True,
            "usageCount": 0
        },
        {
            "id": "write_file",
            "name": "Запись файла",
            "description": "Запись в файл",
            "scope": "files.local",
            "risk": "medium",
            "requiresConfirmation": True,
            "enabled": True,
            "usageCount": 0
        },
        {
            "id": "delete_file",
            "name": "Удаление файла",
            "description": "Удаление файла",
            "scope": "files.dangerous",
            "risk": "high",
            "requiresConfirmation": True,
            "enabled": True,
            "usageCount": 0
        }
    ]
    return {"tools": tools}

@app.post("/api/tools/{tool_id}/execute")
async def execute_tool(tool_id: str, execution: ToolExecution):
    """Выполнение инструмента"""
    # Mock выполнение
    return {
        "status": "success",
        "result": f"Инструмент {tool_id} выполнен",
        "tool_id": tool_id
    }

@app.get("/api/logs")
async def get_logs():
    """Получение логов"""
    # Mock логи
    logs = [
        {
            "id": "1",
            "timestamp": datetime.now().isoformat(),
            "level": "info",
            "component": "system",
            "message": "Система запущена"
        },
        {
            "id": "2",
            "timestamp": datetime.now().isoformat(),
            "level": "info",
            "component": "chat",
            "message": "Чат инициализирован"
        }
    ]
    return {"logs": logs}

@app.get("/api/audit")
async def get_audit_log():
    """Получение аудит-лога"""
    return {"audit_log": []}

# WebSocket для real-time обновлений
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket для real-time обновлений"""
    await websocket.accept()
    state.websocket_connections.append(websocket)
    
    try:
        while True:
            # Отправка обновлений метрик каждые 2 секунды
            state.update_metrics()
            await websocket.send_json({
                "type": "metrics",
                "data": state.metrics
            })
            
            await asyncio.sleep(2)
    
    except WebSocketDisconnect:
        state.websocket_connections.remove(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        if websocket in state.websocket_connections:
            state.websocket_connections.remove(websocket)

# Обслуживание статических файлов frontend
if (Path(__file__).parent / "dist").exists():
    app.mount("/assets", StaticFiles(directory=Path(__file__).parent / "dist" / "assets"), name="assets")

# Catch-all route для SPA
@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    """Обслуживание SPA routes"""
    index_path = Path(__file__).parent / "dist" / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return JSONResponse({"error": "Frontend not built"}, status_code=404)

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.environ.get("PORT", 8000))
    
    logger.info(f"🚀 Запуск сервера на порту {port}")
    logger.info(f"📊 API: http://localhost:{port}/api")
    logger.info(f"🎨 Frontend: http://localhost:{port}")
    logger.info(f"🔌 WebSocket: ws://localhost:{port}/ws")
    
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
