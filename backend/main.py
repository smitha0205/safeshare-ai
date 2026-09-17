from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rules import get_risk

app = FastAPI(title="SafeShare AI")

# Allow the React (Vite) frontend to call this API during local development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    documentType: str
    platform: str
    purpose: str


class AnalyzeResponse(BaseModel):
    riskScore: int
    riskLevel: str
    explanation: str
    recommendation: str


@app.get("/health")
def health():
    return {"ok": True}


def _guidance(document_type: str, platform: str, risk_level: str) -> tuple[str, str]:
    if risk_level == "Low":
        return (
            f"Sharing a {document_type} on {platform} is usually appropriate when the destination is official.",
            "Proceed, but share only what is requested and confirm the destination is genuine.",
        )
    if risk_level == "Medium":
        return (
            f"Sharing a {document_type} on {platform} has some risk. Limit what you send if you continue.",
            "Share only if necessary, redact extra details, and avoid uploading the full document.",
        )
    if risk_level == "High":
        return (
            f"Sharing a {document_type} on {platform} is often unsafe. This destination is a poor fit for this document.",
            "Avoid sharing unless you have a strong, verified reason. Prefer an official channel instead.",
        )
    return (
        f"Sharing a {document_type} on {platform} is very likely unsafe. This combination is a high-exposure risk.",
        "Do not share this document here. Use an official portal or in-person verification instead.",
    )


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    risk = get_risk(request.documentType, request.platform)
    explanation, recommendation = _guidance(
        request.documentType,
        request.platform,
        risk["riskLevel"],
    )
    return {
        "riskScore": risk["riskScore"],
        "riskLevel": risk["riskLevel"],
        "explanation": explanation,
        "recommendation": recommendation,
    }
