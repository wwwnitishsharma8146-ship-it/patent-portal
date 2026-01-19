# Updated Features - Deployment Guide

## Changes Made

### ✅ 1. Sequential Application IDs
**Before**: `UIC-PAT-20260115-ABC123` (random)
**After**: `UIC-PAT-1`, `UIC-PAT-2`, `UIC-PAT-3`, etc. (sequential)

The system now automatically generates sequential application numbers starting from 1.

### ✅ 2. Team Members in Separate Columns
**Before**: All team members in one column like "Member1 (Role), Member2 (Role)"
**After**: Each team member gets 4 separate columns:
- Member 1 Name, Member 1 Role, Member 1 Department, Member 1 Email
- Member 2 Name, Member 2 Role, Member 2 Department, Member 2 Email
- ... up to Member 5

## Google Sheets Column Structure (New)

Your Google Sheet will now have these columns:

| Column | Field Name |
|--------|------------|
| A | Application ID |
| B | Submission Date |
| C | Full Name |
| D | Email |
| E | Department |
| F | Branch |
| G | Applicant Type |
| H | Contact Number |
| I | Patent Title |
| J | Patent Type |
| K | Description |
| L | Novelty |
| M | Member 1 Name |
| N | Member 1 Role |
| O | Member 1 Department |
| P | Member 1 Email |
| Q | Member 2 Name |
| R | Member 2 Role |
| S | Member 2 Department |
| T | Member 2 Email |
| U | Member 3 Name |
| V | Member 3 Role |
| W | Member 3 Department |
| X | Member 3 Email |
| Y | Member 4 Name |
| Z | Member 4 Role |
| AA | Member 4 Department |
| AB | Member 4 Email |
| AC | Member 5 Name |
| AD | Member 5 Role |
| AE | Member 5 Department |
| AF | Member 5 Email |

**Total: 32 columns** (12 application fields + 20 team member fields)

## Deployment Steps

### Step 1: Update Google Apps Script for Sheets

1. Go to https://script.google.com
2. Find your Google Sheets script project (deployment ID: `AKfycby44PN4TqP2Q2Y9a-AtE-2jnntE6azhlJc_lyB5Zguco0FFA3n-KCDV37-MXdZzhShd-g`)
3. Delete ALL existing code
4. Copy the ENTIRE contents of `google_apps_script.js` from this project
5. Paste into the Google Apps Script editor
6. Click Save (disk icon or Ctrl+S)

### Step 2: Setup Headers (One-Time)

1. In the Google Apps Script editor, find the function dropdown (top toolbar)
2. Select `setupHeaders` from the dropdown
3. Click the Run button (▶️ play icon)
4. Authorize the script if prompted
5. This will create proper column headers in your Google Sheet

**Note**: Only run `setupHeaders` once! It will create the header row with all 32 column names.

### Step 3: Redeploy the Script

1. Click **Deploy** button (top right)
2. Select **Manage deployments**
3. Find the deployment ending in `...MXdZzhShd-g`
4. Click the pencil/edit icon
5. Under "Version", select **New version**
6. Add description: "Team members in separate columns + sequential IDs"
7. Click **Deploy**
8. Click **Done**

### Step 4: Test the New Features

1. Server is already running at http://127.0.0.1:5002
2. Submit a new patent application with team members
3. Check the application ID - should be `UIC-PAT-1` (or next sequential number)
4. Check Google Sheets - team members should appear in separate columns

## Expected Results

### Application ID Format
```
First submission:  UIC-PAT-1
Second submission: UIC-PAT-2
Third submission:  UIC-PAT-3
...and so on
```

### Google Sheets Example
If you submit an application with 2 team members:

| Application ID | ... | Member 1 Name | Member 1 Role | Member 1 Dept | Member 1 Email | Member 2 Name | Member 2 Role | Member 2 Dept | Member 2 Email | Member 3 Name | ... |
|----------------|-----|---------------|---------------|---------------|----------------|---------------|---------------|---------------|----------------|---------------|-----|
| UIC-PAT-1 | ... | John Doe | Co-inventor | CS | john@example.com | Jane Smith | Researcher | Engineering | jane@example.com | (empty) | ... |

## Important Notes

### Sequential IDs
- The system looks at the last application ID in the database
- Extracts the number and adds 1
- If database is empty, starts from 1
- **Warning**: If you delete records from the database, the numbering will continue from the last number, not reset

### Team Members
- System supports up to 5 team members
- Each member gets 4 columns (Name, Role, Department, Email)
- If fewer than 5 members, remaining columns will be empty
- If more than 5 members are added, only first 5 will be saved to Google Sheets

### Existing Data
- Old records with format `UIC-PAT-20260115-ABC123` will remain unchanged
- New submissions will use the new format `UIC-PAT-1`, `UIC-PAT-2`, etc.
- Old Google Sheets rows will have team members in one column
- New rows will have team members in separate columns

## Troubleshooting

### Issue: Application IDs still showing old format
**Solution**: 
- Make sure you restarted the Flask server
- Check server logs for errors
- The server should be running the updated code

### Issue: Team members not appearing in separate columns
**Solution**:
- Verify you updated the Google Apps Script
- Make sure you redeployed with a NEW version
- Run the `setupHeaders` function to create proper column headers
- Check Apps Script execution logs for errors

### Issue: Sequential numbering seems wrong
**Solution**:
- The system continues from the last number in the database
- Check your database: `SELECT application_id FROM applications ORDER BY id DESC LIMIT 1`
- If you want to reset numbering, you'd need to clear the database

## Testing Checklist

- [ ] Server restarted and running on port 5002
- [ ] Google Apps Script updated with new code
- [ ] `setupHeaders` function executed (one time)
- [ ] Google Apps Script redeployed with new version
- [ ] Test submission shows sequential ID (e.g., UIC-PAT-1)
- [ ] Google Sheets shows team members in separate columns
- [ ] All team member details (name, role, department, email) appear correctly

## Files Updated

1. ✅ `backend/app.py` - Sequential IDs + separate team member columns in payload
2. ✅ `google_apps_script.js` - Updated to handle separate team member columns
3. ✅ Server restarted with new code

Everything is ready! Just update your Google Apps Script and test.
