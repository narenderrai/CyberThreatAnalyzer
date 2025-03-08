import os
import json
from openai import OpenAI


class GPTHelper:

    def __init__(self):
        # Get API key from environment or use default
        api_key = os.environ.get("OPENROUTER_API_KEY", 
                  "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")

        print("Using OpenRouter API")
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        self.openai_model = os.environ.get('OPENAI_MODEL',
                                           'deepseek/deepseek-r1:free')

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
            
            # Try to extract JSON from markdown code blocks if present
            if response_text.startswith("```json") and "```" in response_text:
                json_content = response_text.split("```json", 1)[1].split("```", 1)[0].strip()
                try:
                    return json.loads(json_content)
                except json.JSONDecodeError:
                    pass  # Fall back to the next parsing attempt
            
            # Try to parse the entire response as JSON
            try:
                return json.loads(response_text)
            except json.JSONDecodeError:
                # Return a structured response with the raw text
                return {
                    "attack_vector": "Analysis unavailable in structured format",
                    "timeline": "See raw analysis below",
                    "impact": "Review raw analysis for details",
                    "mitigation": "Review raw analysis for details",
                    "raw_analysis": response_text
                }
                
        except Exception as e:
            print(f"Error in OpenRouter request: {str(e)}")
            return {"error": f"Request failed: {str(e)}"}

    def analyze_threat(self, query, context=""):
        print(f"\nAnalyzing threat query: {query}")
        prompt = f"""You are a cybersecurity expert analyzing threat data. 
        Provide detailed, factual responses about cyber threats, attack vectors, and TTPs.
        
        Context: {context}
        Query: {query}
        
        Format your response as JSON with the following structure:
        {{
            "attack_vector": "Description of attack methods",
            "timeline": "Progression of the attack",
            "impact": "Potential consequences",
            "mitigation": "Recommended countermeasures"
        }}
        """

        return self._send_request(prompt)

    def tag_threat_data(self, data):
        print(f"\nTagging threat data: {data}")
        prompt = f"""Tag the following cyber threat data with relevant categories.
        
        Data to analyze: {data}
        
        Respond with ONLY a valid JSON object using this structure:
        {{
            "TTP": ["list", "of", "tactics"],
            "attack_vector": "Primary attack methods used",
            "threat_actor": "Identified threat actor or group",
            "target_sector": "Targeted industry or sector",
            "Severity Level": "One of: Low/Medium/High/Critical"
        }}
        """

        return self._send_request(prompt)
