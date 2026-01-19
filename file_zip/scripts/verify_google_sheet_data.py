#!/usr/bin/env python3
"""
Verify Google Sheet Data - Help check if data is appearing correctly
"""

import requests
import json
from datetime import datetime

def send_test_patent():
    """Send a clearly identifiable test patent to Google Sheets"""
    print("📊 SENDING TEST PATENT TO GOOGLE SHEETS")
    print("=" * 50)
    
    url = 'https://script.google.com/macros/s/AKfycby44PN4TqP2Q2Y9a-AtE-2jnntE6azhlJc_lyB5Zguco0FFA3n-KCDV37-MXdZzhShd-g/exec'
    
    # Create a very distinctive test entry
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    test_data = {
        'applicationId': f'VERIFY-{datetime.now().strftime("%Y%m%d-%H%M%S")}',
        'fullName': f'🔍 VERIFICATION TEST USER - {timestamp}',
        'email': 'verification@test.com',
        'department': '🧪 TEST DEPARTMENT',
        'branch': '🔬 TEST BRANCH',
        'applicantType': 'Student',
        'contactNo': '9999999999',
        'patentTitle': f'🚀 VERIFICATION PATENT - {timestamp}',
        'patentType': 'Utility Patent',
        'description': f'This is a verification test patent submitted at {timestamp}. If you can see this in your Google Sheet, the integration is working perfectly!',
        'novelty': f'🎯 LOOK FOR THIS ENTRY in your Google Sheet! Submitted at {timestamp}',
        'teamMembers': [
            {
                'name': '👥 Test Team Member 1',
                'role': 'Co-inventor'
            },
            {
                'name': '👥 Test Team Member 2', 
                'role': 'Researcher'
            }
        ]
    }
    
    try:
        print(f"📤 Sending test patent: {test_data['applicationId']}")
        print(f"🎯 Look for: '{test_data['patentTitle']}'")
        
        response = requests.post(url, json=test_data, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Test patent sent successfully!")
                print(f"📊 Application ID: {test_data['applicationId']}")
                print(f"🕐 Timestamp: {timestamp}")
                
                print("\n" + "=" * 50)
                print("📋 WHAT TO CHECK IN YOUR GOOGLE SHEET:")
                print("=" * 50)
                print(f"1. Look for Application ID: {test_data['applicationId']}")
                print(f"2. Patent Title should contain: 'VERIFICATION PATENT'")
                print(f"3. Full Name should contain: 'VERIFICATION TEST USER'")
                print(f"4. Department should be: '🧪 TEST DEPARTMENT'")
                print(f"5. Team Members should show: '👥 Test Team Member 1 (Co-inventor), 👥 Test Team Member 2 (Researcher)'")
                
                print("\n📍 WHERE TO LOOK:")
                print("• Open your Google Sheet")
                print("• Check the first tab/sheet")
                print("• Look at the most recent rows (bottom of the sheet)")
                print("• Data should appear within a few seconds")
                
                print("\n🔍 IF YOU DON'T SEE THE DATA:")
                print("• Check if you have multiple tabs - data might be in a different tab")
                print("• Verify you're looking at the correct Google Sheet")
                print("• Make sure the sheet has column headers in Row 1")
                print("• Try refreshing the Google Sheet page")
                
                return True
            else:
                print(f"❌ Google Apps Script error: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP error {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending test patent: {e}")
        return False

def main():
    success = send_test_patent()
    
    if success:
        print("\n🎉 TEST PATENT SENT SUCCESSFULLY!")
        print("📊 Check your Google Sheet now for the verification data")
        print("🔗 Google Sheet URL should be in your browser bookmarks or recent files")
    else:
        print("\n❌ Failed to send test patent")
        print("🔧 Check the troubleshooting guide in diagnose_google_sheets.py")

if __name__ == "__main__":
    main()