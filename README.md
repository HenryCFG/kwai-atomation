Kwai Automation
This project provides a Python-based solution to automate the scheduling of videos on Kwai through a third-party website. Since Kwai itself does not offer a direct way to schedule video uploads, this tool leverages web automation to bridge that gap.

Project Structure
The repository contains two main Python scripts:

main-names.py: This script is responsible for renaming video files in a specified folder. It renames them by prepending a numerical index and appending a unique random code, ensuring that the videos are processed in a sorted order and have unique identifiers.
main.py: This is the core automation script. It uses Selenium to interact with a web platform (Cutmotions) that allows for scheduling video uploads. It handles video uploads, adds titles from an Excel spreadsheet, sets timed publication, and manages regional settings (Brazil, UTC-03:00).

Features
Automated Video Renaming: Organizes video files by prepending a number and adding a unique identifier.
Batch Video Upload: Uploads multiple video files to the scheduling platform.
Dynamic Title Assignment: Assigns video titles from an Excel spreadsheet (names.xlsx).
Timed Publishing: Configures videos for timed release, incrementing the publication time for each video.
Regional Settings: Sets the country to "Brazil" and the timezone to "UTC−03:00" for scheduled uploads.
Error Handling and Retries: Includes mechanisms to handle common web automation issues, such as page reloads and element not found errors, with retries.
Progress Tracking: Displays a progress bar and statistics (success, skipped, errors, elapsed time, ETA) during the automation process.
Video Deletion (Post-Upload): Automatically deletes videos from the local folder after successful upload and scheduling.


Getting Started

Prerequisites
Python 3.x
Google Chrome browser
ChromeDriver (compatible with your Chrome version)
Required Python libraries (install via pip):
pip install selenium pandas openpyxl natsort

Setup
Download ChromeDriver:
Download the appropriate ChromeDriver for your Chrome browser version from https://sites.google.com/chromium.org/driver/ and place it in a directory accessible by your system's PATH, or specify its path directly in main.py.

Video Folder:
Create a folder named videos (or modify videos_folder in main.py and main-names.py) and place your video files (e.g., .mp4) inside it.

Default path: C:\Users\henrycfg\Desktop\Automacao\videos.
Titles Spreadsheet:
Create an Excel file named names.xlsx (or modify titles_df in main.py) in the C:\Users\henrycfg\Desktop\Automacao\ directory. This spreadsheet should have a column named title containing the desired titles for your videos. Each row in this column will correspond to a video in the order they are processed.

Default path: C:\Users\henrycfg\Desktop\Automacao\names.xlsx.
Usage
Rename Videos (Optional but Recommended):
Run main-names.py first to rename your video files. This script sorts files numerically and appends a unique code for better organization.



python main-names.py
Run the Automation:
Execute the main.py script to start the automation process.


python main.py
The script will:

Open a Chrome browser window and navigate to the scheduling platform.
Wait for manual login (80 seconds).
Switch to the relevant tab.
Begin uploading and scheduling videos one by one.
Print progress updates to the console.

Important Notes
Manual Login: The main.py script includes a long time.sleep(80) after opening the browser. This is to allow you to manually log in to the cutmotions.com/pool website. The automation will proceed once this time elapses.
Website Changes: This automation relies on the specific structure and element IDs/XPaths of the cutmotions.com website. Future changes to the website's design may break the script, requiring updates to the Selenium locators.
Error Screenshots: In case of certain errors, the script will save screenshots to help with debugging (e.g., error_upload_timeout_*.png, error_edit_*.png).
Headless Mode: For production environments, consider running Chrome in headless mode to improve performance and reduce resource consumption. This would require modifications to the webdriver.Chrome() initialization.
