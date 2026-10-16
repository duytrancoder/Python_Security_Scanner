import os
import sys
import re
from dotenv import load_dotenv
from openai import OpenAI
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

load_dotenv()

api_key = os.getenv("ROUTER_API_KEY")
base_url = os.getenv("ROUTER_BASE_URL", "http://localhost:20128/v1")
model = os.getenv("ROUTER_MODEL", "ag/gemini-3.8-flash")

if not api_key:
    print(Fore.RED + Style.BRIGHT + "❌ Error: ROUTER_API_KEY is not set in .env")
    sys.exit(1)

# Check command line arguments
if len(sys.argv) < 2:
    print(Fore.YELLOW + "Usage: python scanner.py <file_path>")
    sys.exit(1)

code_path = sys.argv[1]

if not os.path.isfile(code_path):
    print(Fore.RED + f"❌ Error: File not found: '{code_path}'")
    sys.exit(1)

# Read file content
try:
    with open(code_path, "r", encoding="utf-8") as f:
        code = f.read()
except Exception as e:
    print(Fore.RED + f"❌ Error reading file '{code_path}': {e}")
    sys.exit(1)

# Security prompt requiring severity ratings
security_prompt = """You are an application security expert. Analyze this code for vulnerabilities.

For each issue found, provide:
1. Vulnerability type: [Name] (with CWE ID if applicable)
2. Severity: [CRITICAL | HIGH | MEDIUM | LOW]
3. Why it is vulnerable (1 sentence)
4. Impact (1 sentence)
5. Secure code fix

Be concise and direct.

Code:
{code}
"""

prompt = security_prompt.format(code=code)

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)

def print_colored_report(report_text):
    """Formats and prints the scan report with color-coded severity levels."""
    print("\n" + Fore.CYAN + Style.BRIGHT + "=" * 60)
    print(Fore.CYAN + Style.BRIGHT + "🛡️   AI SECURITY SCAN REPORT")
    print(Fore.CYAN + Style.BRIGHT + "=" * 60 + "\n")
    
    in_code_block = False
    
    for line in report_text.splitlines():
        stripped = line.strip()
        
        # Handle code blocks
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            print(Fore.LIGHTBLACK_EX + line)
            continue
            
        if in_code_block:
            print(Fore.GREEN + line)
            continue
            
        # Highlight Severity Levels
        if re.search(r"\bCRITICAL\b", line, re.IGNORECASE) and any(kw in line.lower() for kw in ["severity", "level", "rating", "*", "-"]):
            print(Fore.RED + Style.BRIGHT + "🔴 " + line)
        elif re.search(r"\bHIGH\b", line, re.IGNORECASE) and any(kw in line.lower() for kw in ["severity", "level", "rating", "*", "-"]):
            print(Fore.LIGHTRED_EX + Style.BRIGHT + "🟠 " + line)
        elif re.search(r"\bMEDIUM\b", line, re.IGNORECASE) and any(kw in line.lower() for kw in ["severity", "level", "rating", "*", "-"]):
            print(Fore.YELLOW + Style.BRIGHT + "🟡 " + line)
        elif re.search(r"\bLOW\b", line, re.IGNORECASE) and any(kw in line.lower() for kw in ["severity", "level", "rating", "*", "-"]):
            print(Fore.BLUE + Style.BRIGHT + "🔵 " + line)
        # Highlight Section Headers & Vulnerability Numbers
        elif stripped.startswith("###") or stripped.startswith("##") or re.match(r"^\d+\.", stripped):
            print(Fore.WHITE + Style.BRIGHT + line)
        # Highlight Secure code fix labels
        elif "secure code fix" in line.lower():
            print(Fore.GREEN + Style.BRIGHT + line)
        # Highlight Impact labels
        elif "impact" in line.lower():
            print(Fore.MAGENTA + Style.BRIGHT + line)
        # Highlight Why it is vulnerable labels
        elif "why it is vulnerable" in line.lower():
            print(Fore.LIGHTYELLOW_EX + line)
        else:
            print(line)
            
    print("\n" + Fore.CYAN + Style.BRIGHT + "=" * 60 + "\n")

try:
    print(Fore.CYAN + f"🔍 Scanning '{code_path}' with {model}...")
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    scan_result = response.choices[0].message.content
    print_colored_report(scan_result)
except Exception as e:
    print(Fore.RED + Style.BRIGHT + f"❌ Scan failed: {e}")
    sys.exit(1)
