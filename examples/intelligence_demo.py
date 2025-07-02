#!/usr/bin/env python3
"""
DACP Intelligence Demo

This script demonstrates how to use the invoke_intelligence function
with different LLM providers.
"""

import os
from dacp import invoke_intelligence


def demo_openai():
    """Demo OpenAI usage."""
    print("🔹 OpenAI Demo")

    config = {
        "engine": "openai",
        "model": "gpt-4",
        "api_key": os.getenv("OPENAI_API_KEY"),  # Set this environment variable
        "temperature": 0.7,
        "max_tokens": 100,
    }

    if not config["api_key"]:
        print("   ⚠️  OPENAI_API_KEY not set - skipping demo")
        return

    try:
        response = invoke_intelligence("What is Python?", config)
        print(f"   ✅ Response: {response[:100]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")


def demo_anthropic():
    """Demo Anthropic (Claude) usage."""
    print("🔹 Anthropic Demo")

    config = {
        "engine": "anthropic",
        "model": "claude-3-haiku-20240307",
        "api_key": os.getenv("ANTHROPIC_API_KEY"),  # Set this environment variable
        "temperature": 0.7,
        "max_tokens": 100,
    }

    if not config["api_key"]:
        print("   ⚠️  ANTHROPIC_API_KEY not set - skipping demo")
        return

    try:
        response = invoke_intelligence("Explain machine learning briefly", config)
        print(f"   ✅ Response: {response[:100]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")


def demo_local():
    """Demo local LLM usage (Ollama)."""
    print("🔹 Local LLM Demo (Ollama)")

    config = {
        "engine": "local",
        "model": "llama2",  # Make sure this model is installed in Ollama
        "endpoint": "http://localhost:11434/api/generate",
        "temperature": 0.7,
        "max_tokens": 50,
    }

    try:
        response = invoke_intelligence("Say hello!", config)
        print(f"   ✅ Response: {response[:100]}...")
    except Exception as e:
        print(f"   ⚠️  Ollama not running or model not available: {e}")


def demo_config_from_yaml():
    """Demo loading config from YAML-like structure."""
    print("🔹 Config from YAML Demo")

    # This simulates loading from an OAS YAML file
    yaml_config = {
        "intelligence": {
            "engine": "anthropic",
            "model": "claude-3-haiku-20240618",
            "endpoint": "https://api.anthropic.com/v1",
            "temperature": 0.5,
            "max_tokens": 75,
        }
    }

    intelligence_config = yaml_config["intelligence"]
    intelligence_config["api_key"] = os.getenv("ANTHROPIC_API_KEY")

    if not intelligence_config["api_key"]:
        print("   ⚠️  ANTHROPIC_API_KEY not set - showing config structure only")
        print(f"   📝 Config structure: {intelligence_config}")
        return

    try:
        response = invoke_intelligence(
            "What's the difference between AI and ML?", intelligence_config
        )
        print(f"   ✅ Response: {response[:100]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")


def main():
    """Run all demos."""
    print("🚀 DACP Intelligence Provider Demos\n")

    demo_openai()
    print()

    demo_anthropic()
    print()

    demo_local()
    print()

    demo_config_from_yaml()
    print()

    print("💡 Tips:")
    print("   • Set OPENAI_API_KEY environment variable to test OpenAI")
    print("   • Set ANTHROPIC_API_KEY environment variable to test Anthropic")
    print("   • Install and run Ollama with llama2 model to test local LLM")
    print("   • See README.md for more configuration options")


if __name__ == "__main__":
    main()
