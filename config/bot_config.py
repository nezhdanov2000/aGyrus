#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration settings for the Booking Bot
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
    ]
}

# Schedule Settings
SCHEDULE_CONFIG = {
    'available_slots': [
        '09:00', '10:00', '11:00', '12:00',
        '13:00', '14:00', '15:00', '16:00', '17:00'
    ],
    'working_days': [0, 1, 2, 3, 4],  # Monday to Friday
    'max_advance_booking_days': 30
}

# Response Settings
RESPONSE_CONFIG = {
    'default_user_id': 'user',
    'max_context_history': 5,
    'enable_gpt2_responses': False  # Will be True when GPT-2 is integrated
}

# GPT-2 Settings (for future integration)
GPT2_CONFIG = {
    'model_name': 'gpt2',
    'max_length': 150,
    'temperature': 0.8,
    'top_k': 50,
    'top_p': 0.95,
    'enable_responses': False
}

# File Paths
PATHS = {
    'intent_model': 'gpt2/model/intent_model.pkl',
    'gpt2_model': 'gpt2/model/',
    'logs': 'logs/',
    'data': 'data/'
}
