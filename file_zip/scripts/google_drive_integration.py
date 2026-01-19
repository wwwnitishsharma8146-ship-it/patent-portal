#!/usr/bin/env python3
"""
Google Drive Integration for UIC Patent Portal
Handles uploading files to Google Drive folder
"""

import os
import json
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
import mimetypes

class GoogleDriveUploader:
    def __init__(self, credentials_file='google_drive_credentials.json'):
        """Initialize Google Drive uploader with service account credentials"""
        self.credentials_file = credentials_file
        self.folder_id = '1ygSWj1VMKiKXUKXDCqMInEGBE-3na5XN'  # Your specified folder ID
        self.service = None
        self.enabled = False
        
        # Try to initialize the service
        self._initialize_service()
    
    def _initialize_service(self):
        """Initialize Google Drive service with credentials"""
        try:
            if not os.path.exists(self.credentials_file):
                print(f"⚠️  Google Drive credentials not found: {self.credentials_file}")
                print("   Run 'python3 setup_google_drive.py' for setup instructions")
                return False
            
            # Load service account credentials
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_file,
                scopes=['https://www.googleapis.com/auth/drive.file']
            )
            
            # Build the service
            self.service = build('drive', 'v3', credentials=credentials)
            self.enabled = True
            print("✅ Google Drive service initialized successfully")
            return True
            
        except Exception as e:
            print(f"⚠️  Failed to initialize Google Drive service: {str(e)}")
            print("   Check your credentials file and permissions")
            return False
    
    def upload_file(self, file_path, application_id, original_filename=None):
        """
        Upload a file to Google Drive folder
        
        Args:
            file_path (str): Local path to the file
            application_id (str): Patent application ID for naming
            original_filename (str): Original filename if different from file_path
            
        Returns:
            dict: Upload result with success status and file info
        """
        if not self.enabled:
            return {
                'success': False,
                'error': 'Google Drive service not available',
                'file_id': None,
                'file_url': None
            }
        
        try:
            # Prepare file metadata
            filename = original_filename or os.path.basename(file_path)
            drive_filename = f"{application_id}_{filename}"
            
            # Detect MIME type
            mime_type, _ = mimetypes.guess_type(file_path)
            if not mime_type:
                mime_type = 'application/octet-stream'
            
            # File metadata for Google Drive
            file_metadata = {
                'name': drive_filename,
                'parents': [self.folder_id],
                'description': f'Patent application file for {application_id}'
            }
            
            # Create media upload object
            media = MediaFileUpload(
                file_path,
                mimetype=mime_type,
                resumable=True
            )
            
            # Upload the file
            print(f"📤 Uploading {filename} to Google Drive...")
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,name,webViewLink,webContentLink'
            ).execute()
            
            file_id = file.get('id')
            file_url = file.get('webViewLink')
            
            print(f"✅ File uploaded successfully: {drive_filename}")
            print(f"   File ID: {file_id}")
            print(f"   View URL: {file_url}")
            
            return {
                'success': True,
                'file_id': file_id,
                'file_url': file_url,
                'drive_filename': drive_filename,
                'original_filename': filename
            }
            
        except Exception as e:
            print(f"❌ Failed to upload {filename}: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'file_id': None,
                'file_url': None
            }
    
    def upload_multiple_files(self, file_paths, application_id, original_filenames=None):
        """
        Upload multiple files to Google Drive
        
        Args:
            file_paths (list): List of local file paths
            application_id (str): Patent application ID
            original_filenames (list): List of original filenames (optional)
            
        Returns:
            list: List of upload results for each file
        """
        results = []
        
        for i, file_path in enumerate(file_paths):
            original_name = None
            if original_filenames and i < len(original_filenames):
                original_name = original_filenames[i]
            
            result = self.upload_file(file_path, application_id, original_name)
            results.append(result)
        
        return results
    
    def test_connection(self):
        """Test Google Drive connection and folder access"""
        if not self.enabled:
            return False
        
        try:
            # Try to access the folder
            folder = self.service.files().get(
                fileId=self.folder_id,
                fields='id,name,permissions'
            ).execute()
            
            print(f"✅ Successfully connected to Google Drive folder: {folder.get('name')}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to access Google Drive folder: {str(e)}")
            print("   Make sure the service account has access to the folder")
            return False

# Global instance
drive_uploader = GoogleDriveUploader()

def upload_to_google_drive(file_path, application_id, original_filename=None):
    """
    Convenience function to upload a single file
    
    Args:
        file_path (str): Local path to file
        application_id (str): Patent application ID
        original_filename (str): Original filename
        
    Returns:
        dict: Upload result
    """
    return drive_uploader.upload_file(file_path, application_id, original_filename)

def upload_multiple_to_google_drive(file_paths, application_id, original_filenames=None):
    """
    Convenience function to upload multiple files
    
    Args:
        file_paths (list): List of local file paths
        application_id (str): Patent application ID
        original_filenames (list): List of original filenames
        
    Returns:
        list: List of upload results
    """
    return drive_uploader.upload_multiple_files(file_paths, application_id, original_filenames)

def test_google_drive_connection():
    """Test Google Drive connection"""
    return drive_uploader.test_connection()

if __name__ == "__main__":
    # Test the connection when run directly
    print("🧪 Testing Google Drive connection...")
    if test_google_drive_connection():
        print("🎉 Google Drive integration is ready!")
    else:
        print("❌ Google Drive integration needs setup")
        print("   Run 'python3 setup_google_drive.py' for instructions")