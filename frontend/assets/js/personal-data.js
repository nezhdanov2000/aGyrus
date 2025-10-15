(function() {
    const API_BASE = window.CONFIG ? window.CONFIG.API_BASE : '/backend/api/';
    
    async function init() {
        if (window.PopupMenu) {
            new PopupMenu();
        }
        
        await loadUserData();
        await loadStatistics();
    }
    
    async function loadUserData() {
        try {
            const response = await fetch(`${API_BASE}get-user.php`);
            const data = await response.json();
            
            if (data.success && data.user) {
                const user = data.user;
                const nameElement = document.getElementById('userName');
                const photoElement = document.getElementById('userPhoto');
                
                // Set user name
                const fullName = `${user.name || ''} ${user.surname || ''}`.trim() || 'User';
                nameElement.textContent = fullName;
                
                // Set user photo (Google photo if available)
                if (user.picture) {
                    photoElement.src = user.picture;
                } else if (user.photo_url) {
                    photoElement.src = user.photo_url;
                } else if (user.photo_link) {
                    photoElement.src = user.photo_link;
                }
                photoElement.alt = fullName;
            }
        } catch (error) {
            console.error('Error loading user data:', error);
            document.getElementById('userName').textContent = 'Error loading user data';
        }
    }
    
    async function loadStatistics() {
        try {
            const response = await fetch(`${API_BASE}my-bookings.php`);
            const data = await response.json();
            
            if (data.success && data.bookings) {
                const bookings = data.bookings;
                const today = new Date().toISOString().split('T')[0]; // YYYY-MM-DD format
                
                // Calculate statistics
                const todayClasses = bookings.filter(b => b.date === today).length;
                const uniqueTutors = new Set(bookings.map(b => b.tutor_id)).size;
                const completedClasses = bookings.length; // All bookings are considered completed for now
                
                // Update UI
                document.getElementById('todayClasses').textContent = todayClasses;
                document.getElementById('numberOfTutors').textContent = uniqueTutors;
                document.getElementById('completedClasses').textContent = completedClasses;
            }
        } catch (error) {
            console.error('Error loading statistics:', error);
            // Keep default values (0)
        }
    }
    
    document.addEventListener('DOMContentLoaded', init);
})();
