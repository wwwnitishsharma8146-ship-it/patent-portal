#!/usr/bin/env python3
"""
Complete website functionality test
"""

import requests
import time

def test_complete_workflow():
    """Test the complete user workflow"""
    print("🚀 Complete Website Functionality Test")
    print("=" * 50)
    
    base_url = "http://localhost:5002"
    session = requests.Session()
    
    # Test 1: Access home page (should redirect to login)
    print("1. 🔒 Testing protected home page access...")
    response = session.get(f"{base_url}/", allow_redirects=False)
    if response.status_code == 302 and '/login' in response.headers.get('Location', ''):
        print("   ✅ Correctly redirected to login")
    else:
        print("   ❌ Failed to redirect to login")
        return False
    
    # Test 2: Load login page
    print("2. 📝 Testing login page...")
    response = session.get(f"{base_url}/login")
    if response.status_code == 200 and 'UIC Patent Portal' in response.text:
        print("   ✅ Login page loaded successfully")
        if 'images.jpeg' in response.text:
            print("   ✅ Background image reference found")
        else:
            print("   ⚠️  Background image reference not found")
    else:
        print("   ❌ Login page failed to load")
        return False
    
    # Test 3: Load signup page
    print("3. 📋 Testing signup page...")
    response = session.get(f"{base_url}/signup")
    if response.status_code == 200 and 'Create Account' in response.text:
        print("   ✅ Signup page loaded successfully")
        if 'images.jpeg' in response.text:
            print("   ✅ Background image reference found")
        else:
            print("   ⚠️  Background image reference not found")
    else:
        print("   ❌ Signup page failed to load")
        return False
    
    # Test 4: Test background image accessibility
    print("4. 🖼️  Testing background image...")
    response = session.get(f"{base_url}/static/images.jpeg")
    if response.status_code == 200 and response.headers.get('Content-Type', '').startswith('image'):
        print("   ✅ Background image accessible")
        print(f"   📊 Image size: {len(response.content)} bytes")
    else:
        print("   ❌ Background image not accessible")
        return False
    
    # Test 5: Create test user
    print("5. 👤 Testing user registration...")
    signup_data = {
        'name': f'Test User {int(time.time())}',
        'email': f'test{int(time.time())}@cuchd.in',
        'password': 'testpass123',
        'confirm_password': 'testpass123',
        'user_type': 'student',
        'department': 'computer',
        'branch': 'Computer Science',
        'contact': '9876543210'
    }
    
    response = session.post(f"{base_url}/signup", data=signup_data, allow_redirects=False)
    if response.status_code == 302 and '/login' in response.headers.get('Location', ''):
        print("   ✅ User registration successful")
    else:
        print("   ❌ User registration failed")
        return False
    
    # Test 6: Login with new user
    print("6. 🔑 Testing user login...")
    login_data = {
        'email': signup_data['email'],
        'password': signup_data['password']
    }
    
    response = session.post(f"{base_url}/login", data=login_data, allow_redirects=False)
    if response.status_code == 302 and response.headers.get('Location') == '/':
        print("   ✅ User login successful")
    else:
        print("   ❌ User login failed")
        return False
    
    # Test 7: Access protected home page
    print("7. 🏠 Testing authenticated home page access...")
    response = session.get(f"{base_url}/")
    if response.status_code == 200 and 'Patent Application Form' in response.text:
        print("   ✅ Home page accessible after login")
        if signup_data['name'] in response.text:
            print("   ✅ User name displayed in header")
        else:
            print("   ⚠️  User name not found in header")
    else:
        print("   ❌ Home page not accessible")
        return False
    
    # Test 8: Test statistics endpoint
    print("8. 📊 Testing statistics...")
    response = session.get(f"{base_url}/stats")
    if response.status_code == 200:
        try:
            stats = response.json()
            if 'success' in stats and stats['success']:
                print("   ✅ Statistics endpoint working")
                print(f"   📈 Total applications: {stats['stats']['total']}")
            else:
                print("   ❌ Statistics endpoint returned error")
                return False
        except:
            print("   ❌ Statistics endpoint returned invalid JSON")
            return False
    else:
        print("   ❌ Statistics endpoint not accessible")
        return False
    
    # Test 9: Logout
    print("9. 🚪 Testing logout...")
    response = session.get(f"{base_url}/logout", allow_redirects=False)
    if response.status_code == 302 and '/login' in response.headers.get('Location', ''):
        print("   ✅ Logout successful")
    else:
        print("   ❌ Logout failed")
        return False
    
    return True

def main():
    try:
        success = test_complete_workflow()
        
        print("\n" + "=" * 50)
        if success:
            print("🎉 ALL TESTS PASSED - Website is fully functional!")
            print("\n✅ Your UIC Patent Portal is ready to use:")
            print("   🌐 URL: http://localhost:5002")
            print("   🔐 Authentication: Working")
            print("   🎨 Background Images: Loading")
            print("   📝 Forms: Functional")
            print("   📊 Database: Connected")
        else:
            print("❌ SOME TESTS FAILED - Please check the issues above")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server.")
        print("💡 Make sure Flask server is running:")
        print("   cd backend && python3 app.py")
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    main()