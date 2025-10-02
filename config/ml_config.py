#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration settings for ML Components
"""

# Intent Classification Settings
INTENT_CONFIG = {
    'vectorizer': {
        'lowercase': True,
        'ngram_range': (1, 2),
        'max_features': 500
    },
    'classifier': {
        'max_iter': 1000,
        'random_state': 42
    },
    'intents': [
        'greeting',
        'book_class',
        'cancel_class',
        'show_schedule',
        'goodbye'
    ],
    'confidence_threshold': 0.3
}

# Entity Extraction Settings
ENTITY_CONFIG = {
    'date_patterns': {
        'relative': ['today', 'tomorrow', 'yesterday'],
        'weekdays': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'],
        'short_weekdays': ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    },
    'time_patterns': {
        '12_hour': r'\b(\d{1,2})\s*(am|pm)\b',
        '24_hour': r'\b(\d{1,2}):(\d{2})\b'
    }
}

# ML Model Paths
ML_PATHS = {
    'intent_model': 'gpt2/model/ml/intent_model.pkl',
    'training_data': 'data/ml/training_data.json',
    'logs': 'logs/ml/'
}
