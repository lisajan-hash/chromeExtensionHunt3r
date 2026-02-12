import os
import struct
import zipfile
import io
import threading
from modules.jsonReturnMiddleware import json_data

def extract_crx(crx_file_path, extraction_path):
    result = {'success': False, 'message': '', 'data': []}

    def extract():
        try:
            # Ensure the output directory exists
            os.makedirs(extraction_path, exist_ok=True)

            with open(crx_file_path, 'rb') as f:
                # Verify the CRX magic number
                magic_number = f.read(4)
                if magic_number != b'Cr24':
                    result['message'] = "Invalid CRX file format."
                    return

                # Read the CRX version
                version = struct.unpack('<I', f.read(4))[0]
                if version not in [2, 3]:
                    result['message'] = f"Unsupported CRX version: {version}."
                    return

                # Parse the header size(s)
                if version == 2:
                    public_key_length, signature_length = struct.unpack('<II', f.read(8))
                    header_size = 16 + public_key_length + signature_length
                elif version == 3:
                    header_size = struct.unpack('<I', f.read(4))[0] + 12

                # Skip the header and read the ZIP content
                f.seek(header_size)
                zip_data = f.read()

            # Extract the ZIP content
            with zipfile.ZipFile(io.BytesIO(zip_data)) as zip_ref:
                zip_ref.extractall(extraction_path)

            # Verify extraction success
            if os.path.exists(extraction_path) and os.listdir(extraction_path):
                result['success'] = True
                result['message'] = "Extraction successful. Files extracted successfully."
                result['data'] = os.listdir(extraction_path)
            else:
                result['message'] = "Extraction failed. No files were found in the output directory."

        except zipfile.BadZipFile:
            result['message'] = "The file's ZIP content is invalid or corrupted."
        except Exception as e:
            result['message'] = f"An unexpected error occurred: {str(e)}"

    # Run extraction in a thread with timeout
    thread = threading.Thread(target=extract)
    thread.start()
    thread.join(timeout=30)

    if thread.is_alive():
        # Timeout occurred
        return json_data(
            Success=False,
            Error=True,
            Message="Extraction timed out after 30 seconds."
        )
    else:
        if result['success']:
            return json_data(
                Success=True,
                Message=result['message'],
                Data=result['data']
            )
        else:
            return json_data(
                Success=False,
                Error=True,
                Message=result['message']
            )
