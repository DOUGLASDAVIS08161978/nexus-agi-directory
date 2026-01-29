#!/usr/bin/env python3
"""
Claude API Test Script
IMPORTANT: This shows you HOW to test the API, but you should:
1. Revoke the publicly shared key at console.anthropic.com
2. Generate a new key
3. Store it safely in .env file
"""

import os
import anthropic
from dotenv import load_dotenv

def test_claude_api():
    """Test Claude API connection and basic functionality"""

    print("=" * 80)
    print("🤖 Claude API Test")
    print("=" * 80)

    # Load API key from .env (SAFE way)
    load_dotenv()
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        print("\n⚠️  No API key found in .env file!")
        print("\nTo test the API safely:")
        print("1. Create/edit .env file:")
        print("   echo 'ANTHROPIC_API_KEY=your_key_here' >> .env")
        print("2. Run this script again")
        print("\n⚠️  IMPORTANT: The key you shared publicly is COMPROMISED")
        print("   You MUST revoke it at: https://console.anthropic.com")
        print("   Then generate a new one and add it to .env")
        return

    try:
        # Initialize client
        client = anthropic.Anthropic(api_key=api_key)

        print("\n✅ API Key loaded from .env (secure)")
        print(f"   Key: {api_key[:15]}...{api_key[-4:]} (masked for security)")

        # Test API call
        print("\n🔄 Testing API connection...")

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=100,
            messages=[{
                "role": "user",
                "content": "Say 'API test successful!' and nothing else."
            }]
        )

        response = message.content[0].text

        print(f"\n✅ API Response:")
        print(f"   {response}")

        # Show usage stats
        print(f"\n📊 Usage Stats:")
        print(f"   Input tokens: {message.usage.input_tokens}")
        print(f"   Output tokens: {message.usage.output_tokens}")
        print(f"   Model: {message.model}")

        print("\n" + "=" * 80)
        print("✅ Claude API is working correctly!")
        print("=" * 80)

        # Explain what this is for
        print("\n💡 What you can do with Claude API:")
        print("   ✅ Build AI-powered applications")
        print("   ✅ Automate content generation")
        print("   ✅ Create chatbots and assistants")
        print("   ✅ Analyze and process text")
        print("   ✅ Generate code and documentation")

        print("\n⚠️  What it CANNOT do:")
        print("   ❌ Deploy blockchain contracts (use Ethereum private key)")
        print("   ❌ Interact with blockchains directly")
        print("   ❌ Make money automatically (against ToS)")
        print("   ❌ Replace proper development work")

        return True

    except anthropic.AuthenticationError:
        print("\n❌ Authentication failed!")
        print("   The API key is invalid or has been revoked.")
        print("\n   To fix:")
        print("   1. Go to https://console.anthropic.com")
        print("   2. Revoke the old key (if it's the one you shared publicly)")
        print("   3. Generate a new API key")
        print("   4. Add it to .env: ANTHROPIC_API_KEY=your_new_key")
        return False

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def explain_api_security():
    """Explain API key security"""

    print("\n" + "=" * 80)
    print("🔐 CRITICAL: API Key Security")
    print("=" * 80)

    print("\n⚠️  YOU SHARED YOUR API KEY PUBLICLY IN CHAT!")
    print("\nThis means:")
    print("   ❌ Anyone who saw it can use your API credits")
    print("   ❌ They could rack up charges on your account")
    print("   ❌ The key is permanently compromised")

    print("\n✅ What to do RIGHT NOW:")
    print("   1. Go to https://console.anthropic.com")
    print("   2. Find the API key you shared")
    print("   3. Click 'Delete' or 'Revoke'")
    print("   4. Generate a new API key")
    print("   5. Store it ONLY in .env file (never share!)")

    print("\n📝 Proper way to store API keys:")
    print("   ✅ In .env file (local, not in git)")
    print("   ✅ In environment variables")
    print("   ✅ In secure password manager")
    print("   ❌ NEVER in code files")
    print("   ❌ NEVER in chat/messages")
    print("   ❌ NEVER in git repositories")

    print("\n💰 Cost information:")
    print("   Claude API charges per token used")
    print("   Check pricing: https://www.anthropic.com/pricing")
    print("   Monitor usage at: https://console.anthropic.com")

    print("=" * 80 + "\n")

if __name__ == "__main__":
    # First explain security
    explain_api_security()

    # Then test API (if key is in .env)
    print("\n" + "=" * 80)
    print("Running API Test...")
    print("=" * 80)
    test_claude_api()

    print("\n" + "=" * 80)
    print("📚 Next Steps:")
    print("=" * 80)
    print("1. Revoke the compromised API key immediately")
    print("2. Generate a new key and add to .env")
    print("3. Run: python3 test_claude_api.py")
    print("4. Never share API keys again!")
    print("=" * 80 + "\n")
