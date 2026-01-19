from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
import sqlite3
import os
import uuid
import json
from datetime import datetime
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib
import requests
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

app = Flask(__name__)

# Configure CORS to properly handle credentials
CORS(app, 
     supports_credentials=True,
     origins=["http://localhost:5002", "http://127.0.0.1:5002"],
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "OPTIONS"])

app.secret_key = 'your-secret-key-change-this-in-production'

# Session configuration
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

DATABASE = "database.db"
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'zip'}

# ========== GOOGLE DRIVE CONFIGURATION ==========
GOOGLE_DRIVE_FOLDER_ID = 'YOUR_GOOGLE_DRIVE_FOLDER_ID_HERE'  # Replace with your folder ID
CREDENTIALS_FILE = 'service_account_key.json'  # Place this file in your app directory
SCOPES = ['https://script.google.com/macros/s/AKfycbyZ2RW7XcUUXMORJXI4LlETTGoQkoCoPAWGEXaLms8OqenA2hwcurYY9R6jdBqQgblx6A/exec']

# ========== GOOGLE SHEETS CONFIGURATION ==========
ENABLE_GOOGLE_SHEETS_SYNC = True
APPS_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbw5wDVBsJZ6LiUM44BBCey_W0fn4ftO66jLbSc3vvPSCY7BF1gn8jv7X4ZXTLyFfRYp/exec'

# ========== GOOGLE DRIVE FILE UPLOAD CONFIGURATION ==========
ENABLE_GOOGLE_DRIVE_UPLOAD = True
GOOGLE_DRIVE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbzFr7rS0xXEiHeFHm6homLqwAccwokjRgsAm3480CppLvdEIYA6sCju5E1I0XD_J4s/exec'

# ========== GOOGLE DRIVE FUNCTIONS ==========
def upload_file_to_google_drive(file_path, application_id, original_filename):
    """Upload file to Google Drive using Apps Script"""
    if not ENABLE_GOOGLE_DRIVE_UPLOAD:
        print("⚠️  Google Drive upload is disabled")
        return None
    
    try:
        import base64
        import mimetypes
        
        # Detect MIME type based on file extension
        mime_type, _ = mimetypes.guess_type(original_filename)
        if not mime_type:
            # Default to PDF if can't detect
            mime_type = 'application/pdf'
        
        print(f"📄 File type detected: {mime_type}")
        
        # Read file and encode to base64
        with open(file_path, 'rb') as f:
            file_content = f.read()
            file_base64 = base64.b64encode(file_content).decode('utf-8')
        
        # Prepare payload for Google Apps Script
        payload = {
            'fileName': f"{application_id}_{original_filename}",
            'fileData': file_base64,
            'mimeType': mime_type,
            'applicationId': application_id
        }
        
        print(f"📤 Uploading {original_filename} ({mime_type}) to Google Drive...")
        print(f"   File size: {len(file_content)} bytes")
        
        # Send to Google Apps Script
        response = requests.post(GOOGLE_DRIVE_SCRIPT_URL, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ File uploaded to Google Drive: {original_filename}")
                print(f"   Drive URL: {result.get('fileUrl')}")
                return result.get('fileUrl')
            else:
                print(f"❌ Google Drive upload failed: {result.get('error', 'Unknown error')}")
                return None
        else:
            print(f"❌ Google Drive HTTP error: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"❌ Google Drive upload error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
def get_drive_service():
    """Authenticate and return Google Drive service"""
    try:
        if not os.path.exists(CREDENTIALS_FILE):
            print(f"⚠️  {CREDENTIALS_FILE} not found. Google Drive disabled.")
            return None
        
        credentials = service_account.Credentials.from_service_account_file(
            CREDENTIALS_FILE, scopes=SCOPES)
        
        service = build('drive', 'v3', credentials=credentials)
        print("✅ Google Drive authenticated")
        return service
    except Exception as e:
        print(f"⚠️  Google Drive auth error: {str(e)}")
        return None

def get_or_create_folder(service, parent_folder_id, folder_name):
    """Get existing folder or create new one"""
    try:
        query = f"name='{folder_name}' and '{parent_folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
        results = service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)',
            pageSize=1
        ).execute()
        
        items = results.get('files', [])
        
        if items:
            print(f"✅ Found folder: {folder_name}")
            return items[0]['id']
        else:
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [parent_folder_id]
            }
            
            folder = service.files().create(
                body=file_metadata,
                fields='id'
            ).execute()
            
            print(f"✅ Created folder: {folder_name}")
            return folder.get('id')
    
    except Exception as e:
        print(f"⚠️  Folder error: {str(e)}")
        return parent_folder_id

