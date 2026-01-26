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
from flask_mail import Mail, Message
import secrets
import time

# Load environment variables from .env file
def load_env():
    """Load environment variables from .env file"""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

load_env()

app = Flask(__name__)

# Configure CORS to properly handle credentials
CORS(app, 
     supports_credentials=True,
     origins=["http://localhost:5002", "http://127.0.0.1:5002", "https://patent-portal-5.onrender.com"],
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "OPTIONS"])

app.secret_key = 'uic-patent-portal-production-key-2026-secure'

# Session configuration
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False

# Email configuration - Using free SMTP service
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', 'www.nitishsharma8146@gmail.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'your-app-password-here')
app.config['MAIL_DEFAULT_SENDER'] = 'UIC Patent Portal <uicpatentportal@gmail.com>'

# Initialize Flask-Mail
mail = Mail(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

DATABASE = "database.db"
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

# ========== GOOGLE DRIVE CONFIGURATION ==========
GOOGLE_DRIVE_FOLDER_ID = 'YOUR_GOOGLE_DRIVE_FOLDER_ID_HERE'  # Replace with your folder ID
CREDENTIALS_FILE = 'service_account_key.json'  # Place this file in your app directory
SCOPES = ['https://script.google.com/macros/s/AKfycbyZ2RW7XcUUXMORJXI4LlETTGoQkoCoPAWGEXaLms8OqenA2hwcurYY9R6jdBqQgblx6A/exec']

# ========  == GOOGLE SHEETS CONFIGURATION ==========
ENABLE_GOOGLE_SHEETS_SYNC = True  # Enabled for Google Sheets integration
APPS_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycby44PN4TqP2Q2Y9a-AtE-2jnntE6azhlJc_lyB5Zguco0FFA3n-KCDV37-MXdZzhShd-g/exec'

# ========== GOOGLE DRIVE FILE UPLOAD CONFIGURATION ==========
ENABLE_GOOGLE_DRIVE_UPLOAD = False  # Disabled for faster deployment
GOOGLE_DRIVE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbzFr7rS0xXEiHeFHm6homLqwAccwokjRgsAm3480CppLvdEIYA6sCju5E1I0XD_J4s/exec'

# ========== GOOGLE DRIVE FUNCTIONS (DISABLED FOR SPEED) ==========
def upload_file_to_google_drive(file_path, application_id, original_filename):
    """Upload file to Google Drive using Apps Script - DISABLED"""
    print("⚠️  Google Drive upload is disabled for faster deployment")
    return None

def get_drive_service():
    """Authenticate and return Google Drive service - DISABLED"""
    print("⚠️  Google Drive service is disabled for faster deployment")
    return None

def get_or_create_folder(service, parent_folder_id, folder_name):
    """Get existing folder or create new one - DISABLED"""
    print("⚠️  Google Drive folder creation is disabled")
    return parent_folder_id

def upload_to_google_drive(file_path, application_id, filename):
    """Upload PDF file to Google Drive and store metadata - DISABLED"""
    print("⚠️  Google Drive upload is disabled for faster deployment")
    return {
        'success': False,
        'file_id': None,
        'file_url': None,
        'error': 'Google Drive disabled for faster deployment'
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
    conn = sqlite3.connect(DATABASE, timeout=30.0)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA journal_mode=WAL;')
    conn.execute('PRAGMA synchronous=NORMAL;')
    conn.execute('PRAGMA cache_size=1000;')
    conn.execute('PRAGMA temp_store=memory;')
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

    cur.execute("""
    CREATE TABLE IF NOT EXISTS password_reset_tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        token TEXT UNIQUE,
        expires_at INTEGER,
        used INTEGER DEFAULT 0,
        created_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
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

# ========== PASSWORD RESET ROUTES ==========
def send_password_reset_email(user_email, user_name, reset_token):
    """Send password reset confirmation email"""
    try:
        confirm_url = url_for('confirm_reset', token=reset_token, _external=True)
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #e92020 0%, #bfdbe5 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .button {{ display: inline-block; background: #28a745; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold; margin: 20px 10px; }}
                .button.cancel {{ background: #6c757d; }}
                .footer {{ text-align: center; margin-top: 30px; font-size: 12px; color: #666; }}
                .warning {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .user-info {{ background: #e9ecef; padding: 15px; border-radius: 5px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔐 Password Reset Request</h1>
                    <p>UIC Patent Portal - Chandigarh University</p>
                </div>
                <div class="content">
                    <h2>Hello {user_name},</h2>
                    <p>We received a request to reset the password for your UIC Patent Portal account.</p>
                    
                    <div class="user-info">
                        <strong>Account Details:</strong><br>
                        Name: {user_name}<br>
                        Email: {user_email}
                    </div>
                    
                    <p><strong>⚠️ IMPORTANT: We need your confirmation before proceeding.</strong></p>
                    <p>Click the button below to confirm that you want to reset your password:</p>
                    
                    <div style="text-align: center;">
                        <a href="{confirm_url}" class="button">✅ Yes, Reset My Password</a>
                    </div>
                    
                    <div class="warning">
                        <strong>🛡️ Security Notice:</strong>
                        <ul>
                            <li>This confirmation link will expire in <strong>1 hour</strong></li>
                            <li>If you didn't request this reset, please ignore this email</li>
                            <li>Your password will NOT be changed until you confirm</li>
                            <li>Never share this link with anyone</li>
                        </ul>
                    </div>
                    
                    <p>If the button doesn't work, copy and paste this link into your browser:</p>
                    <p style="word-break: break-all; background: #e9ecef; padding: 10px; border-radius: 5px; font-family: monospace;">
                        {confirm_url}
                    </p>
                    
                    <p><strong>If you didn't request this password reset:</strong><br>
                    Simply ignore this email. Your password will remain unchanged and secure.</p>
                    
                    <p>Best regards,<br>
                    <strong>UIC Patent Portal Team</strong><br>
                    University Innovation Cell<br>
                    Chandigarh University</p>
                </div>
                <div class="footer">
                    <p>This is an automated security email. Please do not reply to this message.</p>
                    <p>© 2026 Chandigarh University - University Innovation Cell</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_body = f"""
        Password Reset Confirmation - UIC Patent Portal
        
        Hello {user_name},
        
        We received a request to reset the password for your UIC Patent Portal account.
        
        IMPORTANT: We need your confirmation before proceeding.
        
        Click this link to confirm that you want to reset your password:
        {confirm_url}
        
        SECURITY NOTICE:
        - This confirmation link will expire in 1 hour
        - If you didn't request this reset, please ignore this email
        - Your password will NOT be changed until you confirm
        
        If you didn't request a password reset, simply ignore this email.
        
        Best regards,
        UIC Patent Portal Team
        University Innovation Cell
        Chandigarh University
        """
        
        msg = Message(
            subject='Confirm Password Reset - UIC Patent Portal',
            recipients=[user_email],
            html=html_body,
            body=text_body
        )
        
        mail.send(msg)
        return True
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    """Handle forgot password requests"""
    if request.method == "POST":
        try:
            email = request.form.get('email')
            
            if not email:
                flash('Please enter your email address', 'error')
                return redirect(url_for('forgot_password'))
            
            # Check if user exists
            conn = get_db()
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE email = ? AND is_active = 1", (email,))
            user = cur.fetchone()
            
            if user:
                # Generate reset token
                reset_token = secrets.token_urlsafe(32)
                expires_at = int(time.time()) + 3600  # 1 hour from now
                
                # Store reset token in database
                cur.execute("""
                    INSERT INTO password_reset_tokens (user_id, token, expires_at, created_at)
                    VALUES (?, ?, ?, ?)
                """, (user[1], reset_token, expires_at, datetime.now().isoformat()))
                
                conn.commit()
                
                # Send password reset email
                email_sent = send_password_reset_email(user[3], user[2], reset_token)
                
                if email_sent:
                    flash(f'Password reset confirmation has been sent to {email}. Please check your email and click the confirmation link.', 'success')
                else:
                    # For development/demo purposes, always show the confirmation link when email fails
                    confirm_url = url_for('confirm_reset', token=reset_token, _external=True)
                    flash('Email service not configured. Use this demo confirmation link:', 'info')
                    flash(f'{confirm_url}', 'success')
                
            else:
                # Don't reveal if email exists or not for security
                flash(f'If an account with {email} exists, a password reset link has been sent.', 'info')
            
            conn.close()
            return redirect(url_for('forgot_password'))
            
        except Exception as e:
            flash(f'Error processing request: {str(e)}', 'error')
            return redirect(url_for('forgot_password'))
    
    return render_template("forgot_password.html")

@app.route("/confirm-reset/<token>", methods=["GET"])
def confirm_reset(token):
    """Show password reset confirmation page"""
    try:
        # Find valid reset token
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT rt.*, u.* FROM password_reset_tokens rt
            JOIN users u ON rt.user_id = u.user_id
            WHERE rt.token = ? AND rt.used = 0 AND rt.expires_at > ?
        """, (token, int(time.time())))
        
        result = cur.fetchone()
        
        if not result:
            flash('Invalid or expired confirmation link. Please request a new password reset.', 'error')
            return redirect(url_for('forgot_password'))
        
        # Extract user data
        user_data = result[6:]   # users columns
        
        conn.close()
        return render_template("confirm_reset.html", 
                             token=token,
                             user_name=user_data[2],
                             user_email=user_data[3],
                             user_department=user_data[6])
        
    except Exception as e:
        flash(f'Error loading confirmation page: {str(e)}', 'error')
        return redirect(url_for('forgot_password'))

@app.route("/cancel-reset/<token>", methods=["GET"])
def cancel_reset(token):
    """Cancel password reset request"""
    try:
        # Mark token as used to prevent further use
        conn = get_db()
        cur = conn.cursor()
        cur.execute("UPDATE password_reset_tokens SET used = 1 WHERE token = ?", (token,))
        conn.commit()
        conn.close()
        
        flash('Password reset request has been cancelled. Your password remains unchanged.', 'info')
        return redirect(url_for('login'))
        
    except Exception as e:
        flash(f'Error cancelling reset: {str(e)}', 'error')
        return redirect(url_for('login'))

@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    """Handle password reset with token - requires confirmation first"""
    try:
        # Find valid reset token
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT rt.*, u.* FROM password_reset_tokens rt
            JOIN users u ON rt.user_id = u.user_id
            WHERE rt.token = ? AND rt.used = 0 AND rt.expires_at > ?
        """, (token, int(time.time())))
        
        result = cur.fetchone()
        
        if not result:
            flash('Invalid or expired reset link. Please request a new password reset.', 'error')
            return redirect(url_for('forgot_password'))
        
        # Extract token and user data
        token_data = result[:6]  # password_reset_tokens columns
        user_data = result[6:]   # users columns
        
        # Check if this is a GET request (coming from confirmation)
        if request.method == "GET":
            # Check if user came from confirmation (has referrer)
            referrer = request.referrer
            if not referrer or 'confirm-reset' not in referrer:
                # Redirect to confirmation page first
                return redirect(url_for('confirm_reset', token=token))
        
        if request.method == "POST":
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            
            if not password or not confirm_password:
                flash('Please fill in all fields', 'error')
                return render_template("reset_password.html")
            
            if password != confirm_password:
                flash('Passwords do not match', 'error')
                return render_template("reset_password.html")
            
            if len(password) < 8:
                flash('Password must be at least 8 characters long', 'error')
                return render_template("reset_password.html")
            
            # Update password and mark token as used
            new_password_hash = generate_password_hash(password)
            cur.execute("UPDATE users SET password_hash = ? WHERE user_id = ?", 
                       (new_password_hash, user_data[1]))
            cur.execute("UPDATE password_reset_tokens SET used = 1 WHERE token = ?", (token,))
            
            conn.commit()
            conn.close()
            
            flash('Password reset successful! You can now login with your new password.', 'success')
            return redirect(url_for('login'))
        
        conn.close()
        return render_template("reset_password.html")
        
    except Exception as e:
        flash(f'Error resetting password: {str(e)}', 'error')
        return redirect(url_for('forgot_password'))

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

# ========== DOCUMENT DOWNLOAD ROUTE ==========
@app.route("/download/idf-form")
def download_idf_form():
    """Download IDF Form Template"""
    try:
        from flask import send_file
        import os
        
        # Path to your existing IDF form document
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'folder', 'Invention Disclosure Form (IDF) (Updated 24th April 2025) (3).docx')
        
        # Check if file exists
        if not os.path.exists(file_path):
            flash('IDF Form template not found', 'error')
            return redirect(url_for('home'))
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name='IDF_Form_Template.docx',
            mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        
    except Exception as e:
        flash(f'Error downloading IDF form: {str(e)}', 'error')
        return redirect(url_for('home'))

if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)

# For Vercel deployment - serverless function handler
def handler(request, response):
    """Vercel serverless function handler"""
    return app(request, response)

# For WSGI deployment
application = app