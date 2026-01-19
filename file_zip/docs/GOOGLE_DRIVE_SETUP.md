# 📁 Google Drive Integration Setup

## 🎯 **Goal**
Automatically upload patent application files (PDFs, documents) to your Google Drive folder when patents are submitted.

**Your Google Drive Folder**: https://drive.google.com/drive/folders/1ygSWj1VMKiKXUKXDCqMInEGBE-3na5XN

## 📋 **Quick Setup Steps**

### 1. **Install Dependencies**
```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### 2. **Run Setup Helper**
```bash
python3 setup_google_drive.py
```

### 3. **Create Google Cloud Project & Service Account**

#### A. Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Note your **Project ID**

#### B. Enable Google Drive API
1. In Google Cloud Console → **APIs & Services** → **Library**
2. Search for **"Google Drive API"**
3. Click on it and press **"Enable"**

#### C. Create Service Account
1. Go to **APIs & Services** → **Credentials**
2. Click **"Create Credentials"** → **"Service Account"**
3. Name: `UIC Patent Portal Drive Access`
4. Click **"Create and Continue"**
5. Skip role assignment → **"Continue"**
6. Click **"Done"**

#### D. Generate Service Account Key
1. Click on your newly created service account
2. Go to **"Keys"** tab
3. Click **"Add Key"** → **"Create New Key"**
4. Choose **"JSON"** format
5. Download the JSON file
6. **Rename it to**: `google_drive_credentials.json`
7. **Place it in your project root directory** (same folder as this README)

### 4. **Share Google Drive Folder with Service Account**

1. **Open your Google Drive folder**:
   ```
   https://drive.google.com/drive/folders/1ygSWj1VMKiKXUKXDCqMInEGBE-3na5XN
   ```

2. **Right-click** on the folder → **"Share"**

3. **Add the service account email**:
   - Open your `google_drive_credentials.json` file
   - Find the `"client_email"` field
   - Copy that email address
   - Paste it in the "Add people and groups" field

4. **Set permissions**: Choose **"Editor"**

5. **Click "Send"**

### 5. **Test the Integration**
```bash
python3 test_google_drive.py
```

## 🔧 **How It Works**

### **File Upload Process**
1. User submits patent application with files
2. Files are saved locally as backup
3. Files are automatically uploaded to Google Drive
4. Google Drive URLs are stored in database
5. User gets confirmation of successful upload

### **File Naming Convention**
Files in Google Drive will be named:
```
{APPLICATION_ID}_{ORIGINAL_FILENAME}
```
Example: `UIC-PAT-20260108-ABC123_patent_document.pdf`

### **Database Storage**
The system stores both local and Google Drive information:
- Local file path (backup)
- Google Drive file ID
- Google Drive view URL
- Upload status

## 📊 **Features**

✅ **Automatic Upload**: Files uploaded to Google Drive during patent submission  
✅ **Backup Storage**: Files also saved locally as backup  
✅ **Error Handling**: If Google Drive fails, files still saved locally  
✅ **Multiple Files**: Supports multiple file uploads per patent  
✅ **File Types**: PDF, DOC, DOCX, JPG, PNG, ZIP supported  
✅ **Organized Storage**: All files go to your specified folder  
✅ **Unique Naming**: Files named with application ID to avoid conflicts  

## 🚨 **Troubleshooting**

### **Common Issues**

#### 1. **"Credentials file not found"**
- Make sure `google_drive_credentials.json` is in the project root
- Check the filename is exactly `google_drive_credentials.json`

#### 2. **"Permission denied" or "Folder not accessible"**
- Verify you shared the Google Drive folder with the service account email
- Make sure you gave "Editor" permissions
- Check the folder ID in the URL matches: `1ygSWj1VMKiKXUKXDCqMInEGBE-3na5XN`

#### 3. **"API not enabled"**
- Make sure Google Drive API is enabled in Google Cloud Console
- Wait a few minutes after enabling for it to take effect

#### 4. **"Service account key invalid"**
- Re-download the service account key JSON file
- Make sure it's valid JSON format
- Ensure the service account has the correct permissions

### **Test Commands**

```bash
# Test Google Drive connection only
python3 -c "from google_drive_integration import test_google_drive_connection; test_google_drive_connection()"

# Test full integration
python3 test_google_drive.py

# Test through website
# 1. Start server: cd backend && python3 app.py
# 2. Go to http://localhost:5002
# 3. Submit a patent with a PDF file
# 4. Check your Google Drive folder
```

## 🔒 **Security Notes**

- **Keep `google_drive_credentials.json` secure and private**
- **Never commit it to version control** (it's in .gitignore)
- **Don't share the service account key publicly**
- **The service account only has access to files it creates**

## 📁 **File Structure**

After setup, your project should have:
```
├── google_drive_credentials.json     # Your service account key (keep private!)
├── google_drive_integration.py       # Google Drive upload code
├── setup_google_drive.py            # Setup helper script
├── test_google_drive.py             # Test script
├── backend/
│   └── app.py                       # Updated with Google Drive integration
└── .gitignore                       # Excludes credentials from git
```

## ✅ **Verification**

After setup, you should see:
1. **In terminal**: `✅ Google Drive service initialized successfully`
2. **During patent submission**: `✅ {filename} uploaded to Google Drive successfully`
3. **In your Google Drive folder**: New files with application ID prefixes
4. **In test results**: All tests passing

Your Google Drive folder will automatically receive all patent application files with organized naming!