#!/usr/bin/env python3
"""
Test Google Drive Integration for UIC Patent Portal
"""

import os
import requests
import time
from google_drive_integration import test_google_drive_connection, upload_to_google_drive

def create_test_file():
    """Create a test PDF file for upload testing"""
    test_content = """
%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj

2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj

3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Contents 4 0 R
>>
endobj

4 0 obj
<<
/Length 44
>>
stream
BT
/F1 12 Tf
100 700 Td
(UIC Patent Test File) Tj
ET
endstream
endobj

xref
0 5
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000206 00000 n 
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
300
%%EOF
"""
    
    test_file_path = "test_patent_document.pdf"
    with open(test_file_path, 'w') as f:
        f.write(test_content)
    
    print(f"📄 Created test PDF file: {test_file_path}")
    return test_file_path

def test_direct_upload():
    """Test direct Google Drive upload"""
    print("\n🧪 Testing Direct Google Drive Upload")
    print("=" * 50)
    
    # Test connection first
    if not test_google_drive_connection():
        print("❌ Google Drive connection failed")
        return False
    
    # Create test file
    test_file = create_test_file()
    
    try:
        # Test upload
        application_id = f"DRIVE-TEST-{int(time.time())}"
        result = upload_to_google_drive(test_file, application_id, "test_patent_document.pdf")
        
        if result['success']:
            print(f"✅ File uploaded successfully!")
            print(f"   File ID: {result['file_id']}")
            print(f"   View URL: {result['file_url']}")
            print(f"   Drive Filename: {result['drive_filename']}")
            
            # Clean up local test file
            os.remove(test_file)
            print(f"🗑️  Cleaned up local test file")
            
            return True
        else:
            print(f"❌ Upload failed: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {str(e)}")
        return False
    finally:
        # Clean up test file if it still exists
        if os.path.exists(test_file):
            os.remove(test_file)

def test_flask_integration():
    """Test Google Drive integration through Flask app"""
    print("\n🌐 Testing Flask Integration with Google Drive")
    print("=" * 50)
    
    base_url = "http://localhost:5002"
    session = requests.Session()
    
    # Step 1: Create and login user
    print("1. 👤 Setting up test user...")
    signup_data = {
        'name': f'Drive Test User {int(time.time())}',
        'email': f'drivetest{int(time.time())}@cuchd.in',
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
    
    # Step 2: Create test file
    test_file = create_test_file()
    
    try:
        # Step 3: Submit patent with file
        print("2. 📝 Submitting patent with Google Drive upload...")
        
        patent_data = {
            'patentTitle': 'Google Drive Test Patent',
            'patentType': 'utility',
            'description': 'This patent tests the Google Drive integration functionality.',
            'novelty': 'This tests whether patent files are properly uploaded to Google Drive.',
            'applicantType': 'student'
        }
        
        # Prepare file for upload
        with open(test_file, 'rb') as f:
            files = {'files': (test_file, f, 'application/pdf')}
            response = session.post(f"{base_url}/submit", data=patent_data, files=files)
        
        if response.status_code == 200:
            try:
                result = response.json()
                if result['success']:
                    print(f"   ✅ Patent submitted: {result['applicationId']}")
                    
                    # Check file upload results
                    files_uploaded = result.get('filesUploaded', 0)
                    google_drive_files = result.get('googleDriveFiles', [])
                    local_files = result.get('localFiles', [])
                    
                    print(f"   📁 Total files uploaded: {files_uploaded}")
                    print(f"   ☁️  Google Drive files: {len(google_drive_files)}")
                    print(f"   💾 Local files: {len(local_files)}")
                    
                    if google_drive_files:
                        print("   ✅ Google Drive upload: SUCCESS")
                        for gd_file in google_drive_files:
                            print(f"      📄 {gd_file['original_filename']}")
                            if gd_file.get('google_drive_url'):
                                print(f"      🔗 {gd_file['google_drive_url']}")
                        return True
                    else:
                        print("   ⚠️  No files uploaded to Google Drive")
                        if local_files:
                            print("   📁 Files saved locally as backup")
                        return False
                else:
                    print(f"   ❌ Patent submission failed: {result['message']}")
                    return False
            except Exception as e:
                print(f"   ❌ JSON parsing failed: {e}")
                return False
        else:
            print(f"   ❌ HTTP error: {response.status_code}")
            return False
            
    finally:
        # Clean up test file
        if os.path.exists(test_file):
            os.remove(test_file)

def main():
    print("🚀 TESTING GOOGLE DRIVE INTEGRATION")
    print("=" * 60)
    
    # Test 1: Direct upload
    direct_success = test_direct_upload()
    
    # Test 2: Flask integration
    try:
        flask_success = test_flask_integration()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Flask server.")
        print("💡 Make sure Flask server is running: cd backend && python3 app.py")
        flask_success = False
    
    # Results
    print("\n" + "=" * 60)
    print("📊 GOOGLE DRIVE INTEGRATION RESULTS")
    print("=" * 60)
    
    print(f"Direct Upload Test: {'✅ WORKING' if direct_success else '❌ FAILED'}")
    print(f"Flask Integration: {'✅ WORKING' if flask_success else '❌ FAILED'}")
    
    if direct_success and flask_success:
        print("\n🎉 Google Drive integration is fully working!")
        print("📁 Files will be automatically uploaded to your Google Drive folder")
        print("🔗 Folder: https://drive.google.com/drive/folders/1ygSWj1VMKiKXUKXDCqMInEGBE-3na5XN")
    elif direct_success and not flask_success:
        print("\n⚠️  Google Drive works directly, but Flask integration has issues")
        print("🔧 Check Flask app configuration and dependencies")
    elif not direct_success:
        print("\n❌ Google Drive integration needs setup")
        print("\n🔧 SETUP STEPS:")
        print("1. Run: python3 setup_google_drive.py")
        print("2. Follow the setup instructions")
        print("3. Make sure google_drive_credentials.json is in place")
        print("4. Share the Google Drive folder with your service account")

if __name__ == "__main__":
    main()