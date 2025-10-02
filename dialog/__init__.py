"""
Dialog Components Package

Компоненты диалоговой системы, используемые как ML, так и GPT-2 частями:
- Управление диалогом и состоянием
- Генерация ответов
- Общие утилиты
"""

from .dialog import DialogState, ScheduleManager
from .responses import ResponseGenerator

__version__ = "1.0.0"
__author__ = "Booking Bot Team"

__all__ = ['DialogState', 'ScheduleManager', 'ResponseGenerator']
