from modules.unarchiver import extract_crx
from modules.list_extension_folder import get_extensions_json
from modules.removeExtensionFromString import removeExtensionKeyword
from modules.manifest_checker import analyze_manifest
from modules.extractUrl import extract_ips_and_urls
from modules.extract_base64 import extract_base64_from_functions
from modules.extract_email import extract_emails_from_js
import json

extebnsion_folder = "extensions"
target_folder = "result"

def start_script():
    list_extnesion_folder = get_extensions_json(extebnsion_folder)
    if (list_extnesion_folder['Success']):
        if list_extnesion_folder['Data'] is not None:
            if len(list_extnesion_folder['Data']) > 0:
                for extensionInformation in list_extnesion_folder['Data']:
                    extension_name=removeExtensionKeyword(extensionInformation['filename'])
                    path = extensionInformation['path']
                    destination_folder = f'{target_folder}/{extension_name}'    
                    extracted_data = json.loads(extract_crx(path, destination_folder))
                    if extracted_data['Success']:
                        if len(extracted_data['Data']):
                            extracted_destination = destination_folder
                            extension_id_value = extension_name
                            manifest_analyzed_value = analyze_manifest(f'{destination_folder}/manifest.json')
                            analyze_url_ip = extract_ips_and_urls(destination_folder)
                            extract_base64_value = extract_base64_from_functions(destination_folder)
                            emails_extractions_values = extract_emails_from_js(destination_folder)
                            print(manifest_analyzed_value)
                            print(analyze_url_ip)
                            print(emails_extractions_values)
                            print(extract_base64_value)
                        else:
                            print('check please your extracted data, something gone not success')    
                    else:
                        print("Something went wrong with crx extraction")    
            else:
                print("Extension list array is empty" )    
        else:
            print("Something went wronmg with list of extensions in Data", list_extnesion_folder['Data'] )    
    else:
        print("Something went wronmg with list enumeration of extensions")    

start_script()    