(function(){
    // Reuse calendar logic but filter by tutor_id from URL
    const API_BASE = window.CONFIG ? window.CONFIG.API_BASE : '/backend/api/';
    let currentWeekStart = new Date();
    let calendarData = {};
    let myBookingsByTimeslotId = new Set();
    let currentStudentId = null;
    let tutorId = null;

    let monthTitle, calendarGrid, prevMonthBtn, nextMonthBtn;
    const monthNames = ['january','february','march','april','may','june','july','august','september','october','november','december'];
    const dayNames = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];

    function getStartOfWeek(date){
        const d = new Date(date.getFullYear(), date.getMonth(), date.getDate());
        const jsDay = d.getDay();
        const daysFromMonday = jsDay === 0 ? 6 : jsDay - 1;
        d.setDate(d.getDate() - daysFromMonday);
        d.setHours(0,0,0,0);
        return d;
    }

    function getTutorIdFromUrl(){
        const params = new URLSearchParams(window.location.search);
        const id = Number(params.get('tutor_id'));
        return Number.isFinite(id) && id > 0 ? id : null;
    }

    async function loadCalendarData(){
        const month = currentWeekStart.getMonth();
        const year = currentWeekStart.getFullYear();
        try{
            const [calRes, myRes, userRes] = await Promise.all([
                fetch(`${API_BASE}tutor/tutor-calendar.php?month=${month+1}&year=${year}&tutor_id=${tutorId}`),
                fetch(`${API_BASE}booking/my-bookings.php`),
                fetch(`${API_BASE}auth/get-user.php`)
            ]);
            const data = await calRes.json();
            const my = await myRes.json().catch(()=>null);
            const userData = await userRes.json().catch(()=>null);
            currentStudentId = (userData && userData.success && userData.user && userData.user.student_id) ? Number(userData.user.student_id) : null;

            if (data && data.success) {
                calendarData = data.data;
            } else {
                calendarData = {};
            }

            myBookingsByTimeslotId = new Set();
            if (my && my.success && Array.isArray(my.bookings)) {
                my.bookings.forEach(b => { if (b.timeslot_id) myBookingsByTimeslotId.add(Number(b.timeslot_id)); });
            }
        }catch(err){
            calendarData = {};
            myBookingsByTimeslotId = new Set();
            currentStudentId = null;
        }
    }

    async function init(){
        tutorId = getTutorIdFromUrl();
        if(!tutorId){
            alert('Tutor not specified');
            return;
        }

        monthTitle = document.getElementById('monthTitle');
        calendarGrid = document.getElementById('calendarGrid');
        prevMonthBtn = document.getElementById('prevMonth');
        nextMonthBtn = document.getElementById('nextMonth');
        if (window.PopupMenu) new PopupMenu();

        prevMonthBtn.addEventListener('click', ()=> changeWeek(-1));
        nextMonthBtn.addEventListener('click', ()=> changeWeek(1));

        currentWeekStart = getStartOfWeek(currentWeekStart);
        await loadCalendarData();
        renderCalendar();
    }

    async function changeWeek(dir){
        currentWeekStart = getStartOfWeek(new Date(currentWeekStart.getTime() + dir*7*24*60*60*1000));
        await loadCalendarData();
        renderCalendar();
    }

    function renderCalendar(){
        const month = currentWeekStart.getMonth();
        monthTitle.textContent = monthNames[month];
        calendarGrid.innerHTML = '';
        renderWeek();
    }

    function renderWeek(){
        for (let i=0;i<7;i++){
            const dayDate = new Date(currentWeekStart.getTime() + i*24*60*60*1000);
            const dayNumber = dayDate.getDate();
            const dayOfWeek = dayDate.getDay();
            const dayIndex = dayOfWeek === 0 ? 6 : dayOfWeek - 1;
            const column = createDayColumn(dayNumber, dayNames[dayIndex], dayDate);
            calendarGrid.appendChild(column);
        }
    }

    function createDayColumn(dayNumber, dayName, dayDate){
        const column = document.createElement('div');
        column.className = 'day-column';
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
        const timeslotsContainer = document.createElement('div');
        timeslotsContainer.className = 'timeslots';

        const year = dayDate.getFullYear();
        const month = dayDate.getMonth();
        const dateKey = `${year}-${String(month+1).padStart(2,'0')}-${String(dayNumber).padStart(2,'0')}`;
        const timeslots = calendarData[dateKey] || [];

        timeslots.forEach(ts => {
            const el = document.createElement('div');
            const isMine = myBookingsByTimeslotId.has(Number(ts.timeslot_id)) || (currentStudentId && Number(ts.student_id)===currentStudentId);
            const stateClass = isMine ? 'mine' : (ts.is_booked ? 'booked' : 'available');
            el.className = `timeslot ${stateClass}`;
            el.innerHTML = `
                <div class="timeslot-time">${ts.start_time} / ${ts.end_time}</div>
                <div class="timeslot-tutor">👨‍🏫 ${ts.tutor_name}</div>
                <div class="timeslot-course">📚 ${ts.course_name || 'No course'}</div>
            ` + (!isMine && ts.is_booked ? `<div class="timeslot-student">👤 ${ts.student_nickname || 'Unknown'}</div>` : '') +
            (isMine && ts.repeatability === 'repeated' ? `<div class="timeslot-recurring">🔄 Recurring</div>` : '');
            el.addEventListener('click', ()=> handleTimeslotClick(dateKey, ts));
            timeslotsContainer.appendChild(el);
        });

        column.appendChild(header);
        column.appendChild(timeslotsContainer);
        return column;
    }

    async function handleTimeslotClick(dateKey, ts){
        // Check if it's my booking - allow cancellation
        const isMine = myBookingsByTimeslotId.has(Number(ts.timeslot_id)) || (currentStudentId && Number(ts.student_id) === currentStudentId);
        
        if (isMine && ts.booking_id) {
            // Check if it's a recurring booking
            if (ts.repeatability === 'repeated') {
                const cancelAll = confirm(`Cancel recurring booking?\n${dateKey}\n${ts.start_time} - ${ts.end_time}\n${ts.tutor_name}\n\nOK = Cancel ALL future recurring bookings\nCancel = Cancel only this one`);
                
                if (cancelAll) {
                    // Cancel all recurring bookings
                    try {
                        const response = await fetch(`${API_BASE}recurring/cancel-recurring.php`, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ timeslot_id: ts.timeslot_id })
                        });

                        const result = await response.json();
                        
                        if (result.success) {
                            alert(`Cancelled ${result.cancelled_count} recurring bookings!`);
                            await loadCalendarData();
                            renderCalendar();
                        } else {
                            alert(`Cancellation failed: ${result.error}`);
                        }
                    } catch (error) {
                        alert('Network error. Please try again.');
                    }
                    return;
                }
            }
            
            // Cancel single booking
            if (!confirm(`Cancel this booking?\n${dateKey}\n${ts.start_time} - ${ts.end_time}\n${ts.tutor_name}`)) {
                return;
            }

            try {
                const response = await fetch(`${API_BASE}booking/cancel-booking.php`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ booking_id: ts.booking_id })
                });

                const result = await response.json();
                
                if (result.success) {
                    alert('Booking cancelled successfully!');
                    await loadCalendarData();
                    renderCalendar();
                } else {
                    alert(`Cancellation failed: ${result.error}`);
                }
            } catch (error) {
                alert('Network error. Please try again.');
            }
            return;
        }

        // Only allow booking available timeslots
        if (ts.is_booked) {
            alert(`This timeslot is already booked by ${ts.student_nickname || 'Unknown'}`);
            return;
        }

        // Show booking options
        const bookingType = confirm(`Book this timeslot?\n${dateKey}\n${ts.start_time} - ${ts.end_time}\n${ts.tutor_name}\n\nClick OK for one-time booking\nClick Cancel to choose booking type`);
        
        if (bookingType === null) {
            return; // User cancelled
        }
        
        // Ask for booking type
        const isRecurring = confirm(`Choose booking type:\n\nOK = Recurring (auto-book similar timeslots)\nCancel = One-time booking`);

        try {
            const response = await fetch(`${API_BASE}booking/book-timeslot.php`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    timeslot_id: ts.timeslot_id,
                    recurring: isRecurring
                })
            });

            const result = await response.json();
            
            if (result.success) {
                let message = result.recurring ? 
                    'Recurring booking created! You will be automatically booked for similar timeslots.' :
                    'Successfully booked!';
                
                if (result.existing_count > 0) {
                    message += `\n\nAlso automatically booked ${result.existing_count} existing matching timeslots!`;
                }
                
                alert(message);
                // Reload calendar data to show updated booking
                await loadCalendarData();
                renderCalendar();
            } else {
                alert(`Booking failed: ${result.error}`);
            }
        } catch (error) {
            alert('Network error. Please try again.');
        }
    }

    document.addEventListener('DOMContentLoaded', init);
})();


