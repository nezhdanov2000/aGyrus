// Interactive chatbot with appointment booking functionality
(function () {
    let dialogState = 'idle';
    let currentData = {};
    const API_BASE = window.CONFIG ? window.CONFIG.API_BASE : '../../backend/api/';
    let input, sendBtn, chat;
    
    // Utility: scroll to bottom
    function scrollToBottom() {
        setTimeout(() => window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' }), 100);
    }
    
    // Handle menu section navigation
    function handleMenuSection(section) {
        switch(section) {
            case 'personal':
                showMainMenu('Personal data management');
                break;
            case 'calendar':
                // Navigate to calendar page
                window.location.href = 'calendar.html';
                break;
            case 'find-tutors':
                startTutorSearch();
                break;
            case 'my-tutors':
                showMyBookings();
                break;
            case 'ai':
                showMainMenu('AI Assistant');
                break;
            default:
                showMainMenu('Welcome to Gyrus AI');
        }
    }
    
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
                    window.location.href = 'index.html';
                }
            })
            .catch(error => {
                console.error('Error loading user data:', error);
            });
    }

    function appendUserBubble(text) {
        const avatarSrc = window.userData?.picture || 'https://i.pravatar.cc/80?img=12';
        const wrap = document.createElement('div');
        wrap.className = 'bubble user';
        wrap.innerHTML = `<div class="content"></div><img class="avatar" src="${avatarSrc}" alt="User"/>`;
        wrap.querySelector('.content').textContent = text;
        chat.appendChild(wrap);
        scrollToBottom();
    }

    function appendBotBubble(text, buttons = []) {
        const wrap = document.createElement('div');
        wrap.className = 'bubble bot';
        wrap.innerHTML = '<div class="content"></div><img class="agent" src="../assets/images/logo.png" alt="Agent"/>';
        
        const content = wrap.querySelector('.content');
        content.textContent = text;
        
        if (buttons.length) {
            const container = document.createElement('div');
            container.className = 'button-container';
            Object.assign(container.style, { marginTop: '10px', display: 'flex', flexWrap: 'wrap', gap: '8px' });
            
            buttons.forEach(button => {
                const btn = document.createElement('button');
                btn.className = 'action-btn';
                btn.textContent = button.text;
                btn.style.cssText = 'background:#e8f0fe;border:1px solid #dadce0;border-radius:8px;padding:8px 12px;font-size:14px;cursor:pointer;transition:background 0.2s';
                btn.onclick = button.action;
                container.appendChild(btn);
            });
            
            content.appendChild(container);
        }
        
        chat.appendChild(wrap);
        scrollToBottom();
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
        
        fetch(API_BASE + 'book-timeslot.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                timeslot_id: timeslot.timeslot_id
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

    function processMessage(text, context = {}) {
        return fetch(API_BASE + '../AI/api/process_message.php', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text, context })
        })
        .then(response => response.json())
        .catch(error => {
            console.error('Message processing error:', error);
            return { success: false, intent: 'general', entities: {} };
        });
    }

    function handleSend() {
        const text = input.value.trim();
        if (!text) return;
        
        appendUserBubble(text);
        input.value = '';

        // Special handling for active dialog states
        if (dialogState === 'searching_tutor') {
            searchTutors(text);
            return;
        }

        // Process message with AI
        processMessage(text, currentData).then(result => {
            if (!result.success) return handleFallback(text);
            
            console.log(`Intent: ${result.intent} (confidence: ${result.confidence})`);
            console.log('Entities:', result.entities);
            
            // Store entities in current data
            if (result.entities) {
                Object.assign(currentData, result.entities);
            }
            
            // Check if AI needs clarification
            if (result.needs_clarification) {
                appendBotBubble(result.response.message);
                return;
            }
            
            // Execute action based on intent and extracted entities
            handleAIAction(result);
        });
    }
    
    function handleAIAction(result) {
        const intent = result.intent;
        const entities = result.entities || {};
        
        if (intent === 'search_tutor') {
            // If we have a subject or tutor name, search directly
            if (entities.subject || entities.tutor_name) {
                const query = entities.subject || entities.tutor_name;
                searchTutors(query);
            } else {
                startTutorSearch();
            }
        }
        else if (intent === 'view_bookings') {
            showMyBookings();
        }
        else if (intent === 'cancel_booking') {
            startCancelBooking();
        }
        else {
            handleFallback();
        }
    }
    
    function handleFallback(text = '') {
        const lower = text.toLowerCase();
        if (lower.includes('tutor') || lower.includes('find')) return startTutorSearch();
        if (lower.includes('booking') || lower.includes('appointment')) return showMyBookings();
        
        appendBotBubble('I didn\'t understand that. Please use the menu buttons or try "find tutor" or "my bookings".');
        showMainMenu();
    }

    // Initialize
    document.addEventListener('DOMContentLoaded', () => {
        input = document.getElementById('messageInput');
        sendBtn = document.getElementById('sendBtn');
        chat = document.querySelector('.chat');
        
        if (!input || !sendBtn || !chat) {
            console.error('Required DOM elements not found');
            return;
        }
        
        sendBtn.addEventListener('click', handleSend);
        input.addEventListener('keydown', e => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSend();
            }
        });

        loadUserData();
        showMainMenu();
        
        // Initialize menu
        if (window.PopupMenu) {
            window.popupMenu = new PopupMenu({ onSectionChange: handleMenuSection });
        }
    });
})();


