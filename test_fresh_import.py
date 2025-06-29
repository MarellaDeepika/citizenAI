#!/usr/bin/env python3
import sys
import os

# Clear any cached modules
modules_to_clear = [name for name in sys.modules.keys() if 'chat_module' in name or 'generate' in name]
for module in modules_to_clear:
    del sys.modules[module]

# Now import fresh
sys.path.insert(0, r'c:\Users\Nik\Downloads\22FE1A6123\citizen_ai')

# Direct import and test
import importlib
chat_module = importlib.import_module('chat_module')

def test_fresh_import():
    """Test with completely fresh import"""
    
    print("Testing with fresh module import...")
    print("=" * 40)
    
    # Test the function directly
    question = "How do I register to vote?"
    print(f"Question: {question}")
    
    response = chat_module.generate_response(question)
    print(f"Response: {response}")

if __name__ == "__main__":
    test_fresh_import()
