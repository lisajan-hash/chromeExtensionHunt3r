import os
import re
from modules.jsonReturnMiddleware import json_data

def extract_base64_from_functions(extension_dir):
    # Patterns for JavaScript Base64-related functions
    btoa_pattern = r'btoa\((.*?)\)'  # btoa() function call (encodes data to Base64)
    atob_pattern = r'atob\((.*?)\)'  # atob() function call (decodes Base64 data)
    buffer_pattern = r'Buffer\.from\((.*?),\s*["\']base64["\']\)'  # Node.js Buffer.from() for Base64 decoding

    extracted_base64 = set()

    def extract_base64_from_match(match):
        """Extract Base64 data from function arguments"""
        # Clean up and remove extra characters
        base64_data = match.group(1).strip().strip('"').strip("'")
        return base64_data

    try:
        for root, _, files in os.walk(extension_dir):
            for file in files:
                if file.endswith('.js') or file.endswith('.json') or file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as file_content:
                            content = file_content.read()
                            
                            # Search for btoa(), atob(), and Buffer.from() calls
                            btoa_matches = re.finditer(btoa_pattern, content)
                            atob_matches = re.finditer(atob_pattern, content)
                            buffer_matches = re.finditer(buffer_pattern, content)

                            # Extract Base64 data from function calls
                            for match in btoa_matches:
                                base64_data = extract_base64_from_match(match)
                                extracted_base64.add(base64_data)

                            for match in atob_matches:
                                base64_data = extract_base64_from_match(match)
                                extracted_base64.add(base64_data)

                            for match in buffer_matches:
                                base64_data = extract_base64_from_match(match)
                                extracted_base64.add(base64_data)

                    except Exception as e:
                        # Log the error for the specific file but continue processing others
                        print(f"Error reading file {file_path}: {e}")

        # Return results
        return json_data(
            Success=True,
            Message="Base64 extraction from functions completed successfully.",
            Data=list(extracted_base64)
        )

    except Exception as e:
        return json_data(
            Success=False,
            Error=True,
            Message=f"An unexpected error occurred: {str(e)}"
        )
