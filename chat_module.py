# chat_module.py
import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Watson API Configuration
watson_api_key = os.getenv('WATSON_API_KEY', 'TWE6DvsLPVcINMhAHTaUF4Ewcd-P2NtdHEFn2mXDYEko')
watson_service_url = os.getenv('WATSON_SERVICE_URL', 'https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com')

def generate_response(user_message):
    """Generate AI response using Watson Natural Language Understanding and custom logic"""
    
    # Check if Watson API key is available
    if not watson_api_key:
        return "Error: Watson API key not configured. Please add WATSON_API_KEY to your .env file."
    
    try:
        # Analyze the user message with Watson NLU
        sentiment_data = analyze_message_with_watson(user_message)
        
        # Generate response based on message content and sentiment
        response = generate_civic_response(user_message, sentiment_data)
        
        return response
        
    except Exception as e:
        print(f"Watson AI error: {e}")
        # Fallback to basic civic responses
        return generate_basic_civic_response(user_message)

def analyze_message_with_watson(message):
    """Use Watson NLU to analyze message sentiment and entities"""
    try:
        url = f"{watson_service_url}/v1/analyze"
        
        headers = {
            'Content-Type': 'application/json',
        }
        
        data = {
            'text': message,
            'features': {
                'sentiment': {},
                'emotion': {},
                'keywords': {'limit': 5},
                'entities': {'limit': 5}
            },
            'version': '2021-08-01'
        }
        
        response = requests.post(
            url,
            headers=headers,
            json=data,
            auth=('apikey', watson_api_key),
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Watson NLU error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Watson NLU analysis error: {e}")
        return None

def generate_civic_response(user_message, watson_data=None):
    """Generate contextual civic response based on message and Watson analysis"""
    
    message_lower = user_message.lower()
    
    # Determine sentiment
    sentiment = "neutral"
    if watson_data and 'sentiment' in watson_data:
        sentiment_score = watson_data['sentiment']['document']['score']
        if sentiment_score > 0.3:
            sentiment = "positive"
        elif sentiment_score < -0.3:
            sentiment = "negative"
    
    # Civic topics and responses
    civic_responses = {
        'infrastructure': {
            'keywords': ['road', 'water', 'electricity', 'bridge', 'transport', 'traffic', 'street', 'sidewalk', 'light'],
            'response': "Infrastructure issues are crucial for community well-being. I can help you understand how to report infrastructure problems to local authorities. You can typically contact your local council or municipal office, or use their online reporting systems. For urgent safety issues, don't hesitate to call emergency services."
        },
        'healthcare': {
            'keywords': ['health', 'hospital', 'clinic', 'doctor', 'medical', 'emergency'],
            'response': "Healthcare access is a fundamental right. If you're experiencing healthcare-related concerns, I recommend contacting your local health department or community health services. Many areas have patient advocacy services that can help navigate healthcare systems and address concerns about quality of care."
        },
        'education': {
            'keywords': ['school', 'education', 'teacher', 'student', 'university', 'college'],
            'response': "Education is vital for community development. For school-related issues, start by contacting the school administration or school board. Many education departments have ombudsman services for more serious concerns. Parent councils and PTAs can also be effective advocacy channels."
        },
        'environment': {
            'keywords': ['pollution', 'environment', 'air quality', 'noise', 'waste', 'recycling', 'green'],
            'response': "Environmental concerns affect everyone's quality of life. Most environmental issues can be reported to local environmental protection agencies. For immediate health hazards, contact emergency services. Consider joining local environmental groups for ongoing advocacy and community action."
        },
        'safety': {
            'keywords': ['safety', 'crime', 'police', 'security', 'emergency', 'danger'],
            'response': "Public safety is a priority for all communities. For immediate emergencies, always call emergency services. For non-emergency safety concerns, contact your local police station or community safety office. Many areas have neighborhood watch programs and community safety initiatives you can join."
        },
        'government': {
            'keywords': ['government', 'council', 'mayor', 'politician', 'vote', 'election', 'policy'],
            'response': "Civic engagement is essential for democracy. You can participate by attending council meetings, contacting your representatives, participating in public consultations, and voting in elections. Most government offices have citizen liaison services to help with concerns and questions."
        }
    }
    
    # Find matching topic
    topic_found = None
    for topic, data in civic_responses.items():
        if any(keyword in message_lower for keyword in data['keywords']):
            topic_found = topic
            break
    
    # Generate response based on topic and sentiment
    if topic_found:
        base_response = civic_responses[topic_found]['response']
        
        if sentiment == "negative":
            prefix = "I understand your frustration with this issue. "
        elif sentiment == "positive":
            prefix = "I'm glad you're taking a proactive approach. "
        else:
            prefix = "Thank you for reaching out about this matter. "
            
        return prefix + base_response
    
    else:
        # General civic assistance
        return """I'm here to help with civic and government-related questions. I can assist with:

• Infrastructure issues (roads, utilities, public facilities)
• Healthcare access and services
• Education and school matters  
• Environmental concerns
• Public safety issues
• Government services and processes
• How to contact the right authorities
• Community engagement opportunities

Please feel free to ask about any specific civic concern, and I'll provide guidance on how to address it effectively."""

def generate_basic_civic_response(user_message):
    """Fallback response generator when Watson is unavailable"""
    
    message_lower = user_message.lower()
    
    if any(word in message_lower for word in ['help', 'how', 'what', 'where', 'when']):
        return """I'm your AI assistant for civic engagement. I can help you with:

• Reporting community issues and concerns
• Understanding government services
• Finding the right authorities to contact
• Learning about civic participation
• Accessing public resources

What specific civic matter would you like assistance with?"""
    
    elif any(word in message_lower for word in ['thank', 'thanks', 'good', 'great']):
        return "You're welcome! I'm here to help make civic engagement easier for everyone. Is there anything specific you'd like to know about government services or community issues?"
    
    else:
        return """Hello! I'm here to help you navigate civic matters and government services. I can assist with reporting issues, understanding public services, and connecting you with the right authorities. What would you like to know about?"""
