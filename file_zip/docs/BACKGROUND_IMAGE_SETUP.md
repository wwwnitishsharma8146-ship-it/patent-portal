# 🖼️ Background Image Setup Guide

## ✅ Current Status
Both login and signup pages are now configured to use the Chandigarh University campus image as background.

## 📁 File Location
**Background Image Path**: `backend/static/cu-campus.jpg`

## 🔄 How to Replace with Your Campus Image

### Method 1: Direct File Replacement
1. **Save your campus image** as `cu-campus.jpg`
2. **Replace the existing file**:
   ```bash
   # Navigate to your project directory
   cd "IOT PATENT WEB SITE"
   
   # Replace the image (drag your image file to terminal or use cp command)
   cp /path/to/your/campus-image.jpg backend/static/cu-campus.jpg
   ```

### Method 2: Using Different Image Name
If you want to use a different filename:

1. **Copy your image** to the static folder:
   ```bash
   cp /path/to/your/image.jpg backend/static/my-campus-bg.jpg
   ```

2. **Update both HTML files** to reference the new image:
   
   **In `backend/templates/login.html`**:
   ```css
   background: linear-gradient(135deg, rgba(0, 51, 102, 0.7) 0%, rgba(0, 0, 0, 0.5) 100%), 
               url('{{ url_for("static", filename="my-campus-bg.jpg") }}');
   ```
   
   **In `backend/templates/signup.html`**:
   ```css
   background: linear-gradient(135deg, rgba(0, 51, 102, 0.7) 0%, rgba(0, 0, 0, 0.5) 100%), 
               url('{{ url_for("static", filename="my-campus-bg.jpg") }}');
   ```

## 🎨 Current Background Implementation

Both pages use this CSS styling:
```css
body {
    font-family: 'Roboto', sans-serif;
    background: linear-gradient(135deg, rgba(0, 51, 102, 0.7) 0%, rgba(0, 0, 0, 0.5) 100%), 
                url('{{ url_for("static", filename="cu-campus.jpg") }}');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}
```

## 🔧 Features
- ✅ **Gradient Overlay**: Dark blue gradient for better text readability
- ✅ **Responsive**: Covers full viewport on all devices
- ✅ **Fixed Attachment**: Background doesn't scroll with content
- ✅ **Centered**: Image is centered and properly sized
- ✅ **Flask Integration**: Uses Flask's `url_for` for proper static file serving

## 📊 Image Requirements
- **Format**: JPG, JPEG, or PNG
- **Recommended Size**: 1920x1080 or higher for best quality
- **File Size**: Keep under 2MB for faster loading
- **Aspect Ratio**: Wide landscape images work best

## 🧪 Testing
After replacing the image, test both pages:
```bash
# Test login page
curl -I http://localhost:5002/login

# Test signup page  
curl -I http://localhost:5002/signup

# Test image accessibility
curl -I http://localhost:5002/static/cu-campus.jpg
```

## 🎯 Result
Your login and signup pages will display:
- Beautiful Chandigarh University campus background
- Professional gradient overlay
- Fully functional authentication forms
- Responsive design for all devices

**The background image is now successfully integrated into your UIC Patent Portal!** 🎉