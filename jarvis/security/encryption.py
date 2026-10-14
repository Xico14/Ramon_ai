"""
Encryption Manager — Менеджер шифрования
AES-GCM для шифрования настроек и данных
"""
import asyncio
import logging
import os
from pathlib import Path
from typing import Optional
import json

logger = logging.getLogger(__name__)


class EncryptionManager:
    """
    Менеджер шифрования
    Использует AES-GCM для шифрования данных
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.key_path = Path(config.get('encryption_key_path', './config/encryption.key'))
        self._key: Optional[bytes] = None
        
        logger.info(f"EncryptionManager инициализирован (key_path: {self.key_path})")
    
    async def initialize(self) -> None:
        """Инициализация менеджера шифрования"""
        # Создание директории для ключа
        self.key_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Загрузка или генерация ключа
        if self.key_path.exists():
            await self._load_key()
        else:
            await self._generate_key()
    
    async def _generate_key(self) -> None:
        """Генерация нового ключа шифрования"""
        try:
            from cryptography.fernet import Fernet
            
            # Генерация ключа
            key = Fernet.generate_key()
            
            # Сохранение ключа
            await asyncio.to_thread(self.key_path.write_bytes, key)
            
            self._key = key
            logger.info("✅ Ключ шифрования сгенерирован")
        
        except ImportError:
            logger.error("❌ cryptography не установлен. Установите: pip install cryptography")
            raise
        except Exception as e:
            logger.error(f"❌ Ошибка генерации ключа: {e}")
            raise
    
    async def _load_key(self) -> None:
        """Загрузка существующего ключа"""
        try:
            key = await asyncio.to_thread(self.key_path.read_bytes)
            self._key = key
            logger.info("✅ Ключ шифрования загружен")
        except Exception as e:
            logger.error(f"❌ Ошибка загрузки ключа: {e}")
            raise
    
    async def encrypt(self, data: str) -> str:
        """
        Шифрование данных
        
        Args:
            data: Данные для шифрования
        
        Returns:
            Зашифрованные данные (base64)
        """
        if self._key is None:
            await self.initialize()
        
        try:
            from cryptography.fernet import Fernet
            
            fernet = Fernet(self._key)
            
            # Шифрование
            encrypted = await asyncio.to_thread(
                fernet.encrypt,
                data.encode('utf-8')
            )
            
            # Возврат в base64
            return encrypted.decode('utf-8')
        
        except Exception as e:
            logger.error(f"❌ Ошибка шифрования: {e}")
            raise
    
    async def decrypt(self, encrypted_data: str) -> str:
        """
        Расшифровка данных
        
        Args:
            encrypted_data: Зашифрованные данные (base64)
        
        Returns:
            Расшифрованные данные
        """
        if self._key is None:
            await self.initialize()
        
        try:
            from cryptography.fernet import Fernet
            
            fernet = Fernet(self._key)
            
            # Расшифровка
            decrypted = await asyncio.to_thread(
                fernet.decrypt,
                encrypted_data.encode('utf-8')
            )
            
            # Возврат строки
            return decrypted.decode('utf-8')
        
        except Exception as e:
            logger.error(f"❌ Ошибка расшифровки: {e}")
            raise
    
    async def encrypt_file(self, input_path: Path, output_path: Path) -> None:
        """
        Шифрование файла
        
        Args:
            input_path: Путь к исходному файлу
            output_path: Путь к зашифрованному файлу
        """
        try:
            # Чтение файла
            content = await asyncio.to_thread(input_path.read_text, encoding='utf-8')
            
            # Шифрование
            encrypted = await self.encrypt(content)
            
            # Запись зашифрованного файла
            await asyncio.to_thread(output_path.write_text, encrypted, encoding='utf-8')
            
            logger.info(f"✅ Файл зашифрован: {input_path} -> {output_path}")
        
        except Exception as e:
            logger.error(f"❌ Ошибка шифрования файла: {e}")
            raise
    
    async def decrypt_file(self, input_path: Path, output_path: Path) -> None:
        """
        Расшифровка файла
        
        Args:
            input_path: Путь к зашифрованному файлу
            output_path: Путь к расшифрованному файлу
        """
        try:
            # Чтение зашифрованного файла
            encrypted = await asyncio.to_thread(input_path.read_text, encoding='utf-8')
            
            # Расшифровка
            decrypted = await self.decrypt(encrypted)
            
            # Запись расшифрованного файла
            await asyncio.to_thread(output_path.write_text, decrypted, encoding='utf-8')
            
            logger.info(f"✅ Файл расшифрован: {input_path} -> {output_path}")
        
        except Exception as e:
            logger.error(f"❌ Ошибка расшифровки файла: {e}")
            raise
    
    async def encrypt_config(self, config: Dict) -> str:
        """
        Шифрование конфигурации
        
        Args:
            config: Конфигурация (dict)
        
        Returns:
            Зашифрованная конфигурация (JSON string)
        """
        try:
            # Конвертация в JSON
            config_json = json.dumps(config, ensure_ascii=False)
            
            # Шифрование
            encrypted = await self.encrypt(config_json)
            
            return encrypted
        
        except Exception as e:
            logger.error(f"❌ Ошибка шифрования конфигурации: {e}")
            raise
    
    async def decrypt_config(self, encrypted_config: str) -> Dict:
        """
        Расшифровка конфигурации
        
        Args:
            encrypted_config: Зашифрованная конфигурация (JSON string)
        
        Returns:
            Расшифрованная конфигурация (dict)
        """
        try:
            # Расшифровка
            config_json = await self.decrypt(encrypted_config)
            
            # Парсинг JSON
            config = json.loads(config_json)
            
            return config
        
        except Exception as e:
            logger.error(f"❌ Ошибка расшифровки конфигурации: {e}")
            raise
    
    async def save_encrypted_config(self, config: Dict, path: Path) -> None:
        """
        Сохранение зашифрованной конфигурации
        
        Args:
            config: Конфигурация
            path: Путь для сохранения
        """
        try:
            encrypted = await self.encrypt_config(config)
            await asyncio.to_thread(path.write_text, encrypted, encoding='utf-8')
            logger.info(f"✅ Зашифрованная конфигурация сохранена: {path}")
        except Exception as e:
            logger.error(f"❌ Ошибка сохранения зашифрованной конфигурации: {e}")
            raise
    
    async def load_encrypted_config(self, path: Path) -> Dict:
        """
        Загрузка зашифрованной конфигурации
        
        Args:
            path: Путь к файлу
        
        Returns:
            Расшифрованная конфигурация
        """
        try:
            encrypted = await asyncio.to_thread(path.read_text, encoding='utf-8')
            config = await self.decrypt_config(encrypted)
            logger.info(f"✅ Зашифрованная конфигурация загружена: {path}")
            return config
        except Exception as e:
            logger.error(f"❌ Ошибка загрузки зашифрованной конфигурации: {e}")
            raise
    
    @property
    def is_initialized(self) -> bool:
        """Инициализирован ли менеджер"""
        return self._key is not None
    
    async def rotate_key(self) -> None:
        """Ротация ключа шифрования"""
        logger.warning("⚠️ Ротация ключа шифрования")
        
        # Генерация нового ключа
        await self._generate_key()
        
        logger.info("✅ Ключ шифрования ротирован")
        logger.warning("⚠️ Все зашифрованные данные нужно перешифровать новым ключом")
