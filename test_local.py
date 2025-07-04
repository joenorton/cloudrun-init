#!/usr/bin/env python3
"""
Simple test script to verify cloudrun-init works locally without Firebase setup.
"""
import requests
import json

def test_endpoints():
    """Test basic endpoints without authentication."""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing cloudrun-init endpoints...")
    print("=" * 50)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Status: {data.get('status')}")
            print(f"   Project: {data.get('project')}")
    except Exception as e:
        print(f"❌ Health endpoint failed: {e}")
    
    # Test version endpoint
    try:
        response = requests.get(f"{base_url}/version")
        print(f"✅ Version endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Version: {data.get('version')}")
            print(f"   Phase: {data.get('phase')}")
    except Exception as e:
        print(f"❌ Version endpoint failed: {e}")
    
    # Test auth status (should work without auth)
    try:
        response = requests.get(f"{base_url}/auth/status")
        print(f"✅ Auth status endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Authenticated: {data.get('authenticated')}")
            print(f"   User: {data.get('user')}")
    except Exception as e:
        print(f"❌ Auth status endpoint failed: {e}")
    
    # Test protected endpoint (should fail without auth)
    try:
        response = requests.get(f"{base_url}/auth/me")
        print(f"✅ Protected /me endpoint: {response.status_code}")
        if response.status_code == 401:
            print("   ✅ Correctly requires authentication")
        else:
            print(f"   ⚠️ Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"❌ Protected endpoint test failed: {e}")
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Root endpoint: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Frontend page served successfully")
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
    
    print("=" * 50)
    print("🎉 Basic functionality test completed!")
    print("\n📝 Next steps:")
    print("1. Set up Firebase project (see FIREBASE_SETUP.md)")
    print("2. Update Firebase config in app/static/index.html")
    print("3. Test authentication flow")
    print("4. Run 'make test' for full test suite (when pytest issues are resolved)")

if __name__ == "__main__":
    test_endpoints() 