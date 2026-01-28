#!/usr/bin/env python3
"""
Test Real Submission Format - Test with the exact data format the frontend sends
"""

import requests
import json
from datetime import datetime

def test_real_submission_format():
    """Test with the exact format that the frontend sends"""
    print("🧪 TESTING REAL SUBMISSION FORMAT")
    print("=" * 50)
    
    url = 'https://script.google.com/macros/s/AKfycby44PN4TqP2Q2Y9a-AtE-2jnntE6azhlJc_lyB5Zguco0FFA3n-KCDV37-MXdZzhShd-g/exec'
    
    # This is the exact format the backend sends (individual member fields)
    backend_format = {
        'applicationId': 'UIC-PAT-REAL-TEST-001',
        'fu