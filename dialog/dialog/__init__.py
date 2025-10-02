"""
Dialog Management Module

Модуль для управления состоянием диалога и расписанием занятий
"""

from .state import DialogState
from .schedule import ScheduleManager

__all__ = ['DialogState', 'ScheduleManager']
