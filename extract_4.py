import os
import re

# Path to the directory containing the files
directory = r"responses\responses"

# Regular expression to match filenames with numbers in brackets (e.g., "file(1).py", "file(2).py")
pattern = re.compile(r"^(.*)\((\d+)\)\.py$")

# Dictionary to store the latest file for each base name
latest_files = {}

# Iterate through all files in the directory
for filename in os.listdir(directory):
    match = pattern.match(filename)
    if match:
        base_name = match.group(1).strip()  # Extract the base name (e.g., "file")
        number = int(match.group(2))        # Extract the number in brackets (e.g., 1, 2, etc.)
        if base_name not in latest_files or number > latest_files[base_name]["number"]:
            # Update the latest file for this base name
            latest_files[base_name] = {"filename": filename, "number": number}

# Delete all duplicate files, keeping only the latest ones
for filename in os.listdir(directory):
    match = pattern.match(filename)
    if match:
        base_name = match.group(1).strip()
        if filename != latest_files[base_name]["filename"]:
            # Delete the file if it's not the latest
            file_path = os.path.join(directory, filename)
            os.remove(file_path)
            print(f"Deleted: {file_path}")

print("Duplicate files removed. Latest files retained.")