#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dialog State Management
"""

from typing import Dict


class DialogState:
    """Dialog state management"""
    
    IDLE = 'idle'
    AWAITING_DATE = 'awaiting_date'
    AWAITING_TIME = 'awaiting_time'
    AWAITING_CANCEL_CONFIRMATION = 'awaiting_cancel_confirmation'
    
    def __init__(self):
        self.state = self.IDLE
        self.context: Dict = {}
    
    def reset(self):
        """Reset to idle state"""
        self.state = self.IDLE
        self.context = {}
    
    def set_state(self, state: str, **kwargs):
        """Set state with context"""
        self.state = state
        self.context.update(kwargs)
