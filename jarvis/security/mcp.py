"""
MCP Server — Model Context Protocol
Управление инструментами для AI-ассистента
"""
import asyncio
import logging
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class ToolRisk(Enum):
    """Уровень риска инструмента"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Tool:
    """Представление инструмента"""
    name: str
    description: str
    scope: str
    risk: ToolRisk
    requires_confirmation: bool
    handler: Callable
    parameters: Dict[str, Any]
    
    def __repr__(self):
        return f"Tool(name={self.name}, scope={self.scope}, risk={self.risk.value})"


class MCPServer:
    """
    Model Context Protocol Server
    Управление инструментами для AI-ассистента
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.tools: Dict[str, Tool] = {}
        self._registered = False
        
        logger.info("MCPServer инициализирован")
    
    def register_tool(
        self,
        name: str,
        description: str,
        scope: str,
        risk: ToolRisk,
        requires_confirmation: bool,
        handler: Callable,
        parameters: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Регистрация инструмента
        
        Args:
            name: Название инструмента
            description: Описание
            scope: Область действия (math, web, files, system, network)
            risk: Уровень риска (low, medium, high)
            requires_confirmation: Требуется ли подтверждение пользователя
            handler: Функция-обработчик
            parameters: Параметры инструмента
        """
        tool = Tool(
            name=name,
            description=description,
            scope=scope,
            risk=risk,
            requires_confirmation=requires_confirmation,
            handler=handler,
            parameters=parameters or {}
        )
        
        self.tools[name] = tool
        logger.info(f"✅ Зарегистрирован инструмент: {name} (scope={scope}, risk={risk.value})")
    
    async def execute_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
        user_confirmed: bool = False
    ) -> Dict[str, Any]:
        """
        Выполнение инструмента
        
        Args:
            tool_name: Название инструмента
            arguments: Аргументы
            user_confirmed: Подтверждено ли пользователем
        
        Returns:
            Результат выполнения
        """
        if tool_name not in self.tools:
            logger.error(f"❌ Инструмент не найден: {tool_name}")
            return {
                'success': False,
                'error': f'Инструмент "{tool_name}" не найден'
            }
        
        tool = self.tools[tool_name]
        
        # Проверка подтверждения для инструментов с высоким риском
        if tool.requires_confirmation and not user_confirmed:
            logger.warning(f"⚠️ Требуется подтверждение для инструмента: {tool_name}")
            return {
                'success': False,
                'requires_confirmation': True,
                'message': f'Инструмент "{tool_name}" требует подтверждения пользователя'
            }
        
        try:
            logger.info(f"🔧 Выполнение инструмента: {tool_name}")
            
            # Выполнение handler
            if asyncio.iscoroutinefunction(tool.handler):
                result = await tool.handler(**arguments)
            else:
                result = tool.handler(**arguments)
            
            logger.info(f"✅ Инструмент выполнен успешно: {tool_name}")
            
            return {
                'success': True,
                'result': result,
                'tool': tool_name
            }
        
        except Exception as e:
            logger.error(f"❌ Ошибка выполнения инструмента {tool_name}: {e}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
                'tool': tool_name
            }
    
    def get_tool(self, tool_name: str) -> Optional[Tool]:
        """Получение инструмента по имени"""
        return self.tools.get(tool_name)
    
    def list_tools(self) -> List[Tool]:
        """Список всех зарегистрированных инструментов"""
        return list(self.tools.values())
    
    def get_tools_by_scope(self, scope: str) -> List[Tool]:
        """Получение инструментов по области действия"""
        return [tool for tool in self.tools.values() if tool.scope == scope]
    
    def get_tools_by_risk(self, risk: ToolRisk) -> List[Tool]:
        """Получение инструментов по уровню риска"""
        return [tool for tool in self.tools.values() if tool.risk == risk]
    
    # Встроенные инструменты
    
    def register_builtin_tools(self) -> None:
        """Регистрация встроенных инструментов"""
        
        # Калькулятор
        self.register_tool(
            name="calculator",
            description="Математические вычисления",
            scope="math",
            risk=ToolRisk.LOW,
            requires_confirmation=False,
            handler=self._tool_calculator,
            parameters={"expression": "Математическое выражение"}
        )
        
        # Поиск в интернете
        self.register_tool(
            name="web_search",
            description="Поиск информации в интернете",
            scope="web",
            risk=ToolRisk.LOW,
            requires_confirmation=False,
            handler=self._tool_web_search,
            parameters={"query": "Поисковый запрос"}
        )
        
        # Чтение файла
        self.register_tool(
            name="read_file",
            description="Чтение содержимого файла",
            scope="files.local",
            risk=ToolRisk.LOW,
            requires_confirmation=False,
            handler=self._tool_read_file,
            parameters={"path": "Путь к файлу"}
        )
        
        # Запись файла
        self.register_tool(
            name="write_file",
            description="Запись в файл",
            scope="files.local",
            risk=ToolRisk.MEDIUM,
            requires_confirmation=True,
            handler=self._tool_write_file,
            parameters={"path": "Путь к файлу", "content": "Содержимое"}
        )
        
        # Удаление файла
        self.register_tool(
            name="delete_file",
            description="Удаление файла",
            scope="files.dangerous",
            risk=ToolRisk.HIGH,
            requires_confirmation=True,
            handler=self._tool_delete_file,
            parameters={"path": "Путь к файлу"}
        )
        
        # Открытие приложения
        self.register_tool(
            name="open_app",
            description="Открытие приложения",
            scope="system.apps",
            risk=ToolRisk.MEDIUM,
            requires_confirmation=True,
            handler=self._tool_open_app,
            parameters={"app_name": "Название приложения"}
        )
        
        # Системная команда
        self.register_tool(
            name="system_command",
            description="Выполнение системной команды",
            scope="system.dangerous",
            risk=ToolRisk.HIGH,
            requires_confirmation=True,
            handler=self._tool_system_command,
            parameters={"command": "Системная команда"}
        )
        
        # Отправка email
        self.register_tool(
            name="send_email",
            description="Отправка email",
            scope="network.email",
            risk=ToolRisk.HIGH,
            requires_confirmation=True,
            handler=self._tool_send_email,
            parameters={"to": "Получатель", "subject": "Тема", "body": "Текст"}
        )
        
        logger.info(f"✅ Зарегистрировано {len(self.tools)} встроенных инструментов")
    
    # Реализации встроенных инструментов
    
    async def _tool_calculator(self, expression: str) -> Dict[str, Any]:
        """Калькулятор"""
        try:
            # Безопасная оценка выражения
            allowed_names = {"abs": abs, "round": round, "min": min, "max": max}
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            return {"result": result}
        except Exception as e:
            return {"error": str(e)}
    
    async def _tool_web_search(self, query: str) -> Dict[str, Any]:
        """Поиск в интернете (заглушка)"""
        # TODO: Реализовать реальный поиск
        return {
            "results": [
                {"title": f"Результат 1 для '{query}'", "url": "https://example.com/1"},
                {"title": f"Результат 2 для '{query}'", "url": "https://example.com/2"},
            ]
        }
    
    async def _tool_read_file(self, path: str) -> Dict[str, Any]:
        """Чтение файла"""
        try:
            from pathlib import Path
            file_path = Path(path)
            if not file_path.exists():
                return {"error": f"Файл не найден: {path}"}
            content = file_path.read_text(encoding='utf-8')
            return {"content": content, "size": len(content)}
        except Exception as e:
            return {"error": str(e)}
    
    async def _tool_write_file(self, path: str, content: str) -> Dict[str, Any]:
        """Запись в файл"""
        try:
            from pathlib import Path
            file_path = Path(path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding='utf-8')
            return {"success": True, "path": str(file_path)}
        except Exception as e:
            return {"error": str(e)}
    
    async def _tool_delete_file(self, path: str) -> Dict[str, Any]:
        """Удаление файла"""
        try:
            from pathlib import Path
            file_path = Path(path)
            if not file_path.exists():
                return {"error": f"Файл не найден: {path}"}
            file_path.unlink()
            return {"success": True, "deleted": str(file_path)}
        except Exception as e:
            return {"error": str(e)}
    
    async def _tool_open_app(self, app_name: str) -> Dict[str, Any]:
        """Открытие приложения (заглушка)"""
        # TODO: Реализовать открытие приложений
        return {"success": True, "app": app_name, "status": "opened"}
    
    async def _tool_system_command(self, command: str) -> Dict[str, Any]:
        """Выполнение системной команды (заглушка)"""
        # TODO: Реализовать с whitelist команд
        return {"success": False, "error": "Системные команды временно отключены"}
    
    async def _tool_send_email(self, to: str, subject: str, body: str) -> Dict[str, Any]:
        """Отправка email (заглушка)"""
        # TODO: Реализовать отправку email
        return {"success": True, "to": to, "subject": subject, "status": "sent"}
