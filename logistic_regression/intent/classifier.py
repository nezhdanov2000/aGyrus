#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Intent Classification using Logistic Regression + TF-IDF
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle
from typing import List, Tuple
import sys
import os

# Add config path to imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'config'))
from ml_config import INTENT_CONFIG


class IntentClassifier:
    """Intent classification using Logistic Regression + TF-IDF"""
    
    def __init__(self):
        # Use configuration from ml_config
        vectorizer_config = INTENT_CONFIG['vectorizer']
        classifier_config = INTENT_CONFIG['classifier']
        
        self.vectorizer = TfidfVectorizer(
            lowercase=vectorizer_config['lowercase'],
            ngram_range=vectorizer_config['ngram_range'],
            max_features=vectorizer_config['max_features']
        )
        self.classifier = LogisticRegression(
            max_iter=classifier_config['max_iter'],
            random_state=classifier_config['random_state']
        )
        self.intents = INTENT_CONFIG['intents']
        self.is_trained = False
    
    def get_training_data(self) -> Tuple[List[str], List[str]]:
        """Training data for 5 intents"""
        
        # Training examples for each intent
        training_data = {
            'greeting': [
                'hello', 'hi', 'hey', 'good morning', 'good afternoon',
                'good evening', 'greetings', 'hi there', 'hello there',
                'hey there', 'whats up', 'howdy', 'yo', 'sup',
                'helo', 'hlo', 'helllo', 'hii', 'heyy', 'hallo',
                'privet', 'привет', 'zdravstvuyte', 'здравствуйте'
            ],
            'book_class': [
                'i want to book a class', 'book a class', 'schedule a class',
                'i would like to schedule', 'can i book', 'i need to book',
                'reserve a class', 'make a booking', 'book me in',
                'i want to join a class', 'sign me up', 'register for class',
                'i want to attend', 'schedule me for', 'book appointment',
                'book', 'booking', 'reserve', 'schedule', 'sign up', 'join',
                'register', 'enroll', 'book me', 'i want to book', 'need booking'
            ],
            'cancel_class': [
                'cancel my class', 'i want to cancel', 'cancel booking',
                'i need to cancel', 'cancel my appointment', 'remove booking',
                'i cant make it', 'cancel my session', 'i want to cancel my class',
                'unbook', 'cancel reservation', 'i need to unregister',
                'remove my booking', 'cancel my reservation', 'cancl', 'cancle',
                'cancel', 'cncl', 'canc', 'unbook me', 'remove me', 'delete booking',
                'scratch that', 'nevermind', 'dont want it', 'change my mind'
            ],
            'show_schedule': [
                'show schedule', 'what classes are available', 'show me schedule',
                'what time slots', 'available times', 'when can i book',
                'show me available classes', 'what are the timings',
                'display schedule', 'view schedule', 'see schedule',
                'available slots', 'free slots', 'open times', 'schedule',
                'times', 'slots', 'availability', 'whats available', 'show times',
                'when available', 'free times', 'open slots'
            ],
            'goodbye': [
                'bye', 'goodbye', 'see you', 'see you later', 'talk to you later',
                'have a good day', 'have a nice day', 'farewell', 'take care',
                'catch you later', 'until next time', 'gotta go', 'im leaving',
                'thanks bye', 'ok bye'
            ]
        }
        
        texts = []
        labels = []
        
        for intent, examples in training_data.items():
            texts.extend(examples)
            labels.extend([intent] * len(examples))
        
        return texts, labels
    
    def train(self):
        """Train the intent classifier"""
        print("Training intent classifier...")
        
        texts, labels = self.get_training_data()
        
        # Vectorize texts
        X = self.vectorizer.fit_transform(texts)
        y = np.array(labels)
        
        # Train classifier
        self.classifier.fit(X, y)
        self.is_trained = True
        
        print(f"✅ Trained on {len(texts)} examples across {len(self.intents)} intents")
    
    def predict(self, text: str) -> Tuple[str, float]:
        """
        Predict intent for given text
        Returns: (intent, confidence)
        """
        if not self.is_trained:
            raise ValueError("Classifier not trained yet!")
        
        X = self.vectorizer.transform([text])
        intent = self.classifier.predict(X)[0]
        probabilities = self.classifier.predict_proba(X)[0]
        confidence = max(probabilities)
        
        return intent, confidence
    
    def save(self, filepath='intent_model.pkl'):
        """Save trained model"""
        with open(filepath, 'wb') as f:
            pickle.dump({
                'vectorizer': self.vectorizer,
                'classifier': self.classifier,
                'intents': self.intents
            }, f)
    
    def load(self, filepath='intent_model.pkl'):
        """Load trained model"""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            self.vectorizer = data['vectorizer']
            self.classifier = data['classifier']
            self.intents = data['intents']
            self.is_trained = True
