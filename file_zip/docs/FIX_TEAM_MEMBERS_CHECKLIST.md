# Fix Team Members in Google Sheets - Checklist

## Problem Identified

✅ **Backend is working correctly** - Team members are being sent with all details
❌ **Google Apps Script needs to be updated** - The script is not using the new format

## Evidence from Logs

The backend is sending:
```
📋 Team members data: [{'name': 'aman', 'role': 'co', 'department': 'mca', 'email': 'a@gmail.com'}, ...]
   Found 2 team members
   Member 1: aman - co
   Member 2: rohan - co
📤 Sending payload to Google Sheets with 2 team members
✅ Data sent to Google Sheet
```

This means the data IS being sent correctly from the backend!

## Solution: Update Google Apps Script

### Step 1: Open Google Apps Script
1. Go to https://script.google.com
2. Sign in with your Google account
3. Find your project with deployment ID: `AKfycby44PN4TqP2Q2Y9a-AtE-2jnntE6azhlJc_lyB5Zguco0FFA3n-KCDV37-MXdZzhShd-g`

### Step 2: Replace ALL Code
1. In the script editor, **SELECT ALL** (Ctrl+A or Cmd+A)
2. **DELETE** all existing code
3. Open the file `google_apps_script.js` from this project
4. **COPY ALL** the code from that file
5. **PASTE** into the Google Apps Script editor
6. **SAVE** (Ctrl+S or Cmd+S or click disk icon)

### Step 3: Run Setup Headers (ONE TIME ONLY)
1. In the function dropdown (top toolbar), select `setupHeaders`
2. Click the **Run** button (▶️ play icon)
3. If prompted, authorize the script to access your Google Sheets
4. Wait for it to complete
5. Check your Google Sheet - you should see new column headers

**Expected Headers:**
```
Application ID | Submission Date | Full Name | Email | Department | Branch | 
Applicant Type | Contact Number | Patent Title | Patent Type | Description | 
Novelty | Member 1 Name | Member 1 Role | Member 1 Department | Member 1 Email |
Member 2 Name | Member 2 Role | Member 2 Department | Member 2 Email | ...
```

### Step 4: Deploy as NEW Version
1. Click **Deploy** button (top right corner)
2. Select **Manage deployments**
3. Find the deployment with ID ending in `...MXdZzhShd-g`
4. Click the **pencil/edit icon** next to it
5. Under "Version", select **New version** (NOT "Latest version")
6. Add description: "Team members in separate columns - v2"
7. Click **Deploy**
8. Click **Done**

### Step 5: Test
1. Go to http://127.0.0.1:5002
2. Submit a new patent application
3. Add 2-3 team members with all details
4. Submit the form
5. Check Google Sheets immediately

**What you should see:**
- New row added
- Application ID in column A
- Team member details in columns M onwards:
  - Column M: First member's name
  - Column N: First member's role
  - Column O: First member's department
  - Column P: First member's email
  - Column Q: Second member's name
  - etc.

## Common Mistakes to Avoid

### ❌ Mistake 1: Not creating a NEW version
- If you just save without deploying a new version, the old code will still run
- Always create a NEW VERSION when deploying

### ❌ Mistake 2: Not running setupHeaders
- Without running setupHeaders, the column headers won't match
- Run it ONCE after updating the code

### ❌ Mistake 3: Updating the wrong script
- Make sure you're updating the SHEETS script (ending in ...MXdZzhShd-g)
- NOT the Drive script (ending in ...QWgYUbSQOUbKP9sNkZOGTH7N)

### ❌ Mistake 4: Not waiting for deployment
- After deploying, wait 10-20 seconds before testing
- Google needs time to propagate the new version

## Verification Steps

### 1. Check Script Version
In Google Apps Script, look at the version number in the deployment. It should be higher than before.

### 2. Check Column Headers
Your Google Sheet should have 32 columns with proper headers.

### 3. Check Test Data
Submit a test application and verify:
- ✅ Application ID is sequential (UIC-PAT-X)
- ✅ All applicant details appear
- ✅ Team member 1 details in columns M-P
- ✅ Team member 2 details in columns Q-T
- ✅ No empty columns where data should be

## If Still Not Working

### Check Apps Script Execution Logs
1. In Google Apps Script editor
2. Click **Executions** (left sidebar, clock icon)
3. Look for recent executions
4. Check for any errors
5. Click on an execution to see details

### Check What Data is Received
Add this to the top of the `doPost` function in Apps Script:
```javascript
console.log('Received data:', JSON.stringify(data, null, 2));
```

This will log exactly what data the script receives.

### Verify Deployment URL
Make sure the backend is using the correct URL:
```
https://script.google.com/macros/s/AKfycby44PN4TqP2Q2Y9a-AtE-2jnntE6azhlJc_lyB5Zguco0FFA3n-KCDV37-MXdZzhShd-g/exec
```

## Current Status

- ✅ Backend code: Updated and working
- ✅ Team members: Being captured correctly
- ✅ Data: Being sent to Google Sheets
- ⏳ Google Apps Script: **NEEDS TO BE UPDATED BY YOU**
- ⏳ Deployment: **NEEDS TO BE REDEPLOYED BY YOU**

## Next Action

**YOU MUST:**
1. Update the Google Apps Script code
2. Run setupHeaders function
3. Deploy as NEW version
4. Test with a new submission

The backend is ready and waiting! The issue is 100% in the Google Apps Script not being updated.
