from flask import Flask, request, jsonify
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

# Simple in-memory storage
applications = []
stats_data = {"submitted": 0, "filed": 0, "published": 0, "granted": 0}

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>UIC Patent Portal</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 0; 
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container { 
            max-width: 800px; 
            margin: 0 auto; 
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
        }
        .form-group { margin: 15px 0; }
        label { 
            display: block; 
            margin-bottom: 5px; 
            font-weight: bold;
            color: #555;
        }
        input, textarea, select { 
            width: 100%; 
            padding: 12px; 
            margin-bottom: 10px; 
            border: 2px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            box-sizing: border-box;
        }
        input:focus, textarea:focus, select:focus {
            border-color: #667eea;
            outline: none;
        }
        button { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            padding: 15px 30px; 
            border: none; 
            cursor: pointer;
            border-radius: 5px;
            font-size: 16px;
            font-weight: bold;
            width: 100%;
            transition: transform 0.2s;
        }
        button:hover { 
            transform: translateY(-2px);
        }
        .stats { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px; 
            margin: 30px 0; 
        }
        .stat-card { 
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 20px; 
            border-radius: 10px; 
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .stat-card h3 {
            margin: 0;
            font-size: 2em;
        }
        .stat-card p {
            margin: 5px 0 0 0;
            opacity: 0.9;
        }
        #result {
            margin-top: 20px;
        }
        .success {
            color: green; 
            padding: 15px; 
            background: #d4edda; 
            border-radius: 5px;
            border: 1px solid #c3e6cb;
        }
        .error {
            color: red; 
            padding: 15px; 
            background: #f8d7da; 
            border-radius: 5px;
            border: 1px solid #f5c6cb;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🏛️ UIC Patent Portal</h1>
        
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
                <label>👤 Full Name:</label>
                <input type="text" name="name" required placeholder="Enter your full name">
            </div>
            
            <div class="form-group">
                <label>📧 Email Address:</label>
                <input type="email" name="email" required placeholder="your.email@example.com">
            </div>
            
            <div class="form-group">
                <label>🏢 Department:</label>
                <input type="text" name="department" placeholder="e.g., Computer Science">
            </div>
            
            <div class="form-group">
                <label>📋 Patent Title:</label>
                <input type="text" name="patentTitle" required placeholder="Enter your patent title">
            </div>
            
            <div class="form-group">
                <label>🔬 Patent Type:</label>
                <select name="patentType" required>
                    <option value="">Select Patent Type</option>
                    <option value="utility">Utility Patent</option>
                    <option value="design">Design Patent</option>
                    <option value="plant">Plant Patent</option>
                </select>
            </div>
            
            <div class="form-group">
                <label>📝 Description:</label>
                <textarea name="description" rows="4" placeholder="Describe your invention..."></textarea>
            </div>
            
            <button type="submit">🚀 Submit Patent Application</button>
        </form>
        
        <div id="result"></div>
    </div>

    <script>
        // Load stats on page load
        loadStats();
        
        function loadStats() {
            fetch('/api/stats')
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById('submitted').textContent = data.stats.submitted;
                        document.getElementById('filed').textContent = data.stats.filed;
                        document.getElementById('published').textContent = data.stats.published;
                        document.getElementById('granted').textContent = data.stats.granted;
                    }
                })
                .catch(err => console.log('Stats load error:', err));
        }

        // Handle form submission
        document.getElementById('patentForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const button = this.querySelector('button');
            const originalText = button.textContent;
            
            button.textContent = '⏳ Submitting...';
            button.disabled = true;
            
            fetch('/api/submit', {
                method: 'POST',
                body: formData
            })
            .then(r => r.json())
            .then(data => {
                const result = document.getElementById('result');
                if (data.success) {
                    result.innerHTML = `<div class="success">
                        <strong>✅ Success!</strong><br>
                        Application ID: <strong>${data.applicationId}</strong><br>
                        Your patent application has been submitted successfully!
                    </div>`;
                    this.reset();
                    loadStats(); // Reload stats
                } else {
                    result.innerHTML = `<div class="error">
                        <strong>❌ Error:</strong> ${data.message}
                    </div>`;
                }
            })
            .catch(err => {
                document.getElementById('result').innerHTML = `<div class="error">
                    <strong>❌ Network Error:</strong> ${err.message}
                </div>`;
            })
            .finally(() => {
                button.textContent = originalText;
                button.disabled = false;
            });
        });
    </script>
</body>
</html>
    """

@app.route("/api/submit", methods=["POST"])
def submit_patent():
    try:
        data = request.form
        
        # Validate required fields
        if not data.get('patentTitle') or not data.get('patentType'):
            return jsonify({
                "success": False,
                "message": "Patent title and type are required"
            }), 400
        
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

@app.route("/api/applications")
def get_applications():
    return jsonify({
        "success": True,
        "applications": applications,
        "total": len(applications)
    })

# Health check endpoint
@app.route("/api/health")
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

# Expose app for Vercel
application = app

# For local development
if __name__ == "__main__":
    app.run(debug=True, port=5000)