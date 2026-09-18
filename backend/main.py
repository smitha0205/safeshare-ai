from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rules import get_risk
from gemini_client import generate_explanation


app = FastAPI(title="SafeShare AI")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    documentType: str
    platform: str
    purpose: str
    language: str


class AnalyzeResponse(BaseModel):
    riskScore: int
    riskLevel: str
    breakdown: dict
    explanation: str
    recommendation: str


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    risk = get_risk(
        request.documentType,
        request.platform,
        request.purpose,
    )

    try:
        gemini_response = generate_explanation(
            request.documentType,
            request.platform,
            request.purpose,
            risk["riskLevel"],
            request.language,
        )

        explanation = ""
        recommendation = ""

        if "Recommendation:" in gemini_response:
            parts = gemini_response.split(
                "Recommendation:",
                1,
            )

            explanation = (
                parts[0]
                .replace("Explanation:", "")
                .strip()
            )

            recommendation = parts[1].strip()

        else:
            explanation = gemini_response.strip()
            recommendation = (
                "Share only when necessary and through trusted platforms."
            )

    except Exception:
        explanation = (
            "The safety score was calculated using "
            "SafeShare AI's transparent rule-based scoring system."
        )

        recommendation = (
            "Review the document sensitivity, platform risk, "
            "and purpose before sharing. Share only when necessary."
        )

    return {
        "riskScore": risk["riskScore"],
        "riskLevel": risk["riskLevel"],
        "breakdown": risk["breakdown"],
        "explanation": explanation,
        "recommendation": recommendation,
    }