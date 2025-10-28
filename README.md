# HamCaller - AI Spam Call Detection 📞🛡️

[![Ollama](https://img.shields.io/badge/Ollama-Compatible-blue)](https://ollama.com)
[![Base Model](https://img.shields.io/badge/Base-Gemma3%201B-green)](https://ollama.com/library/gemma3)
[![License](https://img.shields.io/badge/License-Gemma%20Terms-red)](https://ai.google.dev/gemma/terms)

**Protect yourself from spam calls with AI.**

HamCaller uses a fine-tuned AI model to instantly classify phone call transcripts as **SPAM** or **LEGITIMATE**. 100% local processing - your data never leaves your device.

## 🚀 Quick Start

### One-Command Installation

**macOS/Linux:**
```bash
git clone https://github.com/ad2546/HamCaller.git
cd HamCaller
chmod +x install.sh run.sh
./install.sh
```

**Windows:**
```cmd
git clone https://github.com/ad2546/HamCaller.git
cd HamCaller
install.bat
```

The install script automatically:
- ✅ Installs Ollama (if not already installed)
- ✅ Downloads the Gemma 3 base model (815 MB)
- ✅ Creates the HamCaller fine-tuned model
- ✅ Installs Python dependencies
- ✅ Tests the installation

### Running the App

After installation:

**macOS/Linux:**
```bash
./run.sh
```

**Windows:**
```cmd
run.bat
```

Then open your browser to: **http://localhost:8000**

### Manual Installation (Advanced)

<details>
<summary>Click to expand manual installation steps</summary>

```bash
# 1. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Pull base model and create HamCaller
ollama pull gemma3:1b
ollama create hamcaller -f model/Modelfile

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Run the application
python3 app.py
```

Then open: **http://localhost:8000**

</details>

## 💻 Usage

### 🌐 Web Interface (Easiest)

1. Run `./run.sh` (or `run.bat` on Windows)
2. Open **http://localhost:8000** in your browser
3. Paste a call transcript
4. Click "Analyze Call"
5. Get instant **SPAM** or **LEGITIMATE** result with confidence score

![Web Interface](https://via.placeholder.com/800x400/0a0a0a/3b82f6?text=Modern+Dark+UI+with+iPhone+Mockup)

### 🖥️ Command Line

Test the model directly from your terminal:

```bash
ollama run hamcaller "Your car warranty is expiring. Press 1 to renew."
# Output: SPAM

ollama run hamcaller "Hi mom, just checking in to see how you're doing."
# Output: LEGITIMATE

ollama run hamcaller "This is Dr. Smith's office confirming your appointment."
# Output: LEGITIMATE
```

### 🐍 Python API

Integrate HamCaller into your Python projects:

```python
import subprocess

def detect_spam(transcript: str) -> dict:
    result = subprocess.run(
        ["ollama", "run", "hamcaller", transcript],
        capture_output=True,
        text=True,
        timeout=30
    )
    classification = result.stdout.strip()
    return {
        "is_spam": "SPAM" in classification.upper(),
        "classification": classification
    }

# Examples
print(detect_spam("You've won a free cruise!"))
# {'is_spam': True, 'classification': 'SPAM'}

print(detect_spam("Package delivery at 3pm"))
# {'is_spam': False, 'classification': 'LEGITIMATE'}
```

## 📊 What It Detects

### ❌ SPAM Calls (89% of training data)
- 🚗 **Extended warranty scams** - "Your car warranty is expiring..."
- 🏛️ **Fake IRS/government calls** - "This is the IRS, you owe..."
- 🎁 **Prize/lottery scams** - "You've won a free cruise..."
- 🤖 **Robocalls** - "Press 1 to renew...", "Press 2 to cancel..."
- 💻 **Tech support scams** - "Your computer has a virus..."
- 🎣 **Phishing attempts** - "Your account has been compromised..."
- 💰 **Debt collection scams** - "Final notice about your debt..."

### ✅ LEGITIMATE Calls (11% of training data)
- 🏥 **Medical appointments** - "Dr. Smith confirming your appointment..."
- 📦 **Delivery notifications** - "Your package is ready for pickup..."
- 👨‍👩‍👧 **Personal/family calls** - "Hi mom, just checking in..."
- 🏢 **Known business contacts** - "Your car is ready from the dealership..."
- 📧 **Service confirmations** - "Confirming your reservation..."
- 🏫 **School communications** - "Principal's office calling about..."

## 🔧 Technical Details

### Model Specifications
| Feature | Details |
|---------|---------|
| **Base Model** | Google Gemma 3 (1B parameters) |
| **Quantization** | Q4_K_M (optimized for speed & size) |
| **Model Size** | 815 MB |
| **Training Data** | 185 real-world phone call transcripts |
| **Training Split** | 165 SPAM (89%) / 20 LEGITIMATE (11%) |
| **Output Format** | Single word: "SPAM" or "LEGITIMATE" |
| **Inference Speed** | ~2-3 seconds per classification |
| **Context Window** | 32,768 tokens |

### Model Configuration
```yaml
temperature: 0.1      # Low for deterministic outputs
top_p: 0.9            # Nucleus sampling
top_k: 40             # Top-k sampling
repeat_penalty: 1.1   # Prevent repetition
```

### System Requirements
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 1GB for model files
- **Platform**: macOS, Linux, or Windows
- **Dependencies**: Python 3.8+, Ollama

## 📁 Project Structure

```
HamCaller/
├── model/Modelfile         # Ollama model definition
├── training_data/          # Training dataset (185 examples)
├── app.py                  # FastAPI web application
├── index.html              # Web UI
├── install.sh / .bat       # Installation scripts
├── run.sh / .bat           # Run scripts
└── requirements.txt        # Python dependencies
```

## 🔒 Privacy & Security

HamCaller prioritizes your privacy:

- 🔐 **100% Local Processing** - All AI inference runs on your device via Ollama
- 🚫 **Zero Data Collection** - No transcripts, logs, or analytics sent anywhere
- 🔑 **No API Keys** - No accounts, registrations, or cloud services required
- ✈️ **Completely Offline** - Works without internet after initial model download
- 🔓 **Open Source** - Full code transparency, audit the entire codebase

**Your call transcripts never leave your computer.**

## 🎯 Use Cases

- 📱 **Personal Protection** - Screen unknown calls before answering
- 🏢 **Business Training** - Train customer service teams on spam patterns
- 📚 **Education** - Teach AI classification and NLP concepts
- 🔬 **Research** - Study spam call linguistics and tactics
- 🛠️ **Integration** - Embed in phone systems, apps, or CRM tools

## ❓ FAQ

<details>
<summary><strong>Q: How accurate is HamCaller?</strong></summary>
<br>
HamCaller is trained on 185 real-world examples and uses pattern recognition to identify spam characteristics. While highly effective for common spam patterns, always use your judgment for important calls.
</details>

<details>
<summary><strong>Q: Does this work with audio files?</strong></summary>
<br>
Currently, HamCaller only accepts text transcripts. You'll need to transcribe audio separately (using tools like Whisper) before analysis.
</details>

<details>
<summary><strong>Q: Can I customize the model?</strong></summary>
<br>
Yes! Edit the <code>model/Modelfile</code> to adjust the system prompt or parameters, then run <code>ollama create hamcaller -f model/Modelfile</code> to rebuild.
</details>

<details>
<summary><strong>Q: Is my data private?</strong></summary>
<br>
Absolutely. Everything runs locally on your machine via Ollama. No data is sent to external servers. You can even use it offline after installation.
</details>

<details>
<summary><strong>Q: What languages are supported?</strong></summary>
<br>
Currently English only. The training data consists of English phone call transcripts. Multi-language support is on the roadmap.
</details>

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

- 🐛 Report bugs via [GitHub Issues](https://github.com/ad2546/HamCaller/issues)
- 💡 Suggest features or improvements
- 📝 Improve documentation
- 🧪 Add more training examples
- 🌍 Add support for other languages

## 📄 License

This project uses Google's Gemma 3 as the base model, which is subject to the [Gemma Terms of Use](https://ai.google.dev/gemma/terms).

## 🙏 Acknowledgments

- **Google DeepMind** - For the Gemma 3 model
- **Ollama** - For the amazing local LLM runtime
- **FastAPI** - For the fast web framework

---

**Made with ❤️ for safer phone calls**

*Star this repo if HamCaller helps protect you from spam! ⭐*
