// Google Identity Services
let googleAuthInitialized = false;

function initializeGoogleAuth() {
    if (googleAuthInitialized) return;
    
    // Load Google Identity Services
    const script = document.createElement('script');
    script.src = 'https://accounts.google.com/gsi/client';
    script.onload = function() {
        google.accounts.id.initialize({
            client_id: '731314897697-cus8dmpsc44gsfsqteetbp4bu0vlpa9o.apps.googleusercontent.com',
            callback: handleCredentialResponse,
            auto_select: false,
            cancel_on_tap_outside: false
        });
        googleAuthInitialized = true;
    };
    document.head.appendChild(script);
}

// Function to trigger Google Sign-In programmatically
function triggerGoogleSignIn() {
    if (!googleAuthInitialized) {
        initializeGoogleAuth();
        // Wait for initialization
        setTimeout(triggerGoogleSignIn, 500);
        return;
    }
    
    // Trigger the One Tap prompt
    google.accounts.id.prompt((notification) => {
        if (notification.isNotDisplayed() || notification.isSkippedMoment()) {
            // Fallback to popup if One Tap doesn't work
            google.accounts.oauth2.initTokenClient({
                client_id: '731314897697-cus8dmpsc44gsfsqteetbp4bu0vlpa9o.apps.googleusercontent.com',
                scope: 'email profile',
                callback: handleCredentialResponse
            }).requestAccessToken();
        }
    });
}

function handleCredentialResponse(response) {
    // Send the credential to the server
    fetch('../../backend/auth/google/verify.php', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            credential: response.credential
        })
    })
    .then(async response => {
        let data;
        try {
            data = await response.json();
        } catch (e) {
            throw new Error('Invalid JSON response from server');
        }
        return { ok: response.ok, data };
    })
    .then(({ ok, data }) => {
        if (ok && data.success) {
            // Redirect to chatbot as post-auth landing
            window.location.href = '/frontend/html/chat.html';
        } else {
            alert('Authentication failed: ' + (data && data.error ? data.error : 'Unknown error'));
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Authentication failed');
    });
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', initializeGoogleAuth);
