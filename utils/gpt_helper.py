import os
import json
from openai import OpenAI

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
MODEL_NAME = "gpt-4o"

class GPTHelper:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def analyze_threat(self, query, context=""):
        try:
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
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
                model=MODEL_NAME,
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
