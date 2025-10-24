"""
HamCaller - Spam Detection API (Hugging Face Version)
Uses Hugging Face Inference API instead of local Ollama
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
from huggingface_hub import InferenceClient

app = FastAPI(title="HamCaller - AI Spam Detection")

# Initialize Hugging Face client
# Using a small, fast model for spam detection
HF_TOKEN = os.getenv("HF_TOKEN", "")
client = InferenceClient(token=HF_TOKEN) if HF_TOKEN else InferenceClient()

# Model to use (free tier compatible)
MODEL = "mistralai/Mistral-7B-Instruct-v0.2"  # Fast and good for classification


class TranscriptRequest(BaseModel):
    transcript: str


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the frontend HTML"""
    with open("index.html", "r") as f:
        return f.read()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "model": MODEL}


@app.post("/detect")
async def detect_spam(request: TranscriptRequest):
    """
    Detect if a phone call transcript is spam or legitimate
    """
    transcript = request.transcript.strip()

    if not transcript:
        raise HTTPException(status_code=400, detail="Transcript cannot be empty")

    # Create optimized prompt for classification
    prompt = f"""<s>[INST] You are a spam call detector. Classify this phone call transcript as SPAM or LEGITIMATE.

SPAM calls include:
- Unsolicited sales calls and robocalls
- Scam attempts (fake IRS, tech support, law enforcement)
- Requests to "press 1" or provide personal information
- Fake prizes, sweepstakes, or lottery wins
- Threats, urgent demands, or fear tactics
- Extended warranty scams

LEGITIMATE calls include:
- Appointment confirmations from real businesses
- Personal calls from family, friends, or colleagues
- Delivery notifications from known services
- Known business contacts
- School, medical, or professional communications

Call transcript: "{transcript}"

Respond with ONLY one word - either SPAM or LEGITIMATE. Nothing else. [/INST]"""

    try:
        # Call Hugging Face API
        response = client.text_generation(
            prompt,
            model=MODEL,
            max_new_tokens=10,
            temperature=0.1,
            top_p=0.9,
        )

        # Parse response
        classification = response.strip().upper()

        # Determine if spam
        is_spam = "SPAM" in classification

        # Calculate confidence based on response clarity
        if classification in ["SPAM", "LEGITIMATE"]:
            confidence = 95.0
        elif "SPAM" in classification or "LEGITIMATE" in classification:
            confidence = 85.0
        else:
            confidence = 70.0
            # Default to spam if unclear (better safe than sorry)
            is_spam = True

        # Generate reasoning
        if is_spam:
            spam_indicators = []
            text_lower = transcript.lower()

            if any(word in text_lower for word in ["press 1", "press 2", "press one"]):
                spam_indicators.append("robocall button press request")
            if any(word in text_lower for word in ["warranty", "expire", "expiring"]):
                spam_indicators.append("warranty scam pattern")
            if any(word in text_lower for word in ["urgent", "immediately", "final notice"]):
                spam_indicators.append("urgency tactics")
            if any(word in text_lower for word in ["irs", "social security", "arrest"]):
                spam_indicators.append("government impersonation")
            if any(word in text_lower for word in ["prize", "winner", "congratulations", "won"]):
                spam_indicators.append("fake prize scam")

            if spam_indicators:
                reasoning = f"Detected spam indicators: {', '.join(spam_indicators)}"
            else:
                reasoning = "AI classified as spam based on language patterns"
        else:
            legit_indicators = []
            text_lower = transcript.lower()

            if any(word in text_lower for word in ["appointment", "confirming", "scheduled"]):
                legit_indicators.append("appointment confirmation")
            if any(word in text_lower for word in ["mom", "dad", "brother", "sister", "family"]):
                legit_indicators.append("family contact")
            if any(word in text_lower for word in ["delivery", "package", "amazon", "fedex", "ups"]):
                legit_indicators.append("delivery notification")
            if any(word in text_lower for word in ["doctor", "dr.", "office", "clinic"]):
                legit_indicators.append("medical/professional")

            if legit_indicators:
                reasoning = f"Legitimate call: {', '.join(legit_indicators)}"
            else:
                reasoning = "AI classified as legitimate based on conversational tone"

        return {
            "is_spam": is_spam,
            "confidence": confidence,
            "classification": "SPAM" if is_spam else "LEGITIMATE",
            "reasoning": reasoning,
            "model": MODEL
        }

    except Exception as e:
        # Fallback to pattern-based detection if API fails
        text_lower = transcript.lower()

        spam_score = 0
        if any(word in text_lower for word in ["press 1", "press 2", "press one"]):
            spam_score += 30
        if any(word in text_lower for word in ["warranty", "expire"]):
            spam_score += 25
        if any(word in text_lower for word in ["urgent", "immediately"]):
            spam_score += 20
        if any(word in text_lower for word in ["irs", "social security"]):
            spam_score += 35
        if any(word in text_lower for word in ["prize", "winner", "won"]):
            spam_score += 30

        is_spam = spam_score > 20
        confidence = min(spam_score + 50, 95) if is_spam else max(100 - spam_score, 60)

        return {
            "is_spam": is_spam,
            "confidence": float(confidence),
            "classification": "SPAM" if is_spam else "LEGITIMATE",
            "reasoning": f"Pattern-based detection (API fallback). Score: {spam_score}",
            "model": "Pattern-based fallback"
        }


if __name__ == "__main__":
    import uvicorn

    print("=" * 60)
    print("HamCaller - AI Spam Detection (Hugging Face)")
    print("=" * 60)
    print("Starting server on http://localhost:7860")
    print("=" * 60)

    uvicorn.run(app, host="0.0.0.0", port=7860)
