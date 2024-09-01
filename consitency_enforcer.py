import json

DEFAULT_FIELDS = {
    "payments.py": {
        "Name": "Not defined",
        "Asset": "Not defined",
        "Asset Type": "Not defined",
        "Payer": "Not defined",
        "Input Payment Frequency": "Not defined",
        "Input Payment Amount": "Not defined",
        "Output Payment Distribution": "Not defined",
        "Distribution Frequency": "Not defined",
        "Distribute to": "Not defined",
        "Pause Payments": "Not defined",
        "Pause Payments by": "Not defined",
        "Admin": "Creator",
        "Managers": "Not defined",
        "Manager Permissions": "Not defined"
    },
    "vaults.py": {
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
    },
    "token_tool.py": {
        "Token Name": "Not defined",
        "Token Symbol": "Not defined",
        "Number of Tokens": "Not defined",
        "Asset Type": "Not defined",
        "Description": "No description",
        "UnifiedData": "False",
        "UnifiedDataIndex": [],
        "UnifiedDataType": [],
        "UnifiedDataName": [],
        "UnifiedDataPoint": [],
        "CanMint": "False",
        "MaxCap": "Not defined",
        "LinkedData": "False",
        "LinkedDataIndex": [],
        "LinkedDataType": [],
        "NumberofLinkedDataTokens": [],
        "LinkedDataName": [],
        "LinkedDataPoint": [],
        "PreferenceSignature": "False",
        "PauseTokens": "False",
        "ForceTransfer": "False",
        "Freeze": "False",
        "Blacklist": "False",
        "TokenFee": "False",
        "FeeEarnedBy": "Not defined",
        "Whitelist": "False",
        "Whitelist Admin": "Not defined",
        "TokenOwner": "Creator"
    },
    "listing.py": {
        "Asset": "Not defined",
        "Number of Tokens": "Not defined",
        "Allow Bids": "No",
        "Floor Price": "Not defined",
        "Allow Loans": "No",
        "Max. Duration": "Not defined",
        "Downpayment in %": "Not defined",
        "Description": "Not defined",
        "Pictures": "Not defined",
        "End Date": "Not defined",
        "Reserved Price": "Not defined",
        "Bid Increment in %": "Not defined",
        "Sales Owner": "Not defined"
    },
    "leasing.py": {
        "Name": "Not defined",
        "Asset": "Not defined",
        "Duration": "Not defined",
        "Security Deposit": "Not defined",
        "Rent Frequency": "Not defined",
        "Rent": "Not defined",
        "Tenant": "Not defined",
        "Landlord(s)": "Not defined",
        "Landlords Contact": "Not defined",
        "Pictures": "Not defined",
        "End Date": "Not defined",
        "Heating": "Not defined",
        "Heating Included": "No",
        "Water": "Not defined",
        "Water Included": "No",
        "Electricity": "Not defined",
        "Electricity Included": "No",
        "Maintenance and repairs": "Not defined",
        "Alterations and renovations": "Not defined"
    }
}

def enforce_consistency(script_name, config):
    default_config = DEFAULT_FIELDS.get(script_name, {})
    enforced_config = default_config.copy()

    for key in enforced_config:
        if key in config and config[key] != "Not defined":
            enforced_config[key] = config[key]

    return enforced_config

def main():
    try:
        import sys
        data = json.loads(sys.stdin.read())
        script_name = data.get("script_name")
        config = data.get("config", {})

        if script_name not in DEFAULT_FIELDS:
            print(json.dumps({"error": "Unknown script name"}))
            return

        enforced_config = enforce_consistency(script_name, config)
        print(json.dumps(enforced_config))
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON input: {str(e)}"}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == '__main__':
    main()
