"""
Degradation Manager — Режим выживания
Автоматическое отключение компонентов при нехватке ресурсов
"""
import asyncio
import logging
from typing import Dict, List, Optional, Callable, Awaitable
from enum import Enum
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class DegradationLevel(Enum):
    """Уровень деградации"""
    NORMAL = "normal"          # Все компоненты работают
    ECONOMY = "economy"        # Отключены некритичные компоненты
    SURVIVAL = "survival"      # Только базовые функции
    EMERGENCY = "emergency"    # Минимальная работоспособность


@dataclass
class DegradationThresholds:
    """Пороги для активации деградации"""
    ram_critical_mb: float = 7000  # Критическое потребление RAM
    ram_warning_mb: float = 6000   # Предупреждение по RAM
    cpu_critical_percent: float = 90.0  # Критическая загрузка CPU
    cpu_warning_percent: float = 75.0   # Предупреждение по CPU


@dataclass
class ComponentPriority:
    """Приоритет компонента"""
    name: str
    priority: int  # 0 = критичный, 10 = некритичный
    min_level: DegradationLevel  # Минимальный уровень для работы
    disable_callback: Optional[Callable[[], Awaitable[None]]] = None
    enable_callback: Optional[Callable[[], Awaitable[None]]] = None


class DegradationManager:
    """
    Менеджер деградации
    Автоматически отключает компоненты при нехватке ресурсов
    """
    
    def __init__(self, config: Dict):
        self.config = config
        
        # Пороги
        self.thresholds = DegradationThresholds(
            ram_critical_mb=config.get('ram_critical_mb', 7000),
            ram_warning_mb=config.get('ram_warning_mb', 6000),
            cpu_critical_percent=config.get('cpu_critical_percent', 90.0),
            cpu_warning_percent=config.get('cpu_warning_percent', 75.0)
        )
        
        # Текущий уровень деградации
        self._current_level = DegradationLevel.NORMAL
        
        # Компоненты с приоритетами
        self._components: List[ComponentPriority] = []
        
        # Отключенные компоненты
        self._disabled_components: set = set()
        
        # Callback при изменении уровня
        self._on_level_change: Optional[Callable[[DegradationLevel], Awaitable[None]]] = None
        
        # Задача мониторинга
        self._running = False
        self._task: Optional[asyncio.Task] = None
        self._check_interval = config.get('check_interval', 10.0)  # секунды
        
        logger.info(
            f"DegradationManager инициализирован "
            f"(RAM warning={self.thresholds.ram_warning_mb}MB, "
            f"critical={self.thresholds.ram_critical_mb}MB)"
        )
    
    def register_component(
        self,
        name: str,
        priority: int,
        min_level: DegradationLevel,
        disable_callback: Optional[Callable[[], Awaitable[None]]] = None,
        enable_callback: Optional[Callable[[], Awaitable[None]]] = None
    ) -> None:
        """
        Регистрация компонента с приоритетом
        
        Args:
            name: Название компонента
            priority: Приоритет (0 = критичный, 10 = некритичный)
            min_level: Минимальный уровень деградации для работы
            disable_callback: Функция отключения компонента
            enable_callback: Функция включения компонента
        """
        component = ComponentPriority(
            name=name,
            priority=priority,
            min_level=min_level,
            disable_callback=disable_callback,
            enable_callback=enable_callback
        )
        
        self._components.append(component)
        # Сортировка по приоритету (меньше = важнее)
        self._components.sort(key=lambda c: c.priority)
        
        logger.info(f"✅ Зарегистрирован компонент: {name} (priority={priority}, min_level={min_level.value})")
    
    def set_level_change_callback(
        self,
        callback: Callable[[DegradationLevel], Awaitable[None]]
    ) -> None:
        """
        Установка callback при изменении уровня деградации
        
        Args:
            callback: Асинхронная функция(level)
        """
        self._on_level_change = callback
    
    async def start(self) -> None:
        """Запуск мониторинга ресурсов"""
        self._running = True
        self._task = asyncio.create_task(self._monitoring_loop())
        logger.info("📉 DegradationManager запущен")
    
    async def _monitoring_loop(self) -> None:
        """Цикл мониторинга ресурсов"""
        import psutil
        import os
        
        while self._running:
            try:
                # Получение текущих ресурсов
                process = psutil.Process(os.getpid())
                ram_used_mb = process.memory_info().rss / 1024 / 1024
                cpu_percent = process.cpu_percent()
                
                # Определение уровня деградации
                new_level = self._determine_level(ram_used_mb, cpu_percent)
                
                # Изменение уровня если нужно
                if new_level != self._current_level:
                    await self._change_level(new_level)
                
                # Логирование (каждые 30 секунд)
                if int(asyncio.get_event_loop().time()) % 30 == 0:
                    logger.info(
                        f"📉 Ресурсы: RAM={ram_used_mb:.0f}MB, "
                        f"CPU={cpu_percent:.1f}%, "
                        f"Level={self._current_level.value}"
                    )
                
                await asyncio.sleep(self._check_interval)
            
            except Exception as e:
                logger.error(f"Ошибка мониторинга ресурсов: {e}")
                await asyncio.sleep(self._check_interval)
    
    def _determine_level(self, ram_mb: float, cpu_percent: float) -> DegradationLevel:
        """
        Определение уровня деградации на основе ресурсов
        
        Args:
            ram_mb: Использование RAM в MB
            cpu_percent: Загрузка CPU в процентах
        
        Returns:
            DegradationLevel
        """
        # Emergency: критические ресурсы
        if ram_mb > self.thresholds.ram_critical_mb or cpu_percent > self.thresholds.cpu_critical_percent:
            return DegradationLevel.EMERGENCY
        
        # Survival: высокое потребление
        if ram_mb > self.thresholds.ram_warning_mb * 1.1 or cpu_percent > self.thresholds.cpu_warning_percent * 1.1:
            return DegradationLevel.SURVIVAL
        
        # Economy: предупреждение
        if ram_mb > self.thresholds.ram_warning_mb or cpu_percent > self.thresholds.cpu_warning_percent:
            return DegradationLevel.ECONOMY
        
        # Normal: все хорошо
        return DegradationLevel.NORMAL
    
    async def _change_level(self, new_level: DegradationLevel) -> None:
        """
        Изменение уровня деградации
        
        Args:
            new_level: Новый уровень
        """
        old_level = self._current_level
        self._current_level = new_level
        
        logger.warning(
            f"⚠️ Уровень деградации изменен: {old_level.value} → {new_level.value}"
        )
        
        # Callback
        if self._on_level_change:
            await self._on_level_change(new_level)
        
        # Применение деградации
        await self._apply_degradation()
    
    async def _apply_degradation(self) -> None:
        """Применение деградации (отключение компонентов)"""
        level_order = [
            DegradationLevel.NORMAL,
            DegradationLevel.ECONOMY,
            DegradationLevel.SURVIVAL,
            DegradationLevel.EMERGENCY
        ]
        
        current_level_index = level_order.index(self._current_level)
        
        for component in self._components:
            min_level_index = level_order.index(component.min_level)
            
            # Если текущий уровень хуже минимального для компонента
            if current_level_index > min_level_index:
                # Отключение компонента
                if component.name not in self._disabled_components:
                    logger.warning(f"🔌 Отключение компонента: {component.name}")
                    
                    if component.disable_callback:
                        try:
                            await component.disable_callback()
                        except Exception as e:
                            logger.error(f"Ошибка отключения {component.name}: {e}")
                    
                    self._disabled_components.add(component.name)
            
            else:
                # Включение компонента если был отключен
                if component.name in self._disabled_components:
                    logger.info(f"🔌 Включение компонента: {component.name}")
                    
                    if component.enable_callback:
                        try:
                            await component.enable_callback()
                        except Exception as e:
                            logger.error(f"Ошибка включения {component.name}: {e}")
                    
                    self._disabled_components.remove(component.name)
    
    def get_current_level(self) -> DegradationLevel:
        """Получение текущего уровня деградации"""
        return self._current_level
    
    def get_disabled_components(self) -> List[str]:
        """Получение списка отключенных компонентов"""
        return list(self._disabled_components)
    
    def get_status(self) -> Dict:
        """Получение статуса деградации"""
        return {
            'current_level': self._current_level.value,
            'disabled_components': list(self._disabled_components),
            'total_components': len(self._components),
            'active_components': len(self._components) - len(self._disabled_components),
            'thresholds': {
                'ram_warning_mb': self.thresholds.ram_warning_mb,
                'ram_critical_mb': self.thresholds.ram_critical_mb,
                'cpu_warning_percent': self.thresholds.cpu_warning_percent,
                'cpu_critical_percent': self.thresholds.cpu_critical_percent
            }
        }
    
    async def force_level(self, level: DegradationLevel) -> None:
        """
        Принудительная установка уровня деградации
        
        Args:
            level: Уровень деградации
        """
        logger.warning(f"⚠️ Принудительная установка уровня: {level.value}")
        await self._change_level(level)
    
    async def stop(self) -> None:
        """Остановка мониторинга"""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        
        # Включение всех отключенных компонентов
        for component in self._components:
            if component.name in self._disabled_components:
                if component.enable_callback:
                    try:
                        await component.enable_callback()
                    except Exception as e:
                        logger.error(f"Ошибка включения {component.name}: {e}")
        
        self._disabled_components.clear()
        logger.info("🛑 DegradationManager остановлен")
    
    @property
    def is_running(self) -> bool:
        """Запущен ли менеджер"""
        return self._running
