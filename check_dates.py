import os
import sys
import subprocess
import json
from datetime import datetime
import argparse


def get_exif_data(filepath):
    """
    Uses exiftool to extract CreateDate and MediaCreateDate in JSON format.
    """
    try:
        # We use -j for JSON output which is safer to parse than text
        cmd = ['exiftool', '-j', '-CreateDate', '-MediaCreateDate', filepath]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            print(f"Error reading {filepath}: {result.stderr}")
            return None

        # exiftool returns a list of objects, we take the first one
        data = json.loads(result.stdout)
        return data[0] if data else None
    except Exception as e:
        print(f"Failed to execute exiftool: {e}")
        return None


def parse_filename_date(filename):
    """
    Parses 'YYYY-MM-DD_HH-MM-SS.mp4' into a datetime object.
    """
    try:
        # Remove extension
        name_only = os.path.splitext(filename)[0]
        # Parse format: 2025-11-16_14-01-14
        return datetime.strptime(name_only, "%Y-%m-%d_%H-%M-%S")
    except ValueError:
        return None


def parse_exif_date(date_str):
    """
    Parses ExifTool date format 'YYYY:MM:DD HH:MM:SS'.
    Ignores timezones or extra chars if present, matching the filename precision.
    """
    if not date_str:
        return None
    try:
        # Take the first 19 chars to get 'YYYY:MM:DD HH:MM:SS'
        # (This ignores potential timezone offsets like -05:00 if they exist)
        clean_str = date_str[:19]
        return datetime.strptime(clean_str, "%Y:%m:%d %H:%M:%S")
    except ValueError:
        return None


def main(folder_path):
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' not found.")
        sys.exit(1)

    print(f"{'FILENAME':<30} | {'STATUS':<10} | {'DETAILS'}")
    print("-" * 80)

    files = [f for f in os.listdir(folder_path) if f.lower().endswith('.mp4')]
    files.sort()

    for filename in files:
        filepath = os.path.join(folder_path, filename)

        # 1. Get Date from Filename
        fname_date = parse_filename_date(filename)
        if not fname_date:
            print(f"{filename:<30} | SKIPPED    | Filename format not recognized")
            continue

        # 2. Get Dates from Metadata
        metadata = get_exif_data(filepath)
        if not metadata:
            continue

        create_date_str = metadata.get('CreateDate')
        media_date_str = metadata.get('MediaCreateDate')

        create_date = parse_exif_date(create_date_str)
        media_date = parse_exif_date(media_date_str)

        # 3. Compare
        issues = []
        if create_date != fname_date:
            issues.append(f"CreateDate mismatch ({create_date_str})")
        if media_date != fname_date:
            issues.append(f"MediaCreateDate mismatch ({media_date_str})")

        if not issues:
            print(f"{filename:<30} | OK         | Dates match filename")
        else:
            # Highlight mismatch in red if your terminal supports colors, or just plain text
            print(f"{filename:<30} | MISMATCH   | {', '.join(issues)}")


if __name__ == "__main__":
    # Default to current directory if no argument provided
    target_folder = sys.argv[1] if len(sys.argv) > 1 else "."
    main(target_folder)