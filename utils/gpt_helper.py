import os
import json
from openai import OpenAI

# Using xAI's Grok API instead of OpenAI for free access
class GPTHelper:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://api.x.ai/v1",
            api_key=os.environ.get("XAI_API_KEY")
        )

    def analyze_threat(self, query, context=""):
        try:
            response = self.client.chat.completions.create(
                model="grok-2-1212",  # Using Grok's latest model
                messages=[
                    {
                        "role": "system",
                        "content": "You are a cybersecurity expert analyzing threat data. "
                        "Provide detailed, factual responses about cyber threats, attack vectors, "
                        "and TTPs. Format responses with clear sections for Attack Vector, "
                        "Timeline, Impact, and Mitigation."
                    },
                    {
                        "role": "user",
                        "content": f"{context}\n\nQuery: {query}"
                    }
                ],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}

    def tag_threat_data(self, data):
        try:
            response = self.client.chat.completions.create(
                model="grok-2-1212",
                messages=[
                    {
                        "role": "system",
                        "content": "Tag the following cyber threat data with relevant "
                        "categories including: TTP, Attack Vector, Threat Actor, Target Sector, "
                        "and Severity Level (Low/Medium/High/Critical)."
                    },
                    {"role": "user", "content": data}
                ],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"error": f"Tagging failed: {str(e)}"}