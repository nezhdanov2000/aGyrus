#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Intent classifier using Logistic Regression
Classifies user messages into intents based on chatbot.js functionality
"""

import pickle
import re
import json
import os
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from nlp_utils import TextNormalizer

def load_training_data():
    """Load training data from JSON files"""
    script_dir = Path(__file__).parent
    data_dir = (script_dir / '..' / 'training_data').resolve()
    
    training_data = []
    
    # Load all JSON files from training_data directory (excluding typo_corrections.json)
    for json_file in data_dir.glob('*.json'):
        if json_file.name == 'typo_corrections.json':
            continue  # Skip typo corrections file
            
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            intent = data['intent']
            examples = data['examples']
            
            for example in examples:
                training_data.append((example, intent))
    
    return training_data

def preprocess_text(text):
    """Preprocess text for classification"""
    # Use TextNormalizer for better preprocessing including typo correction
    text = TextNormalizer.normalize(text)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def train_logistic_regression():
    """Train Logistic Regression model"""
    training_data = load_training_data()
    texts = [preprocess_text(text) for text, _ in training_data]
    labels = [label for _, label in training_data]
    
    model = Pipeline([
        ('tfidf', TfidfVectorizer(
            ngram_range=(1, 3),
            max_features=500,
            min_df=1,
            stop_words='english'
        )),
        ('clf', LogisticRegression(
            random_state=42,
            max_iter=1000,
            C=1.0,
            class_weight='balanced'
        ))
    ])
    
    model.fit(texts, labels)
    return model

def train_decision_tree():
    """Train Decision Tree model"""
    training_data = load_training_data()
    texts = [preprocess_text(text) for text, _ in training_data]
    labels = [label for _, label in training_data]
    
    model = Pipeline([
        ('tfidf', TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=300,
            min_df=2,
            stop_words='english'
        )),
        ('clf', DecisionTreeClassifier(
            random_state=42,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2
        ))
    ])
    
    model.fit(texts, labels)
    return model

def train_knn():
    """Train K-Nearest Neighbors model"""
    training_data = load_training_data()
    texts = [preprocess_text(text) for text, _ in training_data]
    labels = [label for _, label in training_data]
    
    model = Pipeline([
        ('tfidf', TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=200,
            min_df=1,
            stop_words='english'
        )),
        ('clf', KNeighborsClassifier(
            n_neighbors=5,
            weights='distance',
            metric='cosine'
        ))
    ])
    
    model.fit(texts, labels)
    return model

def train_model(model_type='logistic'):
    """Train the intent classifier with specified model type"""
    if model_type == 'logistic':
        return train_logistic_regression()
    elif model_type == 'decision_tree':
        return train_decision_tree()
    elif model_type == 'knn':
        return train_knn()
    else:
        raise ValueError("Model type must be 'logistic', 'decision_tree', or 'knn'")

def save_model(model, model_type='logistic', filepath=None):
    """Save trained model to file"""
    if filepath is None:
        filename = f'intent_model_{model_type}.pkl'
        filepath = (Path(__file__).parent / '..' / 'models' / filename).resolve()
    with open(filepath, 'wb') as f:
        pickle.dump(model, f)

def load_model(model_type='logistic', filepath=None):
    """Load trained model from file"""
    if filepath is None:
        filename = f'intent_model_{model_type}.pkl'
        filepath = (Path(__file__).parent / '..' / 'models' / filename).resolve()
    with open(filepath, 'rb') as f:
        return pickle.load(f)

def predict_intent(model, text):
    """Predict intent for given text"""
    processed_text = preprocess_text(text)
    intent = model.predict([processed_text])[0]
    probabilities = model.predict_proba([processed_text])[0]
    confidence = max(probabilities)
    
    return {
        'intent': intent,
        'confidence': float(confidence)
    }

if __name__ == '__main__':
    import os
    import sys
    
    # Parse command line arguments
    model_type = 'logistic'  # Default model
    if len(sys.argv) > 1 and sys.argv[1] in ['logistic', 'decision_tree', 'knn']:
        model_type = sys.argv[1]
        sys.argv.pop(1)  # Remove model type from args
    
    # Get script directory
    script_dir = Path(__file__).parent
    model_filename = f'intent_model_{model_type}.pkl'
    model_path = (script_dir / '..' / 'models' / model_filename).resolve()
    
    # Check if model exists
    if not os.path.exists(model_path):
        print(f"Training new {model_type} model...")
        model = train_model(model_type)
        save_model(model, model_type, model_path)
        print(f"Model saved to {model_path}")
    else:
        print(f"Loading existing {model_type} model...")
        model = load_model(model_type, model_path)
    
    # If text provided as argument, classify it
    if len(sys.argv) > 1:
        text = ' '.join(sys.argv[1:])
        result = predict_intent(model, text)
        print(f"Model: {model_type}")
        print(f"Text: {text}")
        print(f"Intent: {result['intent']}")
        print(f"Confidence: {result['confidence']:.2%}")
    else:
        # Interactive mode
        print(f"\nIntent Classifier Ready! (Model: {model_type})")
        print("Enter text to classify (or 'quit' to exit):\n")
        
        while True:
            try:
                text = input("> ").strip()
                if text.lower() in ['quit', 'exit', 'q']:
                    break
                if not text:
                    continue
                
                result = predict_intent(model, text)
                print(f"Intent: {result['intent']} (confidence: {result['confidence']:.2%})\n")
            except KeyboardInterrupt:
                print("\nBye!")
                break