def upload_to_google_drive(file_path, application_id, filename):
    """Upload PDF file to Google Drive and store metadata"""
    try:
        service = get_drive_service()
        if not service:
            return {
                'success': False,
                'file_id': None,
                'file_url': None,
                'error': 'Google Drive service unavailable'
            }
        
        # Create folder structure: PatentApplications > Application ID
        parent_folder = get_or_create_folder(service, GOOGLE_DRIVE_FOLDER_ID, 'PatentApplications')
        app_folder = get_or_create_folder(service, parent_folder, application_id)
        
        # Prepare file metadata for Google Drive
        file_metadata = {
            'name': filename,
            'parents': [app_folder]
        }
        
        # Upload file with resume capability
        media = MediaFileUpload(file_path, resumable=True)
        
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink, name'
        ).execute()
        
        file_id = file.get('id')
        file_url = file.get('webViewLink')
        
        print(f"📤 {filename} uploaded successfully")
        print(f"   File ID: {file_id}")
        print(f"   File URL: {file_url}")
        
        return {
            'success': True,
            'file_id': file_id,
            'file_url': file_url,
            'error': None
        }
    
    except HttpError as error:
        error_msg = f"Drive API error: {error}"
        print(f"⚠️  {error_msg}")
        return {
            'success': False,
            'file_id': None,
            'file_url': None,
            'error': error_msg
        }
    except Exception as e:
        error_msg = f"Upload error: {str(e)}"
        print(f"⚠️  {error_msg}")
        return {
            'success': False,
            'file_id': None,
            'file_url': None,
            'error': error_msg
        }

# ========== GOOGLE SHEETS FUNCTION ==========
def send_to_google_sheet_via_apps_script(application_data, team_members=None):
    """Send data to Google Sheet using Apps Script with team members in separate columns"""
    if not ENABLE_GOOGLE_SHEETS_SYNC:
        return True
    
    if 'YOUR_APPS_SCRIPT_URL_HERE' in APPS_SCRIPT_URL:
        print("⚠️  Apps Script URL not configured")
        return False
    
    try:
        payload = {
            'applicationId': application_data.get('application_id', ''),
            'fullName': application_data.get('name', ''),
            'email': application_data.get('email', ''),
            'department': application_data.get('department', ''),
            'branch': application_data.get('branch', ''),
            'applicantType': application_data.get('applicant_type', ''),
            'contactNo': application_data.get('contact', ''),
            'patentTitle': application_data.get('patent_title', ''),
            'patentType': application_data.get('patent_type', ''),
        }
        
        # Add team members in separate columns (up to 5 members)
        print(f"📋 Team members data: {team_members}")
        if team_members and isinstance(team_members, list):
            print(f"   Found {len(team_members)} team members")
            for i, member in enumerate(team_members[:5], 1):  # Limit to 5 members
                payload[f'member{i}Name'] = member.get('name', '')
                payload[f'member{i}Role'] = member.get('role', '')
                payload[f'member{i}Department'] = member.get('department', '')
                payload[f'member{i}Email'] = member.get('email', '')
                print(f"   Member {i}: {member.get('name', 'N/A')} - {member.get('role', 'N/A')}")
        else:
            print(f"   No team members found")
        
        # Fill empty columns for remaining member slots
        num_members = len(team_members) if team_members else 0
        for i in range(num_members + 1, 6):  # Fill up to 5 member slots
            payload[f'member{i}Name'] = ''
            payload[f'member{i}Role'] = ''
            payload[f'member{i}Department'] = ''
            payload[f'member{i}Email'] = ''
        
        print(f"📤 Sending payload to Google Sheets with {num_members} team members")
        print(f"   Payload keys: {list(payload.keys())}")
        print(f"   Member fields in payload:")
        for i in range(1, 6):
            if payload.get(f'member{i}Name'):
                print(f"      member{i}Name: {payload.get(f'member{i}Name')}")
                print(f"      member{i}Role: {payload.get(f'member{i}Role')}")
                print(f"      member{i}Department: {payload.get(f'member{i}Department')}")
                print(f"      member{i}Email: {payload.get(f'member{i}Email')}")
        
        response = requests.post(APPS_SCRIPT_URL, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ Data sent to Google Sheet")
                return True
        
        print(f"⚠️  Sheet sync failed")
        return False
            
    except Exception as e:
        print(f"⚠️  Error: {str(e)}")
        return False

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ========== DATABASE ==========
def get_db():
    conn = sqlite3.connect(DATABASE, timeout=20.0)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA journal_mode=WAL;')
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT UNIQUE,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        user_type TEXT NOT NULL,
        department TEXT,
        branch TEXT,
        contact TEXT,
        registration_date TEXT,
        is_active INTEGER DEFAULT 1
    )
    """)

    try:
        cur.execute("DROP TABLE IF EXISTS applications")
    except:
        pass
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        application_id TEXT UNIQUE,
        user_id TEXT,
        name TEXT,
        email TEXT,
        department TEXT,
        branch TEXT,
        applicant_type TEXT,
        contact TEXT,
        patent_title TEXT,
        patent_type TEXT,
        description TEXT,
        novelty TEXT,
        submission_date TEXT,
        status TEXT DEFAULT 'submitted',
        filed_date TEXT,
        published_date TEXT,
        granted_date TEXT,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS team_members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        application_id TEXT,
        member_name TEXT,
        member_role TEXT,
        member_department TEXT,
        member_email TEXT
    )
    """)

    try:
        cur.execute("DROP TABLE IF EXISTS files")
    except:
        pass
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        application_id TEXT,
        file_name TEXT,
        file_path TEXT,
        original_filename TEXT,
        google_drive_file_id TEXT,
        google_drive_url TEXT,
        upload_status TEXT DEFAULT 'local'
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ========== AUTHENTICATION ==========
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json or 'XMLHttpRequest' in request.headers.get('X-Requested-With', ''):
                return jsonify({
                    "success": False,
                    "message": "Authentication required",
                    "redirect": "/login"
                }), 401
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    if 'user_id' not in session:
        return None
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = ?", (session['user_id'],))
    user = cur.fetchone()
    conn.close()
    return user

