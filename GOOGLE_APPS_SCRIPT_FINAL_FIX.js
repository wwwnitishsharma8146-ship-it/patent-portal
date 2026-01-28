// UIC Patent Portal - Google Apps Script (FINAL FIX)
// Copy this ENTIRE code into your Google Apps Script editor and deploy it

function doPost(e) {
  try {
    // Log the incoming request for debugging
    console.log('Received POST request:', e.postData.contents);
    
    // Get the active spreadsheet (the one this script is attached to)
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = spreadsheet.getActiveSheet();
    
    // Parse the incoming JSON data
    const data = JSON.parse(e.postData.contents);
    
    // Initialize all member variables with empty strings to avoid null errors
    let member1Name = '', member1Role = '', member1Department = '', member1Email = '';
    let member2Name = '', member2Role = '', member2Department = '', member2Email = '';
    let member3Name = '', member3Role = '', member3Department = '', member3Email = '';
    let member4Name = '', member4Role = '', member4Department = '', member4Email = '';
    let member5Name = '', member5Role = '', member5Department = '', member5Email = '';
    
    // Handle different data formats safely
    try {
      // Check if data has individual member fields (backend format)
      if (data.member1Name !== undefined) {
        member1Name = data.member1Name || '';
        member1Role = data.member1Role || '';
        member1Department = data.member1Department || '';
        member1Email = data.member1Email || '';
        member2Name = data.member2Name || '';
        member2Role = data.member2Role || '';
        member2Department = data.member2Department || '';
        member2Email = data.member2Email || '';
        member3Name = data.member3Name || '';
        member3Role = data.member3Role || '';
        member3Department = data.member3Department || '';
        member3Email = data.member3Email || '';
        member4Name = data.member4Name || '';
        member4Role = data.member4Role || '';
        member4Department = data.member4Department || '';
        member4Email = data.member4Email || '';
        member5Name = data.member5Name || '';
        member5Role = data.member5Role || '';
        member5Department = data.member5Department || '';
        member5Email = data.member5Email || '';
      }
      // Check if data has teamMembers array (frontend format)
      else if (data.teamMembers && Array.isArray(data.teamMembers)) {
        const members = data.teamMembers;
        if (members.length > 0 && members[0]) {
          member1Name = members[0].name || '';
          member1Role = members[0].role || '';
          member1Department = members[0].department || '';
          member1Email = members[0].email || '';
        }
        if (members.length > 1 && members[1]) {
          member2Name = members[1].name || '';
          member2Role = members[1].role || '';
          member2Department = members[1].department || '';
          member2Email = members[1].email || '';
        }
        if (members.length > 2 && members[2]) {
          member3Name = members[2].name || '';
          member3Role = members[2].role || '';
          member3Department = members[2].department || '';
          member3Email = members[2].email || '';
        }
        if (members.length > 3 && members[3]) {
          member4Name = members[3].name || '';
          member4Role = members[3].role || '';
          member4Department = members[3].department || '';
          member4Email = members[3].email || '';
        }
        if (members.length > 4 && members[4]) {
          member5Name = members[4].name || '';
          member5Role = members[4].role || '';
          member5Department = members[4].department || '';
          member5Email = members[4].email || '';
        }
      }
    } catch (memberError) {
      console.log('Error processing team members:', memberError);
      // Continue with empty member fields
    }
    
    // Safely extract all other fields with null checks
    const applicationId = data.applicationId || data.application_id || '';
    const fullName = data.fullName || data.name || '';
    const email = data.email || '';
    const department = data.department || '';
    const branch = data.branch || '';
    const applicantType = data.applicantType || data.applicant_type || '';
    const contactNo = data.contactNo || data.contact || '';
    const patentTitle = data.patentTitle || data.patent_title || '';
    const patentType = data.patentType || data.patent_type || '';
    const description = data.description || '';
    const novelty = data.novelty || '';
    
    // Prepare the row data with all safety checks
    const rowData = [
      applicationId,                              // A: Application ID
      new Date().toLocaleString('en-US'),         // B: Submission Date
      fullName,                                   // C: Full Name
      email,                                      // D: Email
      department,                                 // E: Department
      branch,                                     // F: Branch
      applicantType,                              // G: Applicant Type
      contactNo,                                  // H: Contact Number
      patentTitle,                                // I: Patent Title
      patentType,                                 // J: Patent Type
      description,                                // K: Description
      novelty,                                    // L: Novelty
      
      // Team Member 1 (M-P)
      member1Name,                                // M: Member 1 Name
      member1Role,                                // N: Member 1 Role
      member1Department,                          // O: Member 1 Department
      member1Email,                               // P: Member 1 Email
      
      // Team Member 2 (Q-T)
      member2Name,                                // Q: Member 2 Name
      member2Role,                                // R: Member 2 Role
      member2Department,                          // S: Member 2 Department
      member2Email,                               // T: Member 2 Email
      
      // Team Member 3 (U-X)
      member3Name,                                // U: Member 3 Name
      member3Role,                                // V: Member 3 Role
      member3Department,                          // W: Member 3 Department
      member3Email,                               // X: Member 3 Email
      
      // Team Member 4 (Y-AB)
      member4Name,                                // Y: Member 4 Name
      member4Role,                                // Z: Member 4 Role
      member4Department,                          // AA: Member 4 Department
      member4Email,                               // AB: Member 4 Email
      
      // Team Member 5 (AC-AF)
      member5Name,                                // AC: Member 5 Name
      member5Role,                                // AD: Member 5 Role
      member5Department,                          // AE: Member 5 Department
      member5Email                                // AF: Member 5 Email
    ];
    
    // Add the row to the sheet
    sheet.appendRow(rowData);
    
    // Log success
    console.log('Successfully added row for application:', applicationId);
    
    // Return success response
    return ContentService
      .createTextOutput(JSON.stringify({
        success: true,
        message: 'Patent application added to Google Sheet successfully',
        applicationId: applicationId,
        timestamp: new Date().toISOString()
      }))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    // Log the error with more details
    console.error('Error in doPost:', error);
    console.error('Error stack:', error.stack);
    console.error('Received data:', e.postData ? e.postData.contents : 'No data');
    
    // Return error response
    return ContentService
      .createTextOutput(JSON.stringify({
        success: false,
        error: error.toString(),
        message: 'Failed to add data to Google Sheet',
        details: error.stack
      }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  // Handle GET requests (for testing)
  return ContentService
    .createTextOutput(JSON.stringify({
      success: true,
      message: 'UIC Patent Portal Google Apps Script is running',
      timestamp: new Date().toISOString(),
      version: '4.0 - Final fix with comprehensive error handling'
    }))
    .setMimeType(ContentService.MimeType.JSON);
}

// Function to setup headers (run this once to create proper column headers)
function setupHeaders() {
  try {
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = spreadsheet.getActiveSheet();
    
    // Check if headers already exist
    if (sheet.getLastRow() === 0) {
      const headers = [
        'Application ID',           // A
        'Submission Date',          // B
        'Full Name',               // C
        'Email',                   // D
        'Department',              // E
        'Branch',                  // F
        'Applicant Type',          // G
        'Contact Number',          // H
        'Patent Title',            // I
        'Patent Type',             // J
        'Description',             // K
        'Novelty',                 // L
        'Member 1 Name',           // M
        'Member 1 Role',           // N
        'Member 1 Department',     // O
        'Member 1 Email',          // P
        'Member 2 Name',           // Q
        'Member 2 Role',           // R
        'Member 2 Department',     // S
        'Member 2 Email',          // T
        'Member 3 Name',           // U
        'Member 3 Role',           // V
        'Member 3 Department',     // W
        'Member 3 Email',          // X
        'Member 4 Name',           // Y
        'Member 4 Role',           // Z
        'Member 4 Department',     // AA
        'Member 4 Email',          // AB
        'Member 5 Name',           // AC
        'Member 5 Role',           // AD
        'Member 5 Department',     // AE
        'Member 5 Email'           // AF
      ];
      
      sheet.appendRow(headers);
      
      // Format header row
      const headerRange = sheet.getRange(1, 1, 1, headers.length);
      headerRange.setFontWeight('bold');
      headerRange.setBackground('#4285f4');
      headerRange.setFontColor('#ffffff');
      
      console.log('Headers created successfully');
      return 'Headers created successfully';
    } else {
      console.log('Headers already exist');
      return 'Headers already exist';
    }
  } catch (error) {
    console.error('Error setting up headers:', error);
    return 'Error setting up headers: ' + error.toString();
  }
}

// Test function to verify the script works
function testScript() {
  try {
    const testData = {
      applicationId: 'UIC-PAT-TEST-FINAL',
      fullName: 'Test User Final Fix',
      email: 'testfinal@example.com',
      department: 'Computer Science',
      branch: 'Software Engineering',
      applicantType: 'Student',
      contactNo: '1234567890',
      patentTitle: 'Test Patent Final Fix',
      patentType: 'Utility',
      description: 'Test description final',
      novelty: 'Test novelty final',
      member1Name: 'Aman Kumar',
      member1Role: 'Co-inventor',
      member1Department: 'MCA',
      member1Email: 'aman@example.com',
      member2Name: 'Rohan Singh',
      member2Role: 'Researcher',
      member2Department: 'Computer Science',
      member2Email: 'rohan@example.com',
      member3Name: '',
      member3Role: '',
      member3Department: '',
      member3Email: '',
      member4Name: '',
      member4Role: '',
      member4Department: '',
      member4Email: '',
      member5Name: '',
      member5Role: '',
      member5Department: '',
      member5Email: ''
    };
    
    console.log('Testing with final fix data:', testData);
    
    // Simulate a POST request
    const mockEvent = {
      postData: {
        contents: JSON.stringify(testData)
      }
    };
    
    const result = doPost(mockEvent);
    const resultContent = result.getContent();
    console.log('Test result:', resultContent);
    
    // Parse and display result
    const resultObj = JSON.parse(resultContent);
    if (resultObj.success) {
      console.log('✅ TEST PASSED - Data added to sheet successfully!');
      console.log('Application ID:', resultObj.applicationId);
      return resultObj;
    } else {
      console.log('❌ TEST FAILED:', resultObj.error);
      return resultObj;
    }
    
  } catch (error) {
    console.error('❌ Test error:', error.toString());
    return { success: false, error: error.toString() };
  }
}