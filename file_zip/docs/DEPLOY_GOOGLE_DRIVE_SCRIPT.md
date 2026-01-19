# 🚨 IMPORTANT: Deploy Google Drive Upload Script

## ❌ **Current Problem**

The URL you provided is for the **Google Sheets** script (patent data), NOT for file uploads.

**Current URL (WRONG for file upload):**
```
https://script.google.com/macros/s/AKfycbyHDue-XLfJVBxCxP3SGrclgpavkJvSpw0CemY-lcAqiB9k_qk4dVjaW7S3Ou_QEL4y_w/exec
```

This script saves patent data to Google Sheets, but doesn't upload files to Google Drive.

## ✅ **Solution: Create NEW Apps Script for File Upload**

### **Step 1: Create New Google Apps Script**

1. Go to: https://script.google.com
2. Click **"New project"**
3. Name it: **"UIC Patent Drive Upload"**

### **Step 2: Copy the Upload Code**

1. Open the file: `google_drive_upload_script.js`
2. **Copy ALL the code** from that file
3. **Paste it** into your new Apps Script project
4. **Save** the project (Ctrl+S)

### **Step 3: Deploy as Web App**

1. Click **"Deploy"** → **"New deployment"**
2. Click the gear icon ⚙️ → Select **"Web app"**
3. Settings:
   - **Description**: "UIC Patent File Upload"
   - **Execute as**: **Me** (your email)
   - **Who has access**: **Anyone**
4. Click **"Deploy"**
5. **Authorize** the script (grant permissions)
6. **Copy the Web App URL** - it will look like:
   ```
   https://script.google.com/macros/s/NEW_DEPLOYMENT_ID_HERE/exec
   ```

### **Step 4: Update Flask App**

1. Open `backend/app.py`
2. Find this line (around line 56):
   ```python
   GOOGLE_DRIVE_SCRIPT_URL = 'https://script.google.com/macros/s/...'
   ```
3. Replace with your **NEW** deployment URL
4. Save the file
5. Restart the server

### **Step 5: Test**

1. Go to http://localhost:5002
2. Submit a patent with a PDF file
3. Check server logs for:
   ```
   ✅ File uploaded to Google Drive: filename.pdf
   Drive URL: https://drive.google.com/file/d/...
   ```
4. Check Google Drive for folder: **"UIC Patent Files"**
5. Your PDF should be there!

## 📋 **What Each Script Does**

### **Google Sheets Script** (Current URL)
- ✅ Saves patent application data
- ✅ Saves to Google Sheets
- ❌ Does NOT upload files

### **Google Drive Script** (Need to create)
- ✅ Receives base64 encoded files
- ✅ Decodes and saves as PDF to Google Drive
- ✅ Returns file URL
- ❌ Does NOT save patent data

## 🎯 **Quick Checklist**

- [ ] Create new Apps Script project
- [ ] Copy code from `google_drive_upload_script.js`
- [ ] Deploy as Web App
- [ ] Copy NEW deployment URL
- [ ] Update `GOOGLE_DRIVE_SCRIPT_URL` in `backend/app.py`
- [ ] Restart server
- [ ] Test file upload

## 💡 **Important Notes**

1. **Keep BOTH scripts** - one for Sheets, one for Drive
2. **Don't replace** the Google Sheets URL
3. **Create a separate** Apps Script project for file uploads
4. **The file upload script** creates a folder called "UIC Patent Files"
5. **Files are named** with Application ID prefix

Once you deploy the correct script, PDF files will upload to Google Drive! 🚀
