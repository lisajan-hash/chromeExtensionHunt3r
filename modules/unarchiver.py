import os
import struct
import zipfile
import io
from modules.jsonReturnMiddleware import json_data

def extract_crx(crx_file_path, extraction_path):
    try:
        # Ensure the output directory exists
        os.makedirs(extraction_path, exist_ok=True)

        with open(crx_file_path, 'rb') as f:
            # Verify the CRX magic number
            magic_number = f.read(4)
            if magic_number != b'Cr24':
                return json_data(
                    Success=False,
                    Error=True,
                    Message="Invalid CRX file format."
                )

            # Read the CRX version
            version = struct.unpack('<I', f.read(4))[0]
            if version not in [2, 3]:
                return json_data(
                    Success=False,
                    Error=True,
                    Message=f"Unsupported CRX version: {version}."
                )

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
            return json_data(
                Success=True,
                Message="Extraction successful. Files extracted successfully.",
                Data=os.listdir(extraction_path)
            )
        else:
            return json_data(
                Success=False,
                Message="Extraction failed. No files were found in the output directory."
            )

    except FileNotFoundError:
        return json_data(
            Success=False,
            Error=True,
            Message=f"File not found: {crx_file_path}. Please verify the path."
        )
    except zipfile.BadZipFile:
        return json_data(
            Success=False,
            Error=True,
            Message="The file's ZIP content is invalid or corrupted."
        )
    except Exception as e:
        return json_data(
            Success=False,
            Error=True,
            Message=f"An unexpected error occurred: {str(e)}"
        )
