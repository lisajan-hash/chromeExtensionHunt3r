import os
import json
from modules.jsonReturnMiddleware import json_data

def get_extensions_json(folder_path):
    try:
        # Check if the folder exists
        if not os.path.exists(folder_path):
            return json.loads(json_data(Success=False, Error=True, Message="Folder does not exist", Data=None))
        
        # Get a list of .crx files in the folder
        extensions = [
            {"filename": file, "path": os.path.join(folder_path, file)}
            for file in os.listdir(folder_path)
            if file.endswith(".crx")
        ]
        
        # Check if there are any .crx files
        if not extensions:
            return json.loads(json_data(Success=True, Message="No .crx files found", Data=[]))
        
        return json.loads(json_data(Success=True, Message="Extensions retrieved successfully", Data=extensions))
    
    except Exception as e:
        return json.loads(json_data(Success=False, Error=True, Message=f"An error occurred: {str(e)}", Data=None))