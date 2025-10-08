// Interactive chatbot with appointment booking functionality
(function () {
    const input = document.getElementById('messageInput');
    const sendBtn = document.getElementById('sendBtn');
    const chat = document.querySelector('.chat');
    
    // Dialog state management
    let dialogState = 'idle';
    let currentData = {};
    
    // API base URL
    const API_BASE = '/backend/api/';
    
    // Load user data on page load
    function loadUserData() {
        fetch(API_BASE + 'get-user.php')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.userData = data.user;
                    console.log('User data loaded:', data.user);
                    // Update existing avatars with user's photo
                    document.querySelectorAll('.bubble.user .avatar').forEach(avatar => {
                        avatar.src = data.user.picture;
                    });
                } else {
                    console.error('User not authenticated:', data.error);
                    // Redirect to login if not authenticated
                    window.location.href = '/frontend/html/index.html';
                }
            })
            .catch(error => {
                console.error('Error loading user data:', error);
            });
    }
    
    // Load user data immediately
    loadUserData();

    function appendUserBubble(text) {
        const wrap = document.createElement('div');
        wrap.className = 'bubble user';
        
        // Use user's photo from PHP or fallback to existing avatar
        const avatarSrc = (window.userData && window.userData.picture) || 
                         (document.querySelector('.bubble.user .avatar')?.src) || 
                         'https://i.pravatar.cc/80?img=12';
        
        wrap.innerHTML = '<div class="content"></div>' +
            `<img class="avatar" src="${avatarSrc}" alt="User"/>`;
        wrap.querySelector('.content').textContent = text;
        chat.appendChild(wrap);
        chat.scrollTo({ top: chat.scrollHeight, behavior: 'smooth' });
    }

    function appendBotBubble(text, buttons = []) {
        const wrap = document.createElement('div');
        wrap.className = 'bubble bot';
        wrap.innerHTML = '<div class="content"></div>' +
            '<img class="agent" src="/frontend/assets/images/logo.png" alt="Agent"/>';
        
        const content = wrap.querySelector('.content');
        content.textContent = text;
        
        if (buttons.length > 0) {
            const buttonContainer = document.createElement('div');
            buttonContainer.className = 'button-container';
            buttonContainer.style.marginTop = '10px';
            buttonContainer.style.display = 'flex';
            buttonContainer.style.flexWrap = 'wrap';
            buttonContainer.style.gap = '8px';
            
            buttons.forEach(button => {
                const btn = document.createElement('button');
                btn.className = 'action-btn';
                btn.textContent = button.text;
                btn.style.cssText = `
                    background: #e8f0fe;
                    border: 1px solid #dadce0;
                    border-radius: 8px;
                    padding: 8px 12px;
                    font-size: 14px;
                    cursor: pointer;
                    transition: background 0.2s;
                `;
                btn.addEventListener('click', () => button.action());
                buttonContainer.appendChild(btn);
            });
            
            content.appendChild(buttonContainer);
        }
        
        chat.appendChild(wrap);
        chat.scrollTo({ top: chat.scrollHeight, behavior: 'smooth' });
    }

    function showMainMenu() {
        dialogState = 'idle';
        currentData = {};
        
        appendBotBubble('Hi! I can help you with appointments. What would you like to do?', [
            { text: '🔍 Find Tutor', action: () => startTutorSearch() },
            { text: '📅 My Bookings', action: () => showMyBookings() },
            { text: '❌ Cancel Booking', action: () => startCancelBooking() }
        ]);
    }

    function startTutorSearch() {
        dialogState = 'searching_tutor';
        appendUserBubble('Find Tutor');
        appendBotBubble('Please enter the tutor name or subject you want to search for:');
    }

    function searchTutors(query) {
        fetch(API_BASE + 'search-tutors.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success && data.tutors.length > 0) {
                currentData.tutors = data.tutors;
                dialogState = 'selecting_tutor';
                
                const buttons = data.tutors.map(tutor => ({
                    text: `${tutor.name} ${tutor.surname} (${tutor.courses})`,
                    action: () => selectTutor(tutor)
                }));
                
                appendBotBubble(`Found ${data.count} tutor(s):`, buttons);
            } else {
                appendBotBubble('No tutors found. Try a different search term.');
                showMainMenu();
            }
        })
        .catch(error => {
            console.error('Search error:', error);
            appendBotBubble('Sorry, there was an error searching for tutors.');
            showMainMenu();
        });
    }

    function selectTutor(tutor) {
        currentData.selectedTutor = tutor;
        dialogState = 'selecting_date';
        appendUserBubble(`${tutor.name} ${tutor.surname}`);
        
        fetch(API_BASE + `tutor-dates.php?tutor_id=${tutor.tutor_id}`)
        .then(response => response.json())
        .then(data => {
            if (data.success && data.dates.length > 0) {
                const buttons = data.dates.map(date => ({
                    text: `${date.date} (${date.available_slots} slots)`,
                    action: () => selectDate(date.date)
                }));
                
                appendBotBubble(`Available dates for ${tutor.name}:`, buttons);
            } else {
                appendBotBubble('No available dates found for this tutor.');
                showMainMenu();
            }
        })
        .catch(error => {
            console.error('Date fetch error:', error);
            appendBotBubble('Sorry, there was an error fetching available dates.');
            showMainMenu();
        });
    }

    function selectDate(date) {
        currentData.selectedDate = date;
        dialogState = 'selecting_timeslot';
        appendUserBubble(date);
        
        fetch(API_BASE + `tutor-timeslots.php?tutor_id=${currentData.selectedTutor.tutor_id}&date=${date}`)
        .then(response => response.json())
        .then(data => {
            if (data.success && data.timeslots.length > 0) {
                const buttons = data.timeslots.map(slot => ({
                    text: `${slot.start_time} - ${slot.end_time}`,
                    action: () => bookTimeslot(slot)
                }));
                
                appendBotBubble(`Available timeslots on ${date}:`, buttons);
            } else {
                appendBotBubble('No available timeslots found for this date.');
                showMainMenu();
            }
        })
        .catch(error => {
            console.error('Timeslot fetch error:', error);
            appendBotBubble('Sorry, there was an error fetching timeslots.');
            showMainMenu();
        });
    }

    function bookTimeslot(timeslot) {
        appendUserBubble(`${timeslot.start_time} - ${timeslot.end_time}`);
        
        // Get the first course ID from tutor's courses
        const courseId = currentData.selectedTutor.course_ids 
            ? parseInt(currentData.selectedTutor.course_ids.split(',')[0].trim())
            : 1;
        
        fetch(API_BASE + 'book-timeslot.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                timeslot_id: timeslot.timeslot_id,
                course_id: courseId
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                appendBotBubble(`✅ Booking confirmed! You have an appointment with ${currentData.selectedTutor.name} on ${currentData.selectedDate} at ${timeslot.start_time}.`, [
                    { text: '📅 My Bookings', action: () => showMyBookings() },
                    { text: '🏠 Main Menu', action: () => showMainMenu() }
                ]);
            } else {
                appendBotBubble(`❌ Booking failed: ${data.error}`);
                showMainMenu();
            }
        })
        .catch(error => {
            console.error('Booking error:', error);
            appendBotBubble('Sorry, there was an error creating the booking.');
            showMainMenu();
        });
    }

    function showMyBookings(showCancelButtons = false) {
        appendUserBubble('My Bookings');
        
        fetch(API_BASE + 'my-bookings.php')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.bookings.length > 0) {
                let message = 'Your current bookings:\n\n';
                const buttons = [];
                
                data.bookings.forEach(booking => {
                    message += `📅 ${booking.date} at ${booking.start_time}\n`;
                    message += `👨‍🏫 ${booking.tutor_name} ${booking.tutor_surname}\n`;
                    message += `📚 ${booking.course_name}\n\n`;
                    
                    // Add cancel button for each booking if requested
                    if (showCancelButtons) {
                        buttons.push({
                            text: `❌ Cancel ${booking.date} ${booking.start_time}`,
                            action: () => cancelBooking(booking.booking_id, booking)
                        });
                    }
                });
                
                // Add main menu button
                buttons.push({ text: '🏠 Main Menu', action: () => showMainMenu() });
                
                appendBotBubble(message, buttons);
            } else {
                appendBotBubble('You have no current bookings.', [
                    { text: '🔍 Find Tutor', action: () => startTutorSearch() },
                    { text: '🏠 Main Menu', action: () => showMainMenu() }
                ]);
            }
        })
        .catch(error => {
            console.error('Bookings fetch error:', error);
            appendBotBubble('Sorry, there was an error fetching your bookings.');
            showMainMenu();
        });
    }

    function startCancelBooking() {
        appendUserBubble('Cancel Booking');
        showMyBookings(true); // Show bookings with cancel options
    }

    function cancelBooking(bookingId, booking) {
        appendUserBubble(`Cancel ${booking.date} ${booking.start_time}`);
        
        fetch(API_BASE + 'cancel-booking.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ booking_id: bookingId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                appendBotBubble(`✅ Booking cancelled successfully! Your appointment with ${booking.tutor_name} on ${booking.date} at ${booking.start_time} has been cancelled.`, [
                    { text: '📅 My Bookings', action: () => showMyBookings() },
                    { text: '🏠 Main Menu', action: () => showMainMenu() }
                ]);
            } else {
                appendBotBubble(`❌ Cancellation failed: ${data.error}`, [
                    { text: '🏠 Main Menu', action: () => showMainMenu() }
                ]);
            }
        })
        .catch(error => {
            console.error('Cancel booking error:', error);
            appendBotBubble('Sorry, there was an error cancelling the booking.', [
                { text: '🏠 Main Menu', action: () => showMainMenu() }
            ]);
        });
    }

    function handleSend() {
        const text = (input.value || '').trim();
        if (!text) return;
        
        appendUserBubble(text);
        input.value = '';

        switch (dialogState) {
            case 'searching_tutor':
                searchTutors(text);
                break;
            default:
                // Handle natural language or show main menu
                if (text.toLowerCase().includes('tutor') || text.toLowerCase().includes('find')) {
                    startTutorSearch();
                } else if (text.toLowerCase().includes('booking') || text.toLowerCase().includes('appointment')) {
                    showMyBookings();
                } else {
                    appendBotBubble('I didn\'t understand that. Please use the menu buttons or try "find tutor" or "my bookings".');
                    showMainMenu();
                }
        }
    }

    // Initialize chatbot
    function init() {
        showMainMenu();
    }

    // Event listeners
    sendBtn.addEventListener('click', handleSend);
    input.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    });

    // Start the chatbot
    init();
})();


