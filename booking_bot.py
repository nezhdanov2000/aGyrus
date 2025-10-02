#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Booking Bot - Main Entry Point

Модульная система чат-бота для бронирования занятий.
Поддерживает два режима:
1. ML-only режим (Logistic Regression для интентов)
2. Hybrid режим (ML + GPT-2 для генерации ответов)
"""

import sys
import io
from typing import Optional

# Fix Windows encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

# Import configuration
from config import bot_config

# Try to import ML components
try:
    from logistic_regression import IntentClassifier, EntityExtractor
    ML_AVAILABLE = True
    print("✅ ML Components loaded")
except ImportError as e:
    print(f"⚠️  ML Components not available: {e}")
    ML_AVAILABLE = False

# Try to import GPT-2 components
try:
    # from gpt2_components.model import GPT2Generator
    GPT2_AVAILABLE = False  # Will be True when GPT-2 is implemented
    print("⚠️  GPT-2 Components not yet implemented")
except ImportError as e:
    print(f"⚠️  GPT-2 Components not available: {e}")
    GPT2_AVAILABLE = False

# Import dialog components
from dialog import DialogState, ScheduleManager, ResponseGenerator


class BookingBot:
    """Main bot class that orchestrates all components"""
    
    def __init__(self, mode: str = "auto"):
        """
        Initialize the booking bot
        
        Args:
            mode: "ml_only", "hybrid", or "auto" (auto-detect available components)
        """
        print("=" * 60)
        print("Initializing Booking Bot...")
        print("=" * 60)
        
        # Determine mode
        if mode == "auto":
            if ML_AVAILABLE and GPT2_AVAILABLE:
                self.mode = "hybrid"
            elif ML_AVAILABLE:
                self.mode = "ml_only"
            else:
                raise RuntimeError("No components available! Please install ML or GPT-2 dependencies.")
        else:
            self.mode = mode
            
        print(f"🤖 Mode: {self.mode}")
        
        # Initialize components based on mode
        self._initialize_components()
        
        print("✅ Bot ready!")
        print("=" * 60)
    
    def _initialize_components(self):
        """Initialize components based on the selected mode"""
        
        # Shared components (always available)
        self.schedule_manager = ScheduleManager()
        self.dialog_state = DialogState()
        self.response_generator = ResponseGenerator()
        
        # ML components (if available)
        if self.mode in ["ml_only", "hybrid"] and ML_AVAILABLE:
            self.intent_classifier = IntentClassifier()
            self.entity_extractor = EntityExtractor()
            # Train intent classifier
            self.intent_classifier.train()
        
        # GPT-2 components (if available)
        if self.mode == "hybrid" and GPT2_AVAILABLE:
            # self.gpt2_generator = GPT2Generator()
            pass  # Will be implemented later
    
    def process_message(self, user_input: str) -> str:
        """Process user message and generate response"""
        
        # Handle dialog state first
        if self.dialog_state.state == DialogState.AWAITING_DATE:
            return self._handle_date_input(user_input)
        elif self.dialog_state.state == DialogState.AWAITING_TIME:
            return self._handle_time_input(user_input)
        
        # Intent classification (if ML is available)
        if hasattr(self, 'intent_classifier'):
            intent, confidence = self.intent_classifier.predict(user_input)
            print(f"[Intent: {intent}, Confidence: {confidence:.2f}]")
            
            # Check confidence threshold
            if confidence < bot_config.INTENT_CONFIG.get('confidence_threshold', 0.3):
                return self._get_fallback_response()
        else:
            # Fallback to simple keyword matching
            intent = self._simple_intent_detection(user_input)
            confidence = 1.0
        
        # Handle based on intent
        return self._handle_intent(intent, user_input)
    
    def _handle_intent(self, intent: str, user_input: str) -> str:
        """Handle different intents"""
        
        if intent == 'greeting':
            return self.response_generator.generate_response('greeting')
        
        elif intent == 'book_class':
            return self._handle_booking_intent(user_input)
        
        elif intent == 'cancel_class':
            return self._handle_cancel_intent()
        
        elif intent == 'show_schedule':
            return self._show_schedule()
        
        elif intent == 'goodbye':
            self.dialog_state.reset()
            return self.response_generator.generate_response('goodbye')
        
        return self._get_fallback_response()
    
    def _handle_booking_intent(self, user_input: str) -> str:
        """Handle booking intent"""
        if hasattr(self, 'entity_extractor'):
            # Extract date and time using ML
            date = self.entity_extractor.extract_date(user_input)
            time = self.entity_extractor.extract_time(user_input)
        else:
            # Simple extraction
            date, time = self._simple_entity_extraction(user_input)
        
        if date and time:
            # Both provided, book directly
            return self._book_class(date, time)
        elif date:
            # Only date provided, ask for time
            self.dialog_state.set_state(DialogState.AWAITING_TIME, date=date)
            return f"Great! I see you want to book for {date}. What time would you prefer?"
        else:
            # Ask for date
            self.dialog_state.set_state(DialogState.AWAITING_DATE)
            return self.response_generator.generate_response('book_class')
    
    def _handle_cancel_intent(self) -> str:
        """Handle cancel intent"""
        bookings = self.schedule_manager.get_user_bookings()
        if not bookings:
            return self.response_generator.generate_response('no_bookings')
        
        response = "Here are your current bookings:\n"
        for i, (date, time) in enumerate(bookings, 1):
            response += f"{i}. {date} at {time}\n"
        response += "\nPlease tell me the date and time you want to cancel."
        
        self.dialog_state.set_state(DialogState.AWAITING_CANCEL_CONFIRMATION)
        return response
    
    def _handle_date_input(self, user_input: str) -> str:
        """Handle date input when booking"""
        if hasattr(self, 'entity_extractor'):
            date = self.entity_extractor.extract_date(user_input)
        else:
            date, _ = self._simple_entity_extraction(user_input)
        
        if not date:
            return "I couldn't understand that date. Please try again (e.g., today, tomorrow, Monday)"
        
        self.dialog_state.set_state(DialogState.AWAITING_TIME, date=date)
        available = self.schedule_manager.get_available_slots(date)
        
        response = f"Available slots for {date}:\n"
        response += ", ".join(available)
        response += "\n\nWhat time would you prefer?"
        
        return response
    
    def _handle_time_input(self, user_input: str) -> str:
        """Handle time input when booking"""
        if hasattr(self, 'entity_extractor'):
            time = self.entity_extractor.extract_time(user_input)
        else:
            _, time = self._simple_entity_extraction(user_input)
        
        date = self.dialog_state.context.get('date')
        
        if not time:
            return "I couldn't understand that time. Please try again (e.g., 9am, 14:00)"
        
        result = self._book_class(date, time)
        self.dialog_state.reset()
        return result
    
    def _book_class(self, date: str, time: str) -> str:
        """Book a class"""
        success = self.schedule_manager.book_slot(date, time)
        
        if success:
            return self.response_generator.generate_response('booking_confirmed', {'date': date, 'time': time})
        else:
            return self.response_generator.generate_response('booking_failed')
    
    def _show_schedule(self) -> str:
        """Show available schedule for next 7 days"""
        from datetime import datetime, timedelta
        
        today = datetime.now()
        response = "📅 Available slots for the next 7 days:\n\n"
        
        for i in range(7):
            date = (today + timedelta(days=i)).strftime('%Y-%m-%d')
            day_name = (today + timedelta(days=i)).strftime('%A')
            available = self.schedule_manager.get_available_slots(date)
            
            response += f"{day_name} ({date}):\n"
            if available:
                response += "  " + ", ".join(available) + "\n"
            else:
                response += "  No slots available\n"
            response += "\n"
        
        return response
    
    def _simple_intent_detection(self, user_input: str) -> str:
        """Simple keyword-based intent detection (fallback)"""
        user_input_lower = user_input.lower()
        
        if any(word in user_input_lower for word in ['hello', 'hi', 'hey', 'привет']):
            return 'greeting'
        elif any(word in user_input_lower for word in ['book', 'забронировать', 'записаться']):
            return 'book_class'
        elif any(word in user_input_lower for word in ['cancel', 'отменить', 'отмена']):
            return 'cancel_class'
        elif any(word in user_input_lower for word in ['schedule', 'расписание', 'время']):
            return 'show_schedule'
        elif any(word in user_input_lower for word in ['bye', 'goodbye', 'пока', 'до свидания']):
            return 'goodbye'
        else:
            return 'unknown'
    
    def _simple_entity_extraction(self, user_input: str) -> tuple:
        """Simple entity extraction (fallback)"""
        user_input_lower = user_input.lower()
        
        # Simple date detection
        date = None
        if 'today' in user_input_lower:
            from datetime import datetime
            date = datetime.now().strftime('%Y-%m-%d')
        elif 'tomorrow' in user_input_lower:
            from datetime import datetime, timedelta
            date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Simple time detection
        time = None
        if 'am' in user_input_lower or 'pm' in user_input_lower:
            import re
            time_match = re.search(r'(\d{1,2})\s*(am|pm)', user_input_lower)
            if time_match:
                hour = int(time_match.group(1))
                period = time_match.group(2)
                if period == 'pm' and hour != 12:
                    hour += 12
                elif period == 'am' and hour == 12:
                    hour = 0
                time = f"{hour:02d}:00"
        
        return date, time
    
    def _get_fallback_response(self) -> str:
        """Get fallback response when intent is unclear"""
        return "I'm not sure I understood that. Could you please rephrase? You can:\n" \
               "- Say hello to start\n" \
               "- Book a class\n" \
               "- Cancel a booking\n" \
               "- Show the schedule\n" \
               "- Say goodbye to end"
    
    def run(self):
        """Run interactive bot"""
        print("\n" + "=" * 60)
        print("🤖 BOOKING BOT - Interactive Mode")
        print(f"📊 Mode: {self.mode}")
        print("=" * 60)
        print("\nType 'quit' to exit\n")
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit']:
                    print("\n" + self.response_generator.generate_response('goodbye'))
                    break
                
                response = self.process_message(user_input)
                print(f"\nBot: {response}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")


def main():
    """Main function to run the booking bot"""
    print("\n" + "=" * 70)
    print("🤖 BOOKING BOT - Starting...")
    print("=" * 70)
    
    try:
        # Initialize and run the bot
        bot = BookingBot()
        bot.run()
    except KeyboardInterrupt:
        print("\n\n👋 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting bot: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
