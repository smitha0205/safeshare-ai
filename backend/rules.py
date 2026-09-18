"""Context-aware rule-based risk scoring for document sharing."""


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
    "Job Portal": 10,
    "AI Chatbot": 30,
    "AI Image Generator": 30,
    "Social Media": 30,
}


def get_purpose_score(purpose: str) -> int:
    text = purpose.strip().lower()

    if any(
        word in text
        for word in [
            "public",
            "post",
            "social media",
            "everyone",
            "publish",
        ]
    ):
        return 30

    if any(
        word in text
        for word in [
            "ai",
            "chatbot",
            "analysis",
            "analyze",
            "generate",
            "image",
        ]
    ):
        return 20

    if any(
        word in text
        for word in [
            "job",
            "employment",
            "recruit",
            "career",
            "resume",
        ]
    ):
        return 5

    if any(
        word in text
        for word in [
            "bank",
            "loan",
            "payment",
            "account",
        ]
    ):
        return 5

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

    return 15


def get_context_adjustment(
    document_type: str,
    platform: str,
    purpose: str,
) -> int:

    document = document_type.strip()
    platform_name = platform.strip()
    purpose_text = purpose.lower()

    # Resume uploaded for jobs
    if (
        document == "Resume"
        and platform_name == "Job Portal"
    ):
        return -25

    # Aadhaar/PAN/Passport for government verification
    if (
        platform_name == "Government Portal"
        and document in [
            "Aadhaar Card",
            "PAN Card",
            "Passport",
        ]
    ):
        return -30

    # PAN or bank statement for banking
    if (
        platform_name == "Banking Website"
        and document in [
            "PAN Card",
            "Bank Statement",
        ]
    ):
        return -25

    # Public posting of sensitive documents
    if (
        platform_name == "Social Media"
        and document in [
            "Aadhaar Card",
            "PAN Card",
            "Passport",
            "Medical Report",
            "Bank Statement",
        ]
    ):
        return 20

    # AI upload of highly sensitive documents
    if (
        platform_name in [
            "AI Chatbot",
            "AI Image Generator",
        ]
        and document in [
            "Aadhaar Card",
            "PAN Card",
            "Passport",
            "Medical Report",
            "Bank Statement",
        ]
    ):
        return 10

    return 0


def get_risk(
    document_type: str,
    platform: str,
    purpose: str,
) -> dict:

    document_score = DOCUMENT_SCORES.get(
        document_type.strip(),
        30,
    )

    platform_score = PLATFORM_SCORES.get(
        platform.strip(),
        20,
    )

    purpose_score = get_purpose_score(
        purpose,
    )

    context_adjustment = get_context_adjustment(
        document_type,
        platform,
        purpose,
    )

    risk_score = (
        document_score
        + platform_score
        + purpose_score
        + context_adjustment
    )

    risk_score = max(
        0,
        min(
            100,
            risk_score,
        ),
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
            "contextAdjustment": context_adjustment,
        },
    }