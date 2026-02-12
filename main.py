from modules.unarchiver import extract_crx
from modules.list_extension_folder import get_extensions_json
from modules.removeExtensionFromString import removeExtensionKeyword
from modules.manifest_checker import analyze_manifest
from modules.extractUrl import extract_ips_and_urls
from modules.extract_base64 import extract_base64_from_functions
from modules.extract_email import extract_emails_from_js
import json
import csv
import os
import argparse

extebnsion_folder = "extensions"
target_folder = "result"
csv_file = "results.csv"
fieldnames = ['Extension_ID', 'Download_Status', 'Permissions', 'Host_Permissions', 'Optional_Host_Permissions', 'IPs', 'URLs', 'Emails', 'Base64_Data']

def start_script(extension_ids=None):
    results = []
    
    if extension_ids:
        total = len(extension_ids)
        # Process specific IDs from CSV or command line
        for i, ext_id in enumerate(extension_ids, 1):
            crx_path = os.path.join(extebnsion_folder, f"{ext_id}.crx")
            if os.path.exists(crx_path) and os.path.getsize(crx_path) > 0:
                # Analyze the extension
                extension_name = removeExtensionKeyword(f"{ext_id}.crx")
                destination_folder = f'{target_folder}/{extension_name}'    
                extracted_data = json.loads(extract_crx(crx_path, destination_folder))
                if extracted_data['Success']:
                    if len(extracted_data['Data']):
                        extension_id_value = extension_name
                        manifest_analyzed_value = json.loads(analyze_manifest(f'{destination_folder}/manifest.json'))
                        analyze_url_ip = json.loads(extract_ips_and_urls(destination_folder))
                        extract_base64_value = json.loads(extract_base64_from_functions(destination_folder))
                        emails_extractions_values = json.loads(extract_emails_from_js(destination_folder))
                        
                        # Collect data for CSV
                        result_row = {
                            'Extension_ID': extension_id_value,
                            'Download_Status': 'Downloaded and Analyzed',
                            'Permissions': '; '.join(manifest_analyzed_value.get('Data', {}).get('permissions', [])),
                            'Host_Permissions': '; '.join(manifest_analyzed_value.get('Data', {}).get('host_permissions', [])),
                            'Optional_Host_Permissions': '; '.join(manifest_analyzed_value.get('Data', {}).get('optional_host_permissions', [])),
                            'IPs': '; '.join(analyze_url_ip.get('Data', {}).get('IPs', [])),
                            'URLs': '; '.join(analyze_url_ip.get('Data', {}).get('URLs', [])),
                            'Emails': '; '.join(emails_extractions_values.get('Data') or []),
                            'Base64_Data': '; '.join(extract_base64_value.get('Data') or [])
                        }
                        results.append(result_row)
                        
                        # Write to CSV incrementally
                        if not os.path.exists(csv_file) or os.path.getsize(csv_file) == 0:
                            mode = 'w'
                        else:
                            mode = 'a'
                        with open(csv_file, mode, newline='', encoding='utf-8') as csvfile:
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                            if mode == 'w':
                                writer.writeheader()
                            writer.writerow(result_row)
                        
                        print(f"Processed {i}/{total}: {extension_id_value}")
                    else:
                        print('check please your extracted data, something gone not success')    
                else:
                    print("Something went wrong with crx extraction")
            else:
                # Extension not downloaded or empty
                result_row = {
                    'Extension_ID': ext_id,
                    'Download_Status': 'Download Failed or Empty',
                    'Permissions': '',
                    'Host_Permissions': '',
                    'Optional_Host_Permissions': '',
                    'IPs': '',
                    'URLs': '',
                    'Emails': '',
                    'Base64_Data': ''
                }
                results.append(result_row)
                
                # Write to CSV incrementally
                if not os.path.exists(csv_file) or os.path.getsize(csv_file) == 0:
                    mode = 'w'
                else:
                    mode = 'a'
                with open(csv_file, mode, newline='', encoding='utf-8') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    if mode == 'w':
                        writer.writeheader()
                    writer.writerow(result_row)
                
                print(f"Extension {ext_id} was not downloaded or is empty")
    else:
        # Original behavior: process all in extensions/
        list_extnesion_folder = get_extensions_json(extebnsion_folder)
        if (list_extnesion_folder['Success']):
            if list_extnesion_folder['Data'] is not None:
                if len(list_extnesion_folder['Data']) > 0:
                    total = len(list_extnesion_folder['Data'])
                    for i, extensionInformation in enumerate(list_extnesion_folder['Data'], 1):
                        extension_name=removeExtensionKeyword(extensionInformation['filename'])
                        path = extensionInformation['path']
                        destination_folder = f'{target_folder}/{extension_name}'    
                        extracted_data = json.loads(extract_crx(path, destination_folder))
                        if extracted_data['Success']:
                            if len(extracted_data['Data']):
                                extracted_destination = destination_folder
                                extension_id_value = extension_name
                                manifest_analyzed_value = json.loads(analyze_manifest(f'{destination_folder}/manifest.json'))
                                analyze_url_ip = json.loads(extract_ips_and_urls(destination_folder))
                                extract_base64_value = json.loads(extract_base64_from_functions(destination_folder))
                                emails_extractions_values = json.loads(extract_emails_from_js(destination_folder))
                                
                                # Collect data for CSV
                                result_row = {
                                    'Extension_ID': extension_id_value,
                                    'Download_Status': 'Downloaded and Analyzed',
                                    'Permissions': '; '.join(str(p) for p in manifest_analyzed_value.get('Data', {}).get('permissions', [])),
                                    'Host_Permissions': '; '.join(str(p) for p in manifest_analyzed_value.get('Data', {}).get('host_permissions', [])),
                                    'Optional_Host_Permissions': '; '.join(str(p) for p in manifest_analyzed_value.get('Data', {}).get('optional_host_permissions', [])),
                                    'IPs': '; '.join(str(ip) for ip in analyze_url_ip.get('Data', {}).get('IPs', [])),
                                    'URLs': '; '.join(str(url) for url in analyze_url_ip.get('Data', {}).get('URLs', [])),
                                    'Emails': '; '.join(str(email) for email in emails_extractions_values.get('Data') or []),
                                    'Base64_Data': '; '.join(str(b64) for b64 in extract_base64_value.get('Data') or [])
                                }
                                results.append(result_row)
                                
                                # Write to CSV incrementally
                                if not os.path.exists(csv_file) or os.path.getsize(csv_file) == 0:
                                    mode = 'w'
                                else:
                                    mode = 'a'
                                with open(csv_file, mode, newline='', encoding='utf-8') as csvfile:
                                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                                    if mode == 'w':
                                        writer.writeheader()
                                    writer.writerow(result_row)
                                
                                print(f"Processed {i}/{total}: {extension_id_value}")
                            else:
                                print('check please your extracted data, something gone not success')    
                        else:
                            print(f"Something went wrong with crx extraction for {extension_name}: {extracted_data.get('Message', 'Unknown error')}")    
                else:
                    print("Extension list array is empty" )    
            else:
                print("Something went wronmg with list of extensions in Data", list_extnesion_folder['Data'] )    
        else:
            print("Something went wronmg with list enumeration of extensions")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze Chrome extensions.")
    parser.add_argument('--csv', help='Path to CSV file with "ID" column containing extension IDs to analyze')
    args = parser.parse_args()
    
    ids = []
    if args.csv:
        try:
            with open(args.csv, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if 'ID' in row and row['ID'].strip():
                        ids.append(row['ID'].strip())
            print(f"Loaded {len(ids)} extension IDs from {args.csv}")
        except FileNotFoundError:
            print(f"Error: CSV file '{args.csv}' not found.")
            exit(1)
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            exit(1)
    
    start_script(ids if ids else None)    