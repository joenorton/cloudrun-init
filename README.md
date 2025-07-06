# Cloudrun-init

A modern Flask-based web application skeleton for Google Cloud Run, inspired by gae-init but reimagined for the container-native, Python 3+ GCP world.

## 🚀 Features

- **Flask 3.x** with factory pattern and blueprint architecture
- **Firebase Authentication** with modern modular SDK (v9+) and JWT token verification
- **Google Cloud NDB** for data persistence
- **HTMX + Alpine.js** for modern, lightweight frontend
- **Tailwind CSS** for styling
- **Docker** multi-stage builds
- **Pytest** testing framework with comprehensive test coverage
- **Local development** with live reload
- **Cloud Run** ready deployment

## 📋 Phase 0.2 Goals (Current)

- ✅ Flask app scaffold with factory pattern
- ✅ Firebase authentication integration
- ✅ Protected routes with `@login_required` decorator
- ✅ `/me` endpoint returning current user info
- ✅ **User persistence with `google-cloud-ndb`**
- ✅ **User model with Firebase UID mapping**
- ✅ **Profile endpoints for viewing/editing user data**
- ✅ **Datastore emulator support for local development**
- ✅ **Middleware for automatic user creation/update**
- ✅ **Comprehensive test coverage for user functionality**
- ✅ Basic project layout and structure
- ✅ Minimal frontend with Firebase SDK
- ✅ Local development support
- ✅ Testing framework with mocked Firebase tokens

## 🏗️ Project Structure

```
cloudrun-init/
├── app/
│   ├── __init__.py
│   ├── main.py              # Flask factory + gunicorn entrypoint
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── firebase.py      # Firebase auth utilities
│   │   └── user_middleware.py # User persistence middleware
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py          # User model with NDB
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication routes
│   │   └── profile.py       # Profile management routes
│   ├── ndb_client.py        # NDB client configuration
│   └── static/
│       └── index.html       # Main frontend page
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest configuration
│   ├── test_auth.py         # Authentication tests
│   ├── test_user_model.py   # User model tests
│   └── test_profile_routes.py # Profile routes tests
├── Dockerfile               # Multi-stage Docker build
├── Makefile                 # Development commands
├── requirements.txt         # Python dependencies
├── env.example              # Environment variables template
└── README.md
```

## 🛠️ Quick Start

### Prerequisites

- Python 3.11+
- Docker (optional)
- Firebase project with Authentication enabled
- Google Cloud project (optional for local development)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd cloudrun-init
   ```

2. **Install dependencies**
   ```bash
   make install
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your Firebase configuration
   ```

4. **Run the development server**
   ```bash
   # For basic development (without database)
   make dev
   
   # For development with Datastore emulator
   make dev-db
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

### Docker Development

1. **Build the Docker image**
   ```bash
   make docker-build
   ```

2. **Run the container**
   ```bash
   make docker-run
   ```

3. **Access the application**
   Navigate to `http://localhost:8080`

## 🧪 Testing

### Run all tests
```bash
make test
```

### Run tests with coverage
```bash
make test-cov
```

### Run linting
```bash
make lint
```

## 🔐 Firebase Configuration

### 1. Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or select an existing one
3. Enable Authentication and add Google as a sign-in provider

### 2. Get Firebase Configuration

1. Go to Project Settings > General
2. Scroll down to "Your apps" section
3. Add a web app if you haven't already
4. Copy the Firebase configuration object

### 3. Set up Service Account

1. Go to Project Settings > Service Accounts
2. Click "Generate new private key"
3. Download the JSON file
4. Set the path in your `.env` file

### 4. Update Frontend Configuration

Edit `app/static/index.html` and replace the Firebase configuration:

```javascript
const firebaseConfig = {
    apiKey: "your-api-key",
    authDomain: "your-project.firebaseapp.com",
    projectId: "your-project-id",
    storageBucket: "your-project.appspot.com",
    messagingSenderId: "123456789",
    appId: "your-app-id"
};
```

## 🌐 API Endpoints

### Public Endpoints

