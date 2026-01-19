// Google Apps Script for Uploading PDF Files to Google Drive
// This script receives base64 encoded files and saves them as actual PDFs

function doPost(e) {
  try {
    // Log incoming request
    Logger.log('Received file upload request');
    
    // Parse the incoming JSON data
    const data = JSON.parse(e.postData.contents);
    
    // Get file data
    const fileName = data.fileName;
    const fileData = data.fileData; // Base64 encoded file
    const mimeType = data.mimeType || 'application/pdf';
    const applicationId = data.applicationId;
    
    Logger.log('File name: ' + fileName);
    Logger.log('MIME type: ' + mimeType);
    Logger.log('Application ID: ' + applicationId);
    
    // Decode base64 file data to bytes
    const decodedData = Utilities.base64Decode(fileData);
    
    // Create blob with proper MIME type - THIS CREATES THE ACTUAL PDF
    const blob = Utilities.newBlob(decodedData, mimeType, fileName);
    
    Logger.log('Blob created with size: ' + blob.getBytes().length + ' bytes');
    
    // Get or create the folder for patent files
    const folderName = 'UIC Patent Files';
    let folder = getFolderByName(folderName);
    
    if (!folder) {
      // Create folder if it doesn't exist
      folder = DriveApp.createFolder(folderName);
      Logger.log('Created new folder: ' + folderName);
    } else {
      Logger.log('Using existing folder: ' + folderName);
    }
    
    // Upload the actual PDF file to the folder
    const file = folder.createFile(blob);
    
    Logger.log('File created in Drive with ID: ' + file.getId());
    
    // Make file accessible with link
    file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
    
    // Get file information
    const fileUrl = file.getUrl();
    const fileId = file.getId();
    const downloadUrl = 'https://drive.google.com/uc?export=download&id=' + fileId;
    
    Logger.log('File uploaded successfully');
    Logger.log('File URL: ' + fileUrl);
    Logger.log('Download URL: ' + downloadUrl);
    
    // Return success response with file information
    return ContentService
      .createTextOutput(JSON.stringify({
        success: true,
        message: 'PDF file uploaded successfully to Google Drive',
        fileId: fileId,
        fileUrl: fileUrl,
        downloadUrl: downloadUrl,
        fileName: fileName,
        applicationId: applicationId,
        fileSize: blob.getBytes().length,
        mimeType: mimeType
      }))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    Logger.log('ERROR: ' + error.toString());
    Logger.log('Stack trace: ' + error.stack);
    
    // Return detailed error response
    return ContentService
      .createTextOutput(JSON.stringify({
        success: false,
        error: error.toString(),
        message: 'Failed to upload file to Google Drive',
        stack: error.stack
      }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  // Handle GET requests (for testing)
  return ContentService
    .createTextOutput(JSON.stringify({
      success: true,
      message: 'UIC Patent Portal - Google Drive PDF Upload Service',
      status: 'Running',
      timestamp: new Date().toISOString(),
      info: 'This service receives base64 encoded files and saves them as PDFs in Google Drive'
    }))
    .setMimeType(ContentService.MimeType.JSON);
}

// Helper function to get folder by name
function getFolderByName(folderName) {
  const folders = DriveApp.getFoldersByName(folderName);
  if (folders.hasNext()) {
    return folders.next();
  }
  return null;
}

// Test function to verify the script works
function testUpload() {
  // Create a simple test PDF
  const testPdfContent = '%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\nxref\n0 2\ntrailer\n<<\n/Size 2\n/Root 1 0 R\n>>\nstartxref\n100\n%%EOF';
  const testBlob = Utilities.newBlob(testPdfContent, 'application/pdf', 'test_file.pdf');
  
  const folderName = 'UIC Patent Files';
  let folder = getFolderByName(folderName);
  
  if (!folder) {
    folder = DriveApp.createFolder(folderName);
  }
  
  const file = folder.createFile(testBlob);
  Logger.log('Test PDF created successfully');
  Logger.log('File URL: ' + file.getUrl());
  Logger.log('File ID: ' + file.getId());
  
  return file.getUrl();
}
