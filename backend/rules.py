"""Rule-based risk scores for sharing a document on a platform."""

LEVEL_SCORES = {
    "Low": 20,
    "Medium": 45,
    "High": 70,
    "Critical": 90,
}

# Explicit (document type, platform) -> risk level.
# Combinations not listed fall back to DEFAULT_LEVEL.
RISK_TABLE = {
    ("Aadhaar Card", "Government Portal"): "Low",
    ("Aadhaar Card", "Banking Website"): "Medium",
    ("Aadhaar Card", "Job Portal"): "High",
    ("Aadhaar Card", "AI Chatbot"): "Critical",
    ("Aadhaar Card", "AI Image Generator"): "Critical",
    ("Aadhaar Card", "Social Media"): "Critical",
    ("PAN Card", "Government Portal"): "Low",
    ("PAN Card", "Banking Website"): "Low",
    ("PAN Card", "Job Portal"): "Medium",
    ("PAN Card", "AI Chatbot"): "Critical",
    ("PAN Card", "AI Image Generator"): "Critical",
    ("PAN Card", "Social Media"): "Critical",
    ("Passport", "Government Portal"): "Low",
    ("Passport", "Banking Website"): "Medium",
    ("Passport", "Job Portal"): "High",
    ("Passport", "AI Chatbot"): "Critical",
    ("Passport", "AI Image Generator"): "Critical",
    ("Passport", "Social Media"): "Critical",
    ("Resume", "Government Portal"): "Low",
    ("Resume", "Banking Website"): "Medium",
    ("Resume", "Job Portal"): "Low",
    ("Resume", "AI Chatbot"): "High",
    ("Resume", "AI Image Generator"): "High",
    ("Resume", "Social Media"): "Medium",
    ("Medical Report", "Government Portal"): "High",
    ("Medical Report", "Banking Website"): "High",
    ("Medical Report", "Job Portal"): "High",
    ("Medical Report", "AI Chatbot"): "Critical",
    ("Medical Report", "AI Image Generator"): "Critical",
    ("Medical Report", "Social Media"): "Critical",
    ("Bank Statement", "Government Portal"): "Medium",
    ("Bank Statement", "Banking Website"): "Low",
    ("Bank Statement", "Job Portal"): "High",
    ("Bank Statement", "AI Chatbot"): "Critical",
    ("Bank Statement", "AI Image Generator"): "Critical",
    ("Bank Statement", "Social Media"): "Critical",
}

DEFAULT_LEVEL = "High"


def get_risk(document_type: str, platform: str) -> dict:
    """Return riskScore and riskLevel for a document/platform pair."""
    level = RISK_TABLE.get((document_type.strip(), platform.strip()), DEFAULT_LEVEL)
    return {
        "riskScore": LEVEL_SCORES[level],
        "riskLevel": level,
    }
