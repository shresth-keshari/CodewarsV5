from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.service_account import Credentials
import os
from datetime import datetime

# Path to your service account credentials JSON file
SERVICE_ACCOUNT_FILE = "credentials.json"

# Google Drive folder ID (from the provided link)
FOLDER_ID = "1hOE2xrzcdEHds91GtP5FNHRuy4bjizPYtVLnqmvImBSdpGS6VZ0umlPfkLg2pNUpsvoRKBFt"

# Output folder to save the downloaded files
OUTPUT_FOLDER = "downloaded_scripts"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Authenticate and build the Google Drive API client
SCOPES = ["https://www.googleapis.com/auth/drive"]
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build("drive", "v3", credentials=credentials)

# Get all .py files in the folder
def get_files_in_folder(folder_id):
    query = f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.file' or mimeType='text/x-python'"
    results = drive_service.files().list(q=query, fields="files(id, name, modifiedTime)").execute()
    return results.get("files", [])

# Download a file from Google Drive
def download_file(file_id, file_name, output_folder):
    request = drive_service.files().get_media(fileId=file_id)
    file_path = os.path.join(output_folder, file_name)
    with open(file_path, "wb") as f:
        downloader = MediaIoBaseDownload(f, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Downloading {file_name}: {int(status.progress() * 100)}%")
    print(f"Downloaded: {file_path}")

# Main logic to download the latest files
def download_latest_files(folder_id, output_folder):
    files = get_files_in_folder(folder_id)
    latest_files = {}

    # Find the latest file for each unique name
    for file in files:
        name = file["name"]
        modified_time = datetime.strptime(file["modifiedTime"], "%Y-%m-%dT%H:%M:%S.%fZ")
        if name not in latest_files or modified_time > latest_files[name]["modifiedTime"]:
            latest_files[name] = {"id": file["id"], "modifiedTime": modified_time}

    # Download the latest files
    for name, file_info in latest_files.items():
        print(f"Downloading latest version of: {name}")
        download_file(file_info["id"], name, output_folder)

# Run the script
download_latest_files(FOLDER_ID, OUTPUT_FOLDER)