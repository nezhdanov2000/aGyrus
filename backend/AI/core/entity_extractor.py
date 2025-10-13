#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entity extractor for chatbot
Extracts: tutor names, subjects, dates, times
"""

import re
import sys
import json
from typing import Dict, List, Any, Optional
from nlp_utils import DateTimeParser, TextNormalizer


class EntityExtractor:
    """Extract entities from user messages"""
    
    # Common subjects/courses
    SUBJECTS = {
        'math': ['math', 'mathematics', 'algebra', 'geometry'],
        'english': ['english', 'eng'],
        'physics': ['physics', 'phys'],
        'chemistry': ['chemistry', 'chem'],
        'biology': ['biology', 'bio'],
        'history': ['history', 'hist'],
        'programming': ['programming', 'code', 'coding', 'python', 'java', 'javascript'],
        'literature': ['literature', 'lit'],
        'russian': ['russian', 'rus'],
        'spanish': ['spanish', 'spa'],
        'french': ['french', 'fra'],
        'german': ['german', 'ger']
    }
    
    def __init__(self):
        self.date_parser = DateTimeParser()
        self.normalizer = TextNormalizer()
    
    def extract_subject(self, text: str) -> Optional[str]:
        """Extract subject/course from text"""
        text_lower = text.lower()
        
        for subject, keywords in self.SUBJECTS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return subject
        
        return None
    
    def extract_tutor_name(self, text: str) -> Optional[str]:
        """
        Extract tutor name from text
        Looks for capitalized words that might be names
        """
        # Pattern for names: Capitalized words (2-15 chars)
        # Example: "John Smith", "Maria", "Ivan Petrov"
        name_pattern = r'\b([A-Z][a-z]{1,14}(?:\s+[A-Z][a-z]{1,14})?)\b'
        
        matches = re.findall(name_pattern, text)
        
        # Filter out common false positives
        exclude_words = {'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
                        'January', 'February', 'March', 'April', 'May', 'June', 'July', 
                        'August', 'September', 'October', 'November', 'December',
                        'Find', 'Search', 'Show', 'Book', 'Cancel', 'View', 'Display', 'Looking',
                        'Need', 'Want'}
        
        for match in matches:
            if match not in exclude_words:
                return match
        
        return None
    
    def extract_action_type(self, text: str) -> Optional[str]:
        """Detect specific action keywords"""
        text_lower = text.lower()
        
        # Booking keywords
        if any(word in text_lower for word in ['book', 'reserve', 'schedule', 'appoint']):
            return 'book'
        
        # Cancel keywords
        if any(word in text_lower for word in ['cancel', 'remove', 'delete', 'abort']):
            return 'cancel'
        
        # Show/view keywords
        if any(word in text_lower for word in ['show', 'view', 'display', 'list']):
            return 'view'
        
        return None
    
    def extract_all(self, text: str) -> Dict[str, Any]:
        """Extract all entities from text"""
        normalized = self.normalizer.normalize(text)
        
        entities = {
            'subject': self.extract_subject(text),
            'tutor_name': self.extract_tutor_name(text),
            'date': self.date_parser.parse_date(text),
            'time': self.date_parser.parse_time(text),
            'action': self.extract_action_type(text),
            'original_text': text
        }
        
        # Remove None values for cleaner output
        return {k: v for k, v in entities.items() if v is not None}


def extract_entities_from_message(text: str) -> Dict[str, Any]:
    """Main function to extract entities"""
    extractor = EntityExtractor()
    return extractor.extract_all(text)


if __name__ == '__main__':
    # Command line interface
    if len(sys.argv) > 1:
        text = ' '.join(sys.argv[1:])
        entities = extract_entities_from_message(text)
        print(json.dumps(entities, ensure_ascii=False, indent=2))
    else:
        # Test mode
        test_cases = [
            "Find math tutor for tomorrow at 3pm",
            "Book lesson with John Smith on Monday at 15:00",
            "Show John Smith's schedule for next week",
            "Cancel my appointment with Maria on Friday",
            "Looking for English tutor for tomorrow morning",
            "Book physics class for 2025-10-20 at 14:30"
        ]
        
        print("Entity Extraction Tests:\n")
        for test in test_cases:
            entities = extract_entities_from_message(test)
            print(f"Text: {test}")
            print(f"Entities: {json.dumps(entities, ensure_ascii=False, indent=2)}\n")

