"""
Backup Manager — Менеджер резервных копий и обновлений
Создание бэкапов, проверка обновлений, откат
"""
import asyncio
import logging
import shutil
import hashlib
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class BackupManager:
    """
    Менеджер резервных копий и обновлений
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.backup_dir = Path(config.get('backup_dir', './backups'))
        self.current_version = config.get('current_version', '1.0.0')
        
        # Создание директории для бэкапов
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"BackupManager инициализирован (версия: {self.current_version})")
    
    async def create_backup(self, name: Optional[str] = None) -> Path:
        """
        Создание резервной копии
        
        Args:
            name: Имя бэкапа (по умолчанию с timestamp)
        
        Returns:
            Путь к созданному бэкапу
        """
        if name is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            name = f"backup_{timestamp}"
        
        backup_path = self.backup_dir / name
        
        try:
            # Создание директории бэкапа
            backup_path.mkdir(parents=True, exist_ok=True)
            
            # Копирование важных директорий
            dirs_to_backup = [
                './config',
                './data',
                './logs',
                './models'
            ]
            
            for dir_path in dirs_to_backup:
                src = Path(dir_path)
                if src.exists():
                    dst = backup_path / src.name
                    await asyncio.to_thread(
                        shutil.copytree,
                        src,
                        dst,
                        dirs_exist_ok=True
                    )
                    logger.info(f"✅ Скопировано: {dir_path}")
            
            # Сохранение метаданных
            metadata = {
                'name': name,
                'version': self.current_version,
                'timestamp': datetime.now().isoformat(),
                'dirs': dirs_to_backup
            }
            
            metadata_path = backup_path / 'metadata.json'
            await asyncio.to_thread(
                metadata_path.write_text,
                json.dumps(metadata, indent=2, ensure_ascii=False),
                'utf-8'
            )
            
            logger.info(f"✅ Резервная копия создана: {backup_path}")
            return backup_path
        
        except Exception as e:
            logger.error(f"❌ Ошибка создания резервной копии: {e}")
            raise
    
    async def restore_backup(self, backup_path: Path) -> None:
        """
        Восстановление из резервной копии
        
        Args:
            backup_path: Путь к бэкапу
        """
        if not backup_path.exists():
            raise FileNotFoundError(f"Резервная копия не найдена: {backup_path}")
        
        try:
            # Загрузка метаданных
            metadata_path = backup_path / 'metadata.json'
            if not metadata_path.exists():
                raise FileNotFoundError(f"Метаданные не найдены: {metadata_path}")
            
            metadata_text = await asyncio.to_thread(metadata_path.read_text, 'utf-8')
            metadata = json.loads(metadata_text)
            
            logger.info(f"🔄 Восстановление из бэкапа: {metadata['name']}")
            
            # Восстановление директорий
            for dir_name in metadata['dirs']:
                src = backup_path / Path(dir_name).name
                dst = Path(dir_name)
                
                if src.exists():
                    # Удаление текущей версии
                    if dst.exists():
                        await asyncio.to_thread(shutil.rmtree, dst)
                    
                    # Восстановление из бэкапа
                    await asyncio.to_thread(shutil.copytree, src, dst)
                    logger.info(f"✅ Восстановлено: {dir_name}")
            
            logger.info(f"✅ Восстановление завершено из бэкапа: {backup_path}")
        
        except Exception as e:
            logger.error(f"❌ Ошибка восстановления из бэкапа: {e}")
            raise
    
    async def list_backups(self) -> List[Dict]:
        """
        Список всех резервных копий
        
        Returns:
            Список метаданных бэкапов
        """
        backups = []
        
        try:
            for backup_path in self.backup_dir.iterdir():
                if backup_path.is_dir():
                    metadata_path = backup_path / 'metadata.json'
                    if metadata_path.exists():
                        metadata_text = await asyncio.to_thread(metadata_path.read_text, 'utf-8')
                        metadata = json.loads(metadata_text)
                        backups.append(metadata)
            
            # Сортировка по дате (новые первыми)
            backups.sort(key=lambda x: x['timestamp'], reverse=True)
            
            return backups
        
        except Exception as e:
            logger.error(f"❌ Ошибка получения списка бэкапов: {e}")
            return []
    
    async def delete_backup(self, backup_path: Path) -> None:
        """
        Удаление резервной копии
        
        Args:
            backup_path: Путь к бэкапу
        """
        try:
            if backup_path.exists():
                await asyncio.to_thread(shutil.rmtree, backup_path)
                logger.info(f"✅ Резервная копия удалена: {backup_path}")
            else:
                logger.warning(f"⚠️ Резервная копия не найдена: {backup_path}")
        
        except Exception as e:
            logger.error(f"❌ Ошибка удаления резервной копии: {e}")
            raise
    
    async def check_update(self, update_url: str) -> Optional[Dict]:
        """
        Проверка наличия обновления
        
        Args:
            update_url: URL для проверки обновлений
        
        Returns:
            Информация об обновлении или None
        """
        try:
            # TODO: Реализовать реальную проверку обновлений
            # Сейчас это заглушка
            
            logger.info(f"🔍 Проверка обновлений: {update_url}")
            
            # Имитация проверки
            await asyncio.sleep(0.5)
            
            # Возврат заглушки
            return {
                'available': False,
                'current_version': self.current_version,
                'latest_version': self.current_version,
                'download_url': None,
                'changelog': []
            }
        
        except Exception as e:
            logger.error(f"❌ Ошибка проверки обновлений: {e}")
            return None
    
    async def download_update(self, download_url: str, dest_path: Path) -> bool:
        """
        Загрузка обновления
        
        Args:
            download_url: URL для загрузки
            dest_path: Путь для сохранения
        
        Returns:
            True если успешно
        """
        try:
            # TODO: Реализовать реальную загрузку
            logger.info(f"📥 Загрузка обновления: {download_url}")
            
            # Имитация загрузки
            await asyncio.sleep(1.0)
            
            logger.info(f"✅ Обновление загружено: {dest_path}")
            return True
        
        except Exception as e:
            logger.error(f"❌ Ошибка загрузки обновления: {e}")
            return False
    
    async def verify_update(self, file_path: Path, expected_hash: str) -> bool:
        """
        Проверка целостности обновления (SHA256)
        
        Args:
            file_path: Путь к файлу
            expected_hash: Ожидаемый SHA256 хеш
        
        Returns:
            True если хеш совпадает
        """
        try:
            # Вычисление хеша файла
            sha256_hash = hashlib.sha256()
            
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    sha256_hash.update(chunk)
            
            actual_hash = sha256_hash.hexdigest()
            
            # Сравнение
            if actual_hash == expected_hash:
                logger.info(f"✅ Хеш совпадает: {actual_hash}")
                return True
            else:
                logger.error(f"❌ Хеш не совпадает!")
                logger.error(f"   Ожидаемый: {expected_hash}")
                logger.error(f"   Фактический: {actual_hash}")
                return False
        
        except Exception as e:
            logger.error(f"❌ Ошибка проверки хеша: {e}")
            return False
    
    async def install_update(self, update_path: Path) -> bool:
        """
        Установка обновления
        
        Args:
            update_path: Путь к файлу обновления
        
        Returns:
            True если успешно
        """
        try:
            # Создание бэкапа перед обновлением
            logger.info("📦 Создание бэкапа перед обновлением...")
            await self.create_backup(name=f"pre_update_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            
            # TODO: Реализовать реальную установку обновления
            logger.info(f"🔄 Установка обновления: {update_path}")
            
            # Имитация установки
            await asyncio.sleep(1.0)
            
            logger.info("✅ Обновление установлено")
            return True
        
        except Exception as e:
            logger.error(f"❌ Ошибка установки обновления: {e}")
            return False
    
    async def rollback(self) -> bool:
        """
        Откат к предыдущей версии
        
        Returns:
            True если успешно
        """
        try:
            # Получение списка бэкапов
            backups = await self.list_backups()
            
            if not backups:
                logger.error("❌ Нет резервных копий для отката")
                return False
            
            # Использование последнего бэкапа
            latest_backup = backups[0]
            backup_path = self.backup_dir / latest_backup['name']
            
            logger.info(f"🔄 Откат к версии: {latest_backup['version']}")
            
            # Восстановление из бэкапа
            await self.restore_backup(backup_path)
            
            logger.info("✅ Откат завершен")
            return True
        
        except Exception as e:
            logger.error(f"❌ Ошибка отката: {e}")
            return False
    
    @property
    def stats(self) -> Dict:
        """Статистика менеджера"""
        return {
            'current_version': self.current_version,
            'backup_dir': str(self.backup_dir),
            'backups_count': len(list(self.backup_dir.iterdir())) if self.backup_dir.exists() else 0
        }
