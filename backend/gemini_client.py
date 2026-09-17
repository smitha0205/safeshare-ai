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
You are SafeShare AI.

Analyze ONLY this scenario:

Document Type: {document}
Platform: {platform}
Purpose: {purpose}
Risk Level: {risk_level}

Explain specifically why sharing this document on this platform may be safe or risky.

Requirements:
- Mention the document type naturally.
- Mention the platform naturally.
- Consider the user's purpose.
- Explain why the given risk level makes sense.
- Use very simple English.
- Write exactly 4 to 5 short sentences.
- Keep the explanation practical and user-friendly.
- Do NOT provide recommendations.
- Do NOT use headings.
- Do NOT mention "Explanation" or "Recommendation".
- Do NOT repeat the risk level directly.

Return only the explanation text.
"""

        response = model.generate_content(prompt)

        print("DOCUMENT:", document)
        print("PLATFORM:", platform)
        print("PURPOSE:", purpose)
        print("RESPONSE:", response.text)

        return response.text

    except Exception as e:
        print("GEMINI ERROR:", e)

        return (
            f"Sharing a {document} on {platform} can expose personal information. "
            f"The platform may store or process the data you upload. "
            f"If sensitive details are included, they could be accessed by unauthorized people. "
            f"It is important to understand how the platform handles your information before sharing it."
        )