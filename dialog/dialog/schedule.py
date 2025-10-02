#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Schedule Management - Simple "Database" for bookings
"""

from typing import Dict, List, Tuple
import sys
import os

# Add config path to imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'config'))
from bot_config import SCHEDULE_CONFIG


class ScheduleManager:
    """Manage class bookings and schedule"""
    
    def __init__(self):
        # Use configuration from bot_config
        self.available_slots = SCHEDULE_CONFIG['available_slots']
        self.working_days = SCHEDULE_CONFIG['working_days']
        self.max_advance_booking_days = SCHEDULE_CONFIG['max_advance_booking_days']
        # Bookings: {date: {time: user_id}}
        self.bookings: Dict[str, Dict[str, str]] = {}
    
    def get_available_slots(self, date: str) -> List[str]:
        """Get available slots for a date"""
        if date not in self.bookings:
            return self.available_slots.copy()
        
        booked = self.bookings[date].keys()
        return [slot for slot in self.available_slots if slot not in booked]
    
    def book_slot(self, date: str, time: str, user_id: str = 'user') -> bool:
        """Book a time slot"""
        if time not in self.available_slots:
            return False
        
        if date not in self.bookings:
            self.bookings[date] = {}
        
        if time in self.bookings[date]:
            return False  # Already booked
        
        self.bookings[date][time] = user_id
        return True
    
    def cancel_booking(self, date: str, time: str, user_id: str = 'user') -> bool:
        """Cancel a booking"""
        if date not in self.bookings:
            return False
        
        if time not in self.bookings[date]:
            return False
        
        if self.bookings[date][time] != user_id:
            return False  # Not user's booking
        
        del self.bookings[date][time]
        return True
    
    def get_user_bookings(self, user_id: str = 'user') -> List[Tuple[str, str]]:
        """Get all bookings for a user"""
        user_bookings = []
        for date, times in self.bookings.items():
            for time, booked_user in times.items():
                if booked_user == user_id:
                    user_bookings.append((date, time))
        return sorted(user_bookings)