- `GET /` - Main application page
- `GET /health` - Health check
- `GET /version` - Application version
- `GET /auth/status` - Authentication status (optional auth)
- `POST /auth/login` - Login with Firebase token
- `POST /auth/logout` - Logout
- `POST /auth/verify` - Verify Firebase token

### Protected Endpoints

- `GET /auth/me` - Get current user information (requires authentication)
- `GET /profile/` - Get current user's profile (requires authentication)
- `PUT /profile/` - Update user's profile (requires authentication)
- `GET /profile/stats` - Get user statistics (requires authentication)
- `POST /profile/sync` - Sync profile with Firebase data (requires authentication)

## 🔧 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Flask secret key | Yes |
| `FIREBASE_PROJECT_ID` | Firebase project ID | Yes |
| `GOOGLE_CLOUD_PROJECT` | Google Cloud project ID | No (for local dev) |
| `FIREBASE_SERVICE_ACCOUNT_KEY` | Path to Firebase service account JSON | No (uses default credentials) |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to Google Cloud service account JSON | No |
| `DATASTORE_PROJECT_ID` | Google Cloud project ID for Datastore | No (uses GOOGLE_CLOUD_PROJECT) |
| `DATASTORE_EMULATOR_HOST` | Datastore emulator host (e.g., localhost:8081) | No (for local development) |

## 👤 User Persistence

### Overview

The application now includes user persistence using Google Cloud NDB (Datastore). When a user authenticates with Firebase, their information is automatically stored in the database and can be retrieved/updated through the profile endpoints.

### Features

- **Automatic User Creation**: Users are created in the database on first login
- **Profile Management**: View and update user profile information
- **Firebase Sync**: Keep local user data in sync with Firebase
- **Local Development**: Full functionality with Datastore emulator

### User Model

The `User` model includes:
- `uid`: Firebase user ID (unique identifier)
- `email`: User's email address
- `display_name`: User's display name
- `created_at`: Account creation timestamp
- `updated_at`: Last update timestamp
- `email_verified`: Email verification status
- `picture`: Profile picture URL
- `provider_id`: OAuth provider used

### Local Development with Datastore

1. **Start the Datastore emulator**
   ```bash
   make emulator
   ```
   
   > **Note**: If you get an error about invalid choice 'datastore', try:
   > ```bash
   > gcloud beta emulators datastore start --host-port=localhost:8081 --project=fake-project
   > ```

2. **Run the app with emulator support**
   ```bash
   make dev-db
   ```

3. **Test the functionality**
   ```bash
   python test_user_persistence.py
   ```

### API Usage

```bash
# Get user profile
curl -H "Authorization: Bearer YOUR_FIREBASE_TOKEN" \
     http://localhost:5000/profile/

# Update display name
curl -X PUT \
     -H "Authorization: Bearer YOUR_FIREBASE_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"display_name": "New Name"}' \
     http://localhost:5000/profile/

# Get user statistics
curl -H "Authorization: Bearer YOUR_FIREBASE_TOKEN" \
     http://localhost:5000/profile/stats

# Sync with Firebase data
curl -X POST \
     -H "Authorization: Bearer YOUR_FIREBASE_TOKEN" \
     http://localhost:5000/profile/sync
```

## 🚀 Deployment

1. **Build and push to Container Registry**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/cloudrun-init
   ```

2. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy cloudrun-init \
     --image gcr.io/PROJECT_ID/cloudrun-init \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --port 8080
   ```

### Using Makefile

```bash
make deploy
```

## 🧭 Roadmap

### Phase 0.2 (Next)
- [ ] NDB models implementation
- [ ] User data persistence
- [ ] Authenticated pages and routes

### Phase 0.3
- [ ] Cloud Tasks queue integration
- [ ] Cron job endpoints
- [ ] Background task processing

### Phase 0.4
- [ ] CI/CD pipeline (Cloud Build + GitHub Actions)
- [ ] Automated testing and deployment

### Phase 0.5
- [ ] Optional: Switch to Firestore
- [ ] User file uploads with signed GCS URLs
- [ ] Advanced frontend features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by [gae-init](https://github.com/gae-init/gae-init)
- Built with modern Python and Google Cloud technologies
- Designed for developer productivity and maintainability 