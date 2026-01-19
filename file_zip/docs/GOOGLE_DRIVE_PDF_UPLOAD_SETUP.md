# 📁 Google Drive PDF Upload Setup

## ✅ **Current Configuration**

Your system is configured to upload PDF files to Google Drive using:

**Google Drive Apps Script URL:**
```
https://script.google.com/macros/s/AKfycbyHDue-XLfJVBxCxP3SGrclgpavkJvSpw0CemY-lcAqiB9k_qk4dVjaW7S3Ou_QEL4y_w/exec
```

**Google Sheets URL (unchanged):**
```
https://script.google.com/macros/s/AKfycby44PN4TqP2Q2Y9a-AtE-2jnntE6azhlJc_lyB5Zguco0FFA3n-KCDV37-MXdZzhShd-g/exec
```

## 🚀 **How It Works**

1. **User uploads PDF** through the patent form
2. **File saved locally** as backup
3. **File encoded to base64** and sent to Google Apps Script
4. **Apps Script decodes** the file and saves it as PDF to Google Drive
5. **Google Drive URL** returned and stored in database

## 📋 **Setup Instructions**

### **Step 1: Copy the Google Apps Script**

The script is in `google_drive_upload_script.js`. Copy this entire code.

### **Step 2: Create/Update Google Apps Script**

1. Go to: https://script.google.com
2. Create new project or open existing one
3. Paste the code from `google_drive_upload_script.js`
4. Save the project

### **Step 3: Deploy as Web App**

1. Click **Deploy** → **New deployment**
2. Choose type: **Web app**
3. Settings:
   - **Execute as**: Me
   - **Who has access**: Anyone
4. Click **Deploy**
5. Copy the Web App URL

### **Step 4: Verify URL in Flask App**

The URL is already configured in `backend/app.py`:
```python
GOOGLE_DRIVE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbyHDue-XLfJVBxCxP3SGrclgpavkJvSpw0CemY-lcAqiB9k_qk4dVjaW7S3Ou_QEL4y_w/exec'
```

## 🧪 **Testing**

### **Test 1: Check Apps Script is Running**
```bash
curl https://script.google.com/macros/s/AKfycbyHDue-XLfJVBxCxP3SGrclgpavkJvSpw0CemY-lcAqiB9k_qk4dVjaW7S3Ou_QEL4y_w/exec
```

Should return:
```json
{
  "success": true,
  "message": "UIC Patent Portal - Google Drive Upload Service is running"
}
```

### **Test 2: Submit Patent with PDF**

1. Go to: http://localhost:5002
2. Fill out patent form
3. Upload a PDF file
4. Submit
5. Check server logs for:
   ```
   ✅ File uploaded to Google Drive: filename.pdf
   Drive URL: https://drive.google.com/...
   ```

### **Test 3: Check Google Drive**

1. Go to your Google Drive
2. Look for folder: **"UIC Patent Files"**
3. Check for uploaded PDFs with names like:
   ```
   UIC-PAT-20260115-XXXXXX_document.pdf
   ```

## 📊 **What Gets Uploaded**

- ✅ **PDF files** - Patent documents, specifications
- ✅ **DOC/DOCX files** - Word documents
- ✅ **Images** - JPG, PNG for diagrams
- ✅ **ZIP files** - Compressed archives

All files are:
- Named with Application ID prefix
- Stored in "UIC Patent Files" folder
- Accessible via shareable link
- Viewable by anyone with the link

## 🔍 **Troubleshooting**

### **Issue: Files not appearing in Google Drive**

**Check:**
1. Apps Script is deployed correctly
2. URL in `backend/app.py` matches deployment URL
3. Server logs show successful upload
4. Google Drive folder "UIC Patent Files" exists

### **Issue: Getting JSON/Script files instead of PDFs**

**Solution:**
- The Apps Script properly decodes base64 data
- Make sure the script code matches `google_drive_upload_script.js`
- The MIME type is correctly set to `application/pdf`

### **Issue: Upload timeout**

**Solution:**
- Large files may take longer
- Timeout is set to 30 seconds
- Consider increasing timeout for large files

## 📝 **Server Logs to Watch**

When uploading works correctly, you'll see:
```
📄 File type detected: application/pdf
📤 Uploading document.pdf (application/pdf) to Google Drive...
   File size: 245678 bytes
✅ File uploaded to Google Drive: document.pdf
   Drive URL: https://drive.google.com/file/d/...
```

## ✅ **Current Status**

- ✅ Google Drive upload enabled
- ✅ Apps Script URL configured
- ✅ MIME type detection working
- ✅ Base64 encoding/decoding implemented
- ✅ Error handling in place
- ✅ Local backup maintained

## 🎯 **Next Steps**

1. **Deploy the Apps Script** with the code from `google_drive_upload_script.js`
2. **Verify the deployment URL** matches the one in `backend/app.py`
3. **Test by uploading a PDF** through the patent form
4. **Check Google Drive** for the uploaded file

Your system is ready to upload PDFs to Google Drive! 🚀
