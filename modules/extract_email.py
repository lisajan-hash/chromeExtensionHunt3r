import os
import re
from modules.jsonReturnMiddleware import json_data

def extract_emails_from_js(extension_dir):
    # Regular expression to match email addresses
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    extracted_emails = set()

    try:
        for root, _, files in os.walk(extension_dir):
            for file in files:
                if file.endswith('.js') or file.endswith('.json') or file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    if os.path.getsize(file_path) > 10 * 1024 * 1024:
                        continue  # Skip files larger than 10MB
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file_content:
                            content = file_content.read()
                            # Extract emails using the regex pattern
                            emails = re.findall(email_pattern, content)
                            extracted_emails.update(emails)
                    except Exception as e:
                        # Log the error for the specific file but continue processing others
                        print(f"Error reading file {file_path}: {e}")

        # Return results
        return json_data(
            Success=True,
            Message="Email extraction completed successfully.",
            Data=list(extracted_emails)
        )

    except Exception as e:
        return json_data(
            Success=False,
            Error=True,
            Message=f"An unexpected error occurred: {str(e)}"
        )
