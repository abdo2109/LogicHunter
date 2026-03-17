# 🎯 LogicHunter
**"Logic is my only weapon." - Ayanokoji Kiyotaka**

**Developed by: 0xHamid (Zero)**

LogicHunter is an AI-powered Bug Bounty and Web Security tool designed to automate JavaScript analysis, context-aware parameter discovery, and API Auth Bypass/BOLA detection using Gemini AI.

## 🚀 Features

1. **Automated JS Secrets & Endpoint Hunter:** Scrapes target JS files, filters junk, applies smart regex, and uses AI to extract hidden secrets, API keys, and endpoints. Includes resume capability and custom sniper mode.
2. **Context-Aware Parameter Discovery:** Analyzes HTTP requests to predict hidden parameters for Mass Assignment and Privilege Escalation, outputting a clean wordlist for fuzzing.
3. **API Auth Bypass & BOLA Analyzer:** Deep dives into HTTP requests to identify IDOR/BOLA vulnerabilities and generates ready-to-use attack scenarios and payloads.

## 🛠️ Installation & Setup

It is highly recommended to run this tool inside a Python Virtual Environment to avoid conflicts.

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/LogicHunter.git
cd LogicHunter

# 2. Create a virtual environment
python3 -m venv env

# 3. Activate the virtual environment
# On Linux/macOS:
source env/bin/activate
# On Windows:
# env\Scripts\activate

# 4. Install requirements
pip install -r requirements.txt
```

## 🔑 Configuration (.env)

Create a `.env` file in the root directory and add your Gemini API Key:
```env
GEMINI_API_KEY=your_api_key_here
```

## ⚠️ Important Notes & Warnings [MUST READ]

- **Terminal Arabic Output Issue (RTL):** The AI's output is configured to reply in **Arabic**. Most terminals (CMD, Bash) do not fully support Right-To-Left (RTL) Arabic text, so the output might look garbled, reversed, or messy in the terminal. 
  **Solution:** Always check the generated Markdown (`.md`) reports saved automatically in your directory for a clean, perfectly formatted report. Alternatively, you can edit the Python code and change the AI prompt instructions to reply in English.
  
- **API Rate Limits:**
  Every AI model has a usage limit (Rate Limit), especially if you are using the free tier of the Gemini API. If the tool crashes with a `ResourceExhausted` error, wait a minute and try again. Please check Google's official pricing and limits for your specific key.

- **Checking Available Models:**
  By default, the tool uses a specific Gemini model. To see which models are available and supported by your specific API key, run the included helper script:
  ```bash
  python check_models.py
  ```

- **API Flexibility:**
  While this script is currently built to use Google's Gemini (`google-generativeai`), it is not strictly limited to it. The core logic and prompts can be easily modified to support other AI providers (like OpenAI, Claude, or DeepSeek) if you wish to adjust the code.

## 💻 Usage

Run the main tool using:
```bash
python hunter.py
```

## 🛡️ Disclaimer
This tool is created for educational purposes and authorized Bug Bounty hunting **ONLY**. Any misuse of this tool is strictly prohibited. The developer (0xHamid) assumes no liability and is not responsible for any misuse or damage caused by this program.
