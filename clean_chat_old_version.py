import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_ai_response(user_message):
    """
    Generate AI response using OpenRouter API with fallback logic.
    """
    try:
        # OpenRouter API integration
        api_key = os.getenv('OPENROUTER_API_KEY')
        if not api_key:
            raise Exception("No API key found")

        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:5000",
            "X-Title": "CitizenAI"
        }

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

        data = {
            "model": "anthropic/claude-3.5-sonnet",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": 800,
            "temperature": 0.7
        }

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

    except Exception as e:
        print(f"OpenRouter failed: {e}")
        return get_fallback_response(user_message)

def get_fallback_response(user_message):
    """
    Generate intelligent fallback responses when APIs are unavailable.
    """
    message_lower = user_message.lower()

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