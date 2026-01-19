# 📊 Google Sheets Integration Setup Guide

## 🎯 **Goal**
Connect your UIC Patent Portal to automatically save patent applications to Google Sheets.

## 📋 **Step 1: Create Google Sheet**

1. **Go to Google Sheets**: https://sheets.google.com
2. **Create New Sheet**: Click "Blank" to create a new spreadsheet
3. **Name it**: "UIC Patent Applications"
4. **Set up columns** in Row 1:
   ```
   A1: Application ID
   B1: Submission Date
   C1: Full Name
   D1: Email
   E1: Department
   F1: Branch
   G1: Applicant Type
   H1: Contact Number
   I1: Patent Title
   J1: Patent Type
   K1: Description
   L1: Novelty
   M1: Team Members
   ```

## 🔧 **Step 2: Create Google Apps Script**

1. **Open Apps Script**: In your Google Sheet, go to `Extensions > Apps Script`
2. **Replace default code** with this:

```javascript
function doPost(e) {
  try {
    // Get the active spreadsheet
    const sheet = SpreadsheetApp.getActiveSheet();
    
    // Parse the incoming data
    const data = JSON.parse(e.postData.contents);
    
    // Prepare row data
    const rowData = [
      data.applicationId || '',
      new Date().toISOString(),
      data.fullName || '',
      data.email || '',
      data.department || '',
      data.branch || '',
      data.applicantType || '',
      data.contactNo || '',
      data.patentTitle || '',
      data.patentType || '',
      data.description || '',
      data.novelty || '',
      JSON.stringify(data.teamMembers || [])
    ];
    
    // Add row to sheet
    sheet.appendRow(rowData);
    
    // Return success response
    return ContentService
      .createTextOutput(JSON.stringify({
        success: true,
        message: 'Data added to sheet successfully',
        applicationId: data.applicationId
      }))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    // Return error response
    return ContentService
      .createTextOutput(JSON.stringify({
        success: false,
        error: error.toString()
      }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  return ContentService
    .createTextOutput(JSON.stringify({
      success: true,
      message: 'UIC Patent Portal Google Apps Script is running'
    }))
    .setMimeType(ContentService.MimeType.JSON);
}
```

## 🚀 **Step 3: Deploy Apps Script**

1. **Save the script**: Click "Save" (Ctrl+S)
2. **Deploy as Web App**:
   - Click "Deploy" > "New deployment"
   - Choose type: "Web app"
   - Execute as: "Me"
   - Who has access: "Anyone"
   - Click "Deploy"
3. **Copy the Web App URL**: It looks like:
   ```
   https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec
   ```

## 🔧 **Step 4: Update Flask App**

Replace the URL in your `backend/app.py`:
```python
APPS_SCRIPT_URL = 'YOUR_NEW_WEB_APP_URL_HERE'
```

## ✅ **Step 5: Test Integration**

Run the test script to verify it works:
```bash
python3 test_google_sheets.py
```

---

## 🔒 **Troubleshooting**

### Common Issues:
1. **Permission denied**: Make sure Apps Script has access to your sheet
2. **Script not found**: Verify the Web App URL is correct
3. **CORS errors**: Ensure "Anyone" has access to the web app

### Test Manually:
You can test your Apps Script URL directly:
```bash
curl -X POST "YOUR_WEB_APP_URL" \
  -H "Content-Type: application/json" \
  -d '{"applicationId":"TEST-123","fullName":"Test User","patentTitle":"Test Patent"}'
```

Should return: `{"success":true,"message":"Data added to sheet successfully"}`