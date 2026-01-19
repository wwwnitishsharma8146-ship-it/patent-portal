#!/usr/bin/env python3
"""
Simple HTML structure validator for login and signup pages
"""

import requests
import re

def test_html_structure(url, page_name):
    """Test basic HTML structure"""
    print(f"🧪 Testing {page_name} HTML structure...")
    
    try:
        response = requests.get(url)
        html = response.text
        
        # Check basic HTML structure
        checks = {
            'DOCTYPE': '<!DOCTYPE html>' in html,
            'HTML tags': '<html' in html and '</html>' in html,
            'HEAD tags': '<head>' in html and '</head>' in html,
            'BODY tags': '<body' in html and '</body>' in html,
            'TITLE tag': '<title>' in html and '</title>' in html,
            'CSS styles': '<style>' in html and '</style>' in html,
            'JavaScript': '<script>' in html and '</script>' in html,
            'Background image': 'images.jpeg' in html,
            'Form element': '<form' in html and '</form>' in html
        }
        
        print(f"📋 {page_name} Structure Check:")
        all_passed = True
        for check, passed in checks.items():
            status = "✅" if passed else "❌"
            print(f"  {status} {check}")
            if not passed:
                all_passed = False
        
        # Check for common HTML errors
        errors = []
        
        # Check for unclosed tags
        if html.count('<div') != html.count('</div>'):
            errors.append("Mismatched div tags")
        
        # Check for duplicate IDs (basic check)
        id_pattern = r'id="([^"]+)"'
        ids = re.findall(id_pattern, html)
        if len(ids) != len(set(ids)):
            errors.append("Duplicate IDs found")
        
        # Check for missing alt attributes in images
        img_pattern = r'<img[^>]*>'
        images = re.findall(img_pattern, html)
        for img in images:
            if 'alt=' not in img:
                errors.append(f"Missing alt attribute: {img[:50]}...")
        
        if errors:
            print(f"⚠️  Potential Issues:")
            for error in errors:
                print(f"    - {error}")
        else:
            print(f"✅ No structural issues found")
        
        return all_passed and len(errors) == 0
        
    except Exception as e:
        print(f"❌ Error testing {page_name}: {e}")
        return False

def main():
    print("🔍 HTML Structure Validation Test")
    print("=" * 50)
    
    base_url = "http://localhost:5002"
    
    # Test login page
    login_valid = test_html_structure(f"{base_url}/login", "Login Page")
    print()
    
    # Test signup page
    signup_valid = test_html_structure(f"{base_url}/signup", "Signup Page")
    print()
    
    print("📊 Final Results:")
    print("=" * 50)
    print(f"Login Page: {'✅ VALID' if login_valid else '❌ ISSUES FOUND'}")
    print(f"Signup Page: {'✅ VALID' if signup_valid else '❌ ISSUES FOUND'}")
    
    if login_valid and signup_valid:
        print("\n🎉 All HTML pages are structurally valid!")
    else:
        print("\n⚠️  Some issues were found. Please review the output above.")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure Flask server is running on localhost:5002")
    except Exception as e:
        print(f"❌ Test error: {e}")