"""
HamCaller - AI-Powered Spam Call Detection
Simple frontend + LLM backend for detecting spam calls
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import subprocess
import uvicorn

app = FastAPI(title="HamCaller - AI Spam Detection")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class DetectRequest(BaseModel):
    transcript: str


class DetectResponse(BaseModel):
    classification: str  # SPAM or LEGITIMATE
    confidence: float
    is_spam: bool
    reasoning: str


# Simple spam detection using Ollama
def detect_spam(transcript: str) -> dict:
    """Detect if transcript is spam using LLM."""

    if len(transcript.strip()) < 5:
        return {
            "classification": "LEGITIMATE",
            "confidence": 50.0,
            "is_spam": False,
            "reasoning": "Too short to analyze"
        }

    # Optimized prompt
    prompt = f"""Classify this phone call as SPAM or LEGITIMATE.

SPAM = Unsolicited sales, scams, robocalls, threats, fake prizes, requests for money
LEGITIMATE = Personal calls, appointments, deliveries, known businesses, family/friends

Examples of SPAM:
- "Your warranty is expiring, press 1"
- "IRS calling about arrest warrant"
- "You won a prize, pay processing fee"

Examples of LEGITIMATE:
- "Hi mom, checking in"
- "Dr. Smith confirming appointment at 2 PM"
- "Delivery driver, can't find your apartment"

Call transcript: {transcript}

Answer with only one word - SPAM or LEGITIMATE:"""

    try:
        # Call Ollama
        result = subprocess.run(
            ["ollama", "run", "hamcaller", prompt],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            raise Exception(f"Ollama error: {result.stderr}")

        response = result.stdout.strip().upper()

        # Parse response
        if "SPAM" in response and "LEGITIMATE" not in response:
            classification = "SPAM"
            is_spam = True
            confidence = 85.0
        elif "LEGITIMATE" in response:
            classification = "LEGITIMATE"
            is_spam = False
            confidence = 85.0
        else:
            classification = "LEGITIMATE"
            is_spam = False
            confidence = 70.0

        return {
            "classification": classification,
            "confidence": confidence,
            "is_spam": is_spam,
            "reasoning": response[:100]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")


@app.post("/detect", response_model=DetectResponse)
async def detect(request: DetectRequest):
    """Detect if call transcript is spam."""
    result = detect_spam(request.transcript)
    return DetectResponse(**result)


@app.get("/")
async def root():
    """Serve frontend."""
    return FileResponse("index.html")


@app.get("/health")
async def health():
    """Health check."""
    return {"status": "ok", "model": "hamcaller via Ollama"}


if __name__ == "__main__":
    print("="*60)
    print("HamCaller - AI Spam Detection")
    print("="*60)
    print("Starting server on http://localhost:8000")
    print("Make sure Ollama is running: ollama serve")
    print("="*60)
    uvicorn.run(app, host="0.0.0.0", port=8000)
