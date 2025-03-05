import os
import json
import openai

class GPTHelper:
    def __init__(self):
        # Check for OpenAI API key in environment
        self.openai_api_key = os.environ.get('OPENAI_API_KEY')
        if self.openai_api_key:
            print("Using OpenAI GPT model")
            openai.api_key = self.openai_api_key
            # Default to GPT-3.5-turbo, but can be configured via env var
            self.openai_model = os.environ.get('OPENAI_MODEL', 'gpt-3.5-turbo')
            self.use_mock = False
        else:
            print("OPENAI_API_KEY environment variable not set, using mock mode")
            self.use_mock = True

    def analyze_threat(self, query, context=""):
        try:
            print(f"\nAnalyzing threat query: {query}")

            if self.use_mock:
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

            print(f"Sending request to OpenAI ({self.openai_model})...")
            completion = openai.chat.completions.create(
                model=self.openai_model,
                messages=[
                    {"role": "system", "content": "You are a cybersecurity expert analyzing threat data."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1024
            )

            response_text = completion.choices[0].message.content
            print(f"Raw response from OpenAI: {response_text}")

            try:
                return json.loads(response_text)
            except json.JSONDecodeError:
                print(f"Failed to parse OpenAI response as JSON: {response_text}")
                return {
                    "error": "Response format error",
                    "raw_response": response_text
                }

        except Exception as e:
            print(f"Error in analyze_threat: {str(e)}")
            return {"error": f"Analysis failed: {str(e)}"}

    def tag_threat_data(self, data):
        try:
            print(f"\nTagging threat data: {data}")

            if self.use_mock:
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

            print(f"Sending request to OpenAI ({self.openai_model}) for tagging...")
            completion = openai.chat.completions.create(
                model=self.openai_model,
                messages=[
                    {"role": "system", "content": "You are a cybersecurity expert analyzing threat data."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=512
            )

            response_text = completion.choices[0].message.content
            print(f"Raw tagging response from OpenAI: {response_text}")

            try:
                return json.loads(response_text)
            except json.JSONDecodeError:
                print(f"Failed to parse OpenAI tagging response as JSON: {response_text}")
                return {
                    "error": "Response format error",
                    "raw_response": response_text
                }

        except Exception as e:
            print(f"Error in tag_threat_data: {str(e)}")
            return {"error": f"Tagging failed: {str(e)}"}