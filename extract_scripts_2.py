import csv
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define the input CSV file and output folders
csv_file = "Codewars V5 Submissions (Responses) - Form Responses 1.csv"
freshers_folder = "freshers_py"
seniors_folder = "senior_py"

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

# Function to download a file using Selenium
def download_file_with_selenium(url, save_folder, filename):
    driver = None  # Initialize the driver variable
    try:
        # Set up Selenium WebDriver (use ChromeDriver in this example)
        service = Service(r"C:\Users\kesha\Desktop\software installer packages\chromedriver-win64\chromedriver-win64\chromekesdriver.exe")  # Use raw string to handle backslashes
        options = webdriver.ChromeOptions()
        prefs = {"download.default_directory": save_folder}  # Set the default download directory
        options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(service=service, options=options)

        # Open the Google Drive link
        driver.get(url)

        # Wait for the download button to appear and click it
        wait = WebDriverWait(driver, 20)
        download_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'download')]"))
        )
        download_button.click()

        # Wait for the download to complete (you can add a more robust check here if needed)
        WebDriverWait(driver, 30).until(
            lambda driver: os.path.exists(os.path.join(save_folder, filename))
        )

        print(f"Downloaded: {os.path.join(save_folder, filename)}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")
    finally:
        if driver is not None:  # Check if the driver was initialized
            driver.quit()

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

    # Download the script using Selenium
    download_file_with_selenium(script_url, folder, filename)