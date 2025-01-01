import json
from modules.jsonReturnMiddleware import json_data

def analyze_manifest(manifest_path):
    try:
        # Read the manifest.json file
        with open(manifest_path, 'r') as file:
            manifest_data = json.load(file)

        # Check for specific keys
        permissions = manifest_data.get("permissions", [])
        host_permissions = manifest_data.get("host_permissions", [])
        optional_host_permissions = manifest_data.get("optional_host_permissions", [])

        # Construct the response data
        analysis_result = {
            "permissions": permissions,
            "host_permissions": host_permissions,
            "optional_host_permissions": optional_host_permissions,
        }

        return json_data(
            Success=True,
            Message="Manifest analyzed successfully.",
            Data=analysis_result
        )

    except FileNotFoundError:
        return json_data(
            Success=False,
            Error=True,
            Message=f"File not found: {manifest_path}. Please verify the path."
        )
    except json.JSONDecodeError:
        return json_data(
            Success=False,
            Error=True,
            Message="Invalid JSON format in manifest.json."
        )
    except Exception as e:
        return json_data(
            Success=False,
            Error=True,
            Message=f"An unexpected error occurred: {str(e)}"
        )
