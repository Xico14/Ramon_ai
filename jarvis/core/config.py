"""
Конфигурация Джарвиса
"""
import yaml
from pathlib import Path
from typing import Any


def load_config(config_path: str) -> dict[str, Any]:
    """Загрузка конфигурации из YAML файла"""
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Конфигурация не найдена: {config_path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    return config


def validate_config(config: dict) -> bool:
    """Валидация конфигурации"""
    required_sections = ['llm', 'audio', 'vad', 'stt', 'tts', 'fsm', 'event_bus']
    
    for section in required_sections:
        if section not in config:
            raise ValueError(f"Отсутствует секция конфигурации: {section}")
    
    return True
