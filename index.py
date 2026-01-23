#!/usr/bin/env python3
"""
Alternative entrypoint for Vercel deployment.
"""

import sys
import os

# Add the api directory to Python path
api_path = os.path.join(os.path.dirname(__file__), 'api')
sys.path.insert(0, api_path)

# Import the Flask app from api directory
try:
    from app import app, application
except ImportError:
    # Fallback Flask app if import fails
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/')
    def hello():
        return jsonify({
            "message": "UIC Patent Portal - Index Entry",
            "status": "Import Error - Check logs",
            "error": "Could not import main app from api directory"
        })
    
    application = app

# Export for Vercel
app = app
application = app

if __name__ == "__main__":
    app.run(debug=True, port=5000)