#!/usr/bin/env python3
"""
Test the new Google Apps Script URL
"""

import requests
import json

def test_new_url():
    url = 'https://script.google.com/macros/s/AKfycbyp5t3kl7z1e2CLzLP4qJ-Qs2_OZXCd7UTpQNqrIiD7l8MHibJaNdIOX1NdpFlwLZ0F/exec'
    
    print("🧪 Testing your new Google Apps Script URL")
    print("=" * 50)
    
    # Test data matching your backend format
    test_data = {
        'applicationId': 'UIC-PAT-TEST-NEW-URL',
        'fullName': 'Test User New URL',
        'email': 'test@newurl.com',
        'department': 'Computer Science',
        'branch': 'Software Engineering',
        'applicantType': 'Student',
        'contactNo': '1234567890',
        'patentTitle': 'Test Patent New URL',
        'patentType': 'Utility',
        'member1Name': 'Team Member 1',
        'member1Role': 'Co-inventor',
        'member1Department': 'CS',
        'member1Email': 'member1@test.com',
        'member2Name': 'Team Member 2',
        'member2Role': 'Researcher',
        'member2Department': 'CS',
        'member2Email': 'member2@test.com',
        'member3Name': '',
        'member3Role': '',
        'member3Department': '',
        'member3Email': '',
        'member4Name': '',
        'member4Role': '',
        'member4Department': '',
        'member4Email': '',
        'member5Name': '',
        'member5Role': '',
        'member5Department': '',
        'member5Email': ''
    }
    
    try:
        print(f"📤 Sending test data to: {url}")
        response = requests.post(url, json=test_data, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ SUCCESS! Your Google Apps Script is working perfectly!")
                print(f"📊 Application ID: {result.get('applicationId')}")
                print(f"🕐 Timestamp: {result.get('timestamp')}")
                print("\n🎉 Your patent portal should work correctly now!")
                print("👉 Open http://127.0.0.1:5000 and submit a form to test")
                return True
            else:
                print(f"❌ Script error: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    test_new_url()