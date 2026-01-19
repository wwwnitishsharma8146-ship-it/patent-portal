#!/usr/bin/env python3
"""
Google Drive Setup for UIC Patent Portal
This script helps you set up Google Drive API credentials
"""

import os
import json

def create_credentials_template():
    """Create a template for Google Drive credentials"""
    
    credentials_template = {
        "type": "service_account",
        "project_id": "YOUR_PROJECT_ID",
        "private_key_id": "YOUR_PRIVATE_KEY_ID", 
        "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n",
        "client_email": "YOUR_SERVICE_ACCOUNT_EMAIL@YOUR_PROJECT_ID.iam.gserviceaccount.com",
        "client_id": "YOUR_CLIENT_ID",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/YOUR_SERVICE_ACCOUNT_EMAIL%40YOUR_PROJECT_ID.iam.gserviceaccount.com"
    }
    
    with open('google_drive_credentials.json.template', 'w') as f:
        json.dump(credentials_template, f, indent=2)
    
    print("📁 Created google_drive_credentials.json.template")

def print_setup_instructions():
    """Print detailed setup instructions"""
    
    print("🔧 GOOGLE DRIVE API SETUP INSTRUCTIONS")
    print("=" * 60)
    
    print("\n📋 STEP 1: Create Google Cloud Project")
    print("1. Go to: https://console.cloud.google.com/")
    print("2. Create a new project or select existing one")
    print("3. Note your Project ID")
    
    print("\n📋 STEP 2: Enable Google Drive API")
    print("1. In Google Cloud Console, go to 'APIs & Services' > 'Library'")
    print("2. Search for 'Google Drive API'")
    print("3. Click on it and press 'Enable'")
    
    print("\n📋 STEP 3: Create Service Account")
    print("1. Go to 'APIs & Services' > 'Credentials'")
    print("2. Click 'Create Credentials' > 'Service Account'")
    print("3. Name it 'UIC Patent Portal Drive Access'")
    print("4. Click 'Create and Continue'")
    print("5. Skip role assignment (click 'Continue')")
    print("6. Click 'Done'")
    
    print("\n📋 STEP 4: Generate Service Account Key")
    print("1. Click on your newly created service account")
    print("2. Go to 'Keys' tab")
    print("3. Click 'Add Key' > 'Create New Key'")
    print("4. Choose 'JSON' format")
    print("5. Download the JSON file")
    print("6. Rename it to 'google_drive_credentials.json'")
    print("7. Place it in your project root directory")
    
    print("\n📋 STEP 5: Share Google Drive Folder")
    print("1. Open your Google Drive folder:")
    print("   https://drive.google.com/drive/folders/1ygSWj1VMKiKXUKXDCqMInEGBE-3na5XN")
    print("2. Right-click > 'Share'")
    print("3. Add the service account email (from the JSON file)")
    print("4. Give it 'Editor' permissions")
    print("5. Click 'Send'")
    
    print("\n📋 STEP 6: Update Configuration")
    print("1. Make sure 'google_drive_credentials.json' is in your project root")
    print("2. The folder ID is already configured: 1ygSWj1VMKiKXUKXDCqMInEGBE-3na5XN")
    
    print("\n📋 STEP 7: Test Integration")
    print("1. Run: python3 test_google_drive.py")
    print("2. Submit a patent with a PDF file")
    print("3. Check your Google Drive folder for the uploaded file")
    
    print("\n⚠️  SECURITY NOTE:")
    print("• Keep google_drive_credentials.json secure and private")
    print("• Add it to .gitignore to avoid committing to version control")
    print("• Never share the service account key publicly")

def create_gitignore():
    """Create/update .gitignore to exclude credentials"""
    
    gitignore_content = """
# Google Drive Credentials
google_drive_credentials.json
google_drive_credentials.json.template

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/

# Database
*.db
*.sqlite

# Uploads
uploads/
backend/uploads/

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content.strip())
    
    print("📝 Created/updated .gitignore")

def main():
    print("🚀 Setting up Google Drive integration for UIC Patent Portal")
    print("=" * 60)
    
    create_credentials_template()
    create_gitignore()
    print_setup_instructions()
    
    print("\n✅ Setup files created!")
    print("📋 Follow the instructions above to complete the setup")

if __name__ == "__main__":
    main()