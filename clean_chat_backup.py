# clean_chat.py - Simple AI Response System
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_ai_response(user_message):
    """
    Generate AI response with fallback for network issues
    """
    try:
        # First try the OpenRouter API
        return get_openrouter_response(user_message)
    except Exception as e:
        # If OpenRouter fails, use simple fallback responses
        print(f"OpenRouter failed: {e}")
        return get_simple_fallback_response(user_message)

def get_openrouter_response(user_message):
    """
    Generate AI response using OpenRouter API
    """
    # Get API key from environment
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        raise Exception("No API key found")
    
    # OpenRouter API endpoint
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    # Headers for OpenRouter
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "CitizenAI"
    }
    
    # System prompt for comprehensive responses
    system_prompt = ("You are an expert AI assistant for CitizenAI. Provide detailed, thorough, and complete responses to citizen questions. "
                    "Your responses should be comprehensive (minimum 8-12 sentences), well-structured with clear sections, "
                    "informative and educational, actionable with specific steps, professional yet accessible, "
                    "and include relevant context and background information. Focus on government services, "
                    "civic issues, community engagement, legal information, public safety, infrastructure, "
                    "environmental concerns, and social services.")
    
    # Prepare the request payload
    data = {
        "model": "anthropic/claude-3.5-sonnet",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 800,
        "temperature": 0.7
    }
    
    # Make the API request
    response = requests.post(url, headers=headers, json=data, timeout=30)
    
    if response.status_code == 200:
        result = response.json()
        if 'choices' in result and len(result['choices']) > 0:
            ai_response = result['choices'][0]['message']['content'].strip()
            return ai_response
        else:
            raise Exception("No choices in response")
    else:
        raise Exception(f"API returned {response.status_code} - {response.text}")

def get_simple_fallback_response(user_message):
    """
    Generate simple fallback responses when OpenRouter is unavailable
    """
    message_lower = user_message.lower()
    
    if any(keyword in message_lower for keyword in ['vote', 'voting', 'election', 'register', 'ballot']):
        return ("Voting is a fundamental democratic right. To register to vote, visit your state's Secretary of State website or register at the DMV. "
                "You must be a U.S. citizen, 18 years old, and a resident of the jurisdiction where you plan to vote. "
                "Research candidates and issues before voting using voter guides. Check your polling location and hours on your local election office website. "
                "Bring valid identification as required by your state. You can vote in-person on Election Day, during early voting periods, or by absentee ballot in many areas. "
                "Contact your local election officials if you have questions or encounter problems voting.")
    
    elif any(keyword in message_lower for keyword in ['local', 'city', 'government', 'services']):
        return ("Local government provides essential daily services including water, sewer, trash collection, police, fire protection, and road maintenance. "
                "Contact your city hall or county office to request services or report problems. Most have websites with contact information and online reporting systems. "
                "Attend city council or county commission meetings to stay informed and provide input on local issues. "
                "You can volunteer for boards and commissions, participate in budget hearings, and run for local office. "
                "Local elections often have low turnout, making your vote more impactful.")
    
    elif any(keyword in message_lower for keyword in ['police', 'fire', 'emergency', 'safety', '911']):
        return ("Call 911 for life-threatening emergencies, crimes in progress, fires, or serious accidents. "
                "For non-urgent situations, use non-emergency numbers to file reports or request services. "
                "Many police departments offer community programs like neighborhood watch and citizen academies. "
                "Install smoke detectors, create emergency plans, and prepare emergency supply kits. "
                "Sign up for local emergency alerts through your county emergency management office. "
                "Report suspicious activity to authorities with detailed descriptions.")
    
    elif any(keyword in message_lower for keyword in ['road', 'pothole', 'traffic', 'infrastructure']):
        return ("Report infrastructure problems like potholes, broken traffic signals, or water main breaks to your local public works department. "
                "Provide specific locations and photos when possible. Most cities have online reporting systems or mobile apps. "
                "Major infrastructure improvements require planning, engineering studies, and significant funding. "
                "Participate in transportation planning meetings and capital improvement plan discussions. "
                "Contact your local representatives about infrastructure priorities and funding needs.")
    
    else:
        return ("Thank you for your question about civic engagement. I'm here to help with information about government services, voting, local issues, and community participation. "
                "You can contact your local government offices directly for specific services, attend public meetings to stay informed, "
                "and participate in the democratic process through voting and community involvement. "
                "For detailed information about specific topics, please feel free to ask more specific questions about voting, local services, public safety, or community engagement.")

if __name__ == "__main__":
    # Test the system
    test_question = "How do I register to vote?"
    print(f"Testing: {test_question}")
    response = get_ai_response(test_question)
    print(f"Response: {response}")
