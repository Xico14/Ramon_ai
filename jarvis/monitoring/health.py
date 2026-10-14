"""
Health Checker — Проверка состояния компонентов
Heartbeat, liveness, readiness checks
"""
import asyncio
import logging
import time
from typing import Dict, List, Optional, Callable, Awaitable
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    """Статус здоровья компонента"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"


@dataclass
class HealthCheck:
    """Результат проверки здоровья"""
    component: str
    status: HealthStatus
    message: str
    latency_ms: float
    timestamp: float
    details: Dict = None
    
    def __post_init__(self):
        if self.details is None:
            self.details = {}


class HealthChecker:
    """
    Проверка состояния компонентов
    Heartbeat, liveness, readiness checks
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.check_interval = config.get('check_interval', 30.0)  # секунды
        self.timeout = config.get('timeout', 5.0)  # секунды
        
        # Проверки компонентов
        self._checks: Dict[str, Callable[[], Awaitable[HealthCheck]]] = {}
        
        # Результаты последних проверок
        self._last_checks: Dict[str, HealthCheck] = {}
        
        # Задача проверки
        self._running = False
        self._task: Optional[asyncio.Task] = None
        
        # Callback при изменении статуса
        self._on_status_change: Optional[Callable[[str, HealthStatus], Awaitable[None]]] = None
        
        logger.info(f"HealthChecker инициализирован (interval={self.check_interval}s)")
    
    def register_check(
        self,
        component: str,
        check_func: Callable[[], Awaitable[HealthCheck]]
    ) -> None:
        """
        Регистрация проверки компонента
        
        Args:
            component: Название компонента
            check_func: Асинхронная функция проверки
        """
        self._checks[component] = check_func
        logger.info(f"✅ Зарегистрирована проверка: {component}")
    
    def set_status_change_callback(
        self,
        callback: Callable[[str, HealthStatus], Awaitable[None]]
    ) -> None:
        """
        Установка callback при изменении статуса
        
        Args:
            callback: Асинхронная функция(component, status)
        """
        self._on_status_change = callback
    
    async def start(self) -> None:
        """Запуск проверок здоровья"""
        self._running = True
        self._task = asyncio.create_task(self._check_loop())
        logger.info("🏥 HealthChecker запущен")
    
    async def _check_loop(self) -> None:
        """Цикл проверок"""
        while self._running:
            try:
                await self._run_all_checks()
                await asyncio.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Ошибка проверки здоровья: {e}")
                await asyncio.sleep(self.check_interval)
    
    async def _run_all_checks(self) -> None:
        """Запуск всех проверок"""
        for component, check_func in self._checks.items():
            try:
                # Запуск проверки с таймаутом
                start_time = time.time()
                check_result = await asyncio.wait_for(
                    check_func(),
                    timeout=self.timeout
                )
                latency_ms = (time.time() - start_time) * 1000
                
                # Обновление результата
                check_result.latency_ms = latency_ms
                check_result.timestamp = time.time()
                
                # Проверка изменения статуса
                old_check = self._last_checks.get(component)
                if old_check and old_check.status != check_result.status:
                    logger.warning(
                        f"⚠️ Статус {component} изменился: "
                        f"{old_check.status.value} → {check_result.status.value}"
                    )
                    
                    # Callback
                    if self._on_status_change:
                        await self._on_status_change(component, check_result.status)
                
                self._last_checks[component] = check_result
                
                # Логирование
                status_icon = {
                    HealthStatus.HEALTHY: "✅",
                    HealthStatus.DEGRADED: "⚠️",
                    HealthStatus.UNHEALTHY: "❌",
                    HealthStatus.UNKNOWN: "❓"
                }[check_result.status]
                
                logger.debug(
                    f"{status_icon} {component}: {check_result.status.value} "
                    f"({latency_ms:.1f}ms)"
                )
            
            except asyncio.TimeoutError:
                logger.error(f"❌ Таймаут проверки {component}")
                self._last_checks[component] = HealthCheck(
                    component=component,
                    status=HealthStatus.UNHEALTHY,
                    message="Таймаут проверки",
                    latency_ms=self.timeout * 1000,
                    timestamp=time.time()
                )
            
            except Exception as e:
                logger.error(f"❌ Ошибка проверки {component}: {e}")
                self._last_checks[component] = HealthCheck(
                    component=component,
                    status=HealthStatus.UNHEALTHY,
                    message=str(e),
                    latency_ms=0.0,
                    timestamp=time.time()
                )
    
    async def check_component(self, component: str) -> Optional[HealthCheck]:
        """
        Проверка одного компонента
        
        Args:
            component: Название компонента
        
        Returns:
            HealthCheck или None
        """
        if component not in self._checks:
            logger.warning(f"⚠️ Проверка не зарегистрирована: {component}")
            return None
        
        try:
            check_func = self._checks[component]
            return await asyncio.wait_for(check_func(), timeout=self.timeout)
        except Exception as e:
            logger.error(f"Ошибка проверки {component}: {e}")
            return None
    
    def get_status(self, component: str) -> HealthStatus:
        """
        Получение статуса компонента
        
        Args:
            component: Название компонента
        
        Returns:
            HealthStatus
        """
        if component not in self._last_checks:
            return HealthStatus.UNKNOWN
        
        return self._last_checks[component].status
    
    def get_all_statuses(self) -> Dict[str, HealthStatus]:
        """Получение статусов всех компонентов"""
        return {
            component: check.status
            for component, check in self._last_checks.items()
        }
    
    def get_overall_health(self) -> HealthStatus:
        """
        Получение общего состояния системы
        
        Returns:
            HealthStatus (худший из всех компонентов)
        """
        if not self._last_checks:
            return HealthStatus.UNKNOWN
        
        statuses = [check.status for check in self._last_checks.values()]
        
        # Приоритет: UNHEALTHY > DEGRADED > HEALTHY
        if HealthStatus.UNHEALTHY in statuses:
            return HealthStatus.UNHEALTHY
        elif HealthStatus.DEGRADED in statuses:
            return HealthStatus.DEGRADED
        elif HealthStatus.HEALTHY in statuses:
            return HealthStatus.HEALTHY
        else:
            return HealthStatus.UNKNOWN
    
    def get_health_report(self) -> Dict:
        """
        Получение полного отчета о здоровье
        
        Returns:
            Dict с информацией о всех компонентах
        """
        report = {
            'overall': self.get_overall_health().value,
            'timestamp': time.time(),
            'components': {}
        }
        
        for component, check in self._last_checks.items():
            report['components'][component] = {
                'status': check.status.value,
                'message': check.message,
                'latency_ms': check.latency_ms,
                'timestamp': check.timestamp,
                'details': check.details
            }
        
        return report
    
    async def stop(self) -> None:
        """Остановка проверок"""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("🛑 HealthChecker остановлен")
    
    @property
    def is_running(self) -> bool:
        """Запущен ли HealthChecker"""
        return self._running
    
    @property
    def registered_components(self) -> List[str]:
        """Список зарегистрированных компонентов"""
        return list(self._checks.keys())
