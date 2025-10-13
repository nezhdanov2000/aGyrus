#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NLP utilities for date/time parsing and text processing
"""

import re
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from difflib import get_close_matches
from pathlib import Path


class DateTimeParser:
    """Parse natural language dates and times"""
    
    # Days of week mapping
    WEEKDAYS = {
        'monday': 0, 'mon': 0,
        'tuesday': 1, 'tue': 1,
        'wednesday': 2, 'wed': 2,
        'thursday': 3, 'thu': 3,
        'friday': 4, 'fri': 4,
        'saturday': 5, 'sat': 5,
        'sunday': 6, 'sun': 6
    }
    
    # Relative date keywords
    RELATIVE_DATES = {
        'today': 0,
        'tomorrow': 1,
        'yesterday': -1,
        'day after tomorrow': 2
    }
    
    @staticmethod
    def parse_date(text: str) -> Optional[str]:
        """
        Parse date from natural language text
        Returns date in YYYY-MM-DD format or None
        """
        text_lower = text.lower()
        today = datetime.now()
        
        # Check for explicit date format (YYYY-MM-DD, DD.MM.YYYY, DD/MM/YYYY)
        date_patterns = [
            r'(\d{4})-(\d{2})-(\d{2})',  # 2025-10-15
            r'(\d{2})\.(\d{2})\.(\d{4})',  # 15.10.2025
            r'(\d{2})/(\d{2})/(\d{4})',  # 15/10/2025
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                if '-' in pattern:
                    year, month, day = match.groups()
                else:
                    day, month, year = match.groups()
                try:
                    date_obj = datetime(int(year), int(month), int(day))
                    return date_obj.strftime('%Y-%m-%d')
                except ValueError:
                    continue
        
        # Check for relative dates
        for keyword, delta in DateTimeParser.RELATIVE_DATES.items():
            if keyword in text_lower:
                target_date = today + timedelta(days=delta)
                return target_date.strftime('%Y-%m-%d')
        
        # Check for weekdays
        for day_name, day_num in DateTimeParser.WEEKDAYS.items():
            if day_name in text_lower:
                # Find next occurrence of this weekday
                current_weekday = today.weekday()
                days_ahead = day_num - current_weekday
                if days_ahead <= 0:  # Target day already passed this week
                    days_ahead += 7
                target_date = today + timedelta(days=days_ahead)
                return target_date.strftime('%Y-%m-%d')
        
        # Check for "next week", "this week"
        if 'next week' in text_lower:
            target_date = today + timedelta(days=7)
            return target_date.strftime('%Y-%m-%d')
        
        return None
    
    @staticmethod
    def parse_time(text: str) -> Optional[str]:
        """
        Parse time from natural language text
        Returns time in HH:MM format or None
        """
        text_lower = text.lower()
        
        # Pattern for HH:MM or HH.MM
        time_pattern = r'(\d{1,2})[:.](\d{2})'
        match = re.search(time_pattern, text)
        if match:
            hour, minute = match.groups()
            hour = int(hour)
            minute = int(minute)
            if 0 <= hour < 24 and 0 <= minute < 60:
                return f"{hour:02d}:{minute:02d}"
        
        # Pattern for "at 3", "at 3pm"
        hour_pattern = r'(?:at)\s+(\d{1,2})'
        match = re.search(hour_pattern, text_lower)
        if match:
            hour = int(match.group(1))
            # Check for am/pm
            if 'pm' in text_lower and hour < 12:
                hour += 12
            elif 'am' in text_lower and hour == 12:
                hour = 0
            if 0 <= hour < 24:
                return f"{hour:02d}:00"
        
        # Morning/afternoon/evening keywords
        time_keywords = {
            'morning': '09:00',
            'afternoon': '14:00',
            'evening': '18:00',
            'night': '20:00'
        }
        
        for keyword, time_val in time_keywords.items():
            if keyword in text_lower:
                return time_val
        
        return None


class TextNormalizer:
    """Normalize and clean text"""
    
    _typo_corrections = None
    
    @classmethod
    def _load_typo_corrections(cls):
        """Load typo corrections from JSON file"""
        if cls._typo_corrections is None:
            try:
                script_dir = Path(__file__).parent
                typo_file = (script_dir / '..' / 'training_data' / 'typo_corrections.json').resolve()
                with open(typo_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    cls._typo_corrections = data['corrections']
            except (FileNotFoundError, KeyError, json.JSONDecodeError):
                # Fallback to empty dict if file not found or invalid
                cls._typo_corrections = {}
        return cls._typo_corrections
    
    @classmethod
    def fix_typos(cls, text: str) -> str:
        """Fix common typos in text"""
        typo_corrections = cls._load_typo_corrections()
        words = text.split()
        corrected_words = []
        
        for word in words:
            # Check for exact match in typo corrections dictionary
            if word.lower() in typo_corrections:
                corrected_words.append(typo_corrections[word.lower()])
            else:
                corrected_words.append(word)
        
        return ' '.join(corrected_words)
    
    @staticmethod
    def normalize(text: str) -> str:
        """Normalize text for processing"""
        # Convert to lowercase
        text = text.lower()
        # Fix common typos
        text = TextNormalizer.fix_typos(text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    @staticmethod
    def extract_quoted_text(text: str) -> Optional[str]:
        """Extract text in quotes"""
        match = re.search(r'["\'](.+?)["\']', text)
        return match.group(1) if match else None


def extract_entities(text: str) -> Dict[str, Any]:
    """
    Extract all entities from text
    Returns dict with found entities
    """
    entities = {
        'date': DateTimeParser.parse_date(text),
        'time': DateTimeParser.parse_time(text),
        'original_text': text
    }
    
    return entities


if __name__ == '__main__':
    # Test cases
    test_cases = [
        "Find tutor for tomorrow at 3pm",
        "Show schedule for next week",
        "Book class on 2025-10-20 at 14:30",
        "Tomorrow morning appointment",
        "Friday evening appointment"
    ]
    
    print("Date/Time Extraction Tests:\n")
    for test in test_cases:
        entities = extract_entities(test)
        print(f"Text: {test}")
        print(f"  Date: {entities['date']}")
        print(f"  Time: {entities['time']}\n")

