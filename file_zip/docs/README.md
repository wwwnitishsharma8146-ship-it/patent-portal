# UIC Patent Portal - Chandigarh University

A comprehensive web application for patent application submission and management at Chandigarh University's University Innovation Cell (UIC).

## Features

- **User Authentication**: Secure login and registration system for students and faculty
- **Patent Application Form**: Complete form for submitting patent applications
- **Team Member Management**: Add multiple team members to patent applications
- **File Upload**: Support for multiple file uploads (PDF, DOC, DOCX, JPEG, PNG, ZIP)
- **Database Integration**: SQLite database for storing users, applications, team members, and files
- **Statistics Dashboard**: Real-time statistics of patent applications
- **Responsive Design**: Mobile-friendly interface
- **Form Validation**: Client-side and server-side validation
- **Session Management**: Secure session-based authentication
- **User Profiles**: Pre-filled forms with user information

## Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Python Flask
- **Database**: SQLite
- **File Handling**: Werkzeug secure file uploads
- **CORS**: Flask-CORS for cross-origin requests

## Setup Instructions

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation

1. **Install Dependencies**:
   ```bash
   cd backend
   pip3 install flask flask-cors
   ```

2. **Run the Application**:
   ```bash
   cd backend
   python3 app.py
   ```

3. **Access the Website**:
   Open your browser and go to: `http://localhost:5002`

4. **Create Account**:
   - Click "Sign up here" to create a new account
   - Fill in your details (name, email, password, user type, department, etc.)
   - Submit the registration form

5. **Login**:
   - Use your email and password to login
   - You'll be redirected to the patent application portal

## Database Schema

The application uses SQLite with the following tables:

### Users Table
- `id`: Primary key
- `user_id`: Unique user identifier
- `name`: User's full name
- `email`: User's email address (unique)
- `password_hash`: Hashed password
- `user_type`: Type of user (student/faculty/researcher/staff)
- `department`: User's department
- `branch`: Branch/Specialization
- `contact`: Contact number
- `registration_date`: Registration timestamp
- `is_active`: Account status (1=active, 0=inactive)

### Applications Table
- `id`: Primary key
- `application_id`: Unique application identifier
- `user_id`: Reference to user who submitted (Foreign Key)
- `name`: Applicant name
- `email`: Applicant email
- `department`: Department
- `branch`: Branch/Specialization
- `applicant_type`: Type of applicant (Faculty/Student/etc.)
- `contact`: Contact number
- `patent_title`: Title of the patent
- `patent_type`: Type of patent
- `description`: Detailed description
- `novelty`: Novelty/Innovation description
- `submission_date`: Submission timestamp

### Team Members Table
- `id`: Primary key
- `application_id`: Reference to application
- `member_name`: Team member name
- `member_role`: Role in project
- `member_department`: Department
- `member_email`: Email address

### Files Table
- `id`: Primary key
- `application_id`: Reference to application
- `file_name`: Original filename
- `file_path`: Server file path

## API Endpoints

### Authentication
- `GET /login`: Login page
- `POST /login`: Process login
- `GET /signup`: Registration page  
- `POST /signup`: Process registration
- `GET /logout`: Logout user

### Application
- `GET /`: Main application page (requires login)
- `POST /submit`: Submit patent application (requires login)
- `GET /stats`: Get application statistics

## File Upload

- **Supported formats**: PDF, DOC, DOCX, JPEG, PNG, ZIP
- **Maximum file size**: 16MB per file
- **Storage**: Files are stored in the `backend/uploads/` directory

## Features in Detail

### Form Validation
- Required field validation
- Email format validation
- Phone number format validation
- File type and size validation

### Auto-save Functionality
- Form data is automatically saved to localStorage
- Data is restored if the page is refreshed

### Progress Indicators
- File upload progress
- Form submission progress
- Loading overlays

### Toast Notifications
- Success/error messages
- Form validation feedback
- File upload status

## Directory Structure

```
├── backend/
│   ├── app.py              # Flask application
│   ├── database.db         # SQLite database
│   ├── templates/
│   │   └── index.html      # Main HTML template
│   ├── static/
│   │   └── images copy.png # University logo
│   └── uploads/            # Uploaded files directory
├── README.md               # This file
└── Chandigarh-University-CU-Logo-Vector.svg-.png
```

## Usage

### First Time Setup
1. **Create Account**:
   - Go to `http://localhost:5002`
   - Click "Sign up here"
   - Fill in your details:
     - Full Name
     - Email Address (use your university email)
     - Account Type (Student/Faculty/Researcher/Staff)
     - Department and Branch
     - Contact Number
     - Password (minimum 6 characters)
   - Submit registration

2. **Login**:
   - Use your email and password to login
   - You'll be redirected to the patent portal

### Submitting Patent Applications
1. **Fill the Application Form**:
   - Your personal details will be pre-filled from your profile
   - Enter patent information (title, type, description, novelty)
   - Add team members if applicable
   - Upload supporting documents

2. **Submit Application**:
   - Click "Submit Patent Application"
   - Receive unique application ID
   - Get confirmation message

3. **Track Statistics**:
   - View real-time statistics on the sidebar
   - See total applications, approved, and pending

### Account Management
- **Logout**: Click the logout icon in the header
- **Profile**: Your information is used to pre-fill application forms

## Development

To modify the application:

1. **Frontend changes**: Edit `backend/templates/index.html`
2. **Backend changes**: Edit `backend/app.py`
3. **Database changes**: Modify the database schema in `init_db()` function

## Security Features

- **Password Hashing**: Secure password storage using Werkzeug's password hashing
- **Session Management**: Flask sessions for user authentication
- **Login Required**: Protected routes require authentication
- **Secure filename handling**: File uploads use secure filename processing
- **File type validation**: Only allowed file types can be uploaded
- **CORS protection**: Cross-origin request protection
- **SQL injection prevention**: Parameterized queries prevent SQL injection
- **Input validation**: Both client-side and server-side validation

## Support

For technical support or questions:
- Email: uic@chandigarh.edu
- Phone: +91-987-654-3210
- Office: UIC Office, Block E, Chandigarh University

---

**Note**: This is a development server. For production deployment, use a proper WSGI server like Gunicorn or uWSGI.