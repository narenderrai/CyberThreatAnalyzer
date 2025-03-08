
import os
from openai import OpenAI

class GPTHelper:
    def __init__(self):
        api_key = os.environ.get("OPENROUTER_API_KEY", "demo")
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        self.openai_model = os.environ.get("OPENAI_MODEL", "openai/gpt-3.5-turbo")
    
    def _send_request(self, prompt):
        try:
            print(f"Sending request to OpenRouter ({self.openai_model})...")
            completion = self.client.chat.completions.create(
                model=self.openai_model,
                messages=[{
                    "role":
                    "system",
                    "content":
                    "You are a cybersecurity expert analyzing threat data."
                }, {
                    "role": "user",
                    "content": prompt
                }],
                temperature=0.3,
                max_tokens=1024,
                extra_headers={
                    "HTTP-Referer": os.environ.get("YOUR_SITE_URL", ""),
                    "X-Title": os.environ.get("YOUR_SITE_NAME", "")
                },
                extra_body={})

            # Get raw response from OpenRouter (DeepSeek)
            response_text = completion.choices[0].message.content.strip()
            print(f"Raw response from OpenRouter: {response_text}")

            return response_text  # Return raw text response instead of parsing as JSON

        except Exception as e:
            print(f"Error in OpenRouter request: {str(e)}")
            return f"Error: {str(e)}"
            
    def analyze_threat(self, query):
        """Analyze the threat based on the provided query"""
        return self._send_request(query)
        
    def tag_threat_data(self, response_text):
        """Extract tags from the response text"""
        # For simplicity, let's extract some basic tags
        tags = {
            "Severity Level": "Medium"  # Default value
        }
        
        # Simple logic to estimate severity based on keywords
        severity_indicators = {
            "Critical": ["critical", "severe", "high-risk", "immediate action"],
            "High": ["high", "significant", "important", "serious"],
            "Medium": ["medium", "moderate", "average"],
            "Low": ["low", "minor", "minimal", "small"]
        }
        
        # Check for severity indicators
        for level, keywords in severity_indicators.items():
            for keyword in keywords:
                if keyword.lower() in response_text.lower():
                    tags["Severity Level"] = level
                    break
        
        # Add other tags based on content
        if "ransomware" in response_text.lower():
            tags["Attack Type"] = "Ransomware"
        elif "phishing" in response_text.lower():
            tags["Attack Type"] = "Phishing"
        elif "malware" in response_text.lower():
            tags["Attack Type"] = "Malware"
            
        return tags
