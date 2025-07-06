#!/usr/bin/env python3
"""
Test script to verify user persistence functionality.
Run this after starting the Datastore emulator and Flask app.
"""
import requests
import json
import time

# Configuration
BASE_URL = 'http://localhost:5000'
TEST_EMAIL = 'test@example.com'
TEST_DISPLAY_NAME = 'Test User'

def test_health():
    """Test health endpoint."""
    print("Testing health endpoint...")
    response = requests.get(f'{BASE_URL}/health')
    print(f"Health status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_version():
    """Test version endpoint."""
    print("Testing version endpoint...")
    response = requests.get(f'{BASE_URL}/version')
    print(f"Version status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_auth_status():
    """Test authentication status without token."""
    print("Testing auth status (unauthenticated)...")
    response = requests.get(f'{BASE_URL}/auth/status')
    print(f"Auth status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_profile_unauthenticated():
    """Test profile endpoint without authentication."""
    print("Testing profile endpoint (unauthenticated)...")
    response = requests.get(f'{BASE_URL}/profile/')
    print(f"Profile status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_with_mock_token():
    """Test with a mock token (will fail but shows the flow)."""
    print("Testing with mock token...")
    headers = {'Authorization': 'Bearer mock-token-123'}
    
    # Test profile endpoint
    response = requests.get(f'{BASE_URL}/profile/', headers=headers)
    print(f"Profile with mock token: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def main():
    """Run all tests."""
    print("=" * 50)
    print("Testing User Persistence Implementation")
    print("=" * 50)
    print()
    
    try:
        test_health()
        test_version()
        test_auth_status()
        test_profile_unauthenticated()
        test_with_mock_token()
        
        print("=" * 50)
        print("Test Summary:")
        print("- Health endpoint should return 200")
        print("- Version should show phase 0.2")
        print("- Auth status should show unauthenticated")
        print("- Profile endpoints should require authentication")
        print("=" * 50)
        print()
        print("To test with real Firebase authentication:")
        print("1. Set up Firebase project and get service account key")
        print("2. Update .env file with Firebase configuration")
        print("3. Use the test HTML files in the static directory")
        print("4. Or use curl with a real Firebase ID token")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Flask app.")
        print("Make sure the app is running with: make dev-db")
        print("And the Datastore emulator is running with: make emulator")

if __name__ == '__main__':
    main() 