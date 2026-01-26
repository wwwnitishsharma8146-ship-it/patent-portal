# ⚡ Quick Email Setup - 2 Minutes

## 🚀 **Option 1: Use Your Gmail (Fastest)**

1. **Enable 2FA** on your Gmail account
2. **Get App Password**:
   - Go to: https://myaccount.google.com/security
   - Click: 2-Step Verification → App passwords
   - Generate password for "Mail"
3. **Set Environment Variables**:
   ```cmd
   set MAIL_USERNAME=your-email@gmail.com
   set MAIL_PASSWORD=your-16-digit-app-password
   python app.py
   ```

## 🚀 **Option 2: Test Mode (Works Now)**

Your app is already running in test mode! 

**Test it:**
1. Go to: `http://127.0.0.1:5000/login`
2. Click: "Forgot your password?"
3. Enter: Any registered email
4. **Copy the demo link** that appears
5. **Use the link** to reset password

## ✅ **Current Status**

- ✅ **Password Reset**: Fully working
- ✅ **Secure Tokens**: Generated and stored
- ✅ **Demo Links**: Shown on screen
- ⚠️ **Email**: Test mode (shows links instead of sending)

## 📧 **To Enable Real Emails**

Just run this before starting the app:
```cmd
set MAIL_USERNAME=your-gmail@gmail.com
set MAIL_PASSWORD=your-app-password
python app.py
```

**Your password reset is working RIGHT NOW!** 🎉