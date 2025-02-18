import os
import json
from google.cloud import aiplatform
import vertexai
from vertexai.language_models import TextGenerationModel

class GPTHelper:
    def __init__(self):
        # Initialize Vertex AI with project details
        vertexai.init(
            project=os.environ.get("GOOGLE_CLOUD_PROJECT"),
            location=os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
        )
        # Initialize PaLM 2 Text model
        self.model = TextGenerationModel.from_pretrained("text-bison@002")
        print("Initialized GPTHelper with Vertex AI PaLM 2 model")

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

            response = self.model.predict(
                prompt,
                temperature=0.3,
                max_output_tokens=1024,
            )

            try:
                return json.loads(response.text)
            except json.JSONDecodeError:
                # If response is not valid JSON, structure it manually
                return {
                    "error": "Response format error",
                    "raw_response": response.text
                }

        except Exception as e:
            print(f"Error in analyze_threat: {str(e)}")
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

            response = self.model.predict(
                prompt,
                temperature=0.3,
                max_output_tokens=512,
            )

            try:
                return json.loads(response.text)
            except json.JSONDecodeError:
                return {
                    "error": "Response format error",
                    "raw_response": response.text
                }

        except Exception as e:
            print(f"Error in tag_threat_data: {str(e)}")
            return {"error": f"Tagging failed: {str(e)}"}