# 📞 HamCaller - AI Spam Call Detector

<div align="center">

**Protect yourself from spam calls with AI-powered detection**

HamCaller analyzes phone call transcripts and identifies whether they're spam or legitimate using advanced language models.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

</div>

---

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

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | HTML, CSS (Tailwind), JavaScript |
| **Backend** | FastAPI |
| **AI Model** | Mistral-7B via Hugging Face Inference API |
| **Deployment** | Docker |

## 🚀 Local Development

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone https://github.com/ad2546/HamCaller.git
cd HamCaller
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:7860
```

## 🐳 Docker Deployment

```bash
docker build -t hamcaller .
docker run -p 7860:7860 hamcaller
```

## 📊 Model Training

The AI model is trained on 185+ real-world examples of spam and legitimate calls, achieving high accuracy in spam detection.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Credits

Built with [FastAPI](https://fastapi.tiangolo.com/) and [Hugging Face](https://huggingface.co/)

---

<div align="center">
Made with ❤️ for safer phone calls
</div>
