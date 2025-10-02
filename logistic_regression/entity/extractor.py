#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entity Extraction for Date & Time from user input
"""

import re
from datetime import datetime, timedelta
from typing import Optional
import sys
import os

# Add config path to imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'config'))
from ml_config import ENTITY_CONFIG


class EntityExtractor:
    """Extract date and time from user input"""
    
    def __init__(self):
        self.days_of_week = {
            'monday': 0, 'tuesday': 1, 'wednesday': 2,
            'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6,
            'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3,
            'fri': 4, 'sat': 5, 'sun': 6
        }
    
    def extract_date(self, text: str) -> Optional[str]:
        """Extract date from text"""
        text_lower = text.lower()
        today = datetime.now()
        
        # Check for "today"
        if 'today' in text_lower:
            return today.strftime('%Y-%m-%d')
        
        # Check for "tomorrow"
        if 'tomorrow' in text_lower:
            return (today + timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Check for day of week
        for day_name, day_num in self.days_of_week.items():
            if day_name in text_lower:
                days_ahead = (day_num - today.weekday()) % 7
                if days_ahead == 0:
                    days_ahead = 7  # Next week
                target_date = today + timedelta(days=days_ahead)
                return target_date.strftime('%Y-%m-%d')
        
        # Check for date pattern (YYYY-MM-DD, DD/MM/YYYY, etc.)
        date_patterns = [
            r'(\d{4}-\d{2}-\d{2})',  # 2025-10-05
            r'(\d{2}/\d{2}/\d{4})',  # 05/10/2025
            r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})',  # 5/10/2025
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        
        return None
    
    def extract_time(self, text: str) -> Optional[str]:
        """Extract time from text"""
        text_lower = text.lower()
        
        # Pattern: 9am, 9:00am, 9:00, 14:00, etc.
        time_patterns = [
            r'(\d{1,2}):(\d{2})\s*(am|pm)?',  # 9:00am, 14:30
            r'(\d{1,2})\s*(am|pm)',  # 9am, 9pm
        ]
        
        for pattern in time_patterns:
            match = re.search(pattern, text_lower)
            if match:
                groups = match.groups()
                hour = int(groups[0])
                
                # Check if we have minutes
                if len(groups) >= 2 and groups[1] and groups[1].isdigit():
                    minute = groups[1]
                else:
                    minute = '00'
                
                # Check for AM/PM
                period = None
                if len(groups) >= 3:
                    period = groups[2]
                elif len(groups) >= 2 and groups[1] in ['am', 'pm']:
                    period = groups[1]
                
                # Convert to 24-hour format
                if period:
                    if period == 'pm' and hour < 12:
                        hour += 12
                    elif period == 'am' and hour == 12:
                        hour = 0
                
                return f"{hour:02d}:{minute}"
        
        return None
