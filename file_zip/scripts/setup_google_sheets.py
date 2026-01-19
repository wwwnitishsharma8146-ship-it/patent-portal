#!/usr/bin/env python3
"""
Google Sheets Setup Helper for UIC Patent Portal
"""

import requests
import json
import os

def test_google_script_url(url):
    """Test if a Google Apps Script URL works"""
    print(f"🧪 Testing Google Apps Script URL...")
    print(f"URL: {url}")
    
    test_data = {
        'applicationId': 'SETUP-TEST-123',
        'fullName': 'Setup Test User',
        'email': 'setuptest@example.com',
        'department': 'Computer Science',
        'branch': 'Software Engineering',
        'applicantType': 'Student',
        'contactNo': '9876543210',
        'patentTitle': 'Google Sheets Setup Test',
        'patentType': 'Utility',
        'description': 'Testing Google Sheets integration setup',
        'novelty': 'This verifies the Google Apps Script is working',
        'teamMembers': [
            {'name': 'Test Member', 'role': 'Co-inventor'}
        ]
    }
    
    try:
        response = requests.post(url, json=test_data, timeout=15)
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print("📋 Response:")
                print(json.dumps(result, indent=2))
                
                if result.get('success'):
                    print("\n🎉 SUCCESS! Google Apps Script is working!")
                    return True
                else:
                    print(f"\n❌ Script Error: {result.get('error', 'Unknown error')}")
                    return False
            except json.JSONDecodeError:
                print(f"⚠️  Non-JSON response: {response.text[:200]}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def update_flask_config(url):
    """Update the Flask app configuration with the new URL"""
    app_py_path = "backend/app.py"
    
    if not os.path.exists(app_py_path):
        print(f"❌ Could not find {app_py_path}")
        return False
    
    try:
        # Read the current file
        with open(app_py_path, 'r') as f:
            content = f.read()
        
        # Replace the URL
        old_line = "APPS_SCRIPT_URL = 'PASTE_YOUR_NEW_WEB_APP_URL_HERE'"
        new_line = f"APPS_SCRIPT_URL = '{url}'"
        
        if old_line in content:
            content = content.replace(old_line, new_line)
        else:
            # Try to find any APPS_SCRIPT_URL line and replace it
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.strip().startswith('APPS_SCRIPT_URL = '):
                    lines[i] = new_line
                    break
            content = '\n'.join(lines)
        
        # Enable Google Sheets sync
        content = content.replace(
            "ENABLE_GOOGLE_SHEETS_SYNC = False",
            "ENABLE_GOOGLE_SHEETS_SYNC = True"
        )
        
        # Write back to file
        with open(app_py_path, 'w') as f:
            f.write(content)
        
        print(f"✅ Updated {app_py_path} with new URL")
        print("✅ Enabled Google Sheets sync")
        return True
        
    except Exception as e:
        print(f"❌ Error updating Flask config: {e}")
        return False

def main():
    print("🔧 Google Sheets Setup Helper")
    print("=" * 50)
    print("This script will help you set up Google Sheets integration.")
    print()
    print("📋 Prerequisites:")
    print("1. ✅ Create Google Sheet with proper headers")
    print("2. ✅ Create Google Apps Script with the provided code")
    print("3. ✅ Deploy Apps Script as Web App (Anyone can access)")
    print("4. ✅ Copy the Web App URL")
    print()
    
    # Get URL from user
    url = input("📎 Enter your Google Apps Script Web App URL: ").strip()
    
    if not url:
        print("❌ No URL provided. Exiting.")
        return
    
    if not url.startswith('https://script.google.com/macros/s/'):
        print("⚠️  Warning: URL doesn't look like a Google Apps Script URL")
        proceed = input("Continue anyway? (y/n): ").strip().lower()
        if proceed != 'y':
            return
    
    # Test the URL
    print("\n" + "=" * 50)
    if test_google_script_url(url):
        print("\n🎯 Google Apps Script is working! Updating Flask configuration...")
        
        if update_flask_config(url):
            print("\n🎉 Setup Complete!")
            print("=" * 50)
            print("✅ Google Sheets integration is now configured")
            print("✅ Flask app updated with your URL")
            print("✅ Google Sheets sync enabled")
            print()
            print("🚀 Next Steps:")
            print("1. Restart your Flask server")
            print("2. Submit a test patent application")
            print("3. Check your Google Sheet for the new data")
            print()
            print("💡 The Flask server will restart automatically with the new configuration.")
        else:
            print("\n❌ Failed to update Flask configuration")
            print("You'll need to manually update backend/app.py")
    else:
        print("\n❌ Google Apps Script is not working properly")
        print("Please check your setup and try again")
        print()
        print("🔧 Common Issues:")
        print("1. Script not deployed as Web App")
        print("2. Access not set to 'Anyone'")
        print("3. Google Sheet doesn't exist or has wrong permissions")
        print("4. Script code has errors")

if __name__ == "__main__":
    main()