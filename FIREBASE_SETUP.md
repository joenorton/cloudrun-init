# Firebase Setup Guide for Cloudrun-init

## Quick Setup Steps

### 1. Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Create a project" or select an existing project
3. Follow the setup wizard

### 2. Enable Authentication

1. In your Firebase project, go to **Authentication** in the left sidebar
2. Click **Get started**
3. Go to the **Sign-in method** tab
4. Enable **Google** as a sign-in provider
5. Configure the OAuth consent screen if prompted

### 3. Get Firebase Configuration

1. Go to **Project Settings** (gear icon in the top left)
2. Scroll down to **Your apps** section
3. Click **Add app** and select **Web** (</>)
4. Register your app with a nickname (e.g., "cloudrun-init")
5. Copy the Firebase configuration object

### 4. Update Frontend Configuration

Edit `app/static/index.html` and replace the Firebase configuration in the `<script type="module">` section:

```javascript
const firebaseConfig = {
    apiKey: "your-actual-api-key",
    authDomain: "your-project.firebaseapp.com",
    projectId: "your-project-id",
    storageBucket: "your-project.appspot.com",
    messagingSenderId: "123456789",
    appId: "your-app-id"
};
```

**Note:** The frontend now uses the modern modular Firebase SDK (v9+) with ES6 imports. The configuration is located in the `<script type="module">` block near the top of the file.

### 5. Set up Service Account (Optional for Local Development)

For full functionality including backend token verification:

1. In **Project Settings** > **Service accounts**
2. Click **Generate new private key**
3. Download the JSON file
4. Create a `.env` file in your project root:

```bash
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_SERVICE_ACCOUNT_KEY=/path/to/your-service-account-key.json
SECRET_KEY=your-secret-key-here
```

### 6. Test Authentication

1. Restart your Flask development server
2. Go to `http://localhost:5000`
3. Click "Sign In with Google"
4. Complete the OAuth flow
5. Check the browser console for the Firebase ID token

## Troubleshooting

### "Firebase App named '[DEFAULT]' already exists"

This error occurs if Firebase is initialized multiple times. The app handles this automatically, but if you see this error, it means the initialization is working correctly.

### "No authentication token provided"

This is expected when you're not logged in. The `/auth/me` endpoint requires authentication.

### "Invalid or expired authentication token"

This means the Firebase token verification failed. Make sure:
- Your Firebase project is correctly configured
- The service account key is valid
- The token hasn't expired

### "Module not found" or import errors

The frontend now uses ES6 modules. Make sure:
- You're using a modern browser that supports ES6 modules
- The Firebase configuration is in the correct `<script type="module">` block
- The import URLs are correct and accessible

## Local Development Without Firebase

For development without Firebase setup:

1. The app will still run and serve the frontend
2. API endpoints will work (except authentication-related ones)
3. You'll see warnings about Firebase initialization - this is normal
4. The `/auth/me` endpoint will return 401 (unauthorized) without valid tokens

## Next Steps

Once Firebase is configured:

1. Test the sign-in flow
2. Test the `/auth/me` endpoint with a valid token
3. Check that user information is displayed correctly
4. Test the logout functionality
5. Verify the Firebase ID token is logged to the console

## Security Notes

- Never commit your Firebase service account key to version control
- Use environment variables for sensitive configuration
- The `.env` file is already in `.gitignore`
- In production, use Google Cloud Secret Manager for sensitive data 