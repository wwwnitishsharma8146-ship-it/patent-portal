#!/usr/bin/env python3
"""
Test the submission fix for authentication issues
"""

import requests
import time

def test_submission_with_authentication():
    """Test patent submission with proper authentication"""
    print("🧪 Testing Patent Submission with Authentication Fix")
    print("=" * 60)
    
    base_url = "http://localhost:5002"
    session = requests.Session()
    
    # Step 1: Create and login user
    print("1. 👤 Creating test user and logging in...")
    
    # Create unique user
    timestamp = int(time.time())
    signup_data = {
        'name': f'Test User {timestamp}',
        'email': f'testuser{timestamp}@cuchd.in',
        'password': 'testpass123',
        'confirm_password': 'testpass123',
        'user_type': 'student',
        'department': 'computer',
        'branch': 'Computer Science',
        'contact': '9876543210'
    }
    
    # Signup
    response = session.post(f"{base_url}/signup", data=signup_data, allow_redirects=False)
    if response.status_code != 302:
        print(f"   ❌ Signup failed: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
        return False
    
    # Login
    login_data = {
        'email': signup_data['email'],
        'password': signup_data['password']
    }
    response = session.post(f"{base_url}/login", data=login_data, allow_redirects=False)
    if response.status_code != 302:
        print(f"   ❌ Login failed: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
        return False
    
    print("   ✅ User created and logged in successfully")
    
    # Step 2: Test accessing the home page
    print("2. 🏠 Testing authenticated access to home page...")
    response = session.get(f"{base_url}/")
    if response.status_code == 200:
        print("   ✅ Home page accessible")
    else:
        print(f"   ❌ Home page access failed: {response.status_code}")
        return False
    
    # Step 3: Test patent submission
    print("3. 📝 Testing patent submission...")
    
    patent_data = {
        'patentTitle': 'Authentication Test Patent',
        'patentType': 'utility',
        'description': 'This patent tests the authentication fix for form submissions.',
        'novelty': 'This tests whether the session cookies are properly included in AJAX requests.',
        'applicantType': 'student'
    }
    
    response = session.post(f"{base_url}/submit", data=patent_data)
    
    print(f"   Response Status: {response.status_code}")
    print(f"   Response Headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        try:
            result = response.json()
            if result.get('success'):
                print(f"   ✅ Patent submitted successfully!")
                print(f"   📋 Application ID: {result.get('applicationId')}")
                print(f"   📊 Google Sheets Sync: {result.get('googleSheetSync', 'N/A')}")
                print(f"   📁 Files Uploaded: {result.get('filesUploaded', 0)}")
                return True
            else:
                print(f"   ❌ Submission failed: {result.get('message', 'Unknown error')}")
                return False
        except Exception as e:
            print(f"   ❌ JSON parsing failed: {e}")
            print(f"   Raw response: {response.text[:300]}")
            return False
    elif response.status_code == 302:
        print("   ❌ Still getting redirected - authentication issue persists")
        print(f"   Redirect location: {response.headers.get('Location', 'Unknown')}")
        return False
    else:
        print(f"   ❌ Unexpected status code: {response.status_code}")
        print(f"   Response: {response.text[:300]}")
        return False

def test_session_persistence():
    """Test that session cookies persist across requests"""
    print("\n🔐 Testing Session Cookie Persistence")
    print("=" * 60)
    
    base_url = "http://localhost:5002"
    session = requests.Session()
    
    # Login
    timestamp = int(time.time())
    login_data = {
        'email': f'testuser{timestamp-1}@cuchd.in',  # Use previous user
        'password': 'testpass123'
    }
    
    response = session.post(f"{base_url}/login", data=login_data, allow_redirects=False)
    if response.status_code == 302:
        print("   ✅ Login successful")
        
        # Check cookies
        cookies = session.cookies.get_dict()
        print(f"   🍪 Session cookies: {list(cookies.keys())}")
        
        # Test multiple requests
        for i in range(3):
            response = session.get(f"{base_url}/")
            if response.status_code == 200:
                print(f"   ✅ Request {i+1}: Authenticated access successful")
            else:
                print(f"   ❌ Request {i+1}: Authentication failed")
                return False
        
        return True
    else:
        print("   ❌ Login failed - cannot test session persistence")
        return False

def main():
    print("🚀 TESTING SUBMISSION AUTHENTICATION FIX")
    print("=" * 70)
    
    try:
        # Test 1: Full submission workflow
        submission_success = test_submission_with_authentication()
        
        # Test 2: Session persistence
        session_success = test_session_persistence()
        
        # Results
        print("\n" + "=" * 70)
        print("📊 TEST RESULTS")
        print("=" * 70)
        
        print(f"Patent Submission: {'✅ WORKING' if submission_success else '❌ FAILED'}")
        print(f"Session Persistence: {'✅ WORKING' if session_success else '❌ FAILED'}")
        
        if submission_success and session_success:
            print("\n🎉 Authentication fix is working!")
            print("✅ Users can now submit patents without authentication errors")
            print("🔐 Session cookies are properly maintained")
        else:
            print("\n❌ Authentication issues still exist")
            print("\n🔧 TROUBLESHOOTING:")
            print("1. Make sure Flask server is running")
            print("2. Check that session cookies are being set")
            print("3. Verify CORS configuration allows credentials")
            print("4. Test with a fresh browser session")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Flask server.")
        print("💡 Make sure Flask server is running: cd backend && python3 app.py")
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    main()