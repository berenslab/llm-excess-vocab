#!/bin/bash

# Check if correct number of arguments is provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 source_dir destination_dir"
    exit 1
fi

source_dir="$1"
dest_dir="$2"

# Check if directories exist
if [ ! -d "$source_dir" ] || [ ! -d "$dest_dir" ]; then
    echo "Error: Both source and destination must be existing directories"
    exit 1
fi

# Remove trailing slashes from paths
source_dir=${source_dir%/}
dest_dir=${dest_dir%/}

# Find all files in source directory
find "$source_dir" -type f | while read -r source_file; do
    # Get relative path
    rel_path=${source_file#$source_dir/}
    dest_file="$dest_dir/$rel_path"
    
    # Check if destination file exists
    if [ -f "$dest_file" ]; then
        # Get sizes using Linux stat command format
        source_size=$(stat -c%s "$source_file")
        dest_size=$(stat -c%s "$dest_file")
        
        # Compare sizes
        if [ "$source_size" -ne "$dest_size" ]; then
            echo "Copying $rel_path (size mismatch: $source_size vs $dest_size bytes)"
            # Create directory structure if needed
            mkdir -p "$(dirname "$dest_file")"
            cp "$source_file" "$dest_file"
        fi
    else
        echo "Copying $rel_path (new file)"
        # Create directory structure if needed
        mkdir -p "$(dirname "$dest_file")"
        cp "$source_file" "$dest_file"
    fi
done

echo "Sync complete!"
