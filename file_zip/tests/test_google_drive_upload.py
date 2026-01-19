#!/usr/bin/env python3
"""
Test Google Drive file upload
"""

import requests
import base64
import json

def test_drive_upload():
    """Test uploading a file to Google Drive"""
    
    GOOGLE_DRIVE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbyHDue-XLfJVBxCxP3SGrclgpavkJvSpw0CemY-lcAqiB9k_qk4dVjaW7S3Ou_QEL4y_w/exec'
    
    print("🧪 Testing Google Drive Upload")
    print("=" * 50)
    
    # Create a simple test PDF content
    test_pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n>>\nendobj\nxref\n0 4\n0000000000 65535 f\n0000000009 00000 n\n0000000058 00000 n\n0000000115 00000 n\ntrailer\n<<\n/Size 4\n/Root 1 0 R\n>>\nstartxref\n196\n%%EOF"
    
    # Encode to base64
    file_base64 = base64.b64encode(test_pdf_content).decode('utf-8')
    
    # Prepare payload
    payload = {
        'fileName': 'TEST-UIC-PAT-12345_test_document.pdf',
        'fileData': file_base64,
        'mimeType': 'application/pdf',
        'applicationId': 'TEST-12345'
    }
    
    print(f"📤 Sending test PDF to Google Drive...")
    print(f"   File size: {len(test_pdf_content)} bytes")
    print(f"   Base64 size: {len(file_base64)} characters")
    
    try:
        response = requests.post(GOOGLE_DRIVE_SCRIPT_URL, json=payload, timeout=30)
        
        print(f"\n📊 Response Status: {response.status_code}")
        print(f"📊 Response Headers: {dict(response.headers)}")
        print(f"\n📄 Response Content:")
        print(response.text[:500])
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"\n✅ JSON Response:")
                print(json.dumps(result, indent=2))
                
                if result.get('success'):
                    print(f"\n🎉 SUCCESS!")
                    print(f"   File URL: {result.get('fileUrl')}")
                    print(f"   File ID: {result.get('fileId')}")
                else:
                    print(f"\n❌ Upload failed: {result.get('error')}")
            except:
                print(f"\n⚠️  Response is not JSON")
        else:
            print(f"\n❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_drive_upload()
