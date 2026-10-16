import os
import sys
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("ROUTER_API_KEY")
base_url = os.getenv("ROUTER_BASE_URL", "http://localhost:20128/v1")
model = os.getenv("ROUTER_MODEL", "ag/gemini-3.8-flash")

if not api_key:
    print("❌ Error: ROUTER_API_KEY is not set in .env")
    sys.exit(1)

# Check command line arguments
if len(sys.argv) < 2:
    print("Usage: python scanner.py <file_path>")
    sys.exit(1)

code_path = sys.argv[1]

if not os.path.isfile(code_path):
    print(f"❌ Error: File not found: '{code_path}'")
    sys.exit(1)

# Read file content
try:
    with open(code_path, "r", encoding="utf-8") as f:
        code = f.read()
except Exception as e:
    print(f"❌ Error reading file '{code_path}': {e}")
    sys.exit(1)

# Security analysis prompt
security_prompt = """You are a security expert. Analyze this code for vulnerabilities.

For each issue, provide:
1. Vulnerability type
2. Why it is vulnerable (1 sentence)
3. Impact (1 sentence)
4. Secure code fix

Be concise.

Code:
{code}
"""

prompt = security_prompt.format(code=code)

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

try:
    print(f"🔍 Scanning '{code_path}' with {model}...")
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    print("\n" + "=" * 50)
    print("🛡️  SECURITY SCAN REPORT")
    print("=" * 50 + "\n")
    print(response.choices[0].message.content)
    print("\n" + "=" * 50)
except Exception as e:
    print(f"❌ Scan failed: {e}")
    sys.exit(1)
