"""
Тесты Фазы 7 — Безопасность и инструменты
Проверка MCP, Scopes, Encryption, Backup
"""
import asyncio
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config import load_config
from security.mcp import MCPServer, ToolRisk
from security.scopes import ScopeManager, AuditLog
from security.encryption import EncryptionManager
from security.backup import BackupManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def test_mcp():
    """
    Тест MCP Server
    """
    logger.info("=" * 60)
    logger.info("🧪 ТЕСТ: MCP Server (Инструменты)")
    logger.info("=" * 60)
    
    try:
        config = load_config('./config.yaml')
        mcp = MCPServer(config.get('security', {}))
        
        # Регистрация встроенных инструментов
        mcp.register_builtin_tools()
        
        # Список инструментов
        tools = mcp.list_tools()
        logger.info(f"\n📊 Зарегистрировано инструментов: {len(tools)}")
        
        for tool in tools:
            logger.info(f"   - {tool.name}: {tool.description} (risk={tool.risk.value})")
        
        # Тест выполнения инструмента (калькулятор)
        logger.info(f"\n🔧 Тест инструмента: calculator")
        result = await mcp.execute_tool('calculator', {'expression': '2 + 2 * 2'})
        
        logger.info(f"   Результат: {result}")
        
        if result['success'] and result['result']['result'] == 6:
            logger.info(f"\n✅ ТЕСТ ПРОЙДЕН: MCP работает")
            return True
        else:
            logger.warning(f"\n⚠️ ТЕСТ: Неправильный результат")
            return False
    
    except Exception as e:
        logger.error(f"❌ Ошибка теста MCP: {e}", exc_info=True)
        return False


async def test_scopes():
    """
    Тест Scope Manager
    """
    logger.info("\n" + "=" * 60)
    logger.info("🧪 ТЕСТ: Scope Manager (Разрешения)")
    logger.info("=" * 60)
    
    try:
        config = load_config('./config.yaml')
        scope_manager = ScopeManager(config.get('security', {}))
        
        # Список областей
        scopes = scope_manager.list_scopes()
        logger.info(f"\n📊 Областей действия: {len(scopes)}")
        
        for scope_info in scopes:
            logger.info(f"   - {scope_info['scope']}: {scope_info['access']}")
        
        # Проверка доступа
        logger.info(f"\n🔍 Проверка доступа:")
        
        test_scopes = ['math', 'web', 'files.dangerous', 'system.dangerous']
        
        for scope in test_scopes:
            access = scope_manager.check_access(scope)
            requires_conf = scope_manager.requires_confirmation(scope)
            
            logger.info(f"   {scope}:")
            logger.info(f"     Доступ: {'✅' if access else '❌'}")
            logger.info(f"     Подтверждение: {'✅' if requires_conf else '❌'}")
        
        logger.info(f"\n✅ ТЕСТ ПРОЙДЕН: Scope Manager работает")
        return True
    
    except Exception as e:
        logger.error(f"❌ Ошибка теста Scopes: {e}", exc_info=True)
        return False


async def test_audit():
    """
    Тест Audit Log
    """
    logger.info("\n" + "=" * 60)
    logger.info("🧪 ТЕСТ: Audit Log (Аудит)")
    logger.info("=" * 60)
    
    try:
        config = load_config('./config.yaml')
        audit = AuditLog(config.get('security', {}))
        
        # Запись тестовых записей
        logger.info(f"\n📝 Запись тестовых записей...")
        
        await audit.log_action(
            tool_name='calculator',
            scope='math',
            risk='low',
            user_confirmed=False,
            success=True,
            arguments={'expression': '2+2'}
        )
        
        await audit.log_action(
            tool_name='delete_file',
            scope='files.dangerous',
            risk='high',
            user_confirmed=True,
            success=True,
            arguments={'path': '/tmp/test.txt'}
        )
        
        await audit.log_action(
            tool_name='system_command',
            scope='system.dangerous',
            risk='high',
            user_confirmed=False,
            success=False,
            error='Требуется подтверждение',
            arguments={'command': 'rm -rf /'}
        )
        
        # Статистика
        stats = audit.get_statistics()
        
        logger.info(f"\n📊 Статистика:")
        logger.info(f"   Всего записей: {stats['total']}")
        logger.info(f"   Успешных: {stats['successful']}")
        logger.info(f"   Неудачных: {stats['failed']}")
        logger.info(f"   Success rate: {stats['success_rate']:.1%}")
        
        logger.info(f"\n✅ ТЕСТ ПРОЙДЕН: Audit Log работает")
        return True
    
    except Exception as e:
        logger.error(f"❌ Ошибка теста Audit: {e}", exc_info=True)
        return False


async def test_encryption():
    """
    Тест Encryption Manager
    """
    logger.info("\n" + "=" * 60)
    logger.info("🧪 ТЕСТ: Encryption Manager (Шифрование)")
    logger.info("=" * 60)
    
    try:
        config = load_config('./config.yaml')
        encryption = EncryptionManager(config.get('security', {}))
        
        # Инициализация
        await encryption.initialize()
        
        # Тест шифрования/расшифровки
        test_data = "Секретные данные: пароль123"
        
        logger.info(f"\n🔐 Тест шифрования:")
        logger.info(f"   Исходные данные: {test_data}")
        
        # Шифрование
        encrypted = await encryption.encrypt(test_data)
        logger.info(f"   Зашифровано: {encrypted[:50]}...")
        
        # Расшифровка
        decrypted = await encryption.decrypt(encrypted)
        logger.info(f"   Расшифровано: {decrypted}")
        
        # Проверка
        if decrypted == test_data:
            logger.info(f"\n✅ ТЕСТ ПРОЙДЕН: Шифрование работает")
            return True
        else:
            logger.error(f"\n❌ ТЕСТ: Данные не совпадают")
            return False
    
    except ImportError as e:
        logger.error(f"❌ cryptography не установлен: {e}")
        logger.info("   Установите: pip install cryptography")
        return False
    except Exception as e:
        logger.error(f"❌ Ошибка теста Encryption: {e}", exc_info=True)
        return False


