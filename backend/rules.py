"""Transparent rule-based risk scoring for document sharing."""

DOCUMENT_SCORES = {
    "Aadhaar Card": 40,
    "PAN Card": 35,
    "Passport": 40,
    "Resume": 20,
    "Medical Report": 35,
    "Bank Statement": 35,
}

PLATFORM_SCORES = {
    "Government Portal": 5,
    "Banking Website": 10,
    "Job Portal": 20,
    "AI Chatbot": 30,
    "AI Image Generator": 30,
    "Social Media": 30,
}


def get_purpose_score(purpose: str) -> int:
    """Calculate risk points based on the sharing purpose."""

    text = purpose.strip().lower()

    # Public sharing has the highest purpose risk.
    if any(
        word in text
        for word in [
            "public",
            "post",
            "social media",
            "everyone",
            "publish",
            "share publicly",
        ]
    ):
        return 30

    # AI-related sharing has higher purpose risk.
    if any(
        word in text
        for word in [
            "ai",
            "chatbot",
            "image",
            "generate",
            "analysis",
            "analyze",
        ]
    ):
        return 20

    # Job-related sharing.
    if any(
        word in text
        for word in [
            "job",
            "employment",
            "recruit",
            "resume",
            "career",
        ]
    ):
        return 15

    # Banking-related sharing.
    if any(
        word in text
        for word in [
            "bank",
            "payment",
            "loan",
            "account",
        ]
    ):
        return 10

    # Government or verification purposes.
    if any(
        word in text
        for word in [
            "government",
            "official",
            "verification",
            "verify",
        ]
    ):
        return 5

    # General sharing purpose.
    return 20


def get_risk(
    document_type: str,
    platform: str,
    purpose: str,
) -> dict:
    """Return transparent score breakdown and overall risk level."""

    document_score = DOCUMENT_SCORES.get(
        document_type.strip(),
        30,
    )

    platform_score = PLATFORM_SCORES.get(
        platform.strip(),
        20,
    )

    purpose_score = get_purpose_score(purpose)

    risk_score = (
        document_score
        + platform_score
        + purpose_score
    )

    if risk_score <= 30:
        risk_level = "Low"
    elif risk_score <= 55:
        risk_level = "Medium"
    elif risk_score <= 75:
        risk_level = "High"
    else:
        risk_level = "Critical"

    return {
        "riskScore": risk_score,
        "riskLevel": risk_level,
        "breakdown": {
            "documentSensitivity": document_score,
            "platformRisk": platform_score,
            "purposeRisk": purpose_score,
        },
    }