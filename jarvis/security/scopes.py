"""
Scope Manager — Управление разрешениями
Контроль доступа к инструментам по областям действия
"""
import asyncio
import logging
import json
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class AuditEntry:
    """Запись в аудит-логе"""
    timestamp: str
    tool_name: str
    scope: str
    risk: str
    user_confirmed: bool
    success: bool
    error: Optional[str] = None
    arguments: Optional[Dict] = None


class ScopeManager:
    """
    Менеджер разрешений
    Контролирует доступ к инструментам по областям действия
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.scopes: Dict[str, str] = config.get('scopes', {})
        
        # Уровни доступа
        self.ACCESS_LEVELS = {
            'unrestricted': 0,      # Без ограничений
            'restricted': 1,        # Ограниченный доступ
            'confirmation_required': 2,  # Требуется подтверждение
            'double_confirmation': 3,    # Двойное подтверждение
            'whitelist_only': 4,    # Только из whitelist
            'always_confirmation': 5,    # Всегда подтверждение
            'blocked': 6            # Заблокировано
        }
        
        logger.info(f"ScopeManager инициализирован ({len(self.scopes)} областей)")
    
    def check_access(self, scope: str) -> bool:
        """
        Проверка доступа к области действия
        
        Args:
            scope: Область действия (math, web, files.local, и т.д.)
        
        Returns:
            True если доступ разрешен
        """
        if scope not in self.scopes:
            logger.warning(f"⚠️ Неизвестная область действия: {scope}")
            return False
        
        access_level = self.scopes[scope]
        
        if access_level == 'blocked':
            logger.warning(f"🚫 Доступ заблокирован для области: {scope}")
            return False
        
        return True
    
    def requires_confirmation(self, scope: str) -> bool:
        """
        Проверка, требуется ли подтверждение для области
        
        Args:
            scope: Область действия
        
        Returns:
            True если требуется подтверждение
        """
        if scope not in self.scopes:
            return True  # По умолчанию требуется подтверждение
        
        access_level = self.scopes[scope]
        
        confirmation_levels = [
            'confirmation_required',
            'double_confirmation',
            'always_confirmation'
        ]
        
        return access_level in confirmation_levels
    
    def requires_double_confirmation(self, scope: str) -> bool:
        """
        Проверка, требуется ли двойное подтверждение
        
        Args:
            scope: Область действия
        
        Returns:
            True если требуется двойное подтверждение
        """
        if scope not in self.scopes:
            return False
        
        return self.scopes[scope] == 'double_confirmation'
    
    def is_whitelist_only(self, scope: str) -> bool:
        """
        Проверка, только ли из whitelist разрешен доступ
        
        Args:
            scope: Область действия
        
        Returns:
            True если только whitelist
        """
        if scope not in self.scopes:
            return False
        
        return self.scopes[scope] == 'whitelist_only'
    
    def get_scope_info(self, scope: str) -> Dict[str, any]:
        """
        Получение информации об области действия
        
        Args:
            scope: Область действия
        
        Returns:
            Информация об области
        """
        if scope not in self.scopes:
            return {
                'scope': scope,
                'access': 'unknown',
                'level': -1,
                'requires_confirmation': True
            }
        
        access_level = self.scopes[scope]
        
        return {
            'scope': scope,
            'access': access_level,
            'level': self.ACCESS_LEVELS.get(access_level, -1),
            'requires_confirmation': self.requires_confirmation(scope),
            'requires_double_confirmation': self.requires_double_confirmation(scope),
            'whitelist_only': self.is_whitelist_only(scope)
        }
    
    def list_scopes(self) -> List[Dict[str, any]]:
        """Список всех областей действия"""
        return [self.get_scope_info(scope) for scope in self.scopes.keys()]


class AuditLog:
    """
    Аудит-лог
    Записывает все действия с инструментами
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.log_path = Path(config.get('audit_log_path', './data/audit.log'))
        self.entries: List[AuditEntry] = []
        self.max_entries = config.get('max_audit_entries', 10000)
        
        # Создание директории
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"AuditLog инициализирован (путь: {self.log_path})")
    
    async def log_action(
        self,
        tool_name: str,
        scope: str,
        risk: str,
        user_confirmed: bool,
        success: bool,
        error: Optional[str] = None,
        arguments: Optional[Dict] = None
    ) -> None:
        """
        Запись действия в аудит-лог
        
        Args:
            tool_name: Название инструмента
            scope: Область действия
            risk: Уровень риска
            user_confirmed: Подтверждено ли пользователем
            success: Успешно ли выполнено
            error: Ошибка (если есть)
            arguments: Аргументы (если есть)
        """
        entry = AuditEntry(
            timestamp=datetime.now().isoformat(),
            tool_name=tool_name,
            scope=scope,
            risk=risk,
            user_confirmed=user_confirmed,
            success=success,
            error=error,
            arguments=arguments
        )
        
        self.entries.append(entry)
        
        # Ограничение размера
        if len(self.entries) > self.max_entries:
            self.entries = self.entries[-self.max_entries:]
        
        # Запись в файл
        await self._write_to_file(entry)
        
        # Логирование
        status = "✅" if success else "❌"
        logger.info(f"{status} AUDIT: {tool_name} (scope={scope}, risk={risk}, confirmed={user_confirmed})")
    
    async def _write_to_file(self, entry: AuditEntry) -> None:
        """Запись записи в файл"""
        try:
            with open(self.log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(asdict(entry), ensure_ascii=False) + '\n')
        except Exception as e:
            logger.error(f"Ошибка записи в аудит-лог: {e}")
    
    async def load_from_file(self) -> None:
        """Загрузка записей из файла"""
        if not self.log_path.exists():
            return
        
        try:
            with open(self.log_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        data = json.loads(line.strip())
                        entry = AuditEntry(**data)
                        self.entries.append(entry)
                    except Exception as e:
                        logger.warning(f"Ошибка парсинга записи аудит-лога: {e}")
            
            logger.info(f"✅ Загружено {len(self.entries)} записей из аудит-лога")
        
        except Exception as e:
            logger.error(f"Ошибка загрузки аудит-лога: {e}")
    
    def get_recent_entries(self, limit: int = 100) -> List[AuditEntry]:
        """Получение последних записей"""
        return self.entries[-limit:]
    
    def get_entries_by_tool(self, tool_name: str) -> List[AuditEntry]:
        """Получение записей по инструменту"""
        return [e for e in self.entries if e.tool_name == tool_name]
    
    def get_entries_by_scope(self, scope: str) -> List[AuditEntry]:
        """Получение записей по области действия"""
        return [e for e in self.entries if e.scope == scope]
    
    def get_failed_entries(self) -> List[AuditEntry]:
        """Получение неудачных записей"""
        return [e for e in self.entries if not e.success]
    
    def get_statistics(self) -> Dict[str, any]:
        """Получение статистики"""
        total = len(self.entries)
        successful = sum(1 for e in self.entries if e.success)
        failed = total - successful
        
        # По инструментам
        by_tool = {}
        for entry in self.entries:
            if entry.tool_name not in by_tool:
                by_tool[entry.tool_name] = {'total': 0, 'success': 0, 'failed': 0}
            by_tool[entry.tool_name]['total'] += 1
            if entry.success:
                by_tool[entry.tool_name]['success'] += 1
            else:
                by_tool[entry.tool_name]['failed'] += 1
        
        # По областям
        by_scope = {}
        for entry in self.entries:
            if entry.scope not in by_scope:
                by_scope[entry.scope] = {'total': 0, 'success': 0, 'failed': 0}
            by_scope[entry.scope]['total'] += 1
            if entry.success:
                by_scope[entry.scope]['success'] += 1
            else:
                by_scope[entry.scope]['failed'] += 1
        
        return {
            'total': total,
            'successful': successful,
            'failed': failed,
            'success_rate': successful / total if total > 0 else 0.0,
            'by_tool': by_tool,
            'by_scope': by_scope
        }
    
    async def clear(self) -> None:
        """Очистка аудит-лога"""
        self.entries.clear()
        
        # Очистка файла
        if self.log_path.exists():
            self.log_path.unlink()
        
        logger.info("🗑️ Аудит-лог очищен")
