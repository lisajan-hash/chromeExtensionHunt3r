import os
import urllib.request
import argparse
import csv

def download_extension(extension_id, output_folder):
    """
    Downloads a Chrome extension .crx file from the Chrome Web Store using its extension ID.
    
    :param extension_id: The unique ID of the Chrome extension.
    :param output_folder: The folder where the .crx file will be saved.
    """
    url = f"https://clients2.google.com/service/update2/crx?response=redirect&prodversion=120.0.6099.109&acceptformat=crx2,crx3&x=id%3D{extension_id}%26uc"
    filename = f"{extension_id}.crx"
    filepath = os.path.join(output_folder, filename)
    
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    try:
        print(f"Downloading extension {extension_id}...")
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'})
        with urllib.request.urlopen(req) as response:
            with open(filepath, 'wb') as f:
                f.write(response.read())
        
        # Check if file has content
        if os.path.getsize(filepath) > 0:
            print(f"Successfully downloaded {extension_id} to {filepath}")
        else:
            print(f"Failed to download {extension_id}: Empty file received")
            os.remove(filepath)  # Remove empty file
    except Exception as e:
        print(f"Failed to download extension {extension_id}: {e}")
        if os.path.exists(filepath):
            os.remove(filepath)  # Clean up on failure

def main():
    parser = argparse.ArgumentParser(description="Download Chrome extensions by their IDs.")
    parser.add_argument('--ids', nargs='+', help='List of Chrome extension IDs to download (e.g., --ids id1 id2 id3)')
    parser.add_argument('--csv', help='Path to CSV file with "ID" column containing extension IDs')
    parser.add_argument('--output', default='extensions', help='Output folder for downloaded .crx files (default: extensions)')
    
    args = parser.parse_args()
    
    ids = args.ids or []
    
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
            return
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return
    
    if not ids:
        print("No extension IDs provided. Use --ids or --csv.")
        return
    
    for ext_id in ids:
        download_extension(ext_id, args.output)
    
    print("Download process completed.")

if __name__ == "__main__":
    main()