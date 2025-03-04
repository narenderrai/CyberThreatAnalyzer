import os
import json
import random
from datetime import datetime
from google.cloud import aiplatform
import vertexai
from vertexai.generative_models import GenerativeModel

class GPTHelper:
    def __init__(self):
        project_id = os.environ.get('GOOGLE_CLOUD_PROJECT')
        if not project_id:
            print("GOOGLE_CLOUD_PROJECT environment variable not set, using mock mode")
            self.mock_mode = True
        else:
            self.mock_mode = False
            vertexai.init(project=project_id)
            self.model = GenerativeModel("gemini-pro")
    
    def analyze_threat(self, query):
        if self.mock_mode:
            return self._generate_mock_response(query)
        
        # Real implementation would go here
        response = self.model.generate_content(query)
        return response.text
    
    def tag_threat_data(self, response_text):
        if self.mock_mode:
            return self._generate_mock_tags()
        
        # Real implementation would go here
        # This would use the model to generate tags based on the response
        prompt = f"Extract threat intelligence tags from this text: {response_text}"
        response = self.model.generate_content(prompt)
        # Parse the response to extract tags
        # This is a placeholder and should be implemented based on actual response format
        return json.loads(response.text) if response.text else {}
    
    def _generate_mock_response(self, query):
        mock_responses = [
            f"Analysis of '{query}': This appears to be a sophisticated phishing campaign targeting financial institutions.",
            f"Regarding '{query}': Evidence suggests this is a ransomware attack with similarities to previous campaigns by APT29.",
            f"Investigation of '{query}': The indicators point to a supply chain attack affecting multiple organizations.",
            f"Threat intelligence on '{query}': This matches patterns of a zero-day vulnerability exploitation in common web frameworks."
        ]
        return random.choice(mock_responses)
    
    def _generate_mock_tags(self):
        severity_levels = ["Low", "Medium", "High", "Critical"]
        attack_vectors = ["Phishing", "Ransomware", "Supply Chain", "Zero-day", "Social Engineering"]
        threat_actors = ["APT29", "Lazarus Group", "Sandworm", "Unknown"]
        
        return {
            "Severity Level": random.choice(severity_levels),
            "Attack Vector": random.choice(attack_vectors),
            "Threat Actor": random.choice(threat_actors),
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Confidence": f"{random.randint(60, 95)}%"
        }

class GPTHelper:
    def __init__(self):
        try:
            # Initialize Vertex AI with project details
            project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
            location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")

            if not project_id:
                print("GOOGLE_CLOUD_PROJECT environment variable not set, using mock mode")
                self.use_mock = True
                return

            print(f"Initializing Vertex AI with Project ID: {project_id}")
            print(f"Google Cloud Location: {location}")
            print(f"Credentials path: {os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')}")

            # Initialize Vertex AI
            vertexai.init(project=project_id, location=location)

            # Initialize the Generative AI model
            self.model = GenerativeModel("gemini-pro")
            self.use_mock = False
            print(f"Successfully initialized GPTHelper with Google Cloud Vertex AI")
        except Exception as e:
            print(f"Error initializing Vertex AI: {str(e)}, using mock mode")
            self.use_mock = True

    def analyze_threat(self, query, context=""):
        try:
            print(f"\nAnalyzing threat query: {query}")
            
            if hasattr(self, 'use_mock') and self.use_mock:
                print("Using mock response for threat analysis")
                # Return a mock response based on the query
                if "ransomware" in query.lower():
                    return {
                        "attack_vector": "Email phishing with malicious attachments, vulnerable RDP, and software exploits",
                        "timeline": "Initial access -> Privilege escalation -> Lateral movement -> Data exfiltration -> Encryption -> Ransom demand",
                        "impact": "Data loss, operational disruption, financial costs, reputational damage",
                        "mitigation": "Regular backups, email filtering, patch management, network segmentation, end-user training"
                    }
                elif "phishing" in query.lower():
                    return {
                        "attack_vector": "Deceptive emails, fake websites, social engineering tactics",
                        "timeline": "Preparation -> Distribution -> User interaction -> Credential theft -> Account compromise",
                        "impact": "Data theft, unauthorized access, financial fraud, malware infection",
                        "mitigation": "Email filtering, user awareness training, MFA, URL filtering, security monitoring"
                    }
                else:
                    return {
                        "attack_vector": "Multiple entry points including social engineering, exploiting vulnerabilities, and insider threats",
                        "timeline": "Reconnaissance -> Initial access -> Establish foothold -> Privilege escalation -> Objective completion",
                        "impact": "Data breaches, service disruption, financial loss, compliance violations",
                        "mitigation": "Defense in depth strategy, regular patching, security monitoring, incident response planning"
                    }
            
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
            
            if hasattr(self, 'use_mock') and self.use_mock:
                print("Using mock response for threat tagging")
                # Generate mock tags based on the provided data
                if isinstance(data, str):
                    if "ransomware" in data.lower():
                        severity = "Critical"
                    elif "phishing" in data.lower():
                        severity = "Medium"
                    else:
                        severity = "High"
                        
                    return {
                        "TTP": "Initial Access, Execution, Persistence, Privilege Escalation, Defense Evasion",
                        "attack_vector": "Email Phishing, Vulnerability Exploitation, Social Engineering",
                        "threat_actor": "Unknown threat actor",
                        "target_sector": "Multiple sectors including Finance, Healthcare, and Government",
                        "Severity Level": severity
                    }
                else:
                    # For structured data (dict), try to extract information
                    severity = "Medium"
                    if isinstance(data, dict):
                        attack_vector = data.get("attack_vector", "")
                        if "ransomware" in str(attack_vector).lower():
                            severity = "Critical"
                        elif "phishing" in str(attack_vector).lower():
                            severity = "Medium"
                            
                    return {
                        "TTP": "Initial Access, Execution, Data Exfiltration",
                        "attack_vector": "Multiple vectors based on opportunity",
                        "threat_actor": "Advanced Persistent Threat (APT)",
                        "target_sector": "Cross-sector targeting",
                        "Severity Level": severity
                    }
            
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