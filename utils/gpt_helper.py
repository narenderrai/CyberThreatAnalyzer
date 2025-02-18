import os
import json
from google.cloud import aiplatform
import vertexai
from vertexai.generative_models import GenerativeModel

class GPTHelper:
    def __init__(self):
        try:
            # Initialize Vertex AI with project details
            project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
            location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

            # Initialize Vertex AI
            vertexai.init(project=project_id, location=location)

            # Initialize the Generative AI model
            self.model = GenerativeModel("gemini-pro")
            print(f"Initialized GPTHelper with Google Cloud Vertex AI (Project: {project_id})")
        except Exception as e:
            print(f"Error initializing Vertex AI: {str(e)}")
            raise

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

            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.3,
                    "max_output_tokens": 1024,
                }
            )

            try:
                return json.loads(response.text)
            except json.JSONDecodeError:
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
                "Severity Level": "One of: Low/Medium/High/Critical"
            }}

            Data to analyze: {data}

            Provide your analysis in the specified JSON format.
            """

            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.3,
                    "max_output_tokens": 512,
                }
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