---
title: HamCaller
emoji: 📞
colorFrom: blue
colorPr: purple
sdk: docker
pinned: false
---

# HamCaller - AI Spam Call Detector

Protect yourself from spam calls with AI-powered detection. HamCaller analyzes phone call transcripts and identifies whether they're spam or legitimate.

## Features

- 🤖 **AI-Powered Detection** - Uses advanced language models to classify calls
- 📱 **iPhone Mockup UI** - Beautiful, modern interface with dark theme
- 🎤 **Speech-to-Text** - Record calls directly using your microphone
- ⚡ **Fast Analysis** - Get results in under 3 seconds
- 🎯 **High Accuracy** - Trained on 185+ real spam and legitimate call examples

## How to Use

1. **Enter a Transcript**: Paste or type a phone call transcript
2. **Or Record**: Click the microphone button to record speech
3. **Analyze**: Click "Analyze Call" to detect spam
4. **View Results**: See if it's spam or legitimate with confidence score

## Examples

### SPAM Calls
- "Your warranty is expiring soon. Press 1 to renew."
- "This is the IRS. You have outstanding tax debt."
- "Congratulations! You've won a free cruise."

### LEGITIMATE Calls
- "Hi mom, just checking in to see how you're doing."
- "This is Dr. Smith's office confirming your appointment tomorrow."
- "Your Amazon package is ready for pickup."

## Technology

- **Frontend**: HTML, CSS (Tailwind), JavaScript
- **Backend**: FastAPI
- **AI Model**: Mistral-7B via Hugging Face Inference API
- **Deployment**: Docker on Hugging Face Spaces

## Local Development

```bash
pip install -r requirements.txt
python app.py
```

Open http://localhost:7860

## Credits

Built with FastAPI and Hugging Face
