import csv
import os
import requests
from datetime import datetime

# Define the input CSV file and output folders
csv_file = "Codewars V5 Submissions (Responses) - Form Responses 1.csv"
freshers_folder = "freshers"
seniors_folder = "senior"

# Create output folders if they don't exist
os.makedirs(freshers_folder, exist_ok=True)
os.makedirs(seniors_folder, exist_ok=True)

# Dictionary to store the latest submission for each team
latest_submissions = {}

# Read the CSV file
with open(csv_file, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        team_name = row["Team Name"].strip()
        timestamp = datetime.strptime(row["Timestamp"], "%m/%d/%Y %H:%M:%S")
        pool = row["Pool"].strip().lower()
        ldap_id = row["Player 1 LDAP ID"].strip()
        script_url = row["Upload your script (upload only the .py file that has your script)"].strip()

        # Check if this team already has a submission
        if team_name in latest_submissions:
            # Update if the current submission is later
            if timestamp > latest_submissions[team_name]["timestamp"]:
                latest_submissions[team_name] = {
                    "timestamp": timestamp,
                    "pool": pool,
                    "ldap_id": ldap_id,
                    "script_url": script_url,
                }
        else:
            # Add the team's submission
            latest_submissions[team_name] = {
                "timestamp": timestamp,
                "pool": pool,
                "ldap_id": ldap_id,
                "script_url": script_url,
            }

# Function to download a file from Google Drive
def download_file_from_google_drive(url, save_path):
    try:
        file_id = url.split("id=")[-1]
        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        response = requests.get(download_url)
        response.raise_for_status()  # Raise an error for bad status codes
        with open(save_path, "wb") as file:
            file.write(response.content)
        print(f"Downloaded: {save_path}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

# Process each team's latest submission
for team_name, data in latest_submissions.items():
    pool = data["pool"]
    ldap_id = data["ldap_id"]
    script_url = data["script_url"]

    # Determine the folder to save the script
    if pool == "freshers":
        folder = freshers_folder
    elif pool == "seniors":
        folder = seniors_folder
    else:
        print(f"Unknown pool for team {team_name}, skipping...")
        continue

    # Create the filename
    sanitized_team_name = team_name.replace(" ", "_").replace("/", "_")
    filename = f"{sanitized_team_name}_{pool}_{ldap_id}.py"
    save_path = os.path.join(folder, filename)

    # Download the script
    download_file_from_google_drive(script_url, save_path)