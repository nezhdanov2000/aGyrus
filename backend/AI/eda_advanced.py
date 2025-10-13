#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Exploratory Data Analysis (EDA) with ASCII visualizations
Creates detailed visualizations using only standard Python libraries
"""

import json
import sys
from pathlib import Path
from collections import Counter, defaultdict
import re
import math

class AdvancedEDAAnalyzer:
    def __init__(self, data_dir="training_data"):
        """Initialize advanced EDA analyzer"""
        self.data_dir = Path(__file__).parent / data_dir
        self.data = {}
        self.stats = {}
        
    def load_training_data(self):
        """Load all training data files"""
        print("📊 Loading training data...")
        
        json_files = list(self.data_dir.glob("*.json"))
        
        for file_path in json_files:
            if file_path.name == "typo_corrections.json":
                continue
                
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            intent_name = file_path.stem
            
            if isinstance(data, list):
                examples = data
            else:
                examples = data.get('examples', [])
            
            self.data[intent_name] = examples
            print(f"  ✓ Loaded {len(examples)} examples for '{intent_name}'")
        
        total_examples = sum(len(examples) for examples in self.data.values())
        print(f"📈 Total intents: {len(self.data)}")
        print(f"📈 Total examples: {total_examples}")
        
    def create_histogram(self, data, title, width=50, height=10):
        """Create ASCII histogram"""
        if not data:
            return ""
        
        min_val, max_val = min(data), max(data)
        bin_count = min(20, len(set(data)))
        
        # Create bins
        if max_val == min_val:
            bins = [min_val]
            bin_counts = [len(data)]
        else:
            bin_width = (max_val - min_val) / bin_count
            bins = [min_val + i * bin_width for i in range(bin_count + 1)]
            bin_counts = [0] * bin_count
            
            for value in data:
                bin_idx = min(int((value - min_val) / bin_width), bin_count - 1)
                bin_counts[bin_idx] += 1
        
        # Normalize for display
        max_count = max(bin_counts) if bin_counts else 1
        normalized_counts = [int((count / max_count) * width) for count in bin_counts]
        
        # Create histogram
        result = [f"\n{title}"]
        result.append("=" * (len(title) + 1))
        
        for i, (bin_start, count, norm_count) in enumerate(zip(bins[:-1], bin_counts, normalized_counts)):
            bin_end = bins[i + 1] if i + 1 < len(bins) else max_val
            bar = "█" * norm_count + "░" * (width - norm_count)
            
            if bin_count <= 10:
                range_str = f"{bin_start:.0f}-{bin_end:.0f}"
            else:
                range_str = f"{bin_start:.1f}-{bin_end:.1f}"
            
            result.append(f"{range_str:>8}: {count:>4} {bar}")
        
        return "\n".join(result)
        
    def create_box_plot(self, data_by_group, title, width=50):
        """Create ASCII box plot"""
        result = [f"\n{title}"]
        result.append("=" * (len(title) + 1))
        
        for group_name, values in data_by_group.items():
            if not values:
                continue
                
            values.sort()
            n = len(values)
            
            # Calculate quartiles
            q1 = values[n // 4]
            median = values[n // 2]
            q3 = values[3 * n // 4]
            min_val = values[0]
            max_val = values[-1]
            
            # Create box plot
            result.append(f"\n{group_name}:")
            result.append(f"  Min: {min_val:>3} | Q1: {q1:>3} | Median: {median:>3} | Q3: {q3:>3} | Max: {max_val:>3}")
            
            # ASCII box plot
            scale = (max_val - min_val) / width if max_val != min_val else 1
            min_pos = int((min_val - min_val) / scale)
            q1_pos = int((q1 - min_val) / scale)
            median_pos = int((median - min_val) / scale)
            q3_pos = int((q3 - min_val) / scale)
            max_pos = int((max_val - min_val) / scale)
            
            box_line = [" "] * width
            for i in range(min_pos, max_pos + 1):
                if 0 <= i < width:
                    if i == min_pos or i == max_pos:
                        box_line[i] = "|"
                    elif q1_pos <= i <= q3_pos:
                        box_line[i] = "█"
                    elif i == median_pos:
                        box_line[i] = "┃"
                    else:
                        box_line[i] = "─"
            
            result.append(f"  {' '.join(box_line)}")
        
        return "\n".join(result)
        
    def create_scatter_plot(self, x_data, y_data, labels, title, width=50, height=20):
        """Create ASCII scatter plot"""
        if len(x_data) != len(y_data):
            return f"\nError: Data length mismatch in {title}"
        
        result = [f"\n{title}"]
        result.append("=" * (len(title) + 1))
        
        # Find ranges
        x_min, x_max = min(x_data), max(x_data)
        y_min, y_max = min(y_data), max(y_data)
        
        if x_max == x_min or y_max == y_min:
            return f"\n{title}: Cannot create scatter plot - no variation in data"
        
        # Create grid
        grid = [[" " for _ in range(width)] for _ in range(height)]
        
        # Plot points
        for x, y in zip(x_data, y_data):
            x_pos = int(((x - x_min) / (x_max - x_min)) * (width - 1))
            y_pos = int(((y - y_min) / (y_max - y_min)) * (height - 1))
            
            if 0 <= x_pos < width and 0 <= y_pos < height:
                grid[height - 1 - y_pos][x_pos] = "●"
        
        # Add axes
        for i in range(height):
            grid[i][0] = "│"
        for j in range(width):
            grid[height - 1][j] = "─"
        grid[height - 1][0] = "└"
        
        # Add labels
        result.append(f"Y: {y_max:.0f} " + "".join(grid[0]))
        for i in range(1, height - 1):
            result.append("    " + "".join(grid[i]))
        result.append(f"    " + "".join(grid[height - 1]))
        result.append(f"     {x_min:.0f}" + " " * (width - 10) + f"{x_max:.0f}")
        result.append(f"     {labels[0]}" + " " * (width - len(labels[0]) - len(labels[1])) + f"{labels[1]}")
        
        return "\n".join(result)
        
    def create_correlation_matrix(self, features, data_by_intent):
        """Create ASCII correlation matrix"""
        result = ["\nFeature Correlation Analysis"]
        result.append("=" * 40)
        
        # Calculate basic correlations between features
        feature_names = list(features.keys())
        
        result.append(f"{'Feature':<15} {'Avg Value':<12} {'Std Dev':<10}")
        result.append("-" * 40)
        
        for feature_name in feature_names:
            all_values = []
            for intent_data in data_by_intent.values():
                if feature_name in intent_data:
                    all_values.extend(intent_data[feature_name])
            
            if all_values:
                avg_val = sum(all_values) / len(all_values)
                variance = sum((x - avg_val) ** 2 for x in all_values) / len(all_values)
                std_dev = math.sqrt(variance)
                result.append(f"{feature_name:<15} {avg_val:<12.2f} {std_dev:<10.2f}")
        
        return "\n".join(result)
        
    def analyze_text_lengths_advanced(self):
        """Advanced text length analysis with visualizations"""
        print("\n📏 ADVANCED TEXT LENGTH ANALYSIS")
        print("="*50)
        
        all_lengths = []
        intent_lengths = {}
        
        for intent, examples in self.data.items():
            lengths = [len(example) for example in examples]
            intent_lengths[intent] = lengths
            all_lengths.extend(lengths)
        
        # Create histogram
        print(self.create_histogram(all_lengths, "Overall Text Length Distribution"))
        
        # Create box plot
        print(self.create_box_plot(intent_lengths, "Text Length Box Plot by Intent"))
        
        # Statistics
        print(f"\nDetailed Statistics:")
        print(f"{'Intent':<15} {'Count':<6} {'Mean':<6} {'Median':<7} {'Std Dev':<8} {'Min':<4} {'Max':<4}")
        print("-" * 60)
        
        for intent, lengths in intent_lengths.items():
            n = len(lengths)
            mean_val = sum(lengths) / n
            lengths.sort()
            median_val = lengths[n // 2]
            variance = sum((x - mean_val) ** 2 for x in lengths) / n
            std_dev = math.sqrt(variance)
            min_val, max_val = min(lengths), max(lengths)
            
            print(f"{intent:<15} {n:<6} {mean_val:<6.1f} {median_val:<7} {std_dev:<8.1f} {min_val:<4} {max_val:<4}")
        
        self.stats['text_lengths'] = {
            'overall': all_lengths,
            'by_intent': intent_lengths
        }
        
    def analyze_word_frequency_advanced(self):
        """Advanced word frequency analysis"""
        print("\n🔤 ADVANCED WORD FREQUENCY ANALYSIS")
        print("="*50)
        
        all_words = []
        intent_words = {}
        
        for intent, examples in self.data.items():
            words = []
            for example in examples:
                words.extend(re.findall(r'\b\w+\b', example.lower()))
            intent_words[intent] = words
            all_words.extend(words)
        
        # Overall word frequency
        word_counts = Counter(all_words)
        most_common = word_counts.most_common(20)
        
        print(f"\nTop 20 Most Common Words (Overall):")
        print(f"{'Rank':<4} {'Word':<15} {'Count':<6} {'Percentage':<10} {'Bar'}")
        print("-" * 55)
        
        total_words = len(all_words)
        max_count = most_common[0][1] if most_common else 1
        
        for i, (word, count) in enumerate(most_common, 1):
            percentage = (count / total_words) * 100
            bar_length = int((count / max_count) * 20)
            bar = "█" * bar_length + "░" * (20 - bar_length)
            print(f"{i:<4} {word:<15} {count:<6} {percentage:<9.1f}% {bar}")
        
        # Word frequency by intent
        print(f"\nWord Frequency by Intent:")
        for intent, words in intent_words.items():
            word_counts_intent = Counter(words)
            most_common_intent = word_counts_intent.most_common(10)
            
            print(f"\n{intent}:")
            print(f"{'Word':<15} {'Count':<6} {'Percentage':<10} {'Bar'}")
            print("-" * 45)
            
            max_count_intent = most_common_intent[0][1] if most_common_intent else 1
            for word, count in most_common_intent:
                percentage = (count / len(words)) * 100
                bar_length = int((count / max_count_intent) * 15)
                bar = "█" * bar_length + "░" * (15 - bar_length)
                print(f"{word:<15} {count:<6} {percentage:<9.1f}% {bar}")
        
        self.stats['word_frequency'] = {
            'overall': dict(word_counts),
            'by_intent': {intent: dict(Counter(words)) for intent, words in intent_words.items()}
        }
        
    def analyze_feature_correlations_advanced(self):
        """Advanced feature correlation analysis"""
        print("\n🔍 ADVANCED FEATURE CORRELATION ANALYSIS")
        print("="*50)
        
        # Extract features for each intent
        features_by_intent = {}
        all_features = defaultdict(list)
        
        for intent, examples in self.data.items():
            features = {
                'text_length': [],
                'word_count': [],
                'avg_word_length': [],
                'sentence_count': [],
                'has_numbers': [],
                'has_capitals': [],
                'has_special_chars': [],
                'starts_capital': []
            }
            
            for example in examples:
                # Basic features
                text_len = len(example)
                words = example.split()
                word_count = len(words)
                avg_word_len = sum(len(word) for word in words) / word_count if words else 0
                sentence_count = len([s for s in example.split('.') if s.strip()])
                
                # Boolean features
                has_numbers = 1 if re.search(r'\d', example) else 0
                has_capitals = 1 if re.search(r'[A-Z]', example) else 0
                has_special_chars = 1 if re.search(r'[^\w\s]', example) else 0
                starts_capital = 1 if example and example[0].isupper() else 0
                
                features['text_length'].append(text_len)
                features['word_count'].append(word_count)
                features['avg_word_length'].append(avg_word_len)
                features['sentence_count'].append(sentence_count)
                features['has_numbers'].append(has_numbers)
                features['has_capitals'].append(has_capitals)
                features['has_special_chars'].append(has_special_chars)
                features['starts_capital'].append(starts_capital)
                
                # Add to overall features
                all_features['text_length'].append(text_len)
                all_features['word_count'].append(word_count)
                all_features['avg_word_length'].append(avg_word_len)
                all_features['sentence_count'].append(sentence_count)
                all_features['has_numbers'].append(has_numbers)
                all_features['has_capitals'].append(has_capitals)
                all_features['has_special_chars'].append(has_special_chars)
                all_features['starts_capital'].append(starts_capital)
            
            features_by_intent[intent] = features
        
        # Create correlation analysis
        print(self.create_correlation_matrix(all_features, features_by_intent))
        
        # Create scatter plots for key relationships
        print(self.create_scatter_plot(
            all_features['text_length'],
            all_features['word_count'],
            ['Text Length', 'Word Count'],
            "Text Length vs Word Count Scatter Plot"
        ))
        
        # Feature distribution by intent
        print(f"\nFeature Distribution by Intent:")
        print(f"{'Intent':<15} {'Avg Length':<12} {'Avg Words':<11} {'Has Numbers':<12} {'Has Capitals':<13}")
        print("-" * 75)
        
        for intent, features in features_by_intent.items():
            avg_length = sum(features['text_length']) / len(features['text_length'])
            avg_words = sum(features['word_count']) / len(features['word_count'])
            has_numbers_pct = (sum(features['has_numbers']) / len(features['has_numbers'])) * 100
            has_capitals_pct = (sum(features['has_capitals']) / len(features['has_capitals'])) * 100
            
            print(f"{intent:<15} {avg_length:<12.1f} {avg_words:<11.1f} {has_numbers_pct:<11.1f}% {has_capitals_pct:<12.1f}%")
        
        self.stats['features'] = features_by_intent
        
    def create_advanced_visualizations(self):
        """Create advanced ASCII visualizations"""
        print("\n📈 ADVANCED VISUALIZATIONS")
        print("="*50)
        
        # Class distribution pie chart (ASCII)
        intent_counts = {intent: len(examples) for intent, examples in self.data.items()}
        total = sum(intent_counts.values())
        
        print(f"\nClass Distribution (ASCII Pie Chart):")
        print("=" * 40)
        
        # Calculate angles for pie slices
        angles = {}
        current_angle = 0
        for intent, count in intent_counts.items():
            percentage = (count / total) * 100
            angle = (count / total) * 360
            angles[intent] = (current_angle, current_angle + angle, percentage)
            current_angle += angle
        
        # Create simple pie representation
        pie_chars = ['█', '▓', '▒', '░']
        for i, (intent, (start_angle, end_angle, percentage)) in enumerate(angles.items()):
            char = pie_chars[i % len(pie_chars)]
            print(f"{char} {intent}: {percentage:.1f}%")
        
        # Create feature heatmap
        print(f"\nFeature Heatmap by Intent:")
        print("=" * 40)
        
        if 'features' in self.stats:
            features = self.stats['features']
            feature_names = ['text_length', 'word_count', 'avg_word_length']
            
            print(f"{'Intent':<15} ", end="")
            for feature in feature_names:
                print(f"{feature:<12}", end="")
            print()
            print("-" * 55)
            
            for intent, intent_features in features.items():
                print(f"{intent:<15} ", end="")
                for feature in feature_names:
                    if feature in intent_features:
                        avg_val = sum(intent_features[feature]) / len(intent_features[feature])
                        print(f"{avg_val:<12.1f}", end="")
                    else:
                        print(f"{'N/A':<12}", end="")
                print()
        
    def generate_advanced_summary(self):
        """Generate advanced summary with insights"""
        print("\n📋 ADVANCED SUMMARY & INSIGHTS")
        print("="*70)
        
        total_examples = sum(len(examples) for examples in self.data.values())
        intent_counts = {intent: len(examples) for intent, examples in self.data.items()}
        
        print(f"DATASET CHARACTERISTICS:")
        print(f"  • Total examples: {total_examples}")
        print(f"  • Number of classes: {len(intent_counts)}")
        print(f"  • Average examples per class: {total_examples/len(intent_counts):.1f}")
        
        # Class balance analysis
        max_count = max(intent_counts.values())
        min_count = min(intent_counts.values())
        imbalance_ratio = max_count / min_count
        
        print(f"\nCLASS BALANCE ANALYSIS:")
        print(f"  • Imbalance ratio: {imbalance_ratio:.2f}")
        if imbalance_ratio < 1.5:
            print(f"  • Status: ✅ EXCELLENT BALANCE")
        elif imbalance_ratio < 2.0:
            print(f"  • Status: ✅ GOOD BALANCE")
        else:
            print(f"  • Status: ⚠️  NEEDS ATTENTION")
        
        # Text complexity analysis
        all_lengths = self.stats['text_lengths']['overall']
        avg_length = sum(all_lengths) / len(all_lengths)
        length_std = math.sqrt(sum((x - avg_length) ** 2 for x in all_lengths) / len(all_lengths))
        
        print(f"\nTEXT COMPLEXITY ANALYSIS:")
        print(f"  • Average length: {avg_length:.1f} characters")
        print(f"  • Length standard deviation: {length_std:.1f}")
        print(f"  • Length coefficient of variation: {length_std/avg_length:.2f}")
        
        if length_std/avg_length > 0.5:
            print(f"  • Status: ⚠️  HIGH VARIABILITY in text lengths")
        else:
            print(f"  • Status: ✅ CONSISTENT text lengths")
        
        # Vocabulary analysis
        word_freq = self.stats['word_frequency']['overall']
        unique_words = len(word_freq)
        total_words = sum(word_freq.values())
        
        print(f"\nVOCABULARY ANALYSIS:")
        print(f"  • Unique words: {unique_words}")
        print(f"  • Total word instances: {total_words}")
        print(f"  • Vocabulary diversity: {unique_words/total_words:.3f}")
        
        # Most distinctive words by intent
        print(f"\nDISTINCTIVE WORDS BY INTENT:")
        for intent, word_counts in self.stats['word_frequency']['by_intent'].items():
            # Find words that are more common in this intent than others
            intent_total = sum(word_counts.values())
            other_totals = sum(sum(counts.values()) for other_intent, counts in 
                             self.stats['word_frequency']['by_intent'].items() if other_intent != intent)
            
            distinctive_words = []
            # Convert to Counter for most_common method
            word_counter = Counter(word_counts)
            for word, count in word_counter.most_common(5):
                word_freq_in_intent = count / intent_total
                word_freq_other = sum(other_counts.get(word, 0) for other_intent, other_counts in 
                                    self.stats['word_frequency']['by_intent'].items() if other_intent != intent) / other_totals
                
                if word_freq_other == 0 or word_freq_in_intent / word_freq_other > 2:
                    distinctive_words.append(word)
            
            if distinctive_words:
                print(f"  {intent}: {', '.join(distinctive_words[:3])}")
        
        print(f"\nRECOMMENDATIONS:")
        if imbalance_ratio > 1.5:
            print(f"  • Consider data augmentation for minority classes")
        if unique_words/total_words < 0.3:
            print(f"  • High vocabulary repetition - consider expanding training data")
        if length_std/avg_length > 0.5:
            print(f"  • Consider text length normalization or padding")
        print(f"  • Monitor model performance across all classes")
        print(f"  • Consider cross-validation for robust evaluation")
        print(f"  • Feature engineering: capitalize on distinctive words per intent")
        
        print("="*70)
        
    def run_complete_advanced_eda(self):
        """Run complete advanced EDA analysis"""
        print("🚀 Starting Advanced Exploratory Data Analysis (EDA)")
        print("="*70)
        
        # Load data
        self.load_training_data()
        
        # Run all advanced analyses
        self.analyze_text_lengths_advanced()
        self.analyze_word_frequency_advanced()
        self.analyze_feature_correlations_advanced()
        self.create_advanced_visualizations()
        self.generate_advanced_summary()
        
        print("\n✅ Advanced EDA Analysis Complete!")
        print("\n📊 Advanced Analysis includes:")
        print("  • Detailed text length analysis with histograms and box plots")
        print("  • Advanced word frequency analysis with distinctive word identification")
        print("  • Feature correlation analysis with scatter plots")
        print("  • ASCII-based visualizations (histograms, box plots, scatter plots)")
        print("  • Comprehensive insights and recommendations")
        print("  • Class balance and vocabulary diversity analysis")


if __name__ == '__main__':
    # Run advanced EDA
    analyzer = AdvancedEDAAnalyzer()
    analyzer.run_complete_advanced_eda()
