#!/usr/bin/env python3
"""
Diagnose Google Sheets Integration Issues
"""

import requests
import json

def test_google_script_access():
    """Test Google Apps Script with different approaches"""
    print("🔍 DIAGNOSING GOOGLE SHEETS INTEGRATION")
    print("=" * 60)
    
    url = 'https://script.google.com/macros/s/AKfycby44PN4TqP2Q2Y9a-AtE-2jnntE6azhlJc_lyB5Zguco0FFA3n-KCDV37-MXdZzhShd-g/exec'
    
    # Test 1: GET request (should work if script is deployed)
    print("1. 🌐 Testing GET request...")
    try:
        response = requests.get(url, timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"   ✅ GET Response: {json.dumps(result, indent=4)}")
            except:
                print(f"   ⚠️  Non-JSON response: {response.text[:200]}")
        else:
            print(f"   ❌ GET failed: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ GET error: {e}")
    
    # Test 2: Simple POST request
    print("\n2. 📤 Testing simple POST...")
    simple_data = {
        'applicationId': 'DIAG-TEST-001',
        'fullName': 'Diagnostic Test',
        'patentTitle': 'Test Patent'
    }
    
    try:
        response = requests.post(url, json=simple_data, timeout=15)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"   Response: {json.dumps(result, indent=4)}")
                if result.get('success'):
                    print("   ✅ Simple POST successful")
                else:
                    print(f"   ❌ Script error: {result.get('error', 'Unknown')}")
            except:
                print(f"   ⚠️  Non-JSON response: {response.text[:200]}")
        else:
            print(f"   ❌ POST failed: {response.text[:200]}")
    except Exception as e:
        print(f"   ❌ POST error: {e}")
    
    # Test 3: Full data POST
    print("\n3. 📋 Testing full data POST...")
    full_data = {
        'applicationId': 'DIAG-TEST-002',
        'fullName': 'Full Diagnostic Test',
        'email': 'diag@test.com',
        'department': 'Computer Science',
        'branch': 'Software Engineering',
        'applicantType': 'Student',
        'contactNo': '1234567890',
        'patentTitle': 'Full Diagnostic Patent',
        'patentType': 'Utility',
        'description': 'This is a full diagnostic test',
        'novelty': 'Testing all fields',
        'teamMembers': [
            {'name': 'Test Member 1', 'role': 'Co-inventor'},
            {'name': 'Test Member 2', 'role': 'Researcher'}
        ]
    }
    
    try:
        response = requests.post(url, json=full_data, timeout=15)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"   Response: {json.dumps(result, indent=4)}")
                if result.get('success'):
                    print("   ✅ Full POST successful - Data should be in sheet!")
                    return True
                else:
                    print(f"   ❌ Script error: {result.get('error', 'Unknown')}")
                    return False
            except:
                print(f"   ⚠️  Non-JSON response: {response.text[:200]}")
                return False
        else:
            print(f"   ❌ POST failed: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"   ❌ POST error: {e}")
        return False

def print_troubleshooting_guide():
    """Print detailed troubleshooting steps"""
    print("\n" + "=" * 60)
    print("🔧 TROUBLESHOOTING GUIDE")
    print("=" * 60)
    
    print("\n📋 COMMON ISSUES & SOLUTIONS:")
    
    print("\n1. ❌ 'Cannot read properties of null (reading appendRow)'")
    print("   CAUSE: Google Apps Script can't access the spreadsheet")
    print("   SOLUTIONS:")
    print("   • Make sure the script is attached to a Google Sheet")
    print("   • Open Google Sheets → Extensions → Apps Script")
    print("   • Verify the script has permission to access the sheet")
    print("   • Try running the testScript() function in Apps Script editor")
    
    print("\n2. ❌ 'Script function not found'")
    print("   CAUSE: Script not properly deployed or wrong URL")
    print("   SOLUTIONS:")
    print("   • Redeploy the script as a Web App")
    print("   • Make sure 'Execute as: Me' and 'Access: Anyone' are set")
    print("   • Copy the new Web App URL to app.py")
    
    print("\n3. ❌ 'Permission denied'")
    print("   CAUSE: Script doesn't have proper permissions")
    print("   SOLUTIONS:")
    print("   • Run the script manually once in Apps Script editor")
    print("   • Grant all requested permissions")
    print("   • Make sure your Google account owns the sheet")
    
    print("\n4. ✅ Script works but no data appears")
    print("   CAUSE: Data might be going to wrong sheet/tab")
    print("   SOLUTIONS:")
    print("   • Check all tabs in your Google Sheet")
    print("   • Verify column headers are in Row 1")
    print("   • Make sure you're looking at the right Google Sheet")
    
    print("\n📝 NEXT STEPS:")
    print("1. Open your Google Sheet")
    print("2. Go to Extensions → Apps Script")
    print("3. Run the testScript() function manually")
    print("4. Check if test data appears in your sheet")
    print("5. If it works manually, redeploy as Web App")

def main():
    success = test_google_script_access()
    print_troubleshooting_guide()
    
    if success:
        print("\n🎉 Google Sheets integration is working!")
        print("📊 Check your Google Sheet for the diagnostic test data")
    else:
        print("\n❌ Google Sheets integration needs fixing")
        print("📋 Follow the troubleshooting guide above")

if __name__ == "__main__":
    main()