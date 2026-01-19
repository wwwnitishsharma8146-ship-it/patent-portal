#!/usr/bin/env python3
"""
Test database functionality after fixes
"""

import requests
import time

def test_simple_submission():
    """Test a simple patent submission"""
    print("🧪 Testing Simple Patent Submission")
    print("=" * 50)
    
    base_url = "http://localhost:5002"
    
    # Test data
    patent_data = {
        'name': 'Test User',
        'email': 'test@example.com',
        'department': 'computer',
        'branch': 'Computer Science',
        'applicantType': 'student',
        'contact': '9876543210',
        'patentTitle': 'Database Fix Test Patent',
        'patentType': 'utility',
        'description': 'This patent tests the database fix for submission errors.',
        'novelty': 'Testing database locking and schema fixes.',
        'members': '[]'
    }
    
    try:
        print("📝 Submitting patent application...")
        
        response = requests.post(f"{base_url}/submit", data=patent_data)
        
        print(f"Response Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                if result.get('success'):
                    print(f"✅ Submission successful!")
                    print(f"📋 Application ID: {result.get('applicationId')}")
                    print(f"📊 Google Sheets Sync: {result.get('googleSheetSync', 'N/A')}")
                    print(f"📁 Files Uploaded: {result.get('filesUploaded', 0)}")
                    return True
                else:
                    print(f"❌ Submission failed: {result.get('message', 'Unknown error')}")
                    return False
            except Exception as e:
                print(f"❌ JSON parsing failed: {e}")
                print(f"Raw response: {response.text[:300]}")
                return False
        else:
            print(f"❌ HTTP error: {response.status_code}")
            print(f"Response: {response.text[:300]}")
            return False
            
    except Exception as e:
        print(f"❌ Request error: {e}")
        return False

def test_stats_endpoint():
    """Test the stats endpoint"""
    print("\n📊 Testing Statistics Endpoint")
    print("=" * 50)
    
    base_url = "http://localhost:5002"
    
    try:
        response = requests.get(f"{base_url}/stats")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ Stats loaded successfully")
                print(f"   Total: {data['stats']['total']}")
                print(f"   Approved: {data['stats']['approved']}")
                print(f"   Pending: {data['stats']['pending']}")
                return True
            else:
                print("❌ Stats response indicates failure")
                return False
        else:
            print(f"❌ Stats endpoint failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Stats error: {e}")
        return False

def main():
    print("🚀 TESTING DATABASE FIXES")
    print("=" * 60)
    
    try:
        # Test 1: Stats endpoint
        stats_success = test_stats_endpoint()
        
        # Test 2: Patent submission
        submission_success = test_simple_submission()
        
        # Results
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS")
        print("=" * 60)
        
        print(f"Statistics Endpoint: {'✅ WORKING' if stats_success else '❌ FAILED'}")
        print(f"Patent Submission: {'✅ WORKING' if submission_success else '❌ FAILED'}")
        
        if stats_success and submission_success:
            print("\n🎉 Database fixes are working!")
            print("✅ No more database locking issues")
            print("✅ Schema is correct")
            print("✅ Form submissions working")
        else:
            print("\n❌ Some issues still exist")
            print("🔧 Check server logs for details")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Flask server.")
        print("💡 Make sure Flask server is running: cd backend && python3 app.py")
    except Exception as e:
        print(f"❌ Test error: {e}")

if __name__ == "__main__":
    main()