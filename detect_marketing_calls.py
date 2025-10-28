"""
Marketing Call Detection using Gemma 3 1B via Ollama.
Classifies call transcripts as marketing/spam calls or legitimate calls.
"""

import requests
import json
import argparse
from typing import Dict, List, Optional
from datetime import datetime
import re


class MarketingCallDetector:
    def __init__(
        self,
        model_name="gemma3:1b",
        ollama_url="http://localhost:11434",
        temperature=0.1
    ):
        """
        Initialize the marketing call detector using Ollama.

        Args:
            model_name: Name of the Ollama model to use
            ollama_url: URL of the Ollama API server
            temperature: Model temperature (lower = more consistent)
        """
        self.model_name = model_name
        self.ollama_url = ollama_url
        self.api_endpoint = f"{ollama_url}/api/generate"
        self.temperature = temperature

        print(f"Initializing Marketing Call Detector")
        print(f"Model: {model_name}")
        print(f"Ollama URL: {ollama_url}")

        # Test connection
        self._test_connection()

    def _test_connection(self):
        """Test connection to Ollama server."""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags")
            if response.status_code == 200:
                print("Connected to Ollama server successfully!")
            else:
                print(f"Warning: Ollama server responded with status {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("Error: Cannot connect to Ollama server.")
            print("   Make sure Ollama is running: 'ollama serve'")
            raise

    def create_detection_prompt(self, transcript: str) -> str:
        """
        Create a prompt for the model to detect marketing calls.

        Args:
            transcript: Call transcript text

        Returns:
            Formatted prompt for the model
        """
        prompt = f"""You are an expert at analyzing phone call transcripts to identify marketing and spam calls.

Analyze the following call transcript and determine if it is a MARKETING/SPAM call or a LEGITIMATE call.

Marketing/Spam call indicators:
- Unsolicited sales pitches
- Offers for products/services not requested
- Time-share, vacation packages, extended warranties
- Debt reduction or loan offers
- Political campaigns or surveys
- Charity solicitations from unknown organizations
- Prize or sweepstakes notifications
- Robocalls with automated messages
- Pressure tactics or urgency to act now
- Requests for personal/financial information upfront

Legitimate call indicators:
- Calls from known contacts or organizations
- Appointment reminders from doctors, dentists, etc.
- Delivery notifications
- Customer service callbacks
- Banking security alerts (from verified sources)
- Emergency or important personal calls

CALL TRANSCRIPT:
{transcript}



INSTRUCTIONS:
1. Analyze the transcript carefully
2. Identify key indicators
3. Provide a classification: MARKETING or LEGITIMATE
4. Provide a confidence score (0-100)
5. Explain your reasoning briefly

RESPONSE FORMAT (JSON):
{{
    "classification": "MARKETING" or "LEGITIMATE",
    "confidence": <0-100>,
    "reasoning": "<brief explanation>",
    "key_indicators": ["<indicator1>", "<indicator2>", ...]
}}

Respond ONLY with valid JSON in the exact format above."""

        return prompt

    def parse_model_response(self, response_text: str) -> Dict:
        """
        Parse the model's response and extract structured data.

        Args:
            response_text: Raw response from the model

        Returns:
            Parsed response dictionary
        """
        try:
            # Try to find JSON in the response
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                result = json.loads(json_match.group())

                # Validate required fields
                required_fields = ["classification", "confidence", "reasoning"]
                for field in required_fields:
                    if field not in result:
                        raise ValueError(f"Missing required field: {field}")

                # Normalize classification
                result["classification"] = result["classification"].upper()
                if result["classification"] not in ["MARKETING", "LEGITIMATE"]:
                    # Try to infer from reasoning
                    if any(word in response_text.upper() for word in ["MARKETING", "SPAM", "SCAM"]):
                        result["classification"] = "MARKETING"
                    else:
                        result["classification"] = "LEGITIMATE"

                # Ensure confidence is numeric
                result["confidence"] = float(result["confidence"])

                # Add key indicators if missing
                if "key_indicators" not in result:
                    result["key_indicators"] = []

                return result
            else:
                # Fallback parsing if no JSON found
                return self._fallback_parse(response_text)

        except (json.JSONDecodeError, ValueError) as e:
            print(f"Warning: Could not parse JSON response: {e}")
            return self._fallback_parse(response_text)

    def _fallback_parse(self, response_text: str) -> Dict:
        """Fallback parsing when JSON extraction fails."""
        text_upper = response_text.upper()

        # Determine classification
        is_marketing = any(word in text_upper for word in [
            "MARKETING", "SPAM", "SCAM", "UNSOLICITED",
            "SALES PITCH", "TELEMARKETER"
        ])

        # Extract confidence if present
        confidence_match = re.search(r'(\d+)%|\bconfidence[:\s]+(\d+)', response_text, re.IGNORECASE)
        confidence = 75  # default
        if confidence_match:
            confidence = int(confidence_match.group(1) or confidence_match.group(2))

        return {
            "classification": "MARKETING" if is_marketing else "LEGITIMATE",
            "confidence": confidence,
            "reasoning": response_text[:200] + "..." if len(response_text) > 200 else response_text,
            "key_indicators": []
        }

    def detect(self, transcript: str, verbose: bool = False) -> Dict:
        """
        Detect if a call transcript is a marketing call.

        Args:
            transcript: Call transcript text
            verbose: Whether to print detailed information

        Returns:
            Detection result dictionary
        """
        if verbose:
            print(f"\nAnalyzing transcript...")

        # Create prompt
        prompt = self.create_detection_prompt(transcript)

        # Call Ollama API
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "temperature": self.temperature
        }

        try:
            response = requests.post(
                self.api_endpoint,
                json=payload,
                timeout=60
            )
            response.raise_for_status()

            # Parse response
            ollama_response = response.json()
            model_output = ollama_response.get("response", "")

            if verbose:
                print(f"\nRaw model response:")
                print(model_output)

            # Parse the structured response
            result = self.parse_model_response(model_output)

            # Add metadata
            result["transcript_preview"] = transcript[:150] + "..." if len(transcript) > 150 else transcript
            result["model_used"] = self.model_name
            result["timestamp"] = datetime.now().isoformat()
            result["is_marketing"] = result["classification"] == "MARKETING"

            return result

        except requests.exceptions.RequestException as e:
            print(f"Error calling Ollama API: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    def detect_batch(self, transcripts: List[str], verbose: bool = False) -> List[Dict]:
        """
        Detect marketing calls for multiple transcripts.

        Args:
            transcripts: List of call transcript texts
            verbose: Whether to print progress

        Returns:
            List of detection results
        """
        results = []
        total = len(transcripts)

        print(f"\nProcessing {total} transcripts...")

        for i, transcript in enumerate(transcripts, 1):
            if verbose or total > 1:
                print(f"\n[{i}/{total}] Processing transcript {i}...")

            try:
                result = self.detect(transcript, verbose=verbose)
                results.append(result)

                # Show brief summary
                status = "MARKETING" if result["is_marketing"] else "LEGITIMATE"
                print(f"  {status} (Confidence: {result['confidence']}%)")

            except Exception as e:
                print(f"  Error processing transcript {i}: {e}")
                results.append({
                    "classification": "ERROR",
                    "confidence": 0,
                    "reasoning": str(e),
                    "is_marketing": False,
                    "error": True
                })

        return results

    def display_result(self, result: Dict):
        """Display result in a formatted way."""
        print("\n" + "=" * 70)
        print("MARKETING CALL DETECTION RESULT")
        print("=" * 70)

        print(f"\nTranscript Preview:")
        print(f"   {result.get('transcript_preview', 'N/A')}")

        classification = result["classification"]
        confidence = result["confidence"]

        print(f"\nClassification: {classification}")
        print(f"Confidence: {confidence}%")

        # Confidence bar
        bar_length = int(confidence * 40 / 100)
        bar = "█" * bar_length + "░" * (40 - bar_length)
        print(f"   [{bar}]")

        if result.get("key_indicators"):
            print(f"\n🔑 Key Indicators:")
            for indicator in result["key_indicators"]:
                print(f"   • {indicator}")

        print(f"\n💭 Reasoning:")
        reasoning_lines = result["reasoning"].split('\n')
        for line in reasoning_lines[:5]:  # Show first 5 lines
            if line.strip():
                print(f"   {line.strip()}")

        # Warning if marketing call
        if result.get("is_marketing"):
            print(f"\n⚠️  WARNING: This appears to be a MARKETING/SPAM call!")
            print(f"   Recommendation: Block this number or hang up immediately.")
        else:
            print(f"\n✅ This appears to be a LEGITIMATE call.")

        print("\n" + "=" * 70 + "\n")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Marketing Call Detection using Gemma 3 1B")
    parser.add_argument(
        "--transcript",
        type=str,
        help="Call transcript text to analyze"
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Path to file containing transcript"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gemma3:1b",
        help="Ollama model name (default: gemma3:1b)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output"
    )

    args = parser.parse_args()

    # Initialize detector
    detector = MarketingCallDetector(model_name=args.model)

    # Interactive mode
    if args.interactive:
        print("\n📞 INTERACTIVE MARKETING CALL DETECTION")
        print("=" * 70)
        print("Enter call transcript (type 'quit' to exit, 'example' for samples)")
        print("=" * 70 + "\n")

        while True:
            try:
                print("📝 Enter call transcript:")
                transcript = input("> ")

                if transcript.lower() == 'quit':
                    print("👋 Goodbye!")
                    break

                if transcript.lower() == 'example':
                    # Show example transcripts
                    examples = get_example_transcripts()
                    for i, example in enumerate(examples, 1):
                        print(f"\n--- Example {i}: {example['label']} ---")
                        print(example['transcript'][:200] + "...")

                    print("\nEnter the number of the example to analyze (or any other text):")
                    choice = input("> ")
                    try:
                        idx = int(choice) - 1
                        if 0 <= idx < len(examples):
                            transcript = examples[idx]['transcript']
                        else:
                            continue
                    except ValueError:
                        continue

                if transcript.strip():
                    result = detector.detect(transcript, verbose=args.verbose)
                    detector.display_result(result)

            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")

    # Single transcript
    elif args.transcript:
        result = detector.detect(args.transcript, verbose=args.verbose)
        detector.display_result(result)

    # File input
    elif args.file:
        try:
            with open(args.file, "r") as f:
                transcript = f.read()
            result = detector.detect(transcript, verbose=args.verbose)
            detector.display_result(result)
        except FileNotFoundError:
            print(f"❌ Error: File '{args.file}' not found")
        except Exception as e:
            print(f"❌ Error reading file: {e}")

    # Default: run examples
    else:
        print("\n📞 MARKETING CALL DETECTION - EXAMPLE ANALYSIS")
        print("=" * 70)

        examples = get_example_transcripts()

        for i, example in enumerate(examples, 1):
            print(f"\n{'=' * 70}")
            print(f"📞 Example {i}: {example['label']}")
            print('=' * 70)

            result = detector.detect(example['transcript'], verbose=args.verbose)
            detector.display_result(result)

        print("\n💡 TIP: Use --interactive flag for interactive mode")
        print("   Or use --transcript \"your transcript\" to analyze specific text")
        print("   Or use --file path/to/transcript.txt to analyze from a file")


def get_example_transcripts() -> List[Dict]:
    """Get example call transcripts for testing."""
    return [
        {
            "label": "Marketing Call - Extended Warranty",
            "transcript": """
            Hello! This is Jennifer calling about your vehicle's extended warranty.
            Our records show that your car's warranty is about to expire, and we want
            to offer you an exclusive opportunity to extend your coverage. This is a
            limited time offer, and if you don't act today, you may lose this chance
            to protect your investment. Can I ask you about your vehicle? We have
            several packages available starting at just $49.99 per month. Press 1 to
            speak with a specialist or press 2 to be removed from our list.
            """
        },
        {
            "label": "Marketing Call - Timeshare Offer",
            "transcript": """
            Congratulations! You've been selected to receive a complimentary 3-day,
            2-night stay at our luxury resort in Cancun! This is an exclusive offer
            for valued members like yourself. There's absolutely no cost, you just
            need to attend a brief 90-minute presentation about our vacation ownership
            opportunities. This is a $1,500 value completely free! But you must claim
            this offer within the next 48 hours. Can I get your email address to send
            you the confirmation details?
            """
        },
        {
            "label": "Legitimate Call - Doctor Appointment",
            "transcript": """
            Hi, this is Sarah from Dr. Johnson's office calling to confirm your
            appointment tomorrow at 2:30 PM. We just wanted to make sure you're still
            able to make it. If you need to reschedule, please give us a call back
            at 555-0123. Also, please remember to bring your insurance card and
            arrive 15 minutes early to fill out any updated paperwork. Thanks, and
            we'll see you tomorrow!
            """
        },
        {
            "label": "Legitimate Call - Package Delivery",
            "transcript": """
            Hello, this is Mike from FedEx. I'm calling about a package delivery
            to your address at 123 Main Street. I attempted delivery this morning
            but no one was home. The package requires a signature. I can try again
            tomorrow between 10 AM and 2 PM, or you can pick it up at our facility
            at 456 Oak Avenue. The tracking number is FX123456789. Please let me
            know which option works better for you.
            """
        },
        {
            "label": "Marketing Call - Debt Consolidation",
            "transcript": """
            Good afternoon! I'm calling from National Debt Solutions. We've been
            reviewing your financial profile, and I have some exciting news. You
            may qualify for our debt consolidation program that could reduce your
            monthly payments by up to 50 percent! We've helped thousands of people
            get out of debt faster. This is completely legal and IRS approved. I just
            need to verify a few pieces of information to see if you qualify. Can I
            ask how much total debt you're currently carrying?
            """
        },
        {
            "label": "Legitimate Call - Bank Security",
            "transcript": """
            Hello, this is the fraud department from First National Bank. We've
            detected some unusual activity on your checking account ending in 4567.
            There were three transactions this morning that we need to verify with
            you. For your security, please call us back at the number on the back
            of your debit card - that's 1-800-555-BANK. Please do not provide any
            information until you've verified this call by calling the official
            number. Thank you.
            """
        }
    ]


if __name__ == "__main__":
    main()
