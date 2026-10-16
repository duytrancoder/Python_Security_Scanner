# 🛡️ AI Security Scanner for Python

An AI-powered Command Line Interface (CLI) tool that leverages Large Language Models (LLMs) via **9Router** / **Google Gemini** to scan, analyze, and detect security vulnerabilities in Python source code.

Inspired by NextWork's *"AI Security Scanner for Python"*, extended with OpenAI-compatible AI routing via 9Router and terminal severity color-coding via Colorama.

---

## ✨ Features

- 🔍 **Automated Vulnerability Detection**: Spots classic security flaws such as SQL Injection (CWE-89), OS Command Injection (CWE-78), Weak Cryptographic Hashes (CWE-328), and Hardcoded Secrets (CWE-798).
- 🎯 **Color-Coded Severity Prioritization**: Colorama-powered terminal output categorizes issues by severity:
  - 🔴 **CRITICAL**: Immediate action required (e.g., RCE, SQLi).
  - 🟠 **HIGH**: Critical architectural or credential risks.
  - 🟡 **MEDIUM**: Dangerous configurations or weak encryption.
  - 🔵 **LOW**: Code quality and minor security enhancements.
- 💡 **Actionable Remediation**: Provides concise root-cause explanations, impact assessments, and drop-in secure code replacements.
- 🔌 **Flexible AI Gateway Support**: Uses standard OpenAI API protocol compatible with **9Router**, Google Gemini, OpenRouter, or local LLM proxies.

---

## 📁 Project Structure

```text
Python_Security_Scanner/
├── .env.example          # Environment variable template
├── .gitignore            # Excludes venv, .env, and caches
├── requirements.txt      # Project dependencies
├── scanner.py            # Main CLI security scanner tool
├── vulnerable.py         # Test file with intentional security flaws
└── README.md             # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- A running [9Router](https://github.com/decolua/9router) instance or an OpenAI-compatible API key / Google Gemini API key.

### 1. Clone the Repository

```bash
git clone https://github.com/duytrancoder/Python_Security_Scanner.git
cd Python_Security_Scanner
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux / macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Open `.env` and configure your API settings:

```env
ROUTER_BASE_URL=http://localhost:20128/v1
ROUTER_API_KEY=your_9router_api_key_here
ROUTER_MODEL=ag/gemini-3.8-flash
```

---

## 💻 Usage

Run the scanner by providing any target Python file path:

```bash
python scanner.py <path_to_file.py>
```

### Example: Scan the Included Test File

```bash
python scanner.py vulnerable.py
```

---

## 📊 Sample Output

```text
🔍 Scanning 'vulnerable.py' with ag/gemini-3.8-flash...

============================================================
🛡️   AI SECURITY SCAN REPORT
============================================================

### Issue 1: SQL Injection
1. Vulnerability type: SQL Injection (CWE-89)
🔴 2. Severity: CRITICAL
3. Why it is vulnerable: Untrusted user input is directly concatenated into the SQL statement using an f-string instead of parameterized queries.
4. Impact: An attacker can bypass authentication, read sensitive database contents, or modify/delete data.
5. Secure code fix:
```python
def authenticate(username, password_hash):
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query, (username, password_hash))
    return cursor.fetchone()
```

---

### Issue 2: OS Command Injection
1. Vulnerability type: Improper Neutralization of Special Elements used in an OS Command (CWE-78)
🔴 2. Severity: CRITICAL
3. Why it is vulnerable: Unsanitized user input is formatted directly into a system shell command executed via os.system.
4. Impact: An attacker can execute arbitrary system commands on the host server.
5. Secure code fix:
```python
import subprocess

def process_input(user_input):
    subprocess.run(["echo", user_input], check=True)
```
============================================================
```

---

## 🛡️ Tested Vulnerability Matrix

| Vulnerability Type | CWE ID | Severity | File / Function Tested |
| :--- | :--- | :--- | :--- |
| **SQL Injection** | [CWE-89](https://cwe.mitre.org/data/definitions/89.html) | 🔴 CRITICAL | `authenticate()` in `vulnerable.py` |
| **OS Command Injection** | [CWE-78](https://cwe.mitre.org/data/definitions/78.html) | 🔴 CRITICAL | `process_input()` in `vulnerable.py` |
| **Weak Password Hashing (MD5)** | [CWE-328](https://cwe.mitre.org/data/definitions/328.html) | 🟠 HIGH | `hash_password()` in `vulnerable.py` |
| **Hardcoded Credentials** | [CWE-798](https://cwe.mitre.org/data/definitions/798.html) | 🟠 HIGH | `DB_PASSWORD`, `API_SECRET` in `vulnerable.py` |

---

## 🔒 Security Best Practices

- Never commit `.env` or sensitive credentials to version control.
- All secrets in this repository are managed via `.gitignore`.
- Credentials inside `vulnerable.py` are purely synthetic mock strings for automated testing purposes.

---

## 📜 License

This project is licensed under the MIT License.
