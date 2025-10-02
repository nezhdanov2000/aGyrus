#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration settings for GPT-2 Components
"""

# GPT-2 Model Settings
GPT2_CONFIG = {
    'model_name': 'gpt2',
    'model_size': '124M',
    'max_length': 150,
    'temperature': 0.8,
    'top_k': 50,
    'top_p': 0.95,
    'repetition_penalty': 1.1,
    'enable_responses': False  # Will be True when GPT-2 is integrated
}

# Generation Settings
GENERATION_CONFIG = {
    'default_prompt_template': "User: {user_input}\nBot:",
    'max_new_tokens': 100,
    'do_sample': True,
    'pad_token_id': None,
    'eos_token_id': None
}

# GPT-2 Model Paths
GPT2_PATHS = {
    'model_dir': 'gpt2/model/124M/',
    'cache_dir': 'cache/gpt2/',
    'logs': 'logs/gpt2/'
}

# Response Templates for GPT-2 Integration
RESPONSE_TEMPLATES = {
    'greeting': "Hello! I'm here to help you book classes.",
    'book_class': "Sure! I'd be happy to help you book a class.",
    'cancel_class': "I'll help you cancel your booking.",
    'show_schedule': "Here's the available schedule:",
    'goodbye': "Goodbye! Have a great day!"
}
