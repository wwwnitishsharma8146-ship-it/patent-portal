#!/usr/bin/env python3
"""
Test the final fix for Google Apps Script
"""

import requests
import json

def test_final_fix():
    url = 'https://script.google.com/macros/s/AKfycbyp5t3kl7z1e2CLzLP4qJ-Qs2_OZXCd7UTpQNqrIiD7l8MHibJaNdIOX1NdpFlwLZ0F/exec'
    
    print("🔧 TESTING FINAL FIX FOR GOOGLE APPS SCRIPT")
    print("=" * 60)
    
    # Test with the exact format your backend sends
    test_data = {
        'applicationId': 'UIC-PAT-FINAL-TEST',
        'fullName': 'Final Test User',
        'email': 'finaltest@example.com',
        'department': 'Computer Science',
        'branch': 'Software Engineering',
        'applicantType': 'Student',
        'contactNo': '9876543210',
        'patentTitle': 'Final Test Patent',
        'patentType': 'Utility',
        'member1Name': 'Test Member 1',
        'member1Role': 'Co-inventor',
        'member1Department': 'CS',
        'member1Email': 'member1@test.com',
        'member2Name': 'Test Member 2',
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
        print(f"📤 Sending test data...")
        print(f"🎯 Application ID: {test_data['applicationId']}")
        
        response = requests.post(url, json=test_data, timeout=15)
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"📋 Response: {json.dumps(result, indent=2)}")
                
                if result.get('success'):
                    print("\n✅ SUCCESS! The fix is working!")
                    print(f"📊 Application ID: {result.get('applicationId')}")
                    print(f"🕐 Timestamp: {result.get('timestamp')}")
                    print("\n🎉 Your patent portal should now work without errors!")
                    print("👉 Try submitting a form at http://127.0.0.1:5000")
                    return True
                else:
                    print(f"\n❌ Script returned error: {result.get('error', 'Unknown error')}")
                    print(f"📋 Details: {result.get('details', 'No details')}")
                    print("\n🔧 You need to update your Google Apps Script with the fixed code!")
                    return False
            except json.JSONDecodeError:
                print(f"\n❌ Invalid JSON response: {response.text[:200]}")
                return False
        else:
            print(f"\n❌ HTTP error {response.status_code}")
            print(f"📋 Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"\n❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    success = test_final_fix()
    
    if not success:
        print("\n" + "=" * 60)
        print("🚨 IMPORTANT: UPDATE YOUR GOOGLE APPS SCRIPT!")
        print("=" * 60)
        print("1. Go to https://script.google.com")
        print("2. Open your existing script")
        print("3. Replace ALL code with the code from GOOGLE_APPS_SCRIPT_FINAL_FIX.js")
        print("4. Save and redeploy")
        print("5. Run this test again")