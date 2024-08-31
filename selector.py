import os
import json
import logging
from openai import OpenAI, APIConnectionError, APIError, APIStatusError

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

PROMPT_TEMPLATE = """
You are an advanced AI assistant specializing in protocol classification for financial and digital asset management tasks. Your role is to accurately determine the most appropriate protocol based on user input. Analyze the input carefully and select the best-matching protocol from the options below.

Available Protocols:
1. payments.py
2. vaults.py
3. token_tool.py
4. leasing.py
5. listing.py

User Input: "{user_input}"

Respond ONLY with a JSON object in the following format:
{{
 "Target": "<protocol_name>",
 "Prompt": "{user_input}"
}}
Where <protocol_name> is one of: payments.py, vaults.py, token_tool.py, leasing.py, listing.py.
"""

def determine_protocol(user_input: str) -> dict:
    try:
        prompt = PROMPT_TEMPLATE.format(user_input=user_input)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a specialized AI assistant for protocol classification."},
                {"role": "user", "content": prompt}
            ]
        )
        response_text = response.choices[0].message.content.strip()
        result = json.loads(response_text)
        if "Target" in result and "Prompt" in result:
            return result
        else:
            return {"error": "Invalid response format from AI"}
    except (APIConnectionError, APIStatusError, APIError) as e:
        return {"error": "API error occurred"}
    except Exception as e:
        return {"error": str(e)}

def main():
    try:
        import sys
        input_data = json.loads(sys.stdin.read())
        user_input = input_data.get("prompt")
        if not user_input:
            raise ValueError("No prompt provided in input")
        result = determine_protocol(user_input)
        print(json.dumps(result))
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON input: {str(e)}"}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == '__main__':
    main()
