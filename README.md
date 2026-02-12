# chromeExtensionHunt3r

A Python tool to retrieve, analyze, and hunt for potentially risky elements in Chrome browser extensions (.crx files). This project helps security researchers and developers identify permissions, encoded data, URLs/IPs, and emails within extensions for risk assessment.

## Features

- **Extension Permissions Analysis**: Extracts and analyzes permissions from `manifest.json`.
- **Encoding Detection**: Scans for Base64-encoded data in JavaScript functions.
- **URL and IP Extraction**: Identifies embedded URLs and IP addresses in extension code.
- **Email Extraction**: Finds email addresses within JavaScript, JSON, and HTML files.
- **CSV Output**: Saves analysis results to a structured CSV file for easy review.
- **Extension Download**: Downloads extensions directly from the Chrome Web Store by ID.

## Usage

### Analyzing Existing Extensions

1. Place your `.crx` extension files in the `extensions/` folder.
2. Run the analysis:
   ```
   python main.py
   ```

Or analyze specific extensions from a CSV (useful after downloading):
```
python main.py --csv extension_list.csv
```

This will check each ID in the CSV, analyze downloaded ones, and mark failed downloads in the results.

### Downloading Extensions

Use the separate download script to fetch extensions by their Chrome Web Store IDs:

```
python download_extensions.py --ids EXTENSION_ID1 EXTENSION_ID2
```

Or provide a CSV file with an "ID" column:

```
python download_extensions.py --csv path/to/your/file.csv
```

Example:
```
python download_extensions.py --ids cjpalhdlnbpafiamejdnhcphjbkeiagm
python download_extensions.py --csv extension_list.csv
```

**Note**: Not all extensions may be downloadable due to Chrome Web Store policies or availability. The script will report failures for empty or unavailable downloads. In such cases, download manually from the Chrome Web Store.

This downloads the extensions to `extensions/` and then you can analyze them with `main.py`.

### CSV Output

The `results.csv` file contains:
- Extension_ID
- Download_Status (e.g., "Downloaded and Analyzed" or "Download Failed or Empty")
- Permissions
- Host_Permissions
- Optional_Host_Permissions
- IPs
- URLs
- Emails
- Base64_Data

Lists are separated by semicolons (`; `) for easy parsing.

## Requirements

- Python 3.x
- No external dependencies (uses built-in libraries like `urllib`, `json`, `csv`)

## Project Structure

- `main.py`: Main analysis script.
- `download_extensions.py`: Extension downloader.
- `modules/`: Analysis modules for different extraction tasks.
- `extensions/`: Folder for .crx files.
- `result/`: Folder for extracted extension contents.
- `results.csv`: Output CSV file.

## Risk Assessment

Use the extracted data to build custom detections for:
- Overly permissive extensions.
- Suspicious URLs or IPs (e.g., known malicious domains).
- Hidden encoded payloads.
- Contact information for further investigation.

## Contributing

Feel free to contribute by adding more analysis modules or improving the extraction logic.

## License

This project is for educational and security research purposes. Use responsibly.