async def test_backup():
    """
    Тест Backup Manager
    """
    logger.info("\n" + "=" * 60)
    logger.info("🧪 ТЕСТ: Backup Manager (Резервные копии)")
    logger.info("=" * 60)
    
    try:
        config = load_config('./config.yaml')
        backup = BackupManager(config.get('security', {}))
        
        # Создание бэкапа
        logger.info(f"\n📦 Создание резервной копии...")
        backup_path = await backup.create_backup(name='test_backup')
        
        logger.info(f"   Бэкап создан: {backup_path}")
        
        # Список бэкапов
        backups = await backup.list_backups()
        logger.info(f"\n📊 Всего бэкапов: {len(backups)}")
        
        for b in backups:
            logger.info(f"   - {b['name']} (версия: {b['version']})")
        
        # Статистика
        stats = backup.stats
        logger.info(f"\n📈 Статистика:")
        logger.info(f"   Текущая версия: {stats['current_version']}")
        logger.info(f"   Количество бэкапов: {stats['backups_count']}")
        
        logger.info(f"\n✅ ТЕСТ ПРОЙДЕН: Backup Manager работает")
        return True
    
    except Exception as e:
        logger.error(f"❌ Ошибка теста Backup: {e}", exc_info=True)
        return False


async def test_integration():
    """
    Интеграционный тест всех компонентов безопасности
    """
    logger.info("\n" + "=" * 60)
    logger.info("🧪 ИНТЕГРАЦИОННЫЙ ТЕСТ: Полная безопасность")
    logger.info("=" * 60)
    
    try:
        config = load_config('./config.yaml')
        
        # Создание всех компонентов
        logger.info("\n1️⃣ Создание компонентов...")
        mcp = MCPServer(config.get('security', {}))
        scope_manager = ScopeManager(config.get('security', {}))
        audit = AuditLog(config.get('security', {}))
        encryption = EncryptionManager(config.get('security', {}))
        backup = BackupManager(config.get('security', {}))
        
        logger.info("   ✅ Все компоненты созданы")
        
        # Регистрация инструментов
        logger.info("\n2️⃣ Регистрация инструментов...")
        mcp.register_builtin_tools()
        logger.info(f"   ✅ Зарегистрировано {len(mcp.list_tools())} инструментов")
        
        # Инициализация шифрования
        logger.info("\n3️⃣ Инициализация шифрования...")
        await encryption.initialize()
        logger.info("   ✅ Шифрование инициализировано")
        
        # Тест выполнения инструмента с аудитом
        logger.info("\n4️⃣ Тест выполнения инструмента...")
        result = await mcp.execute_tool('calculator', {'expression': '10 * 5'})
        
        # Запись в аудит
        await audit.log_action(
            tool_name='calculator',
            scope='math',
            risk='low',
            user_confirmed=False,
            success=result['success']
        )
        
        logger.info(f"   ✅ Инструмент выполнен и записан в аудит")
        
        # Создание бэкапа
        logger.info("\n5️⃣ Создание бэкапа...")
        await backup.create_backup(name='integration_test')
        logger.info("   ✅ Бэкап создан")
        
        # Статистика
        logger.info("\n📊 Итоговая статистика:")
        logger.info(f"   Инструментов: {len(mcp.list_tools())}")
        logger.info(f"   Областей действия: {len(scope_manager.list_scopes())}")
        logger.info(f"   Записей в аудите: {len(audit.entries)}")
        logger.info(f"   Бэкапов: {backup.stats['backups_count']}")
        
        logger.info(f"\n✅ ИНТЕГРАЦИОННЫЙ ТЕСТ ПРОЙДЕН")
        return True
    
    except ImportError as e:
        logger.error(f"❌ Необходимые пакеты не установлены: {e}")
        logger.info("   Установите: pip install cryptography")
        return False
    except Exception as e:
        logger.error(f"❌ Ошибка интеграционного теста: {e}", exc_info=True)
        return False


async def main():
    """Главная функция"""
    logger.info("\n" + "=" * 60)
    logger.info("🚀 ФАЗА 7: Тесты безопасности")
    logger.info("=" * 60 + "\n")
    
    results = {}
    
    # Тест MCP
    results['mcp'] = await test_mcp()
    
    # Тест Scopes
    results['scopes'] = await test_scopes()
    
    # Тест Audit
    results['audit'] = await test_audit()
    
    # Тест Encryption
    results['encryption'] = await test_encryption()
    
    # Тест Backup
    results['backup'] = await test_backup()
    
    # Интеграционный тест
    results['integration'] = await test_integration()
    
    # Итоги
    logger.info("\n" + "=" * 60)
    logger.info("📊 ИТОГИ ФАЗЫ 7")
    logger.info("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"   {status}: {test_name}")
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    logger.info(f"\n   Результат: {passed}/{total} тестов пройдено")
    
    if passed == total:
        logger.info("\n🎉 Все тесты Фазы 7 пройдены!")
        logger.info("\nСледующие шаги:")
        logger.info("1. Фаза 7.5-7.8: Полировка (Beta & Performance)")
        logger.info("2. Фаза 8: Упаковка (Nuitka)")
    else:
        logger.info("\n⚠️ Некоторые тесты не пройдены.")
    
    return passed == total


if __name__ == '__main__':
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
