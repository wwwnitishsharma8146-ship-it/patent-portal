#!/usr/bin/env python3
"""
Simple test script to verify the Flask app works locally
"""

import sys
import os

# Add api directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'api'))

try:
    from app import app
    print("✅ Successfully imported Flask app")
    
    # Test the app
    with app.test_client() as client:
        response = client.get('/')
        print(f"✅ Home route status: {response.status_code}")
        
        response = client.get('/api/health')
        print(f"✅ Health route status: {response.status_code}")
        
        response = client.get('/api/stats')
        print(f"✅ Stats route status: {response.status_code}")
        
    print("✅ All tests passed - Flask app is working correctly")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()