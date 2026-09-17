from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    # Dummy response for now. Later this will use rules + Gemini.
    return {
        "riskScore": 90,
        "riskLevel": "Critical",
        "explanation": "This is a test explanation.",
        "recommendation": "Do not share sensitive documents.",
    }
