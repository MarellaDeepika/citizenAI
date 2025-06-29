# clean_chat.py - AI Response System with Watson Integration
import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

def get_ai_response(user_message):
    """
    Generate AI response using Watson API with fallback to OpenRouter
    """
    try:
        # Try Watson first (more reliable and generous limits)
        return get_watson_response(user_message)
    except Exception as e:
        print(f"Watson failed: {e}")
        try:
            # Fallback to OpenRouter with reduced tokens
            return get_openrouter_response(user_message)
        except Exception as e2:
            print(f"OpenRouter also failed: {e2}")
            # Return a helpful fallback response
            return get_fallback_response(user_message)

def get_watson_response(user_message):
    """
    Generate AI response using IBM Watson API
    """
    # Watson credentials from environment
    watson_api_key = os.getenv('WATSON_API_KEY')
    watson_url = os.getenv('WATSON_URL')
    watson_version = os.getenv('WATSON_VERSION', '2021-06-14')
    
    if not watson_api_key or not watson_url:
        raise Exception("Watson API credentials not found")
    
    # Watson API endpoint
    url = f"{watson_url}/v1/message?version={watson_version}"
    
    # Headers for Watson
    headers = {
        "Content-Type": "application/json"
    }
    
    # Watson request payload
    data = {
        "input": {
            "message_type": "text",
            "text": user_message,
            "options": {
                "return_context": True
            }
        },
        "context": {
            "global": {
                "system": {
                    "turn_count": 1
                }
            },
            "skills": {
                "main skill": {
                    "user_defined": {
                        "role": "civic_assistant"
                    }
                }
            }
        }
    }
    
    # Make the API request with basic auth
    response = requests.post(
        url, 
        headers=headers, 
        json=data, 
        auth=('apikey', watson_api_key),
        timeout=30
    )
    
    if response.status_code == 200:
        result = response.json()
        if 'output' in result and 'generic' in result['output']:
            responses = result['output']['generic']
            if responses and len(responses) > 0:
                return responses[0].get('text', 'No response available')
        raise Exception("No valid response in Watson result")
    else:
        raise Exception(f"Watson API returned {response.status_code} - {response.text}")

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
    
    # Enhanced system prompt for detailed, well-structured responses
    system_prompt = """You are an expert AI assistant for CitizenAI, a comprehensive civic engagement platform. Provide exceptionally detailed, well-structured responses that fully educate and empower citizens.

FORMATTING REQUIREMENTS:
- Use clear HTML formatting for web display
- Structure with headings (## for main sections, ### for subsections)
- Use bullet points (•) and numbered lists for clarity
- Include line breaks for readability
- Bold important terms and key points
- Use proper paragraph breaks

RESPONSE REQUIREMENTS:
- Length: Minimum 300-500 words with comprehensive detail
- Structure: Organized sections with clear headings
- Depth: Provide full context, background, and explanations
- Actionability: Include specific step-by-step procedures
- Completeness: Address all aspects and related considerations
- Educational: Explain the reasoning behind processes
- Professional: Clear, accessible language

CONTENT STRUCTURE:
## Overview
Brief summary of the topic and its importance

## Key Information
• Essential facts and requirements
• Important deadlines and timelines
• Legal framework and regulations

## Step-by-Step Process
1. Detailed procedure with specific actions
2. Required documentation and materials
3. Where to go and who to contact

## Important Considerations
• Common challenges and solutions
• Tips for success
• What to expect during the process

## Additional Resources
• Contact information and websites
• Related services and programs
• Next steps and follow-up actions

FOCUS AREAS:
Government services, voting processes, local government participation, public safety, infrastructure reporting, legal rights, community engagement, public meetings, budget processes, and environmental regulations.

Always provide complete information that anticipates follow-up questions and gives citizens everything they need for informed civic participation."""
    
    # Prepare the request payload
    data = {
        "model": "anthropic/claude-3.5-sonnet",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 800,  # Reduced to fit within credit limits
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

def get_fallback_response(user_message):
    """
    Generate intelligent fallback responses when APIs are unavailable
    """
    message_lower = user_message.lower()
    
    # Comprehensive civic engagement responses
    if any(keyword in message_lower for keyword in ['vote', 'voting', 'election', 'register', 'ballot', 'poll']):
        return """
        <h2>Voter Registration and Voting Information</h2>
        <p><strong>Voting is your fundamental democratic right.</strong> Here's what you need to know:</p>
        
        <h3>Registration Requirements</h3>
        <ul>
            <li>U.S. citizenship</li>
            <li>18 years old by Election Day</li>
            <li>State residency requirements met</li>
            <li>Not disqualified by state law</li>
        </ul>
        
        <h3>How to Register</h3>
        <ol>
            <li><strong>Online:</strong> Visit your state's Secretary of State website</li>
            <li><strong>In-person:</strong> DMV, election office, or designated locations</li>
            <li><strong>By mail:</strong> Download and submit voter registration form</li>
        </ol>
        
        <h3>Important Deadlines</h3>
        <p>Registration deadlines vary by state (typically 15-30 days before elections). Check your state's specific requirements.</p>
        
        <h3>Need Help?</h3>
        <p>Contact your local election office or visit <strong>vote.gov</strong> for state-specific information.</p>
        """
    
    elif any(keyword in message_lower for keyword in ['local', 'city', 'government', 'services', 'municipal']):
        return """
        <h2>Local Government Services</h2>
        <p><strong>Your local government provides essential daily services</strong> that directly impact your quality of life.</p>
        
        <h3>Key Services</h3>
        <ul>
            <li>Water and sewer management</li>
            <li>Waste collection and recycling</li>
            <li>Police and fire protection</li>
            <li>Road maintenance and traffic management</li>
            <li>Parks and recreation facilities</li>
            <li>Building permits and inspections</li>
        </ul>
        
        <h3>How to Get Help</h3>
        <ol>
            <li><strong>City Hall:</strong> Main hub for most services</li>
            <li><strong>Online Portals:</strong> Many cities offer 24/7 online services</li>
            <li><strong>Phone Lines:</strong> Direct contact with departments</li>
            <li><strong>Mobile Apps:</strong> Report issues and track requests</li>
        </ol>
        
        <h3>Stay Engaged</h3>
        <p>Attend city council meetings, participate in budget discussions, and volunteer for local boards and commissions.</p>
        """
    
    elif any(keyword in message_lower for keyword in ['police', 'fire', 'emergency', 'safety', '911', 'crime']):
        return """
        <h2>Public Safety and Emergency Services</h2>
        <p><strong>Your safety is the top priority</strong> of local emergency services.</p>
        
        <h3>When to Call 911</h3>
        <ul>
            <li>Life-threatening emergencies</li>
            <li>Crimes in progress</li>
            <li>Fires or smoke</li>
            <li>Serious accidents</li>
            <li>Medical emergencies</li>
        </ul>
        
        <h3>Non-Emergency Situations</h3>
        <p>Use your local police department's <strong>non-emergency number</strong> for:</p>
        <ul>
            <li>Filing reports after incidents</li>
            <li>Noise complaints</li>
            <li>Minor traffic issues</li>
            <li>General questions</li>
        </ul>
        
        <h3>Emergency Preparedness</h3>
        <ol>
            <li>Create an emergency plan with your family</li>
            <li>Build an emergency supply kit</li>
            <li>Sign up for local emergency alerts</li>
            <li>Know your evacuation routes</li>
        </ol>
        
        <h3>Community Programs</h3>
        <p>Many departments offer neighborhood watch programs, citizen academies, and safety education.</p>
        """
    
    elif any(keyword in message_lower for keyword in ['road', 'pothole', 'traffic', 'infrastructure', 'street']):
        return """
        <h2>Infrastructure and Road Maintenance</h2>
        <p><strong>Well-maintained infrastructure</strong> is essential for community safety and economic vitality.</p>
        
        <h3>How to Report Problems</h3>
        <ol>
            <li><strong>Online Systems:</strong> Most cities have web portals for reporting</li>
            <li><strong>Mobile Apps:</strong> Many offer dedicated apps like "311" services</li>
            <li><strong>Phone:</strong> Call your public works department</li>
            <li><strong>In-Person:</strong> Visit city hall or public works office</li>
        </ol>
        
        <h3>What to Include in Reports</h3>
        <ul>
            <li>Exact location (address or landmarks)</li>
            <li>Photos if possible</li>
            <li>Description of the problem</li>
            <li>Any safety concerns</li>
        </ul>
        
        <h3>Infrastructure Planning</h3>
        <p>Major improvements require:</p>
        <ul>
            <li>Engineering studies and environmental reviews</li>
            <li>Public input and community meetings</li>
            <li>Budget allocation and funding sources</li>
            <li>Construction planning and permits</li>
        </ul>
        
        <h3>Get Involved</h3>
        <p>Participate in transportation planning meetings and capital improvement plan discussions to influence priorities.</p>
        """
    
    else:
        return """
        <h2>CitizenAI - Your Civic Engagement Assistant</h2>
        <p><strong>Welcome to your comprehensive guide</strong> for civic participation and government services.</p>
        
        <h3>What I Can Help With</h3>
        <ul>
            <li><strong>Voting & Elections:</strong> Registration, polling locations, candidate information</li>
            <li><strong>Local Government:</strong> Services, departments, contact information</li>
            <li><strong>Public Safety:</strong> Emergency services, crime prevention, community programs</li>
            <li><strong>Infrastructure:</strong> Reporting problems, understanding improvement processes</li>
            <li><strong>Community Engagement:</strong> Meetings, volunteering, civic participation</li>
        </ul>
        
        <h3>How to Get Specific Help</h3>
        <ol>
            <li>Ask specific questions about government services</li>
            <li>Inquire about voting procedures and requirements</li>
            <li>Request information about local meetings and events</li>
            <li>Learn about your rights and responsibilities as a citizen</li>
        </ol>
        
        <h3>Stay Connected</h3>
        <p>Regular civic engagement strengthens democracy. Attend local meetings, vote in all elections, and stay informed about community issues.</p>
        
        <p><em>For the most current information, always verify details with your local government offices.</em></p>
        """

def get_openrouter_response(user_message):
    """
    Generate AI response using OpenRouter API (with reduced tokens)
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
    
    # Simplified system prompt to reduce token usage
    system_prompt = """You are CitizenAI, a civic engagement assistant. Provide clear, helpful information about government services, voting, local issues, and community participation. Use HTML formatting with headings and lists for better readability. Keep responses focused and actionable."""
    
    # Prepare the request payload with reduced tokens
    data = {
        "model": "anthropic/claude-3.5-sonnet",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 500,  # Significantly reduced to stay within credit limits
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

if __name__ == "__main__":
    # Test the system
    test_question = "How do I register to vote?"
    print(f"Testing: {test_question}")
    try:
        response = get_ai_response(test_question)
        print(f"✓ Success! Response length: {len(response)}")
        print(f"Response preview: {response[:200]}...")
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    # Test the system
    test_question = "How do I register to vote?"
    print(f"Testing: {test_question}")
    try:
        response = get_ai_response(test_question)
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error: {e}")
