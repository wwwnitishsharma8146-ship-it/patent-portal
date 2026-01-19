#!/usr/bin/env python3
"""
Test your new Google Apps Script
"""

import requests
import json

def test_google_script():
    print("🧪 Testing Your New Google Apps Script")
    print("=" * 50)
    
    # You'll need to replace this with your actual Web App URL
    url = input("Enter your Google Apps Script Web App URL: ").strip()
    
    if not url:
        print("❌ No URL provided")
        return False
    
    # Test data
    test_data = {
        'applicationId': 'TEST-SETUP-123',
        'fullName': 'Test Setup User',
        'email': 'testsetup@example.com',
        'department': 'Computer Science',
        'branch': 'Software Engineering',
        'applicantType': 'Student',
        'contactNo': '9876543210',
        'patentTitle': 'Google Sheets Integration Test',
        'patentType': 'Utility',
        'description': 'Testing the new Google Sheets integration setup',
        'novelty': 'This tests if the Google Apps Script is working correctly',
        'teamMembers': [
            {'name': 'Team Member 1', 'role': 'Co-inventor'},
            {'name': 'Team Member 2', 'role': 'Researcher'}
        ]
    }
    
    print("📤 Sending test data to Google Apps Script...")
    print(f"URL: {url}")
    
    try:
        response = requests.post(url, json=test_data, timeout=15)
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print("📋 Response:")
                print(json.dumps(result, indent=2))
                
                if result.get('success'):
                    print("\n🎉 SUCCESS! Your Google Apps Script is working!")
                    print("✅ Check your Google Sheet - you should see a new row with test data")
                    return True
                else:
                    print(f"\n❌ Script Error: {result.get('error', 'Unknown error')}")
                    return False
            except json.JSONDecodeError:
                print(f"⚠️  Non-JSON response: {response.text}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timeout - Google Apps Script may be slow or not responding")
        return False
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def main():
    print("🔧 Google Sheets Setup Verification")
    print("=" * 50)
    print("Before running this test:")
    print("1. ✅ Create Google Sheet with headers")
    print("2. ✅ Create and deploy Google Apps Script")
    print("3. ✅ Copy the Web App URL")
    print("4. ✅ Make sure 'Anyone' has access to the web app")
    print()
    
    success = test_google_script()
    
    if success:
        print("\n🎯 Next Steps:")
        print("1. Copy your Web App URL")
        print("2. Update backend/app.py with your URL")
        print("3. Test patent submission through your portal")
    else:
        print("\n🔧 Troubleshooting:")
        print("1. Check Google Apps Script permissions")
        print("2. Verify the script is deployed as 'Anyone' can access")
        print("3. Make sure your Google Sheet exists and is accessible")

if __name__ == "__main__":
    main()