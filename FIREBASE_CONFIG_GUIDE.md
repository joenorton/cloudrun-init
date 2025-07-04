# Firebase Configuration Guide

## Quick Setup (5 minutes)

### Step 1: Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Create a project"
3. Name it (e.g., "cloudrun-init-demo")
4. Follow the setup wizard (you can disable Google Analytics for now)

### Step 2: Enable Authentication
1. In your Firebase project, click "Authentication" in the left sidebar
2. Click "Get started"
3. Go to "Sign-in method" tab
4. Click "Google" and enable it
5. Add your email as an authorized domain if prompted

### Step 3: Get Your Configuration
1. Click the gear icon (⚙️) next to "Project Overview" to open Project Settings
2. Scroll down to "Your apps" section
3. Click "Add app" and select the web icon (</>)
4. Register your app with a nickname (e.g., "cloudrun-init")
5. Copy the configuration object that looks like this:

```javascript
const firebaseConfig = {
  apiKey: "AIzaSyC...",
  authDomain: "your-project.firebaseapp.com",
  projectId: "your-project-id",
  storageBucket: "your-project.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abc123"
};
```

### Step 4: Update Your Application
1. Open `app/static/index.html`
2. Find the `<script type="module">` section (around line 15)
3. Replace the placeholder configuration with your actual config:

```javascript
// Replace this:
const firebaseConfig = {
    apiKey: "your-api-key",
    authDomain: "your-project.firebaseapp.com",
    projectId: "your-project-id",
    storageBucket: "your-project.appspot.com",
    messagingSenderId: "123456789",
    appId: "your-app-id"
};

// With your actual config from Firebase Console
```

### Step 5: Test
1. Refresh your browser at `http://localhost:5000`
2. Open browser console (F12) to see Firebase initialization messages
3. Click "Sign In with Google"
4. Complete the OAuth flow
5. Check console for the Firebase ID token

## Troubleshooting

### "Firebase not configured" error
- Make sure you replaced ALL placeholder values in the config
- Check that your `apiKey` and `projectId` are not the placeholder values

### "Sign in failed" error
- Make sure Google authentication is enabled in Firebase Console
- Check that your domain is authorized (localhost should work for development)

### Console shows warnings
- Look for the warning message about Firebase configuration
- Follow the steps above to update the config

### Page not loading
- Check browser console for JavaScript errors
- Make sure you're using a modern browser that supports ES6 modules

## What You Should See

### Before Configuration:
- Page loads but shows "Firebase not configured" in console
- Sign-in button shows error when clicked

### After Configuration:
- Console shows "✅ Firebase initialized successfully"
- Sign-in button works and opens Google OAuth popup
- After sign-in, user info appears and token is logged to console

## Next Steps

Once Firebase is working:
1. Test the `/auth/me` endpoint with the logged token
2. Set up backend Firebase service account for full functionality
3. Deploy to Cloud Run when ready 