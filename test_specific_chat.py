#!/usr/bin/env python3
import sys
import os

# Add the project directory to the Python path
sys.path.insert(0, r'c:\Users\Nik\Downloads\22FE1A6123\citizen_ai')

from chat_module import generate_response

def test_chat_with_specific_questions():
    """Test the chat module with specific questions"""
    
    print("Testing OpenRouter AI Chat with specific questions...")
    print("=" * 50)
    
    test_questions = [
        "How do I register to vote?",
        "What are the local recycling guidelines?",
        "How can I report a pothole?",
        "When are city council meetings held?",
        "How do I get a building permit?"
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Question: {question}")
        print("-" * 30)
        response = generate_response(question)
        print(f"Response: {response}")
        print()

if __name__ == "__main__":
    test_chat_with_specific_questions()
