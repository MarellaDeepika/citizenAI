#!/usr/bin/env python3
import requests
import time

def test_flask_app():
    """Test the Flask app endpoints"""
    
    base_url = "http://127.0.0.1:5000"
    
    print("Testing CitizenAI Flask Application")
    print("=" * 40)
    
    # Test 1: Home page
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Home page: {response.status_code}")
    except Exception as e:
        print(f"❌ Home page error: {e}")
    
    # Test 2: Dashboard
    try:
        response = requests.get(f"{base_url}/dashboard")
        print(f"✅ Dashboard: {response.status_code}")
    except Exception as e:
        print(f"❌ Dashboard error: {e}")
    
    # Test 3: Chat endpoint
    try:
        chat_data = {"message": "How do I register to vote?"}
        response = requests.post(f"{base_url}/chat", data=chat_data)
        print(f"✅ Chat endpoint: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   AI Response: {result.get('reply', 'No reply')[:100]}...")
            print(f"   Sentiment: {result.get('sentiment', 'No sentiment')}")
        else:
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Chat endpoint error: {e}")
    
    print("\n🎉 Testing complete!")

if __name__ == "__main__":
    # Wait a moment for the server to be ready
    time.sleep(2)
    test_flask_app()
