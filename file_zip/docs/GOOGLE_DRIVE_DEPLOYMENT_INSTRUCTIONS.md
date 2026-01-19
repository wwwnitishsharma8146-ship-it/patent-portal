# Google Drive PDF Upload - Deployment Instructions

## Current Status
✅ Backend code is ready and configured with your deployment URL
✅ Google Apps Script code is ready in `google_drive_upload_script.js`
⚠️ You need to deploy the updated script to Google Apps Script

## Your Configuration
- **Google Drive Script URL**: `https://script.google.com/macros/s/AKfycbzoz5m64cZ5Q7Jwo_adbcuiPJgdDOtw1b38W_A4Fze5QWgYUbSQOUbKP9sNkZOGTH7N/exec`
- **Deployment ID**: `AKfycbzoz5m64cZ5Q7Jwo_adbcuiPJgdDOtw1b38W_A4Fze5QWgYUbSQOUbKP9sNkZOGTH7N`
- **Google Sheets URL**: `https://script.google.com/macros/s/AKfycby44PN4TqP2Q2Y9a-AtE-2jnntE6azhlJc_lyB5Zguco0FFA3n-KCDV37-MXdZzhShd-g/exec` (unchanged)

## Step-by-Step Deployment

### Step 1: Open Your Google Apps Script Project
1. Go to https://script.google.com
2. Find your existing project with deployment ID `AKfycbzoz5m64cZ5Q7Jwo_adbcuiPJgdDOtw1b38W_A4Fze5QWgYUbSQOUbKP9sNkZOGTH7N`
3. Open the project

### Step 2: Replace the Script Code
1. Delete ALL existing code in the script editor
2. Copy the ENTIRE contents of `google_drive_upload_script.js` from this project
3. Paste it into the Google Apps Script editor
4. Click the disk icon or press Ctrl+S (Cmd+S on Mac) to save

### Step 3: Redeploy the Script
1. Click on **Deploy** button (top right)
2. Select **Manage deployments**
3. Find the deployment with ID ending in `...QWgYUbSQOUbKP9sNkZOGTH7N`
4. Click the pencil/edit icon next to it
5. Under "Version", select **New version**
6. Add a description like "Fixed PDF upload - saves actual PDFs not JSON"
7. Click **Deploy**
8. Click **Done**

### Step 4: Test the Deployment
1. Make sure your Flask server is running on port 5002
2. Open http://127.0.0.1:5002 in your browser
3. Fill out the patent application form
4. Upload a PDF file
5. Submit the form
6. Check the server logs for:
   - `📤 Uploading [filename] (application/pdf) to Google Drive...`
   - `✅ File uploaded to Google Drive: [filename]`
   - `Drive URL: https://drive.google.com/...`

### Step 5: Verify in Google Drive
1. Go to your Google Drive
2. Look for a folder named **"UIC Patent Files"**
3. Check if the uploaded PDF appears there
4. Try opening the PDF to verify it's a real PDF file (not JSON or script code)

## What the Updated Script Does

The new script properly:
1. ✅ Receives base64 encoded file data from your Flask backend
2. ✅ Decodes the base64 data to actual bytes
3. ✅ Creates a proper blob with the correct MIME type (`application/pdf`)
4. ✅ Saves the file as an actual PDF in Google Drive
5. ✅ Returns the file URL and download link
6. ✅ Creates/uses a folder named "UIC Patent Files"

## Key Changes from Previous Version

**Before**: Script was saving JSON data or script code as files
**After**: Script properly decodes base64 and creates actual PDF files

The critical fix is this line:
```javascript
const blob = Utilities.newBlob(decodedData, mimeType, fileName);
```

This creates a proper binary blob from the decoded base64 data, which Google Drive then saves as an actual PDF file.

## Troubleshooting

### If PDFs still don't appear in Drive:
1. Check the Apps Script execution logs:
   - In Apps Script editor, click **Executions** (left sidebar)
   - Look for recent executions and any error messages
2. Verify the deployment is active and using the latest version
3. Make sure the script has permission to access Google Drive

### If you see "Drive URL: None" in server logs:
- This means the Apps Script didn't return a successful response
- Check Apps Script execution logs for errors
- Verify you redeployed with the new version

### If files appear but aren't PDFs:
- Make sure you copied the ENTIRE script from `google_drive_upload_script.js`
- Verify the deployment is using the NEW version (not an old cached version)

## Server is Running
Your Flask server is currently running at: http://127.0.0.1:5002

You can test the form submission right now after deploying the updated Apps Script!
