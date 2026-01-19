#!/usr/bin/env python3
"""
Test Google Sheets integration
"""

import requests
import time
import json

def test_google_sheets_integration():
    """Test the complete Google Sheets workflow"""
    print("📊 Testing Google Sheets Integration")
    print("=" * 50)
    
    base_url = "http://localhost:5002"
    session = requests.Session()
    
    # Step 1: Create and login user
    print("1. 👤 Setting up test user...")
    signup_data = {
        'name': f'Sheets Test User {int(time.time())}',
        'email': f'sheetstest{int(time.time())}@cuchd.in',
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
        print("   ❌ Signup failed")
        return False
    
    # Login
    login_data = {
        'email': signup_data['email'],
        'password': signup_data['password']
    }
    response = session.post(f"{base_url}/login", data=login_data, allow_redirects=False)
    if response.status_code != 302:
        print("   ❌ Login failed")
        return False
    
    print("   ✅ User setup complete")
    
    # Step 2: Submit patent with Google Sheets sync enabled
    print("2. 📝 Submitting patent (Google Sheets sync enabled)...")
    
    patent_data = {
        'patentTitle': 'Google Sheets Test Patent',
        'patentType': 'utility',
        'description': 'This patent tests the Google Sheets integration functionality.',
        'novelty': 'This tests whether patent data is properly synced to Google Sheets.',
        'applicantType': 'student'
    }
    
    response = session.post(f"{base_url}/submit", data=patent_data)
    
    if response.status_code == 200:
        try:
            result = response.json()
            if result['success']:
                print(f"   ✅ Patent submitted: {result['applicationId']}")
                
                # Check Google Sheets sync status
                google_sync = result.get('googleSheetSync', False)
                if google_sync:
                    print("   ✅ Google Sheets sync: SUCCESS")
                    print("   📊 Data should appear in your Google Sheet")
                else:
                    print("   ❌ Google Sheets sync: FAILED")
                    print("   ⚠️  Check Google Apps Script configuration")
                
                return google_sync
            else:
                print(f"   ❌ Patent submission failed: {result['message']}")
                return False
        except Exception as e:
            print(f"   ❌ JSON parsing failed: {e}")
            return False
    else:
        print(f"   ❌ HTTP error: {response.status_code}")
        return False

def test_google_script_directly():
    """Test the Google Apps Script URL directly"""
    print("\n3. 🔗 Testing Google Apps Script directly...")
    
    url = 'https://script.google.com/macros/s/AKfycby44PN4TqP2Q2Y9a-AtE-2jnntE6azhlJc_lyB5Zguco0FFA3n-KCDV37-MXdZzhShd-g/exec'
    
    test_payload = {
        'applicationId': 'DIRECT-TEST-123',
        'fullName': 'Direct Test User',
        'email': 'directtest@example.com',
        'department': 'computer',
        'branch': 'Computer Science',
        'applicantType': 'student',
        'contactNo': '9876543210',
        'patentTitle': 'Direct Google Script Test',
        'patentType': 'utility',
        'description': 'Testing Google Apps Script directly',
        'novelty': 'Direct API test',
        'teamMembers': []
    }
    
    try:
        response = requests.post(url, json=test_payload, timeout=15)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"   Response: {json.dumps(result, indent=2)}")
                
                if result.get('success'):
                    print("   ✅ Google Apps Script working correctly")
                    return True
                else:
                    print(f"   ❌ Google Apps Script error: {result.get('error', 'Unknown error')}")
                    return False
            except:
                print(f"   ⚠️  Non-JSON response: {response.text[:200]}")
                return False
        else:
            print(f"   ❌ HTTP error: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("   ❌ Request timeout - Google Apps Script may be slow")
        return False
    except Exception as e:
        print(f"   ❌ Request failed: {e}")
        return False

def main():
    try:
        # Test through Flask app
        flask_success = test_google_sheets_integration()
        
        # Test Google Script directly
        direct_success = test_google_script_directly()
        
        print("\n" + "=" * 50)
        print("📊 GOOGLE SHEETS INTEGRATION RESULTS")
        print("=" * 50)
        
        print(f"Flask Integration: {'✅ WORKING' if flask_success else '❌ FAILED'}")
        print(f"Direct Script Test: {'✅ WORKING' if direct_success else '❌ FAILED'}")
        
        if flask_success and direct_success:
            print("\n🎉 Google Sheets integration is working!")
            print("📊 Patent data should appear in your Google Sheet")
        elif direct_success and not flask_success:
            print("\n⚠️  Google Script works, but Flask integration has issues")
            print("🔧 Check Flask app configuration")
        elif not direct_success:
            print("\n❌ Google Apps Script has issues")
            print("\n🔧 TROUBLESHOOTING STEPS:")
            print("1. Check if Google Sheet exists and is accessible")
            print("2. Verify Google Apps Script permissions")
            print("3. Ensure the script is deployed as a web app")
            print("4. Check if the spreadsheet ID is correct in the script")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Flask server.")
        print("💡 Make sure Flask server is running: cd backend && python3 app.py")
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    main()