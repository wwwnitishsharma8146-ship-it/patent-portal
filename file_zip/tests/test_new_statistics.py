#!/usr/bin/env python3
"""
Test the new patent statistics system
"""

import requests
import json

def test_statistics():
    """Test the new statistics endpoint"""
    print("📊 Testing New Patent Statistics")
    print("=" * 50)
    
    try:
        response = requests.get("http://localhost:5002/stats")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Statistics endpoint working")
            print(f"📈 Response: {json.dumps(data, indent=2)}")
            
            if data.get('success'):
                stats = data['stats']
                print(f"\n📊 Current Statistics:")
                print(f"   Applications Submitted: {stats['submitted']}")
                print(f"   Patents Filed: {stats['filed']}")
                print(f"   Patents Published: {stats['published']}")
                print(f"   Patents Granted: {stats['granted']}")
                return True
            else:
                print("❌ Statistics response indicates failure")
                return False
        else:
            print(f"❌ HTTP error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🚀 TESTING NEW PATENT STATISTICS SYSTEM")
    print("=" * 60)
    
    success = test_statistics()
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS")
    print("=" * 60)
    
    if success:
        print("✅ New statistics system is working!")
        print("🌐 Check the website at http://localhost:5002")
        print("📈 You should see the new 4-column statistics layout")
    else:
        print("❌ Statistics system needs fixing")

if __name__ == "__main__":
    main()