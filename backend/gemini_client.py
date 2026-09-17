import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-3.6-flash")


def generate_explanation(document, platform, purpose, risk_level):
    try:
        prompt = f"""
You are SafeShare AI, a privacy and document-sharing risk advisor.

Document: {document}
Platform: {platform}
Purpose: {purpose}
Risk Level: {risk_level}

The user is deciding whether to share a document on a platform.

Explain the privacy and security risks associated with this situation.

Use simple and easy-to-understand English.
Write for a college student or general user.
Use a friendly and informative tone.
Avoid legal jargon, technical terms, and complex vocabulary.
Keep sentences short and clear.

Do NOT provide a recommendation.
Do NOT use headings like "Explanation" or "Recommendation".
Do NOT repeat the risk level.

Return only a short explanation in 4-5 lines.
"""

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        print("GEMINI ERROR:", e)

        return (
            "Sharing this document on the selected platform may expose personal information. "
            "Sensitive details could be stored, accessed, or misused if the platform is not designed "
            "to handle such documents securely."
        )