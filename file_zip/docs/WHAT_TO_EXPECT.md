# What to Expect After Deployment

## Current Setup Status

✅ **Flask Backend**: Running on http://127.0.0.1:5002
✅ **Google Sheets Integration**: Working (URL: ...MXdZzhShd-g/exec)
✅ **Google Drive Script URL**: Configured (URL: ...QWgYUbSQOUbKP9sNkZOGTH7N/exec)
⚠️ **Google Drive Script**: Needs redeployment with updated code

## What Happens When You Submit a Form

### 1. Form Submission
When you fill out the patent form and click submit, the backend will:
- Save the application to the local database
- Save team member information
- Process uploaded files

### 2. File Upload Process
For each PDF file you upload, you'll see these logs:

```
📄 File type detected: application/pdf
📤 Uploading [filename].pdf (application/pdf) to Google Drive...
   File size: [size] bytes
```

### 3. Successful Upload (After You Deploy the Script)
If the Apps Script is properly deployed, you'll see:

```
✅ File uploaded to Google Drive: [filename].pdf
   Drive URL: https://drive.google.com/file/d/[file-id]/view
```

### 4. Current Behavior (Before Deployment)
Right now, you might see:

```
❌ Google Drive HTTP error: [status code]
   Response: [error message]
```

OR

```
⚠️  Google Drive upload failed for [filename].pdf
   File saved locally as backup
```

This is because the Apps Script needs to be redeployed with the updated code.

### 5. Google Sheets Sync
After file upload, the data is sent to Google Sheets:

```
✅ Data sent to Google Sheet
```

### 6. Final Response
The form will show a success message with:
- Application ID (e.g., UIC-PAT-20260115-ABC123)
- Number of files uploaded
- Google Drive status

## After You Deploy the Updated Script

### Expected Server Logs:
```
📝 Submit request from 127.0.0.1
📝 Guest submission
📄 File type detected: application/pdf
📤 Uploading test.pdf (application/pdf) to Google Drive...
   File size: 12345 bytes
✅ File uploaded to Google Drive: test.pdf
   Drive URL: https://drive.google.com/file/d/1abc...xyz/view
✅ test.pdf uploaded to Google Drive successfully
✅ Data sent to Google Sheet
127.0.0.1 - - [15/Jan/2026 21:57:30] "POST /submit HTTP/1.1" 200 -
```

### Expected in Google Drive:
- Folder: **UIC Patent Files**
- File: **UIC-PAT-20260115-ABC123_test.pdf**
- File type: Actual PDF (not JSON or script code)
- Accessible with link sharing enabled

### Expected in Google Sheets:
- New row with all application data
- Application ID
- Applicant details
- Patent information
- Team members (if any)

## How to Verify Everything Works

1. **Open the website**: http://127.0.0.1:5002
2. **Fill the form**:
   - Enter applicant details
   - Add patent title and description
   - Upload a PDF file
   - Click Submit
3. **Check server logs** (in your terminal where Flask is running)
4. **Check Google Drive**:
   - Go to https://drive.google.com
   - Find "UIC Patent Files" folder
   - Verify the PDF is there and can be opened
5. **Check Google Sheets**:
   - Open your Google Sheet
   - Verify the new row appears with all data

## Common Issues and Solutions

### Issue: "Drive URL: None" in logs
**Solution**: Redeploy the Apps Script with the updated code

### Issue: Files appear as JSON or script code
**Solution**: Make sure you copied the ENTIRE script from `google_drive_upload_script.js` and redeployed

### Issue: No files in Google Drive
**Solution**: 
- Check Apps Script execution logs for errors
- Verify the deployment ID matches: AKfycbzoz5m64cZ5Q7Jwo_adbcuiPJgdDOtw1b38W_A4Fze5QWgYUbSQOUbKP9sNkZOGTH7N
- Make sure you created a NEW version when redeploying

### Issue: Records missing from Google Sheets
**Possible causes**:
- Network timeout during submission
- Google Sheets API rate limiting
- Apps Script execution time limit
- Check Apps Script execution logs for the Sheets script

## Next Steps

1. ✅ Server is running
2. ⏳ Deploy the updated Google Apps Script (follow GOOGLE_DRIVE_DEPLOYMENT_INSTRUCTIONS.md)
3. ⏳ Test form submission
4. ⏳ Verify PDFs appear in Google Drive
5. ⏳ Verify data appears in Google Sheets

The backend code is ready and waiting for you to deploy the Apps Script!
