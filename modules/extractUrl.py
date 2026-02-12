import os
import re
import ipaddress  # For IP address validation
from modules.jsonReturnMiddleware import json_data

def extract_ips_and_urls(extension_dir):
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    url_pattern = r'https?://[^\s"\'<>]+'

    extracted_ips = set()
    extracted_urls = set()

    try:
        for root, _, files in os.walk(extension_dir):
            for file in files:
                if file.endswith('.js'):
                    file_path = os.path.join(root, file)
                    if os.path.getsize(file_path) > 10 * 1024 * 1024:
                        continue  # Skip files larger than 10MB
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as js_file:
                            content = js_file.read()
                            # Extract potential IPs and validate them
                            potential_ips = re.findall(ip_pattern, content)
                            for ip in potential_ips:
                                try:
                                    # Validate IP address
                                    ipaddress.ip_address(ip)
                                    extracted_ips.add(ip)
                                except ValueError:
                                    pass  # Skip invalid IPs
                            # Extract URLs
                            extracted_urls.update(re.findall(url_pattern, content))
                    except Exception as e:
                        # Log the error for the specific file but continue processing others
                        print(f"Error reading file {file_path}: {e}")

        # Return results
        return json_data(
            Success=True,
            Message="Extraction completed successfully.",
            Data={
                "IPs": list(extracted_ips),
                "URLs": list(extracted_urls)
            }
        )

    except Exception as e:
        return json_data(
            Success=False,
            Error=True,
            Message=f"An unexpected error occurred: {str(e)}"
        )
