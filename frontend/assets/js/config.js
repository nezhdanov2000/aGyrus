/**
 * Configuration file for frontend paths
 * This file centralizes all API endpoints and paths
 * Making the project portable across different environments
 */

// Base configuration
const CONFIG = {
    // Base URL for API endpoints
    // Use relative paths for portability
    API_BASE: '/backend/api/',
    
    // Alternative: Use localhost for local development
    // API_BASE: 'http://localhost/backend/api/',
    
    // Frontend base URL
    FRONTEND_BASE: '../',
    
    // Assets paths
    ASSETS_BASE: '../assets/',
    
    // Components paths  
    COMPONENTS_BASE: '../components/',
    
    // HTML pages paths
    PAGES_BASE: '../html/'
};

// Export for use in other scripts
window.CONFIG = CONFIG;

// Log configuration for debugging
console.log('Frontend Configuration:', CONFIG);
