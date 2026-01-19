// UIC Patent Portal - Google Apps Script
// Copy this entire code into your Google Apps Script editor
// Updated to show team members in separate columns

function doPost(e) {
  try {
    // Log the incoming request for debugging
    console.log('Received POST request:', e.postData.contents);
    
    // Get the active spreadsheet (the one this script is attached to)
    const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = spreadsheet.getActiveSheet();
    
    // Parse the incoming JSON data
    const data = JSON.parse(e.postData.contents);
    
    // Prepare the row data with team members in separate columns
    const rowData = [
      data.applicationId || '',                    // A: Application ID
      new Date().toLocaleString('en-US'),         // B: Submission Date
      data.fullName || '',                        // C: Full Name
      data.email || '',                           // D: Email
      data.department || '',                      // E: Department
      data.branch || '',                          // F: Branch
      data.applicantType || '',                   // G: Applicant Type
      data.contactNo || '',                       // H: Contact Number
      data.patentTitle || '',                     // I: Patent Title
      data.patentType || '',                      // J: Patent Type
      
      // Team Member 1 (K-N)
      data.member1Name || '',                     // K: Member 1 Name
      data.member1Role || '',                     // L: Member 1 Role
      data.member1Department || '',               // M: Member 1 Department
      data.member1Email || '',                    // N: Member 1 Email
      
      // Team Member 2 (O-R)
      data.member2Name || '',                     // O: Member 2 Name
      data.member2Role || '',                     // P: Member 2 Role
      data.member2Department || '',               // Q: Member 2 Department
      data.member2Email || '',                    // R: Member 2 Email
      
      // Team Member 3 (S-V)
      data.member3Name || '',                     // S: Member 3 Name
      data.member3Role || '',                     // T: Member 3 Role
      data.member3Department || '',               // U: Member 3 Department
      data.member3Email || '',                    // V: Member 3 Email
      
      // Team Member 4 (W-Z)
      data.member4Name || '',                     // W: Member 4 Name
      data.member4Role || '',                     // X: Member 4 Role
      data.member4Department || '',               // Y: Member 4 Department
      data.member4Email || '',                    // Z: Member 4 Email
      
      // Team Member 5 (AA-AD)
      data.member5Name || '',                     // AA: Member 5 Name
      data.member5Role || '',                     // AB: Member 5 Role
      data.member5Department || '',               // AC: Member 5 Department
      data.member5Email || ''                     // AD: Member 5 Email
    ];
    
    // Add the row to the sheet
    sheet.appendRow(rowData);
    
    // Log success
    console.log('Successfully added row for application:', data.applicationId);
    
    // Return success response
    return ContentService
      .createTextOutput(JSON.stringify({
        success: true,
        message: 'Patent application added to Google Sheet successfully',
        applicationId: data.applicationId,
        timestamp: new Date().toISOString()
      }))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    // Log the error
    console.error('Error in doPost:', error);
    
    // Return error response
    return ContentService
      .createTextOutput(JSON.stringify({
        success: false,
        error: error.toString(),
        message: 'Failed to add data to Google Sheet'
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
      version: '2.0 - Team members in separate columns'
    }))
    .setMimeType(ContentService.MimeType.JSON);
}

// Function to setup headers (run this once to create proper column headers)
function setupHeaders() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = spreadsheet.getActiveSheet();
  
  // Check if headers already exist
  if (sheet.getLastRow() === 0) {
    const headers = [
      'Application ID',
      'Submission Date',
      'Full Name',
      'Email',
      'Department',
      'Branch',
      'Applicant Type',
      'Contact Number',
      'Patent Title',
      'Patent Type',
      'Member 1 Name',
      'Member 1 Role',
      'Member 1 Department',
      'Member 1 Email',
      'Member 2 Name',
      'Member 2 Role',
      'Member 2 Department',
      'Member 2 Email',
      'Member 3 Name',
      'Member 3 Role',
      'Member 3 Department',
      'Member 3 Email',
      'Member 4 Name',
      'Member 4 Role',
      'Member 4 Department',
      'Member 4 Email',
      'Member 5 Name',
      'Member 5 Role',
      'Member 5 Department',
      'Member 5 Email'
    ];
    
    sheet.appendRow(headers);
    
    // Format header row
    const headerRange = sheet.getRange(1, 1, 1, headers.length);
    headerRange.setFontWeight('bold');
    headerRange.setBackground('#4285f4');
    headerRange.setFontColor('#ffffff');
    
    console.log('Headers created successfully');
  } else {
    console.log('Headers already exist');
  }
}

// Test function to verify the script works
function testScript() {
  try {
    const testData = {
      applicationId: 'UIC-PAT-TEST',
      fullName: 'Test User',
      email: 'test@example.com',
      department: 'Computer Science',
      branch: 'Software Engineering',
      applicantType: 'Student',
      contactNo: '1234567890',
      patentTitle: 'Test Patent',
      patentType: 'Utility',
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
    
    console.log('Testing with data:', testData);
    
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
    } else {
      console.log('❌ TEST FAILED:', resultObj.error);
    }
    
    return resultObj;
  } catch (error) {
    console.error('❌ Test error:', error.toString());
    return { success: false, error: error.toString() };
  }
}