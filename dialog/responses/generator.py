#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Response Generation (without GPT-2 for now, will add later)
"""

from typing import Dict


class ResponseGenerator:
    """Generate natural responses for the bot"""
    
    def __init__(self):
        self.responses = {
            'greeting': "Hello! I'm here to help you book classes. You can ask me to:\n"
                       "- Book a class\n"
                       "- Cancel a booking\n"
                       "- Show the schedule\n"
                       "How can I assist you?",
            
            'book_class': "Sure! I'd be happy to help you book a class. "
                         "What date would you like to book? (e.g., today, tomorrow, Monday, 2025-10-05)",
            
            'cancel_class': "I can help you cancel your booking. Let me show you your bookings.",
            
            'show_schedule': "Here's the schedule:",
            
            'goodbye': "Goodbye! Have a great day! Feel free to come back anytime you need to book a class.",
            
            'awaiting_date': "Great! Now, what time would you prefer? "
                            "(e.g., 9am, 10:00, 14:30)",
            
            'booking_confirmed': "✅ Perfect! Your class is booked for {date} at {time}. "
                               "I'll send you a reminder. See you then!",
            
            'booking_failed': "Sorry, that time slot is not available. Would you like to see available slots?",
            
            'no_bookings': "You don't have any bookings at the moment.",
            
            'cancel_success': "✅ Your booking for {date} at {time} has been cancelled.",
            
            'cancel_failed': "I couldn't find that booking. Please check your bookings.",
        }
    
    def generate_response(self, intent: str, context: Dict = None) -> str:
        """Generate response for given intent and context"""
        if context is None:
            context = {}
        
        template = self.responses.get(intent, "I'm not sure how to help with that. Could you rephrase?")
        
        # Format template with context if needed
        try:
            return template.format(**context)
        except KeyError:
            return template
