#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Exploratory Data Analysis (EDA) for AI Training Data
Uses only standard Python libraries (no external dependencies)
"""

import json
import sys
from pathlib import Path
from collections import Counter, defaultdict
import re
import math

class SimpleEDAAnalyzer:
    def __init__(self, data_dir="training_data"):
        """Initialize EDA analyzer with training data directory"""
        self.data_dir = Path(__file__).parent / data_dir
        self.data = {}
        self.stats = {}
        
    def load_training_data(self):
        """Load all training data files"""
        print("📊 Loading training data...")
        
        # Load all JSON files
        json_files = list(self.data_dir.glob("*.json"))
        
        for file_path in json_files:
            if file_path.name == "typo_corrections.json":
                continue  # Skip typo corrections as it's not training data
                
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Extract intent name from filename
            intent_name = file_path.stem
            
            # Convert to list of examples
            if isinstance(data, list):
                examples = data
            else:
                examples = data.get('examples', [])
            
            self.data[intent_name] = examples
            print(f"  ✓ Loaded {len(examples)} examples for '{intent_name}'")
        
        total_examples = sum(len(examples) for examples in self.data.values())
        print(f"📈 Total intents: {len(self.data)}")
        print(f"📈 Total examples: {total_examples}")
        
    def analyze_text_lengths(self):
        """Analyze text length distribution"""
        print("\n📏 TEXT LENGTH ANALYSIS")
        print("="*50)
        
        all_lengths = []
        intent_lengths = defaultdict(list)
        
        for intent, examples in self.data.items():
            for example in examples:
                length = len(example)
                all_lengths.append(length)
                intent_lengths[intent].append(length)
        
        # Overall statistics
        all_lengths.sort()
        n = len(all_lengths)
        
        print(f"Overall Text Length Statistics:")
        print(f"  Total examples: {n}")
        print(f"  Minimum length: {min(all_lengths)} characters")
        print(f"  Maximum length: {max(all_lengths)} characters")
        print(f"  Average length: {sum(all_lengths)/n:.1f} characters")
        print(f"  Median length: {all_lengths[n//2]} characters")
        
        # By intent
        print(f"\nText Length by Intent:")
        for intent, lengths in intent_lengths.items():
            lengths.sort()
            avg_len = sum(lengths)/len(lengths)
            median_len = lengths[len(lengths)//2]
            print(f"  {intent}:")
            print(f"    Examples: {len(lengths)}")
            print(f"    Average: {avg_len:.1f} characters")
            print(f"    Median: {median_len} characters")
            print(f"    Range: {min(lengths)}-{max(lengths)} characters")
        
        self.stats['text_lengths'] = {
            'overall': all_lengths,
            'by_intent': dict(intent_lengths)
        }
        
    def analyze_class_distribution(self):
        """Analyze class distribution and imbalance"""
        print("\n📊 CLASS DISTRIBUTION ANALYSIS")
        print("="*50)
        
        intent_counts = {intent: len(examples) for intent, examples in self.data.items()}
        total = sum(intent_counts.values())
        
        print(f"Class Distribution:")
        print(f"{'Intent':<20} {'Count':<8} {'Percentage':<12} {'Bar'}")
        print("-" * 50)
        
        max_count = max(intent_counts.values())
        
        for intent, count in sorted(intent_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total) * 100
            bar_length = int((count / max_count) * 20)
            bar = "█" * bar_length + "░" * (20 - bar_length)
            print(f"{intent:<20} {count:<8} {percentage:<11.1f}% {bar}")
        
        # Imbalance analysis
        min_count = min(intent_counts.values())
        imbalance_ratio = max_count / min_count
        
        print(f"\nClass Imbalance Analysis:")
        print(f"  Largest class: {max_count} examples")
        print(f"  Smallest class: {min_count} examples")
        print(f"  Imbalance ratio: {imbalance_ratio:.2f}")
        
        if imbalance_ratio > 2:
            print(f"  ⚠️  High class imbalance detected!")
        else:
            print(f"  ✅ Classes are reasonably balanced")
            
        self.stats['class_distribution'] = intent_counts
        
    def analyze_word_frequency(self):
        """Analyze word frequency patterns"""
        print("\n🔤 WORD FREQUENCY ANALYSIS")
        print("="*50)
        
        all_words = []
        intent_words = defaultdict(list)
        
        for intent, examples in self.data.items():
            for example in examples:
                words = re.findall(r'\b\w+\b', example.lower())
                all_words.extend(words)
                intent_words[intent].extend(words)
        
        # Overall word frequency
        word_counts = Counter(all_words)
        most_common = word_counts.most_common(15)
        
        print(f"Top 15 Most Common Words (Overall):")
        print(f"{'Rank':<6} {'Word':<15} {'Count':<8} {'Percentage'}")
        print("-" * 45)
        
        total_words = len(all_words)
        for i, (word, count) in enumerate(most_common, 1):
            percentage = (count / total_words) * 100
            print(f"{i:<6} {word:<15} {count:<8} {percentage:.1f}%")
        
        # Word frequency by intent
        print(f"\nTop 10 Words by Intent:")
        for intent, words in intent_words.items():
            word_counts_intent = Counter(words)
            most_common_intent = word_counts_intent.most_common(10)
            
            print(f"\n{intent}:")
            for word, count in most_common_intent:
                percentage = (count / len(words)) * 100
                print(f"  {word}: {count} ({percentage:.1f}%)")
        
        self.stats['word_frequency'] = {
            'overall': dict(word_counts),
            'by_intent': {intent: dict(Counter(words)) for intent, words in intent_words.items()}
        }
        
    def analyze_text_features(self):
        """Analyze various text features"""
        print("\n🔍 TEXT FEATURE ANALYSIS")
        print("="*50)
        
        features = defaultdict(lambda: defaultdict(int))
        
        for intent, examples in self.data.items():
            for example in examples:
                # Basic features
                features[intent]['total_texts'] += 1
                features[intent]['total_chars'] += len(example)
                features[intent]['total_words'] += len(example.split())
                features[intent]['total_sentences'] += len([s for s in example.split('.') if s.strip()])
                
                # Special features
                if re.search(r'\d', example):
                    features[intent]['has_numbers'] += 1
                if re.search(r'[A-Z]', example):
                    features[intent]['has_capitals'] += 1
                if re.search(r'[^\w\s]', example):
                    features[intent]['has_special_chars'] += 1
                if example and example[0].isupper():
                    features[intent]['starts_capital'] += 1
        
        print(f"Text Features by Intent:")
        print(f"{'Intent':<20} {'Avg Chars':<10} {'Avg Words':<10} {'Has Numbers':<12} {'Has Capitals':<13}")
        print("-" * 70)
        
        for intent, feat in features.items():
            total = feat['total_texts']
            avg_chars = feat['total_chars'] / total
            avg_words = feat['total_words'] / total
            has_numbers_pct = (feat['has_numbers'] / total) * 100
            has_capitals_pct = (feat['has_capitals'] / total) * 100
            
            print(f"{intent:<20} {avg_chars:<10.1f} {avg_words:<10.1f} {has_numbers_pct:<11.1f}% {has_capitals_pct:<12.1f}%")
        
        self.stats['text_features'] = dict(features)
        
    def create_simple_visualizations(self):
        """Create simple text-based visualizations"""
        print("\n📈 SIMPLE VISUALIZATIONS")
        print("="*50)
        
        # Text length histogram
        print("Text Length Distribution (Histogram):")
        all_lengths = self.stats['text_lengths']['overall']
        
        # Create bins
        min_len, max_len = min(all_lengths), max(all_lengths)
        bin_size = max(1, (max_len - min_len) // 10)
        bins = list(range(min_len, max_len + bin_size, bin_size))
        
        # Count values in each bin
        histogram = defaultdict(int)
        for length in all_lengths:
            bin_idx = min((length - min_len) // bin_size, len(bins) - 1)
            histogram[bin_idx] += 1
        
        # Print histogram
        max_count = max(histogram.values()) if histogram else 1
        for i in range(len(bins) - 1):
            count = histogram.get(i, 0)
            bar_length = int((count / max_count) * 30)
            bar = "█" * bar_length
            bin_range = f"{bins[i]:3d}-{bins[i+1]-1:3d}"
            print(f"{bin_range}: {count:3d} {bar}")
        
        # Class distribution bar chart
        print(f"\nClass Distribution (Bar Chart):")
        intent_counts = self.stats['class_distribution']
        max_count = max(intent_counts.values())
        
        for intent, count in sorted(intent_counts.items(), key=lambda x: x[1], reverse=True):
            bar_length = int((count / max_count) * 30)
            bar = "█" * bar_length
            percentage = (count / sum(intent_counts.values())) * 100
            print(f"{intent:<20}: {count:3d} ({percentage:5.1f}%) {bar}")
        
    def generate_summary_report(self):
        """Generate comprehensive summary report"""
        print("\n📋 COMPREHENSIVE SUMMARY REPORT")
        print("="*70)
        
        total_examples = sum(len(examples) for examples in self.data.values())
        total_intents = len(self.data)
        
        print(f"DATASET OVERVIEW:")
        print(f"  • Total examples: {total_examples}")
        print(f"  • Number of intents: {total_intents}")
        print(f"  • Average examples per intent: {total_examples/total_intents:.1f}")
        
        # Class balance assessment
        intent_counts = self.stats['class_distribution']
        max_count = max(intent_counts.values())
        min_count = min(intent_counts.values())
        imbalance_ratio = max_count / min_count
        
        print(f"\nCLASS BALANCE:")
        print(f"  • Most common intent: {max_count} examples")
        print(f"  • Least common intent: {min_count} examples")
        print(f"  • Imbalance ratio: {imbalance_ratio:.2f}")
        
        if imbalance_ratio > 3:
            print(f"  • Status: ⚠️  HIGH IMBALANCE - Consider data augmentation")
        elif imbalance_ratio > 2:
            print(f"  • Status: ⚠️  MODERATE IMBALANCE - Monitor performance")
        else:
            print(f"  • Status: ✅ WELL BALANCED")
        
        # Text length analysis
        all_lengths = self.stats['text_lengths']['overall']
        avg_length = sum(all_lengths) / len(all_lengths)
        
        print(f"\nTEXT LENGTH ANALYSIS:")
        print(f"  • Average text length: {avg_length:.1f} characters")
        print(f"  • Length range: {min(all_lengths)}-{max(all_lengths)} characters")
        print(f"  • Length variation: {max(all_lengths) - min(all_lengths)} characters")
        
        # Word frequency insights
        word_freq = self.stats['word_frequency']['overall']
        most_common_word = max(word_freq.items(), key=lambda x: x[1])
        
        print(f"\nVOCABULARY INSIGHTS:")
        print(f"  • Total unique words: {len(word_freq)}")
        print(f"  • Most frequent word: '{most_common_word[0]}' ({most_common_word[1]} times)")
        print(f"  • Vocabulary richness: {len(word_freq)} unique words in {total_examples} examples")
        
        print(f"\nRECOMMENDATIONS:")
        if imbalance_ratio > 2:
            print(f"  • Add more examples to underrepresented classes")
        if avg_length < 20:
            print(f"  • Consider if texts are too short for effective classification")
        if avg_length > 100:
            print(f"  • Consider if texts are too long - may need truncation")
        print(f"  • Monitor model performance on minority classes")
        print(f"  • Consider cross-validation to assess generalization")
        
        print("="*70)
        
    def run_complete_eda(self):
        """Run complete EDA analysis"""
        print("🚀 Starting Simple Exploratory Data Analysis (EDA)")
        print("="*70)
        
        # Load data
        self.load_training_data()
        
        # Run all analyses
        self.analyze_text_lengths()
        self.analyze_class_distribution()
        self.analyze_word_frequency()
        self.analyze_text_features()
        self.create_simple_visualizations()
        self.generate_summary_report()
        
        print("\n✅ Simple EDA Analysis Complete!")
        print("\n📊 Analysis includes:")
        print("  • Text length distribution and statistics")
        print("  • Class distribution and imbalance analysis")
        print("  • Word frequency analysis by intent")
        print("  • Text feature analysis (numbers, capitals, etc.)")
        print("  • Simple text-based visualizations")
        print("  • Comprehensive summary report with recommendations")


if __name__ == '__main__':
    # Run EDA
    analyzer = SimpleEDAAnalyzer()
    analyzer.run_complete_eda()
