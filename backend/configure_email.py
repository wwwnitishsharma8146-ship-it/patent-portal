#!/usr/bin/env python3
"""
Quick Email Configuration for UIC Patent Portal
"""

import os

def setup_gmail_email():
    """Setup Gmail for sending emails"""
    print("🔧 Gmail Email Setup for UIC Patent Portal")
    print("=" * 50)
    
    print("\n📧 To send real emails, you need:")
    print("1. A Gmail account")
    print("2. Enable 2-Factor Authentication")
    print("3. Generate an App Password")
    
    print("\n🔗 Quick Setup:")
    print("1. Go to: https://myaccount.google.com/security")
    print("2. Enable 2-Step Verification")
    print("3. Go to App passwords")
    print("4. Generate password for 'Mail'")
    print("5. Use the 16-character password below")
    
    email = input("\nEnter your Gmail address: ").strip()
    password = input("Enter your Gmail App Password (16 chars): ").strip()
    
    # Update the Flask app configuration
    app_py_path = 'app.py'
    
    # Read the current app.py
    with open(app_py_path, 'r') as f:
        content = f.read()
    
    # Replace the email configuration
    old_config = """app.config['MAIL_USERNAME'] = 'uicpatentportal@gmail.com'  # Demo email
app.config['MAIL_PASSWORD'] = 'demo-password'  # Will be replaced"""
    
    new_config = f"""app.config['MAIL_USERNAME'] = '{email}'
app.config['MAIL_PASSWORD'] = '{password}'"""
    
    content = content.replace(old_config, new_config)
    
    # Write back to app.py
    with open(app_py_path, 'w') as f:
        f.write(content)
    
    print(f"\n✅ Email configured successfully!")
    print(f"📧 Sender: {email}")
    print(f"🚀 You can now run: python app.py")
    print(f"📬 Real emails will be sent to users!")

if __name__ == "__main__":
    setup_gmail_email()