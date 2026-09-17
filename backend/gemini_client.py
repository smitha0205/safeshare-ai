import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-3.6-flash")


def generate_explanation(document, platform, purpose, risk_level, language):
    try:
        prompt = f"""
You are SafeShare AI.

Document Type: {document}
Platform: {platform}
Purpose: {purpose}
Risk Level: {risk_level}
Language: {language}

Generate your response in {language}.

Provide:

Explanation:
- 4 to 5 short sentences
- Simple language
- Mention document and platform naturally
- Explain why it may be safe or risky

Recommendation:
- One short practical recommendation

Format exactly like:

Explanation: <text>

Recommendation: <text>
"""

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        print("GEMINI ERROR:", e)

        return """Explanation: Sharing this document may expose personal information on the selected platform.

Recommendation: Share only when necessary and through trusted platforms."""