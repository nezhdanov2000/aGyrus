/**
 * Calendar Component
 * Interactive calendar with timeslot management
 */
(function() {
    // Calendar state
    let currentWeekStart = new Date();
    let calendarData = {};
    let myBookingsByTimeslotId = new Set();
    let currentStudentId = null;
    
    // API base URL
    const API_BASE = window.CONFIG ? window.CONFIG.API_BASE : '/backend/api/';
    
    // DOM elements
    let monthTitle, calendarGrid, prevMonthBtn, nextMonthBtn, clearAllBtn;
    
    // Month names
    const monthNames = [
        'january', 'february', 'march', 'april', 'may', 'june',
        'july', 'august', 'september', 'october', 'november', 'december'
    ];
    
    // Day names
    const dayNames = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    
    function getStartOfWeek(date) {
        const d = new Date(date.getFullYear(), date.getMonth(), date.getDate());
        const jsDay = d.getDay(); // 0=Sun, 1=Mon, ... 6=Sat
        const daysFromMonday = jsDay === 0 ? 6 : jsDay - 1; // convert so Monday is 0
        d.setDate(d.getDate() - daysFromMonday);
        d.setHours(0, 0, 0, 0);
        return d;
    }

    // Load calendar data from API
    async function loadCalendarData() {
        const month = currentWeekStart.getMonth();
        const year = currentWeekStart.getFullYear();
        
        
        try {
            // Fetch month calendar and student's bookings in parallel
            const [calRes, myRes, userRes] = await Promise.all([
                fetch(`${API_BASE}tutor-calendar.php?month=${month + 1}&year=${year}`),
                fetch(`${API_BASE}my-bookings.php`),
                fetch(`${API_BASE}get-user.php`)
            ]);
            const data = await calRes.json();
            let my = null;
            try {
                my = await myRes.json();
            } catch (e) {
                my = null;
            }
            try {
                const userData = await userRes.json();
                currentStudentId = (userData && userData.success && userData.user && userData.user.student_id) ? Number(userData.user.student_id) : null;
            } catch (e) {
                currentStudentId = null;
            }
            
            if (data.success) {
                calendarData = data.data;
                
            } else {
                console.error('❌ Failed to load calendar data:', data.error);
                calendarData = {};
            }

            // Build a lookup of student's booked timeslots
            myBookingsByTimeslotId = new Set();
            if (my && my.success && Array.isArray(my.bookings)) {
                my.bookings.forEach(b => {
                    if (b.timeslot_id) {
                        myBookingsByTimeslotId.add(Number(b.timeslot_id));
                    }
                });
            }
            
        } catch (error) {
            console.error('❌ Error loading calendar data:', error);
            calendarData = {};
            myBookingsByTimeslotId = new Set();
            currentStudentId = null;
        }
    }
    
    // Initialize calendar
    async function init() {
        
        
        // Get DOM elements
        monthTitle = document.getElementById('monthTitle');
        calendarGrid = document.getElementById('calendarGrid');
        prevMonthBtn = document.getElementById('prevMonth');
        nextMonthBtn = document.getElementById('nextMonth');
        clearAllBtn = document.getElementById('clearAllBtn');
        
        // Check if elements exist
        if (!monthTitle || !calendarGrid || !prevMonthBtn || !nextMonthBtn || !clearAllBtn) {
            console.error('❌ Required calendar elements not found');
            return;
        }
        
        
        
        // Bind event listeners
        prevMonthBtn.addEventListener('click', () => changeMonth(-1));
        nextMonthBtn.addEventListener('click', () => changeMonth(1));
        clearAllBtn.addEventListener('click', clearAllTimeslots);
        
        // Initialize popup menu (using default navigation)
        if (window.PopupMenu) {
            window.popupMenu = new PopupMenu();
            
        }
        
        // Align current week start to Monday for consistent navigation
        currentWeekStart = getStartOfWeek(currentWeekStart);

        // Load data and render calendar
        await loadCalendarData();
        renderCalendar();
        
        
    }
    
    
    // Change week
    async function changeMonth(direction) {
        // Move to next/previous week (7 days) using milliseconds
        const newTime = currentWeekStart.getTime() + (direction * 7 * 24 * 60 * 60 * 1000);
        currentWeekStart = getStartOfWeek(new Date(newTime));
        
        // Load data for the new week's month and render
        await loadCalendarData();
        renderCalendar();
    }
    
    // Render calendar
    function renderCalendar() {
        const month = currentWeekStart.getMonth();
        const year = currentWeekStart.getFullYear();
        
        
        // Update month title
        monthTitle.textContent = monthNames[month];
        
        // Clear calendar grid
        calendarGrid.innerHTML = '';
        
        // Render week
        renderWeek();
    }
    
    // Render week (7 days from currentWeekStart)
    function renderWeek() {
        for (let i = 0; i < 7; i++) {
            // Create a new date for each day by adding i days in milliseconds
            const dayDate = new Date(currentWeekStart.getTime() + (i * 24 * 60 * 60 * 1000));
            
            const dayNumber = dayDate.getDate();
            const dayOfWeek = dayDate.getDay();
            
            // Convert JavaScript day (0=Sunday) to our dayNames array (0=Monday)
            let dayIndex = dayOfWeek === 0 ? 6 : dayOfWeek - 1; // Sunday becomes index 6
            
            const dayColumn = createDayColumn(dayNumber, dayNames[dayIndex], dayDate);
            calendarGrid.appendChild(dayColumn);
        }
    }
    
    // Create day column
    function createDayColumn(dayNumber, dayName, dayDate) {
        const column = document.createElement('div');
        column.className = 'day-column';
        
        // Day header
        const header = document.createElement('div');
        header.className = 'day-header';
        
        const dayNameEl = document.createElement('div');
        dayNameEl.className = 'day-name';
        dayNameEl.textContent = dayName;
        
        const dayNum = document.createElement('div');
        dayNum.className = 'day-number';
        dayNum.textContent = dayNumber;
        
        header.appendChild(dayNameEl);
        header.appendChild(dayNum);
        
        // Timeslots container
        const timeslotsContainer = document.createElement('div');
        timeslotsContainer.className = 'timeslots';
        
        // Get timeslots for this day from API data
        const year = dayDate.getFullYear();
        const month = dayDate.getMonth();
        const dateKey = `${year}-${String(month + 1).padStart(2, '0')}-${String(dayNumber).padStart(2, '0')}`;
        const timeslots = calendarData[dateKey] || [];
        
        // Create timeslot elements - only show student's own bookings
        timeslots.forEach(timeslot => {
            const isMine = myBookingsByTimeslotId.has(Number(timeslot.timeslot_id)) || (currentStudentId && Number(timeslot.student_id) === currentStudentId);
            
            // Only display timeslots that belong to the current student
            if (!isMine) {
                return; // Skip this timeslot if it's not mine
            }
            
            const timeslotEl = document.createElement('div');
            timeslotEl.className = 'timeslot mine';
            
            let timeslotContent = `
                <div class="timeslot-time">${timeslot.start_time} / ${timeslot.end_time}</div>
                <div class="timeslot-tutor">👨‍🏫 ${timeslot.tutor_name}</div>
                <div class="timeslot-course">📚 ${timeslot.course_name || 'No course'}</div>
                <div class="timeslot-student">👤 Your booking</div>
            `;
            
            timeslotEl.innerHTML = timeslotContent;
            
            // Add click handler for timeslot
            timeslotEl.addEventListener('click', () => {
                handleTimeslotClick(dateKey, timeslot);
            });
            
            timeslotsContainer.appendChild(timeslotEl);
        });
        
        column.appendChild(header);
        column.appendChild(timeslotsContainer);
        
        return column;
    }
    
    // Handle timeslot click
    function handleTimeslotClick(dateKey, timeslot) {
        console.log(`🕐 My booking clicked: ${dateKey}`, timeslot);
        
        let message = `Your Booking: ${dateKey}\n`;
        message += `Time: ${timeslot.start_time} - ${timeslot.end_time}\n`;
        message += `Tutor: ${timeslot.tutor_name}\n`;
        message += `Course: ${timeslot.course_name || 'No course'}\n`;
        message += `Status: Your booking\n`;
        message += `\nWould you like to cancel this booking?`;
        
        if (confirm(message)) {
            // In a real app, this would make an API call to cancel the booking
            alert('This would cancel your booking.\n\nIn a real app, this would make an API call to the backend to cancel the booking.');
        }
    }
    
    // Clear all timeslots
    function clearAllTimeslots() {
        
        
        if (confirm('Are you sure you want to clear all timeslots for this month?')) {
            // In a real app, this would make an API call to delete timeslots
            alert('This would delete all timeslots for the current month.\n\nIn a real app, this would make an API call to the backend.');
            
            // For demo purposes, just clear the local data
            calendarData = {};
            renderCalendar();
            
            
        }
    }
    
    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', init);
    
})();
