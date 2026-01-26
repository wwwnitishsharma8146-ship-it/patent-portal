# 📧 Email Setup Guide for Password Reset

## 🚀 Quick Setup

### **Step 1: Choose Email Provider**

#### **Option A: Gmail (Recommended)**
1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. **Set Environment Variables**:
   ```bash
   set MAIL_USERNAME=your-email@gmail.com
   set MAIL_PASSWORD=your-16-digit-app-password
   ```

#### **Option B: Outlook/Hotmail**
1. **Enable 2-Factor Authentication**
2. **Generate App Password** in Microsoft Account Security
3. **Update Flask Configuration**:
   ```python
   app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
   app.config['MAIL_PORT'] = 587
   ```

#### **Option C: Custom SMTP**
Update the configuration in `app.py`:
```python
app.config['MAIL_SERVER'] = 'your-smtp-server.com'
app.config['MAIL_PORT'] = 587  # or 465 for SSL
app.config['MAIL_USE_TLS'] = True
```

### **Step 2: Set Environment Variables**

#### **Windows (Command Prompt):**
```cmd
set MAIL_USERNAME=your-email@gmail.com
set MAIL_PASSWORD=your-app-password
python app.py
```

#### **Windows (PowerShell):**
```powershell
$env:MAIL_USERNAME="your-email@gmail.com"
$env:MAIL_PASSWORD="your-app-password"
python app.py
```

#### **Linux/Mac:**
```bash
export MAIL_USERNAME=your-email@gmail.com
export MAIL_PASSWORD=your-app-password
python app.py
```

### **Step 3: Test the System**

1. **Go to**: `http://127.0.0.1:5000/login`
2. **Click**: "Forgot your password?"
3. **Enter**: A registered email address
4. **Check**: Your email inbox for the reset link
5. **Click**: The reset link in the email
6. **Set**: Your new password

## 🔧 **Current Demo Mode**

**Without email configuration**, the system will:
- ✅ Generate secure reset tokens
- ✅ Store them in database with expiration
- ✅ Show demo reset link on screen
- ✅ Allow password reset via the link
- ❌ Not send actual emails

**With email configuration**, the system will:
- ✅ Send professional HTML emails
- ✅ Include secure reset links
- ✅ Provide clear instructions
- ✅ Include security warnings
- ✅ Work completely automatically

## 📋 **Email Template Features**

The password reset email includes:
- **Professional Design** with UIC branding
- **Secure Reset Button** with direct link
- **Security Warnings** about link expiration
- **Fallback Text Link** if button doesn't work
- **Clear Instructions** for users
- **Contact Information** for support

## 🔐 **Security Features**

- **Secure Tokens**: 32-byte URL-safe tokens
- **Time Expiration**: Links expire in 1 hour
- **Single Use**: Tokens can only be used once
- **Database Tracking**: All reset attempts logged
- **No Password Exposure**: Original passwords never revealed

## 🚨 **Important Notes**

1. **Never use your regular email password** - always use app passwords
2. **Keep credentials secure** - use environment variables
3. **Test thoroughly** before production deployment
4. **Monitor email delivery** for any issues
5. **Have backup contact method** for users

## 📞 **Support**

If users can't receive emails:
1. Check spam/junk folders
2. Verify email address is correct
3. Try different email provider
4. Contact system administrator
5. Use alternative recovery method

Your password reset system is now ready for production use! 🎉