# ========== AUTH ROUTES ==========
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/login", methods=["POST"])
def login_post():
    try:
        data = request.form
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            flash('Please fill all fields', 'error')
            return redirect(url_for('login'))
        
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ? AND is_active = 1", (email,))
        user = cur.fetchone()
        conn.close()
        
        if user and check_password_hash(user[4], password):
            session['user_id'] = user[1]
            session['user_name'] = user[2]
            session['user_type'] = user[5]
            flash(f'Welcome back, {user[2]}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('login'))
            
    except Exception as e:
        flash(f'Login error: {str(e)}', 'error')
        return redirect(url_for('login'))

@app.route("/signup", methods=["POST"])
def signup_post():
    try:
        data = request.form
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        user_type = data.get('user_type')
        department = data.get('department')
        branch = data.get('branch')
        contact = data.get('contact')
        
        if not all([name, email, password, confirm_password, user_type]):
            flash('Please fill all required fields', 'error')
            return redirect(url_for('signup'))
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('signup'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
            return redirect(url_for('signup'))
        
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cur.fetchone():
            flash('Email already registered', 'error')
            conn.close()
            return redirect(url_for('signup'))
        
        user_id = f"UIC-USER-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        password_hash = generate_password_hash(password)
        
        cur.execute("""
            INSERT INTO users (
                user_id, name, email, password_hash, user_type,
                department, branch, contact, registration_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id, name, email, password_hash, user_type,
            department, branch, contact, datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
        
    except Exception as e:
        flash(f'Registration error: {str(e)}', 'error')
        return redirect(url_for('signup'))

@app.route("/logout")
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

# ========== MAIN ROUTES ==========
@app.route("/")
def home():
    user = get_current_user() if 'user_id' in session else None
    if not user:
        return redirect(url_for('login'))
    return render_template("index.html", user=user)

# ========== SUBMIT PATENT WITH GOOGLE DRIVE ==========
@app.route("/submit", methods=["POST"])
def submit_patent():
    try:
        print(f"📝 Submit request from {request.remote_addr}")
        
        user = get_current_user() if 'user_id' in session else None
        
        if user:
            print(f"✅ Logged in user: {user[2]} ({user[1]})")
        else:
            print("📝 Guest submission")

        data = request.form
        files = request.files.getlist("files")

        required_fields = ['patentTitle', 'patentType']
        missing_fields = []
        
        for field in required_fields:
            if not data.get(field) or not data.get(field).strip():
                missing_fields.append(field)
        
        if missing_fields:
            return jsonify({
                "success": False,
                "message": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400

        # Generate sequential application ID
        conn = get_db()
        cur = conn.cursor()
        
        # Get the highest application number
        cur.execute("SELECT application_id FROM applications ORDER BY id DESC LIMIT 1")
        last_app = cur.fetchone()
        
        if last_app and last_app[0]:
            # Extract number from last application ID (e.g., "UIC-PAT-5" -> 5)
            try:
                last_num = int(last_app[0].split('-')[-1])
                next_num = last_num + 1
            except:
                next_num = 1
        else:
            next_num = 1
        
        application_id = f"UIC-PAT-{next_num}"

        if user:
            application_data = {
                'application_id': application_id,
                'user_id': user[1],
                'name': data.get("name") or user[2],
                'email': data.get("email") or user[3],
                'department': data.get("department") or user[6],
                'branch': data.get("branch") or user[7],
                'applicant_type': data.get("applicantType"),
                'contact': data.get("contact") or user[8],
                'patent_title': data.get("patentTitle"),
                'patent_type': data.get("patentType"),
                'description': data.get("description"),
                'novelty': data.get("novelty"),
                'submission_date': datetime.now().isoformat()
            }
        else:
            application_data = {
                'application_id': application_id,
                'user_id': 'GUEST',
                'name': data.get("name") or "Guest User",
                'email': data.get("email") or "guest@example.com",
                'department': data.get("department") or "Not Specified",
                'branch': data.get("branch") or "Not Specified",
                'applicant_type': data.get("applicantType") or "student",
                'contact': data.get("contact") or "Not Provided",
                'patent_title': data.get("patentTitle"),
                'patent_type': data.get("patentType"),
                'description': data.get("description"),
                'novelty': data.get("novelty"),
                'submission_date': datetime.now().isoformat()
            }

        # Save application
        cur.execute("""
            INSERT INTO applications (
                application_id, user_id, name, email, department, branch,
                applicant_type, contact, patent_title, patent_type,
                description, novelty, submission_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            application_data['application_id'],
            application_data['user_id'],
            application_data['name'],
            application_data['email'],
            application_data['department'],
            application_data['branch'],
            application_data['applicant_type'],
            application_data['contact'],
            application_data['patent_title'],
            application_data['patent_type'],
            application_data['description'],
            application_data['novelty'],
            application_data['submission_date']
        ))

        # Save team members
        team_members = []
        members_json = data.get("members")
        if members_json:
            try:
                members = json.loads(members_json)
                for member in members:
                    cur.execute("""
                        INSERT INTO team_members (
                            application_id, member_name, member_role,
                            member_department, member_email
                        ) VALUES (?, ?, ?, ?, ?)
                    """, (
                        application_id,
                        member.get("name", ""),
                        member.get("role", ""),
                        member.get("department", ""),
                        member.get("email", "")
                    ))
                    team_members.append(member)
            except:
                pass

        # ========== UPLOAD FILES TO GOOGLE DRIVE ==========
        # ========== UPLOAD FILES TO GOOGLE DRIVE ==========
        uploaded_files_info = []
        for file in files:
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                local_filename = f"{application_id}_{timestamp}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], local_filename)
                file.save(filepath)

                file_info = {
                    'original_filename': file.filename,
                    'local_filename': local_filename,
                    'local_path': filepath,
                    'google_drive_file_id': None,
                    'google_drive_url': None,
                    'upload_status': 'local'
                }

                # Upload to Google Drive using Apps Script
                if ENABLE_GOOGLE_DRIVE_UPLOAD:
                    try:
                        drive_url = upload_file_to_google_drive(filepath, application_id, file.filename)
                        
                        if drive_url:
                            file_info['google_drive_url'] = drive_url
                            file_info['upload_status'] = 'google_drive'
                            print(f"✅ {file.filename} uploaded to Google Drive successfully")
                        else:
                            print(f"⚠️  Google Drive upload failed for {file.filename}")
                            print("   File saved locally as backup")
                    except Exception as e:
                        print(f"⚠️  Upload error: {str(e)}")
                        print("   File saved locally as backup")
                else:
                    print(f"📁 {file.filename} saved locally (Google Drive upload disabled)")

                # Save to database
                cur.execute("""
                    INSERT INTO files (
                        application_id, file_name, file_path, original_filename,
                        google_drive_file_id, google_drive_url, upload_status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    application_id,
                    file_info['local_filename'],
                    file_info['local_path'],
                    file_info['original_filename'],
                    file_info['google_drive_file_id'],
                    file_info['google_drive_url'],
                    file_info['upload_status']
                ))

                uploaded_files_info.append(file_info)

        conn.commit()
        conn.close()

        # ========== GOOGLE SHEETS SYNC (AFTER PDF UPLOAD) ==========
        google_sheet_success = False
        try:
            if ENABLE_GOOGLE_SHEETS_SYNC and 'PASTE_YOUR_NEW_WEB_APP_URL_HERE' not in APPS_SCRIPT_URL:
                google_sheet_success = send_to_google_sheet_via_apps_script(application_data, team_members)
        except Exception as e:
            print(f"Sheet sync failed: {str(e)}")
            google_sheet_success = False

        return jsonify({
            "success": True,
            "applicationId": application_id,
            "message": "Patent application submitted successfully!",
            "googleSheetSync": google_sheet_success,
            "filesUploaded": len(uploaded_files_info),
            "googleDriveFiles": [f for f in uploaded_files_info if f['upload_status'] == 'google_drive'],
            "localFiles": [f for f in uploaded_files_info if f['upload_status'] == 'local']
        })

    except Exception as e:
        print(f"Error submitting patent: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"Error submitting application: {str(e)}"
        }), 500

# ========== STATS ==========
@app.route("/stats")
def stats():
    conn = get_db()
    cur = conn.cursor()

    submitted = cur.execute("SELECT COUNT(*) FROM applications").fetchone()[0]
    filed = cur.execute("SELECT COUNT(*) FROM applications WHERE status = 'filed'").fetchone()[0]
    published = cur.execute("SELECT COUNT(*) FROM applications WHERE status = 'published'").fetchone()[0]
    granted = cur.execute("SELECT COUNT(*) FROM applications WHERE status = 'granted'").fetchone()[0]

    conn.close()

    return jsonify({
        "success": True,
        "stats": {
            "submitted": submitted,
            "filed": filed,
            "published": published,
            "granted": granted
        }
    })

# ========== UPDATE STATUS ==========
@app.route("/update-status", methods=["POST"])
@login_required
def update_patent_status():
    try:
        data = request.json
        application_id = data.get('application_id')
        new_status = data.get('status')
        
        if not application_id or not new_status:
            return jsonify({
                "success": False,
                "message": "Missing application_id or status"
            }), 400
        
        if new_status not in ['submitted', 'filed', 'published', 'granted']:
            return jsonify({
                "success": False,
                "message": "Invalid status"
            }), 400
        
        conn = get_db()
        cur = conn.cursor()
        
        date_field = None
        if new_status == 'filed':
            date_field = 'filed_date'
        elif new_status == 'published':
            date_field = 'published_date'
        elif new_status == 'granted':
            date_field = 'granted_date'
        
        if date_field:
            cur.execute(f"""
                UPDATE applications 
                SET status = ?, {date_field} = ? 
                WHERE application_id = ?
            """, (new_status, datetime.now().isoformat(), application_id))
        else:
            cur.execute("""
                UPDATE applications 
                SET status = ? 
                WHERE application_id = ?
            """, (new_status, application_id))
        
        if cur.rowcount == 0:
            conn.close()
            return jsonify({
                "success": False,
                "message": "Application not found"
            }), 404
        
        conn.commit()
        conn.close()
        
        return jsonify({
            "success": True,
            "message": f"Status updated to {new_status}",
            "application_id": application_id,
            "new_status": new_status
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error updating status: {str(e)}"
        }), 500

if __name__ == "__main__":
    app.run(debug=True)