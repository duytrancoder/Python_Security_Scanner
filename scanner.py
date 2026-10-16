import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("ROUTER_API_KEY")
base_url = os.getenv("ROUTER_BASE_URL", "http://localhost:20128/v1")
model = os.getenv("ROUTER_MODEL", "ag/gemini-3.8-flash")

if not api_key:
    print("❌ Error: ROUTER_API_KEY is not set in .env")
    exit(1)

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

# Test with a simple prompt
try:
    print(f"Connecting to 9Router ({base_url}) using model '{model}'...")
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Why is the sky blue? Answer in one short sentence."}]
    )
    print("✅ Connection successful!")
    print("Response:\n", response.choices[0].message.content)
except Exception as e:
    print(f"❌ Connection failed: {e}")
