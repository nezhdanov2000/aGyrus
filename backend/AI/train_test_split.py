#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Train-Test Split Implementation
Separates data into training and testing sets (80% train, 20% test)
"""

import json
import re
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import numpy as np

def load_training_data():
    """Load training data from JSON files"""
    script_dir = Path(__file__).parent
    data_dir = (script_dir / 'training_data').resolve()
    
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
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def split_data():
    """
    Split data into features (X) and target (y), then into train/test sets
    Returns: X_train, X_test, y_train, y_test
    """
    print("🔄 Loading training data...")
    training_data = load_training_data()
    
    # Separate features (X) and target (y)
    X = [preprocess_text(text) for text, _ in training_data]
    y = [label for _, label in training_data]
    
    print(f"📊 Total examples: {len(X)}")
    print(f"📊 Total features (texts): {len(X)}")
    print(f"📊 Total targets (labels): {len(y)}")
    
    # Check class distribution
    unique_labels, counts = np.unique(y, return_counts=True)
    print(f"\n📈 Class distribution:")
    for label, count in zip(unique_labels, counts):
        percentage = (count / len(y)) * 100
        print(f"  {label}: {count} examples ({percentage:.1f}%)")
    
    # Split into train/test sets (80% train, 20% test)
    print(f"\n🔀 Splitting data into train/test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=0.2,           # 20% for testing
        random_state=42,         # For reproducibility
        stratify=y               # Maintain class distribution
    )
    
    print(f"✅ Split completed:")
    print(f"  📚 Training set: {len(X_train)} examples ({len(X_train)/len(X)*100:.1f}%)")
    print(f"  🧪 Test set: {len(X_test)} examples ({len(X_test)/len(X)*100:.1f}%)")
    
    # Check train/test class distribution
    print(f"\n📊 Training set class distribution:")
    train_unique, train_counts = np.unique(y_train, return_counts=True)
    for label, count in zip(train_unique, train_counts):
        percentage = (count / len(y_train)) * 100
        print(f"  {label}: {count} examples ({percentage:.1f}%)")
    
    print(f"\n📊 Test set class distribution:")
    test_unique, test_counts = np.unique(y_test, return_counts=True)
    for label, count in zip(test_unique, test_counts):
        percentage = (count / len(y_test)) * 100
        print(f"  {label}: {count} examples ({percentage:.1f}%)")
    
    return X_train, X_test, y_train, y_test

def train_and_evaluate_model(X_train, X_test, y_train, y_test, model_name="Logistic Regression"):
    """
    Train a model on training data and evaluate on test data
    """
    print(f"\n🤖 Training {model_name} model...")
    
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 3),
        max_features=500,
        min_df=1,
        stop_words='english'
    )
    
    # Transform training data
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    print(f"📊 TF-IDF Features: {X_train_tfidf.shape[1]} features")
    print(f"📊 Training shape: {X_train_tfidf.shape}")
    print(f"📊 Test shape: {X_test_tfidf.shape}")
    
    # Train model (using Logistic Regression as example)
    from sklearn.linear_model import LogisticRegression
    model = LogisticRegression(
        random_state=42,
        max_iter=1000,
        C=1.0,
        class_weight='balanced'
    )
    
    model.fit(X_train_tfidf, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test_tfidf)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"🎯 Model Accuracy: {accuracy:.3f} ({accuracy*100:.1f}%)")
    
    # Classification report
    print(f"\n📋 Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # Confusion Matrix
    print(f"\n🔍 Confusion Matrix:")
    cm = confusion_matrix(y_test, y_pred)
    labels = model.classes_
    
    # Print header
    print("Predicted:", end="")
    for label in labels:
        print(f"{label:>12}", end="")
    print()
    
    # Print matrix
    for i, true_label in enumerate(labels):
        print(f"Actual {true_label:>8}:", end="")
        for j, pred_label in enumerate(labels):
            print(f"{cm[i][j]:>12}", end="")
        print()
    
    return model, vectorizer, accuracy

def main():
    """Main function to demonstrate train/test split"""
    print("🚀 Train-Test Split Implementation")
    print("=" * 50)
    
    # Split the data
    X_train, X_test, y_train, y_test = split_data()
    
    # Train and evaluate model
    model, vectorizer, accuracy = train_and_evaluate_model(
        X_train, X_test, y_train, y_test
    )
    
    # Test some examples
    print(f"\n🧪 Testing with sample predictions:")
    test_samples = [
        "hello there",
        "find math tutor", 
        "show my bookings",
        "cancel my appointment"
    ]
    
    for sample in test_samples:
        processed = preprocess_text(sample)
        X_sample = vectorizer.transform([processed])
        prediction = model.predict(X_sample)[0]
        confidence = model.predict_proba(X_sample).max()
        print(f"  '{sample}' → {prediction} (confidence: {confidence:.3f})")
    
    print(f"\n✅ Train-Test Split Analysis Complete!")
    print(f"📊 Final Model Performance: {accuracy:.3f} accuracy")

if __name__ == '__main__':
    main()
