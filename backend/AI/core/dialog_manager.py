#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dialog Manager - manages conversation context and state
"""

import json
import sys
from typing import Dict, Any, Optional, List
from pathlib import Path
import pickle
from intent_classifier import load_model, predict_intent, preprocess_text
from entity_extractor import extract_entities_from_message


class DialogManager:
    """Manages dialog flow and context"""
    
    def __init__(self):
        # Load intent classifier model
        script_dir = Path(__file__).parent
        model_path = (script_dir / '..' / 'models' / 'intent_model_logistic.pkl').resolve()
        
        if model_path.exists():
            self.intent_model = load_model('logistic', str(model_path))
        else:
            self.intent_model = None
    
    def process_message(self, user_message: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Process user message and return structured response
        
        Args:
            user_message: User's text input
            context: Optional context from previous conversation
        
        Returns:
            Dict with: intent, entities, response, actions, needs_clarification
        """
        if context is None:
            context = {}
        
        # Step 1: Predict intent
        intent_result = self._predict_intent(user_message)
        intent = intent_result['intent']
        confidence = intent_result['confidence']
        
        # Step 2: Extract entities
        entities = extract_entities_from_message(user_message)
        
        # Step 3: Merge with context
        merged_entities = {**context, **entities}
        
        # Step 4: Determine what information is missing
        missing_info = self._check_missing_info(intent, merged_entities)
        
        # Step 5: Generate response
        response = self._generate_response(intent, merged_entities, missing_info)
        
        return {
            'intent': intent,
            'confidence': confidence,
            'entities': entities,
            'context': merged_entities,
            'missing_info': missing_info,
            'response': response,
            'needs_clarification': len(missing_info) > 0
        }
    
    def _predict_intent(self, text: str) -> Dict[str, Any]:
        """Predict intent using ML model"""
        if self.intent_model:
            return predict_intent(self.intent_model, text)
        else:
            # Fallback to keyword matching
            return self._fallback_intent(text)
    
    def _fallback_intent(self, text: str) -> Dict[str, Any]:
        """Fallback intent detection using keywords"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['find', 'search', 'looking']):
            return {'intent': 'search_tutor', 'confidence': 0.7}
        
        if any(word in text_lower for word in ['booking', 'appointment', 'schedule']):
            # Check if it's cancellation
            if any(word in text_lower for word in ['cancel', 'delete', 'remove']):
                return {'intent': 'cancel_booking', 'confidence': 0.7}
            return {'intent': 'view_bookings', 'confidence': 0.7}
        
        if any(word in text_lower for word in ['cancel']):
            return {'intent': 'cancel_booking', 'confidence': 0.7}
        
        return {'intent': 'general', 'confidence': 0.5}
    
    def _check_missing_info(self, intent: str, entities: Dict) -> List[str]:
        """Check what information is missing for the intent"""
        missing = []
        
        if intent == 'search_tutor':
            # For search, we need at least subject OR tutor name
            if not entities.get('subject') and not entities.get('tutor_name'):
                missing.append('search_query')
        
        elif intent == 'cancel_booking':
            # For cancel, we might need date or tutor name to identify booking
            # But we can also show all bookings and let user choose
            pass  # No strict requirements
        
        elif intent == 'view_bookings':
            # View bookings can work with or without filters
            pass  # No strict requirements
        
        return missing
    
    def _generate_response(self, intent: str, entities: Dict, missing_info: List[str]) -> Dict[str, Any]:
        """Generate response based on intent and entities"""
        
        # If critical information is missing, ask for it
        if missing_info:
            return self._generate_clarification_request(intent, missing_info)
        
        # Generate action-ready response
        response = {
            'type': 'action',
            'intent': intent,
            'message': self._get_default_message(intent, entities),
            'action_data': entities
        }
        
        return response
    
    def _generate_clarification_request(self, intent: str, missing_info: List[str]) -> Dict[str, Any]:
        """Generate request for missing information"""
        
        if 'search_query' in missing_info:
            message = "What would you like to search for? You can specify a subject (like 'math' or 'english') or a tutor's name."
        else:
            message = "I need more information. Could you please provide more details?"
        
        return {
            'type': 'clarification',
            'message': message,
            'missing': missing_info
        }
    
    def _get_default_message(self, intent: str, entities: Dict) -> str:
        """Get default message for intent"""
        
        if intent == 'search_tutor':
            if entities.get('subject'):
                return f"Searching for {entities['subject']} tutors..."
            elif entities.get('tutor_name'):
                return f"Searching for {entities['tutor_name']}..."
            else:
                return "Searching for tutors..."
        
        elif intent == 'view_bookings':
            if entities.get('date'):
                return f"Showing your bookings for {entities['date']}..."
            elif entities.get('tutor_name'):
                return f"Showing your bookings with {entities['tutor_name']}..."
            else:
                return "Showing your bookings..."
        
        elif intent == 'cancel_booking':
            return "Which booking would you like to cancel?"
        
        else:
            return "How can I help you?"


def process_user_message(message: str, context_json: str = None) -> str:
    """
    Main entry point for processing messages
    Returns JSON string
    """
    context = json.loads(context_json) if context_json else {}
    
    manager = DialogManager()
    result = manager.process_message(message, context)
    
    return json.dumps(result, ensure_ascii=False)


if __name__ == '__main__':
    # Command line interface
    if len(sys.argv) > 1:
        message = ' '.join(sys.argv[1:])
        result = process_user_message(message)
        print(result)
    else:
        # Interactive test mode
        print("Dialog Manager Test Mode")
        print("Type messages to test (or 'quit' to exit)\n")
        
        manager = DialogManager()
        context = {}
        
        while True:
            try:
                user_input = input("You: ").strip()
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                if not user_input:
                    continue
                
                result = manager.process_message(user_input, context)
                
                # Update context for next turn
                context = result.get('context', {})
                
                print(f"\nIntent: {result['intent']} ({result['confidence']:.2%})")
                print(f"Entities: {json.dumps(result['entities'], ensure_ascii=False)}")
                print(f"Response: {result['response']['message']}")
                if result['needs_clarification']:
                    print(f"Missing: {result['missing_info']}")
                print()
                
            except KeyboardInterrupt:
                print("\nBye!")
                break
            except Exception as e:
                print(f"Error: {e}")

