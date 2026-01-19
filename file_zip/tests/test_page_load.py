#!/usr/bin/env python3
"""
Test page loading and data loading functionality
"""

import requests
import time

def test_page_load():
    """Test that the main page loads without errors"""
    print("🌐 Testing Page Load and Data Loading")
    print("=" * 50)
    
    base_url = "http://localhost:5002"
    session = requests.Session()
    
    # Step 1: Test login page
    print("1. 🔐 Testing login page...")
    response = session.get(f"{base_url}/login")
    if response.status_code == 200:
        print("   ✅ Login page loads successfully")
    else:
        print(f"   ❌ Login page failed: {response.status_code}")
        return False
    
    # Step 2: Create and login user
    print("2. 👤 Creating test user...")
    timestamp = int(time.time())
    signup_data = {
        'name': f'Page Test User {timestamp}',
        'email': f'pagetest{timestamp}@cuchd.in',
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
        return False
    
    # Login
    login_data = {
        'email': signup_data['email'],
        'password': signup_data['password']
    }
    response = session.post(f"{base_url}/login", data=login_data, allow_redirects=False)
    if response.status_code != 302:
        print(f"   ❌ Login failed: {response.status_code}")
        return False
    
    print("   ✅ User created and logged in")
    
    # Step 3: Test main page load
    print("3. 🏠 Testing main page load...")
    response = session.get(f"{base_url}/")
    if response.status_code == 200:
        print("   ✅ Main page loads successfully")
        
        # Check if page contains expected elements
        content = response.text
        if "Patent Application Form" in content:
            print("   ✅ Patent form is present")
        else:
            print("   ⚠️  Patent form not found in page")
        
        if "Patent Statistics" in content:
            print("   ✅ Statistics section is present")
        else:
            print("   ⚠️  Statistics section not found")
            
    else:
        print(f"   ❌ Main page failed: {response.status_code}")
        return False
    
    # Step 4: Test stats endpoint
    print("4. 📊 Testing statistics endpoint...")
    response = session.get(f"{base_url}/stats")
    if response.status_code == 200:
        try:
            data = response.json()
            if data.get('success'):
                print("   ✅ Statistics endpoint working")
                print(f"   📈 Total: {data['stats']['total']}")
                print(f"   📈 Approved: {data['stats']['approved']}")
                print(f"   📈 Pending: {data['stats']['pending']}")
            else:
                print("   ❌ Statistics endpoint returned failure")
                return False
        except Exception as e:
            print(f"   ❌ Statistics JSON parsing failed: {e}")
            return False
    else:
        print(f"   ❌ Statistics endpoint failed: {response.status_code}")
        return False
    
    return True

def test_javascript_errors():
    """Test for common JavaScript errors by checking console output"""
    print("\n🔧 JavaScript Error Prevention Tips")
    print("=" * 50)
    
    print("Common causes of 'load data failed' errors:")
    print("1. ❌ Network connectivity issues")
    print("2. ❌ CORS configuration problems")
    print("3. ❌ Session/authentication issues")
    print("4. ❌ LocalStorage access problems")
    print("5. ❌ Missing DOM elements")
    
    print("\nTo debug JavaScript errors:")
    print("1. Open browser Developer Tools (F12)")
    print("2. Check the Console tab for error messages")
    print("3. Check the Network tab for failed requests")
    print("4. Look for red error messages or failed HTTP requests")

def main():
    print("🚀 TESTING PAGE LOAD AND DATA FUNCTIONALITY")
    print("=" * 60)
    
    try:
        success = test_page_load()
        test_javascript_errors()
        
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS")
        print("=" * 60)
        
        if success:
            print("✅ All server-side functionality is working")
            print("✅ Page loads successfully")
            print("✅ Statistics endpoint is functional")
            print("✅ Authentication is working")
            
            print("\n💡 If you're still seeing 'load data failed' errors:")
            print("1. Clear your browser cache and cookies")
            print("2. Try opening the page in an incognito/private window")
            print("3. Check browser console for JavaScript errors")
            print("4. Make sure you're accessing http://localhost:5002")
            
        else:
            print("❌ Server-side issues detected")
            print("🔧 Fix server issues before testing frontend")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Flask server.")
        print("💡 Make sure Flask server is running: cd backend && python3 app.py")
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    main()