from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)

# Configure CORS
CORS(app, 
     supports_credentials=True,
     origins=["*"],
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "OPTIONS"])

app.secret_key = 'uic-patent-portal-production-key-2026-secure'

# Simple in-memory storage for demo (since Vercel doesn't support SQLite well)
applications = []
stats_data = {"submitted": 0, "filed": 0, "published": 0, "granted": 0}

# Simple HTML template for the home page
HOME_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>UIC Patent Portal</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        .form-group { margin: 15px 0; }
        label { display: block; margin-bottom: 5px; }
        input, textarea, select { width: 100%; padding: 8px; margin-bottom: 10px; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; cursor: pointer; }
        button:hover { background: #0056b3; }
        .stats { display: flex; gap: 20px; margin: 20px 0; }
        .stat-card { background: #f8f9fa; padding: 15px; border-radius: 5px; text-align: center; }
    </style>
</head>
<body>
    <div class="container">
        <h1>UIC Patent Portal</h1>
        
        <div class="stats">
            <div class="stat-card">
                <h3 id="submitted">0</h3>
                <p>Submitted</p>
            </div>
            <div class="stat-card">
                <h3 id="filed">0</h3>
                <p>Filed</p>
            </div>
            <div class="stat-card">
                <h3 id="published">0</h3>
                <p>Published</p>
            </div>
            <div class="stat-card">
                <h3 id="granted">0</h3>
                <p>Granted</p>
            </div>
        </div>

        <form id="patentForm">
            <div class="form-group">
                <label>Name:</label>
                <input type="text" name="name" required>
            </div>
            
            <div class="form-group">
                <label>Email:</label>
                <input type="email" name="email" required>
            </div>
            
            <div class="form-group">
                <label>Department:</label>
                <input type="text" name="department">
            </div>
            
            <div class="form-group">
                <label>Patent Title:</label>
                <input type="text" name="patentTitle" required>
            </div>
            
            <div class="form-group">
                <label>Patent Type:</label>
                <select name="patentType" required>
                    <option value="">Select Type</option>
                    <option value="utility">Utility Patent</option>
                    <option value="design">Design Patent</option>
                    <option value="plant">Plant Patent</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>Description:</label>
                <textarea name="description" rows="4"></textarea>
            </div>
            
            <button type="submit">Submit Patent Application</button>
        </form>
        
        <div id="result" style="margin-top: 20px;"></div>
    </div>

    <script>
        // Load stats
        fetch('/api/stats')
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    document.getElementById('submitted').textContent = data.stats.submitted;
                    document.getElementById('filed').textContent = data.stats.filed;
                    document.getElementById('published').textContent = data.stats.published;
                    document.getElementById('granted').textContent = data.stats.granted;
                }
            });

        // Handle form submission
        document.getElementById('patentForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            
            fetch('/api/submit', {
                method: 'POST',
                body: formData
            })
            .then(r => r.json())
            .then(data => {
                const result = document.getElementById('result');
                if (data.success) {
                    result.innerHTML = `<div style="color: green; padding: 10px; background: #d4edda; border-radius: 5px;">
                        <strong>Success!</strong> Application ID: ${data.applicationId}
                    </div>`;
                    this.reset();
                    // Reload stats
                    location.reload();
                } else {
                    result.innerHTML = `<div style="color: red; padding: 10px; background: #f8d7da; border-radius: 5px;">
                        <strong>Error:</strong> ${data.message}
                    </div>`;
                }
            })
            .catch(err => {
                document.getElementById('result').innerHTML = `<div style="color: red;">Error: ${err.message}</div>`;
            });
        });
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HOME_TEMPLATE)

@app.route("/api/submit", methods=["POST"])
def submit_patent():
    try:
        data = request.form
        
        # Generate application ID
        app_id = f"UIC-PAT-{len(applications) + 1}"
        
        # Create application record
        application = {
            'application_id': app_id,
            'name': data.get('name', ''),
            'email': data.get('email', ''),
            'department': data.get('department', ''),
            'patent_title': data.get('patentTitle', ''),
            'patent_type': data.get('patentType', ''),
            'description': data.get('description', ''),
            'submission_date': datetime.now().isoformat(),
            'status': 'submitted'
        }
        
        applications.append(application)
        stats_data['submitted'] += 1
        
        return jsonify({
            "success": True,
            "applicationId": app_id,
            "message": "Patent application submitted successfully!"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error: {str(e)}"
        }), 500

@app.route("/api/stats")
def stats():
    return jsonify({
        "success": True,
        "stats": stats_data
    })

# Export for Vercel
app = app