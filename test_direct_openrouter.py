#!/usr/bin/env python3
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_openrouter_direct():
    """Test OpenRouter API directly without any other imports"""
    
    print("Testing OpenRouter API directly...")
    print("=" * 40)
    
    # Get API key from environment
    api_key = os.getenv('OPENROUTER_API_KEY')
    print(f"API Key loaded: {'Yes' if api_key else 'No'}")
    print(f"API Key starts with: {api_key[:20] if api_key else 'None'}...")
    
    if not api_key:
        print("ERROR: No API key found!")
        return
    
    # OpenRouter API endpoint
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    # Headers for OpenRouter
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "CitizenAI"
    }
    
    # Test question
    test_question = "How do I register to vote?"
    
    # System prompt
    system_prompt = """You are a helpful AI assistant for CitizenAI. Provide clear, concise, and direct answers to citizen questions.

Keep your responses:
- Brief and to the point (2-3 sentences max)
- Easy to understand
- Actionable when possible
- Professional but friendly

Focus on helping citizens with government services, local issues, and civic engagement."""

    # Prepare the request payload
    data = {
        "model": "anthropic/claude-3.5-sonnet",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": test_question}
        ],
        "max_tokens": 150,
        "temperature": 0.7
    }
    
    try:
        print(f"\nAsking: {test_question}")
        print("Making API request...")
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                ai_response = result['choices'][0]['message']['content'].strip()
                print(f"\nAI Response:")
                print(f"{ai_response}")
                print("\n✅ SUCCESS: OpenRouter is working correctly!")
            else:
                print("ERROR: No choices in response")
                print(result)
        else:
            print(f"ERROR: API returned {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_openrouter_direct()
