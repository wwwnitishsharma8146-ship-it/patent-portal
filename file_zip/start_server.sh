#!/bin/bash

# UIC Patent Portal - Server Startup Script

echo "🚀 Starting UIC Patent Portal..."
echo "================================"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

# Navigate to backend directory
cd backend

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install flask flask-cors

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Start the Flask server
echo "🌐 Starting Flask server on http://localhost:5002"
echo "📊 Database will be initialized automatically"
echo "🔗 Open http://localhost:5002 in your browser"
echo "👤 You'll be redirected to login page first"
echo "⏹️  Press Ctrl+C to stop the server"
echo "================================"

python3 app.py