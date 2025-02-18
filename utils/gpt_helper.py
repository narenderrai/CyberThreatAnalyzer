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

            if not project_id:
                raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")

            print(f"Initializing Vertex AI with Project ID: {project_id}")
            print(f"Google Cloud Location: {location}")
            print(f"Credentials path: {os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')}")

            # Initialize Vertex AI
            vertexai.init(project=project_id, location=location)

            # Initialize the Generative AI model
            self.model = GenerativeModel("gemini-pro")
            print(f"Successfully initialized GPTHelper with Google Cloud Vertex AI")
        except Exception as e:
            print(f"Error initializing Vertex AI: {str(e)}")
            raise

    def analyze_threat(self, query, context=""):
        try:
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

            print("Sending request to Vertex AI...")
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.3,
                    "max_output_tokens": 1024,
                }
            )
            print(f"Raw response from Vertex AI: {response.text}")

            try:
                return json.loads(response.text)
            except json.JSONDecodeError:
                print(f"Failed to parse response as JSON: {response.text}")
                return {
                    "error": "Response format error",
                    "raw_response": response.text
                }

        except Exception as e:
            print(f"Error in analyze_threat: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}

    def tag_threat_data(self, data):
        try:
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

            print("Sending request to Vertex AI for tagging...")
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.3,
                    "max_output_tokens": 512,
                }
            )
            print(f"Raw tagging response from Vertex AI: {response.text}")

            try:
                return json.loads(response.text)
            except json.JSONDecodeError:
                print(f"Failed to parse tagging response as JSON: {response.text}")
                return {
                    "error": "Response format error",
                    "raw_response": response.text
                }

        except Exception as e:
            print(f"Error in tag_threat_data: {str(e)}")
            return {"error": f"Tagging failed: {str(e)}"}