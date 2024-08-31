import json
import re
from flask import Flask

def is_valid_input(user_input):
    return bool(re.match(r'^[\w\s.,!?-]*$', user_input.strip()))

def determine_protocol(user_input):
    prompt = user_input.lower()
    if "payment" in prompt or "dividend" in prompt or "stream" in prompt:
        return "payments.py"
    elif "vault" in prompt or "lockup" in prompt:
        return "vaults.py"
    elif "token" in prompt or "mint" in prompt or "asset" in prompt:
        return "token_tool.py"
    elif "lease" in prompt or "rent" in prompt:
        return "leasing.py"
    elif "list" in prompt or "sale" in prompt:
        return "listing.py"
    return None

def orchestrate(user_input):
    if not is_valid_input(user_input):
        return {"error": "Invalid input format"}
    
    protocol = determine_protocol(user_input)
    if not protocol:
        return {"error": "Could not determine protocol"}

    return {
        "Target": protocol,
        "Prompt": user_input
    }
