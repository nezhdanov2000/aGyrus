#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interactive examples demonstrating AI capabilities (English output)
"""

import json
import sys
from pathlib import Path

# Make core/ importable when running this script directly
CURRENT_DIR = Path(__file__).parent
CORE_DIR = (CURRENT_DIR / 'core').resolve()
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from dialog_manager import DialogManager
from intent_classifier import load_model, predict_intent


def compare_all_models(text):
    """Compare all three ML models on the same input"""
    models = ['logistic', 'decision_tree', 'knn']
    results = {}
    
    print("\n" + "🤖 MODEL COMPARISON ".center(70, "="))
    print(f"📝 Text: '{text}'")
    print("-"*70)
    
    for model_type in models:
        try:
            model = load_model(model_type)
            result = predict_intent(model, text)
            results[model_type] = result
            
            # Format model name for display
            model_display = model_type.replace('_', ' ').title()
            print(f"{model_display:20} → {result['intent']:15} ({result['confidence']:.1%})")
        except Exception as e:
            model_display = model_type.replace('_', ' ').title()
            print(f"{model_display:20} → Error: {str(e)[:30]}...")
    
    print("="*70)
    return results

def print_result(user_message, result):
    """Pretty print the result"""
    print("\n" + "="*70)
    print(f"👤 User: {user_message}")
    print("-"*70)
    print(f"🎯 Intent: {result['intent']} (confidence: {result['confidence']:.1%})")
    
    if result['entities']:
        print(f"📋 Extracted entities:")
        for key, value in result['entities'].items():
            if key != 'original_text':
                print(f"   • {key}: {value}")
    
    print(f"\n🤖 Bot: {result['response']['message']}")
    
    if result['needs_clarification']:
        print(f"❓ Needs clarification: {result['missing_info']}")
    
    print("="*70)


def run_examples():
    """Run example scenarios"""
    
    print("\n" + "🚀 AI CHATBOT EXAMPLES ".center(70, "="))
    print("\nDemonstrating natural language understanding capabilities\n")
    
    manager = DialogManager()
    
    examples = [
        # Search examples
        ("Find math tutor", "Simple search by subject"),
        ("I need English tutor for tomorrow at 3pm", "Search with date and time"),
        ("Looking for physics teacher", "Alternative phrasing"),
        
        # View bookings examples
        ("Show my bookings", "View all appointments"),
        ("What's my schedule", "Alternative phrasing"),
        ("My appointments", "Another variation"),
        
        # Cancel booking examples
        ("Cancel booking", "Cancel request"),
        ("I want to cancel my appointment", "More natural phrasing"),
        
        # Complex examples
        ("Book English class on Monday morning", "Booking with time preference"),
        ("Find John Smith", "Search by tutor name"),
    ]
    
    for i, (message, description) in enumerate(examples, 1):
        print(f"\n📝 Example {i}: {description}")
        result = manager.process_message(message)
        print_result(message, result)
        
        # Add some spacing
        if i < len(examples):
            input("\nPress Enter for next example...")
    
    print("\n" + "✅ All examples completed! ".center(70, "="))
    print("\nThe AI system can:")
    print("  ✓ Understand intent from natural language")
    print("  ✓ Extract entities (subjects, dates, times, names)")
    print("  ✓ Handle various phrasings of the same intent")
    print("  ✓ Maintain conversation context")
    print("\n")


def interactive_mode():
    """Interactive testing mode"""
    print("\n" + "💬 INTERACTIVE MODE ".center(70, "="))
    print("\nType messages to see how the AI processes them")
    print("Each message will show results from ALL 3 ML models!")
    print("Commands: 'examples' - run examples, 'compare <text>' - compare models, 'quit' - exit\n")
    
    manager = DialogManager()
    context = {}
    
    while True:
        try:
            # Check if we're in an interactive environment
            if not sys.stdin.isatty():
                print("❌ Interactive mode requires a terminal. Use 'python3 compare_models.py' for non-interactive testing.")
                break
                
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
                
            if user_input.lower() == 'examples':
                run_examples()
                continue
                
            if user_input.lower() in ['help', '?']:
                print("\nTry these examples:")
                print("  • Find math tutor")
                print("  • I need English tutor for tomorrow at 3pm")
                print("  • Show my bookings")
                print("  • Cancel appointment")
                print("\nCommands:")
                print("  • 'compare <text>' - compare all models on specific text")
                print("  • 'examples' - run example scenarios")
                print("  • 'quit' - exit")
                print()
                continue
                
            if user_input.lower().startswith('compare '):
                text_to_compare = user_input[8:].strip()
                if text_to_compare:
                    compare_all_models(text_to_compare)
                    print()
                continue
            
            # Process message with dialog manager (default logistic model)
            result = manager.process_message(user_input, context)
            context = result['context']
            
            # Show condensed output from dialog manager
            print(f"\n🎯 {result['intent']} ({result['confidence']:.0%})", end="")
            if result['entities']:
                entities_str = ', '.join([f"{k}={v}" for k, v in result['entities'].items() 
                                         if k != 'original_text'])
                if entities_str:
                    print(f" | 📋 {entities_str}", end="")
            print(f"\n🤖 {result['response']['message']}")
            
            # Compare all models
            compare_all_models(user_input)
            print()
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except EOFError:
            print("\n❌ Interactive input not available. Use 'python3 compare_models.py' for testing.")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'examples':
        run_examples()
    else:
        # Default: interactive mode
        interactive_mode()
