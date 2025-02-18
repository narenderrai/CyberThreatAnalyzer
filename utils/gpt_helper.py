import os
import json
from huggingface_hub import InferenceClient

class GPTHelper:
    def __init__(self):
        self.client = InferenceClient(token=os.environ.get("HUGGINGFACE_API_KEY"))
        # Using OpenAssistant model which is free and optimized for chat
        self.model = "OpenAssistant/oasst-sft-6-llama-30b"

    def analyze_threat(self, query, context=""):
        try:
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

            response = self.client.text_generation(
                prompt,
                model=self.model,
                max_new_tokens=1024,
                temperature=0.3,
                return_full_text=False
            )

            try:
                return json.loads(response)
            except json.JSONDecodeError:
                # If response is not valid JSON, structure it manually
                return {
                    "error": "Response format error",
                    "raw_response": response
                }

        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}

    def tag_threat_data(self, data):
        try:
            prompt = f"""Tag the following cyber threat data with relevant categories.
            Respond in JSON format with these fields: 
            {{
                "TTP": "List of tactics, techniques, and procedures",
                "attack_vector": "Primary attack methods used",
                "threat_actor": "Identified threat actor or group",
                "target_sector": "Targeted industry or sector",
                "severity_level": "One of: Low/Medium/High/Critical"
            }}

            Data to analyze: {data}

            Provide your analysis in the specified JSON format.
            """

            response = self.client.text_generation(
                prompt,
                model=self.model,
                max_new_tokens=512,
                temperature=0.3,
                return_full_text=False
            )

            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return {
                    "error": "Response format error",
                    "raw_response": response
                }

        except Exception as e:
            return {"error": f"Tagging failed: {str(e)}"}