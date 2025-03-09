import os
import json
from openai import OpenAI


class GPTHelper:

    def __init__(self):
        # Get API key from environment variable or use default
        self.openai_api_key = os.environ.get("OPENROUTER_API_KEY", "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")

        print("Using OpenRouter API")
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.openai_api_key,
        )
        # Set a default model for OpenRouter - this was causing the "No models provided" error
        self.openai_model = "deepseek/deepseek-coder:latest"

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

            response_text = completion.choices[0].message.content.strip()
            print(f"Raw response from OpenRouter: {response_text}")
            return json.loads(response_text)
        except json.JSONDecodeError:
            print(
                f"Failed to parse OpenRouter response as JSON: {response_text}"
            )
            return {
                "error": "Response format error",
                "raw_response": response_text
            }
        except Exception as e:
            print(f"Error in OpenRouter request: {str(e)}")
            return {"error": f"Request failed: {str(e)}"}

    def analyze_threat(self, query, context=""):
        print(f"\nAnalyzing threat query: {query}")
        prompt = f"""You are a cybersecurity expert analyzing threat data. 
        Provide detailed, factual responses about cyber threats, attack vectors, and TTPs.
        Format your response as JSON with the following structure:
        {{
            "attack_vector": "Description of attack methods",
            "timeline": "Progression of the attack",
            "impact": "Potential consequences",
            "mitigation": "Recommended countermeasures"
        }}

        Context: {context}
        Query: {query}

        Please provide your analysis in the specified JSON format.
        """

        return self._send_request(prompt)

    def tag_threat_data(self, data):
        print(f"\nTagging threat data: {data}")
        prompt = f"""Tag the following cyber threat data with relevant categories.
        Respond in JSON format with these fields: 
        {{
            "TTP": "List of tactics, techniques, and procedures",
            "attack_vector": "Primary attack methods used",
            "threat_actor": "Identified threat actor or group",
            "target_sector": "Targeted industry or sector",
            "Severity Level": "One of: Low/Medium/High/Critical"
        }}

        Data to analyze: {data}

        Provide your analysis in the specified JSON format.
        """

        return self._send_request(prompt)
