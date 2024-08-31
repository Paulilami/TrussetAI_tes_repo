import os
import json
import logging
import re
from openai import OpenAI, APIConnectionError, APIError, APIStatusError

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

DEFAULT_CONFIG = {
    "Name": "Not defined",
    "Asset": "Not defined",
    "Asset Type": "Not defined",
    "Access Control": "Not defined",
    "Duration": "Not defined",
    "Penalty": "Not defined",
    "Input Payments": "Not defined",
    "Input Payments Frequency": "Not defined",
    "Input Payment Currency": "Not defined",
    "Output Payment Distribution": "Not defined",
    "Distribution Frequency": "Not defined",
    "Distribute to": "Not defined",
    "Vault Description": "No description",
    "Admin": "Creator",
    "Managers": "Not defined",
    "Manager Permissions": "Not defined"
}

PROMPT_TEMPLATE = """
You are an AI assistant specialized in configuring digital token vaults. Your job is to generate a well-structured vault configuration based on the user's input. Follow these guidelines strictly:

1. All fields default to "Not defined" unless explicitly specified by the user.
2. Do not infer information. Only update fields that the user clearly specifies in the input.
3. Your response must follow the exact field structure and order as defined below.
4. This may be a follow-up prompt. Only modify fields that the user explicitly mentions in their new input.

### Configuration Structure:
{protocol_fields}

### Current Configuration:
{current_config}

### User's Input:
{user_input}

### Instructions:
Based on the user's input, update only the fields directly related to the input. Return a single, well-structured JSON object with all fields included, even if they are unchanged.
"""

def validate_and_correct_config(config):
    corrected_config = DEFAULT_CONFIG.copy()
    for field in corrected_config:
        if field in config:
            corrected_config[field] = config[field] if config[field] != "Not defined" else "Not defined"
    return corrected_config

def create_or_update_vault(user_input: str, current_config: dict) -> dict:
    try:
        prompt = PROMPT_TEMPLATE.format(
            protocol_fields=json.dumps(DEFAULT_CONFIG, indent=2),
            current_config=json.dumps(current_config, indent=2),
            user_input=user_input
        )

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a specialized AI assistant for vault configurations."},
                {"role": "user", "content": prompt}
            ]
        )

        response_text = response.choices[0].message.content.strip()

        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            updated_config = json.loads(json_str)
            validated_config = validate_and_correct_config(updated_config)
            return validated_config
        else:
            return current_config

    except (APIConnectionError, APIStatusError, APIError) as e:
        return current_config
    except Exception as e:
        return current_config

def main():
    try:
        import sys
        data = json.loads(sys.stdin.read())
        user_input = data.get("prompt")
        current_config = data.get("current_config", DEFAULT_CONFIG.copy())

        updated_config = create_or_update_vault(user_input, current_config)

        print(json.dumps(updated_config))
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON input: {str(e)}"}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == '__main__':
    main()
