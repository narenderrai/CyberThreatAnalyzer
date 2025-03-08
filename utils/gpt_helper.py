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

        # Get raw response from OpenRouter (DeepSeek)
        response_text = completion.choices[0].message.content.strip()
        print(f"Raw response from OpenRouter: {response_text}")

        return response_text  # Return raw text response instead of parsing as JSON

    except Exception as e:
        print(f"Error in OpenRouter request: {str(e)}")
        return f"Error: {str(e)}"
