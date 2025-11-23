#!/bin/bash

# Directory containing the files
TARGET_DIR="/mnt/dados/DashCam/Converted/Back"

# Check if directory exists
if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Directory $TARGET_DIR does not exist."
    exit 1
fi

echo "Scanning $TARGET_DIR for MKV files..."

# Loop through all .mkv files in the directory
for filepath in "$TARGET_DIR"/*.mkv; do
    # Check if file exists (handles case where no mkv files are found)
    [ -e "$filepath" ] || continue

    # Get just the filename (e.g., 2025-11-23_01-32-01.mkv)
    filename=$(basename "$filepath")

    # Use Regex to extract date and time components
    # Pattern looks for: YYYY-MM-DD _ HH - MM - SS
    if [[ $filename =~ ([0-9]{4}-[0-9]{2}-[0-9]{2})_([0-9]{2})-([0-9]{2})-([0-9]{2}) ]]; then
        
        # Construct ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ
        # ${BASH_REMATCH[1]} is the Date (2025-11-23)
        # ${BASH_REMATCH[2]} is Hour
        # ${BASH_REMATCH[3]} is Minute
        # ${BASH_REMATCH[4]} is Second
        
        NEW_DATE="${BASH_REMATCH[1]}T${BASH_REMATCH[2]}:${BASH_REMATCH[3]}:${BASH_REMATCH[4]}Z"

        echo "Processing: $filename"
        echo "  -> New Date: $NEW_DATE"

        # --- COMMAND SECTION ---
        # UNCOMMENT the line below to actually execute the change
        mkvpropedit "$filepath" --set date="$NEW_DATE"
        
    else
        echo "Skipping: $filename (Does not match date pattern)"
    fi
done
