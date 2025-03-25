import os
import json
from openai import OpenAI


class GPTHelper:

    def __init__(self):
        # Get API key from environment variable or prompt user if not found
        self.openai_api_key = os.environ.get("OPENROUTER_API_KEY")
        
        # Debug output to verify API key
        if self.openai_api_key:
            masked_key = self.openai_api_key[:4] + "..." + self.openai_api_key[-4:] if len(self.openai_api_key) > 8 else "***"
            print(f"Found OpenRouter API key: {masked_key}")
        else:
            print("WARNING: No OpenRouter API key found. API calls will fail.")
            print("Please set your OPENROUTER_API_KEY as an environment variable.")
            # Default key for initialization, but it won't work for actual API calls
            self.openai_api_key = "missing_key"

        print("Using OpenRouter API")
        # OpenRouter requires API key in Authorization header format
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.openai_api_key,
            default_headers={
                "HTTP-Referer": "https://replit.com/",
                "X-Title": "Cyber Threat Analysis Platform"
            }
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
            # The OpenAI client already has the API key set, no need for extra headers
            completion = self.client.chat.completions.create(
                model=self.openai_model,
                messages=[{
                    "role": "system",
                    "content": "You are a cybersecurity expert analyzing threat data."
                }, {
                    "role": "user",
                    "content": prompt
                }],
                temperature=0.3,
                max_tokens=1024)

            response_text = completion.choices[0].message.content.strip()
            print(f"Raw response from OpenRouter: {response_text}")
            
            # Try to parse as JSON
            try:
                json_response = json.loads(response_text)
                return {
                    "status": "success",
                    "format": "json",
                    "data": json_response
                }
            except json.JSONDecodeError:
                print(f"Failed to parse OpenRouter response as JSON, formatting as text")
                # Provide a structured fallback response
                # Parse the text response into structured format
                fallback_response = {
                    "attack_vectors": response_text[:200] + "..." if len(response_text) > 200 else response_text,
                    "ttps": {
                        "tactics": "Unable to extract specific tactics from unstructured response",
                        "techniques": "Unable to extract specific techniques from unstructured response",
                        "procedures": "Unable to extract specific procedures from unstructured response"
                    },
                    "iocs": "No IoCs extracted from unstructured response",
                    "cves": "No CVEs identified in unstructured response",
                    "attack_timeline": "Timeline could not be constructed from unstructured response",
                    "incident_reports": "No specific incidents identified in unstructured response",
                    "threat_intel": "Additional threat intelligence not available from unstructured response"
                }
                return {
                    "status": "success",
                    "format": "json",
                    "data": fallback_response
                }
        except Exception as e:
            print(f"Error in OpenRouter request: {str(e)}")
            return {
                "error": f"Request failed: {str(e)}",
                "raw_response": "",
                "setup_instructions": "Verify your OpenRouter API key is valid and properly configured."
            }

    
    # need to work on this function for prompt in order to get the right response.

    
    def analyze_threat(self, query, context=""):
        print(f"\nAnalyzing threat query: {query}")
        prompt = f"""You are a cybersecurity expert providing a detailed threat analysis.

        For the following query, analyze the threat and provide SPECIFIC, DETAILED information in this exact JSON structure:

        {{
            "attack_vectors": "Provide a DETAILED list of specific attack methods and pathways used (e.g., Spear phishing emails targeting finance department, Remote Desktop Protocol exploitation on port 3389, etc.)",
            "ttps": {{
                "tactics": "List SPECIFIC attacker objectives (e.g., Initial Access through phishing, Lateral Movement via compromised credentials, etc.)",
                "techniques": "List DETAILED attack techniques used (e.g., T1566.001 - Spearphishing Attachment, T1110 - Brute Force, etc.)",
                "procedures": "Step-by-step breakdown of the attack implementation (minimum 3 specific steps)"
            }},
            "iocs": "List ALL relevant indicators: IP addresses (e.g., 192.168.1.1), file hashes (e.g., a1b2c3...), domains (e.g., malicious-domain.com), email addresses, etc. If none known, state 'No verified IoCs available.'",
            "cves": "List specific CVE IDs and descriptions (e.g., CVE-2021-34527 - PrintNightmare). If none relevant, state 'No specific CVEs associated.'",
            "attack_timeline": "Provide a chronological breakdown of attack stages with specific timeframes or sequence of events. If theoretical, provide typical timeline.",
            "incident_reports": "Reference specific historical incidents related to this type of attack (e.g., 'Colonial Pipeline Ransomware Attack - May 2021'). If none relevant, state 'No specific incidents documented.'",
            "threat_intel": "Current threat landscape updates, active threat actors, or emerging trends related to this threat. Be specific."
        }}

        Query: {query}
        Context: {context}

        REQUIREMENTS:
        1. NEVER use placeholder text. Provide real, detailed technical information.
        2. NEVER leave any field empty or with generic responses.
        3. ALL responses must be security-focused and technically accurate.
        4. Include MITRE ATT&CK references where applicable.
        5. If information is truly not available for a field, provide a clear explanation why.
        6. Format lists as comma-separated strings.
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
