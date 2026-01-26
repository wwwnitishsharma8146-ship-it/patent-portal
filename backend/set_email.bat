@echo off
echo Setting up Gmail for UIC Patent Portal
echo.
echo Your Gmail: www.nitishsharma8146@gmail.com
echo.
echo To get your App Password:
echo 1. Go to: https://myaccount.google.com/security
echo 2. Enable 2-Step Verification
echo 3. Click App passwords
echo 4. Generate password for Mail
echo 5. Copy the 16-character password
echo.
set /p APP_PASSWORD="Enter your Gmail App Password (16 characters): "
echo.
echo Setting environment variables...
set MAIL_USERNAME=www.nitishsharma8146@gmail.com
set MAIL_PASSWORD=%APP_PASSWORD%
echo.
echo ✅ Email configured! Starting Flask app...
python app.py