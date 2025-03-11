import os
import json
from openai import OpenAI


class GPTHelper:

    def __init__(self):
        # Get API key from environment variable or prompt user if not found
        self.openai_api_key = os.environ.get("OPENROUTER_API_KEY")
        
        if not self.openai_api_key:
            print("WARNING: No OpenRouter API key found. API calls will fail.")
            print("Please set your OPENROUTER_API_KEY as an environment variable.")
            # Default key for initialization, but it won't work for actual API calls
            self.openai_api_key = "missing_key"

        print("Using OpenRouter API")
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.openai_api_key,
        )
        # Set a default model for OpenRouter - this was causing the "No models provided" error
        self.openai_model = "deepseek/deepseek-r1-zero:free"

    def _send_request(self, prompt):
        if not self.openai_api_key or self.openai_api_key == "missing_key":
            return {
                "error": "OpenRouter API key not set. Please set the OPENROUTER_API_KEY environment variable.",
                "raw_response": "",
                "setup_instructions": "Go to Secrets Tool in Replit and add your OPENROUTER_API_KEY"
            }
            
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

            response_text = completion.choices[0].message.content.strip()
            print(f"Raw response from OpenRouter: {response_text}")
            
            # Try to parse as JSON, but return formatted text if it fails
            try:
                return json.loads(response_text)
            except json.JSONDecodeError:
                print(f"Failed to parse OpenRouter response as JSON, displaying as text")
                # Create a structured response with text sections
                return {
                    "Analysis": response_text,
                    "Note": "Response was not in JSON format as requested, showing raw text instead."
                }
        except Exception as e:
            print(f"Error in OpenRouter request: {str(e)}")
            return {
                "error": f"Request failed: {str(e)}",
                "raw_response": "",
                "setup_instructions": "Verify your OpenRouter API key is valid and properly configured."
            }

    def analyze_threat(self, query, context=""):
        print(f"\nAnalyzing threat query: {query}")
        prompt = f"""You are a cybersecurity expert analyzing threat data. 
        Provide detailed, factual responses about cyber threats, attack vectors, and TTPs.
        
        IMPORTANT: Your response MUST be in valid JSON format with the following structure:
        {{
            "attack_vector": "Description of attack methods",
            "timeline": "Progression of the attack",
            "impact": "Potential consequences",
            "mitigation": "Recommended countermeasures"
        }}

        Context: {context}
        Query: {query}

        IMPORTANT: Ensure your response is valid JSON that can be parsed with json.loads(). Do not include markdown, backticks, or any text outside of the JSON structure.
        """

        return self._send_request(prompt)

    def tag_threat_data(self, data):
        print(f"\nTagging threat data: {data}")
        prompt = f"""Tag the following cyber threat data with relevant categories.
        
        IMPORTANT: Your response MUST be in valid JSON format with these fields: 
        {{
            "TTP": "List of tactics, techniques, and procedures",
            "attack_vector": "Primary attack methods used",
            "threat_actor": "Identified threat actor or group",
            "target_sector": "Targeted industry or sector",
            "Severity Level": "One of: Low/Medium/High/Critical"
        }}

        Data to analyze: {data}

        IMPORTANT: Ensure your response is valid JSON that can be parsed with json.loads(). Do not include markdown, backticks, or any text outside of the JSON structure.
        """

        return self._send_request(prompt)
