# How to Verify Google Drive PDFs

## Quick Verification Steps

### 1. Check if Files are in Google Drive
1. Go to https://drive.google.com
2. In the search bar, type: `"UIC Patent Files"`
3. You should see a folder with this name
4. Open the folder
5. Look for your uploaded PDF files

### 2. Verify Files are Actual PDFs (Not JSON/Script Code)

**Method 1: Click to Open**
- Click on any file in the folder
- If it opens as a PDF in Google Drive's PDF viewer, it's correct ✅
- If it shows JSON text or script code, it's wrong ❌

**Method 2: Check File Type**
- Right-click on a file
- Select "File information" or "Details"
- Check the "Type" field
- Should say: "PDF document" or "application/pdf" ✅
- Should NOT say: "Plain text" or "application/json" ❌

**Method 3: Download and Open**
- Right-click on a file
- Select "Download"
- Open the downloaded file with a PDF reader
- If it opens as a PDF, it's correct ✅
- If it shows text/code, it's wrong ❌

### 3. Check File Names
Files should be named like:
```
UIC-PAT-20260115-ABC123_20260115_181101_original_filename.pdf
```

Format: `[Application-ID]_[Timestamp]_[Original-Filename]`

### 4. Check File Sizes
- PDF files should have reasonable sizes (typically 100KB - 10MB)
- If files are very small (< 1KB), they might be JSON/text files
- The server logs show file sizes, e.g., "File size: 1594986 bytes" (1.59 MB)

## What You Should See

### ✅ Correct Setup:
- Folder: "UIC Patent Files" exists
- Files: Multiple PDF files with application IDs
- Type: PDF documents
- Preview: Opens in Google Drive PDF viewer
- Download: Opens as PDF in PDF reader

### ❌ Incorrect Setup (Old Issue):
- Files show as plain text
- Content is JSON data or script code
- Can't preview as PDF
- File type shows as "text/plain" or "application/json"

## Recent Upload from Logs

Based on your server logs, this file was uploaded:
```
File: UIC-PAT-20260115-51530F_20260115_181101_UIC-PAT-20260108-421AA2_20260108_230244_Asymptotic_Notations.pdf
Size: 1594986 bytes (1.59 MB)
Drive URL: https://drive.google.com/file/d/1RTTWF97ldc0BvxgBULhsr8PEF5HvU5Fz/view?usp=drivesdk
```

### Direct Link to Check:
Click this link to verify the file:
https://drive.google.com/file/d/1RTTWF97ldc0BvxgBULhsr8PEF5HvU5Fz/view?usp=drivesdk

**What to expect:**
- Should open in Google Drive
- Should show PDF preview
- Should have PDF controls (zoom, download, print)
- Should NOT show JSON or script code

## If Files are Still Wrong

If you click the link above and see JSON/script code instead of a PDF:

### Solution:
1. Go to https://script.google.com
2. Find your project with deployment ID: `AKfycbzoz5m64cZ5Q7Jwo_adbcuiPJgdDOtw1b38W_A4Fze5QWgYUbSQOUbKP9sNkZOGTH7N`
3. Replace ALL code with the contents of `google_drive_upload_script.js`
4. Deploy as NEW VERSION (not just save)
5. Test again with a new submission

## If Files are Correct

If the files are actual PDFs (which they should be based on the logs), then:
- ✅ Everything is working perfectly!
- ✅ No further action needed
- ✅ The system is ready to use

## Troubleshooting

### Issue: Can't find "UIC Patent Files" folder
**Solution**: 
- Search for the file ID directly: `1RTTWF97ldc0BvxgBULhsr8PEF5HvU5Fz`
- The folder might be in "Shared with me" if created by a service account
- Check if you're logged into the correct Google account

### Issue: Files are there but can't open
**Solution**:
- Check file permissions
- Make sure you have access to the folder
- Try downloading the file instead of previewing

### Issue: Files are JSON/text instead of PDFs
**Solution**:
- Redeploy the Apps Script with the updated code
- Make sure to create a NEW VERSION when deploying
- Clear browser cache and try again

## Next Steps

1. Click the Drive URL above to verify the file
2. Check if it's an actual PDF
3. If yes: ✅ Everything is working!
4. If no: Follow the redeployment steps in GOOGLE_DRIVE_DEPLOYMENT_INSTRUCTIONS.md
