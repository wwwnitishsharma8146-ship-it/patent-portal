#!/usr/bin/env python3
"""
Debug browser session issues
"""

import requests
import time

def test_browser_like_session():
    """Test session behavior like a browser would"""
    print("🌐 Testing Browser-Like Session Behavior")
    print("=" * 50)
    
    base_url = "http://localhost:5002"
    
    # Create a session that behaves like a browser
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })
    
    print("1. 🏠 Accessing home page (should redirect to login)...")
    response = session.get(f"{base_url}/", allow_redirects=True)
    print(f"   Status: {response.status_code}")
    print(f"   Final URL: {response.url}")
    print(f"   Cookies: {dict(session.cookies)}")
    
    if "login" in response.url:
        print("   ✅ Correctly redirected to login")
    else:
        print("   ⚠️  Not redirected to login")
    
    print("\n2. 👤 Creating and logging in user...")
    timestamp = int(time.time())
    
    # First, get the signup page to establish session
    response = session.get(f"{base_url}/signup")
    print(f"   Signup page status: {response.status_code}")
    print(f"   Cookies after signup page: {dict(session.cookies)}")
    
    # Signup
    signup_data = {
        'name': f'Debug User {timestamp}',
        'email': f'debug{timestamp}@cuchd.in',
        'password': 'testpass123',
        'confirm_password': 'testpass123',
        'user_type': 'student',
        'department': 'computer',
        'branch': 'Computer Science',
        'contact': '9876543210'
    }
    
    response = session.post(f"{base_url}/signup", data=signup_data, allow_redirects=False)
    print(f"   Signup status: {response.status_code}")
    print(f"   Signup redirect: {response.headers.get('Location', 'None')}")
    print(f"   Cookies after signup: {dict(session.cookies)}")
    
    # Login
    login_data = {
        'email': signup_data['email'],
        'password': signup_data['password']
    }
    
    response = session.post(f"{base_url}/login", data=login_data, allow_redirects=False)
    print(f"   Login status: {response.status_code}")
    print(f"   Login redirect: {response.headers.get('Location', 'None')}")
    print(f"   Cookies after login: {dict(session.cookies)}")
    
    if response.status_code == 302:
        print("   ✅ Login successful")
    else:
        print("   ❌ Login failed")
        return False
    
    print("\n3. 🏠 Accessing home page after login...")
    response = session.get(f"{base_url}/")
    print(f"   Status: {response.status_code}")
    print(f"   Cookies: {dict(session.cookies)}")
    
    if response.status_code == 200:
        print("   ✅ Home page accessible")
    else:
        print("   ❌ Home page not accessible")
        return False
    
    print("\n4. 📊 Testing stats endpoint...")
    response = session.get(f"{base_url}/stats")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"   ✅ Stats loaded: {data}")
        except:
            print("   ❌ Stats JSON parsing failed")
    
    print("\n5. 📝 Testing form submission...")
    
    # Test with form data (like browser would send)
    patent_data = {
        'name': signup_data['name'],
        'email': signup_data['email'],
        'department': 'computer',
        'branch': 'Computer Science',
        'applicantType': 'student',
        'contact': '9876543210',
        'patentTitle': 'Debug Test Patent',
        'patentType': 'utility',
        'description': 'This is a debug test patent to check session handling.',
        'novelty': 'Testing browser-like session behavior.',
        'members': '[]'
    }
    
    # Add headers that a browser would send
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': f'{base_url}/'
    }
    
    response = session.post(f"{base_url}/submit", data=patent_data, headers=headers)
    print(f"   Submit status: {response.status_code}")
    print(f"   Submit cookies: {dict(session.cookies)}")
    
    if response.status_code == 200:
        try:
            result = response.json()
            print(f"   ✅ Submission successful: {result.get('applicationId')}")
            return True
        except Exception as e:
            print(f"   ❌ JSON parsing failed: {e}")
            print(f"   Response: {response.text[:200]}")
    elif response.status_code == 401:
        print("   ❌ Authentication failed (401)")
        print(f"   Response: {response.text[:200]}")
    elif response.status_code == 302:
        print("   ❌ Redirected (302) - session lost")
        print(f"   Redirect to: {response.headers.get('Location')}")
    else:
        print(f"   ❌ Unexpected status: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
    
    return False

def main():
    print("🔍 DEBUGGING BROWSER SESSION ISSUES")
    print("=" * 60)
    
    try:
        success = test_browser_like_session()
        
        print("\n" + "=" * 60)
        print("📊 DEBUG RESULTS")
        print("=" * 60)
        
        if success:
            print("✅ Session handling is working correctly")
        else:
            print("❌ Session handling has issues")
            print("\n🔧 POSSIBLE CAUSES:")
            print("1. Session cookies not being set properly")
            print("2. CSRF protection interfering")
            print("3. Cookie domain/path issues")
            print("4. Session timeout")
            print("5. Browser security settings")
        
    except Exception as e:
        print(f"❌ Debug error: {e}")

if __name__ == "__main__":
    main()