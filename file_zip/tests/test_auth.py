#!/usr/bin/env python3
"""
Test script for UIC Patent Portal Authentication
"""

import requests
import json

BASE_URL = "http://localhost:5002"

def test_signup():
    """Test user registration"""
    print("🧪 Testing User Registration...")
    
    signup_data = {
        'name': 'Test Student',
        'email': 'test.student@cuchd.in',
        'password': 'testpass123',
        'confirm_password': 'testpass123',
        'user_type': 'student',
        'department': 'computer',
        'branch': 'Computer Science Engineering',
        'contact': '9876543210'
    }
    
    response = requests.post(f"{BASE_URL}/signup", data=signup_data, allow_redirects=False)
    
    if response.status_code == 302:
        print("✅ Signup successful - redirected to login")
        return True
    else:
        print(f"❌ Signup failed - Status: {response.status_code}")
        return False

def test_login():
    """Test user login"""
    print("🧪 Testing User Login...")
    
    # Create session
    session = requests.Session()
    
    login_data = {
        'email': 'test.student@cuchd.in',
        'password': 'testpass123'
    }
    
    response = session.post(f"{BASE_URL}/login", data=login_data, allow_redirects=False)
    
    if response.status_code == 302 and response.headers.get('Location') == '/':
        print("✅ Login successful - redirected to home")
        return session
    else:
        print(f"❌ Login failed - Status: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        return None

def test_protected_access(session):
    """Test accessing protected pages"""
    print("🧪 Testing Protected Page Access...")
    
    if not session:
        print("❌ No session available")
        return False
    
    response = session.get(f"{BASE_URL}/")
    
    if response.status_code == 200 and "UIC Patent Portal" in response.text:
        print("✅ Successfully accessed protected home page")
        return True
    else:
        print(f"❌ Failed to access home page - Status: {response.status_code}")
        return False

def test_logout(session):
    """Test user logout"""
    print("🧪 Testing User Logout...")
    
    if not session:
        print("❌ No session available")
        return False
    
    response = session.get(f"{BASE_URL}/logout", allow_redirects=False)
    
    if response.status_code == 302:
        print("✅ Logout successful - redirected to login")
        
        # Test that we can't access protected page anymore
        response = session.get(f"{BASE_URL}/", allow_redirects=False)
        if response.status_code == 302:
            print("✅ Protected page correctly redirects after logout")
            return True
        else:
            print("❌ Protected page still accessible after logout")
            return False
    else:
        print(f"❌ Logout failed - Status: {response.status_code}")
        return False

def main():
    print("🚀 UIC Patent Portal Authentication Test")
    print("=" * 50)
    
    # Test signup
    signup_success = test_signup()
    
    # Test login
    session = test_login()
    
    # Test protected access
    if session:
        access_success = test_protected_access(session)
        
        # Test logout
        logout_success = test_logout(session)
    else:
        access_success = False
        logout_success = False
    
    print("\n📊 Test Results:")
    print("=" * 50)
    print(f"Signup: {'✅ PASS' if signup_success else '❌ FAIL'}")
    print(f"Login: {'✅ PASS' if session else '❌ FAIL'}")
    print(f"Protected Access: {'✅ PASS' if access_success else '❌ FAIL'}")
    print(f"Logout: {'✅ PASS' if logout_success else '❌ FAIL'}")
    
    all_passed = all([signup_success, session, access_success, logout_success])
    print(f"\nOverall: {'🎉 ALL TESTS PASSED' if all_passed else '⚠️  SOME TESTS FAILED'}")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure Flask server is running on localhost:5002")
    except Exception as e:
        print(f"❌ Test error: {e}")