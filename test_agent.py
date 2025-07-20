#!/usr/bin/env python3
"""
Example script to test the AI Agent functionality
"""

import os
from agent_ import AIAgent

def test_agent():
    """Test the AI agent with sample interactions."""
    
    # Check for API key
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        print("❌ GROQ_API_KEY not found in environment variables")
        print("Please set it with: export GROQ_API_KEY='your_key_here'")
        return False
    
    try:
        # Initialize agent
        print("🚀 Initializing AI Agent...")
        agent = AIAgent(groq_api_key)
        
        # Test cases
        test_cases = [
            "Hello! Can you introduce yourself?",
            "Calculate 25 * 4 + 10",
            "What's the weather in London?",
            "Can you help me understand what tools you have available?"
        ]
        
        print("✅ Agent initialized successfully!")
        print("\n" + "="*50)
        print("Running test cases...")
        print("="*50)
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📝 Test {i}: {test_case}")
            print("-" * 40)
            response = agent.chat(test_case)
            print(f"🤖 Response: {response}")
            print("-" * 40)
        
        print("\n✅ All tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

if __name__ == "__main__":
    test_agent()
