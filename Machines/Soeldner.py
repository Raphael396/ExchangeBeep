import os
import winsound
import pyautogui as pag
import time
import cv2  # OpenCV zum Laden und Vergleichen von Bildern
import numpy as np
import requests
import zipfile
import io
import subprocess  # Um das Skript nach dem Update neu zu starten

# Frequency and duration for beep sound
freq = 500
dur = 500

# Path to the image
image_path = "Image assets/Soeldner.png"
original_image = cv2.imread(image_path)

# Check if the image was loaded successfully
if original_image is None:
    print(f"Fehler: Das Bild konnte nicht geladen werden. Überprüfe den Pfad: {image_path}")
    exit()  # Exit the program if image is not loaded

# GitHub API URL to get the latest release info
GITHUB_API_URL = "https://api.github.com/repos/Raphael396/ExchangeBeep/releases/latest"

# Directory where the script is located
TARGET_DIR = os.path.dirname(os.path.realpath(__file__))

# Function to get the latest release information from GitHub
def get_latest_release():
    """Fetch the latest release info from GitHub."""
    response = requests.get(GITHUB_API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        print("Fehler beim Abrufen des Releases:", response.status_code)
        return None

# Function to download the latest release as a zip
def download_release_zip(download_url):
    """Download the latest release zip from GitHub."""
    response = requests.get(download_url)
    if response.status_code == 200:
        return zipfile.ZipFile(io.BytesIO(response.content))
    else:
        print("Fehler beim Herunterladen des Archivs:", response.status_code)
        return None

# Function to extract and patch the files
def extract_and_patch(zip_file):
    """Extract the zip and overwrite files in the target directory."""
    for file in zip_file.namelist():
        zip_file.extract(file, TARGET_DIR)
        print(f"Datei {file} extrahiert und gepatcht.")

# Function to update the script from GitHub
def update_script():
    """Check for the latest release and update the script."""
    release = get_latest_release()
    if release:
        print(f"Neue Version verfügbar: {release['tag_name']}")
        # Get the download URL for the zip file
        zip_download_url = release['assets'][0]['browser_download_url']
        print(f"Lade Release von {zip_download_url} herunter...")
        
        # Download and extract the zip
        zip_file = download_release_zip(zip_download_url)
        
        if zip_file:
            print("Entpacke und patchen...")
            extract_and_patch(zip_file)
            print("Update abgeschlossen!")
            
            # Restart the script after updating
            print("Das Skript wird jetzt neu gestartet...")
            subprocess.Popen([sys.executable, __file__])  # Restart the script
            exit()  # Exit the current process

# Function to search for the image on the screen
def search_image_exact(image, threshold=0.99):
    """Search for the exact image on the screen."""
    # Take a screenshot of the screen
    screenshot = pag.screenshot()

    # Convert the screenshot to an OpenCV-compatible format (from PIL to OpenCV)
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Perform template matching
    result = cv2.matchTemplate(screenshot, image, cv2.TM_CCOEFF_NORMED)

    # Find the best match
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # If the best match is above the threshold, return the position
    if max_val >= threshold:
        return max_loc
    else:
        return None  # No match found

# Main loop to check for the image and perform actions
while True:
    pos = search_image_exact(original_image)
    if pos:  # If the image is found
        winsound.Beep(freq, dur)

        # Debug output of the position
        print(f"Bild gefunden bei: {pos}")

        # Get the screen size
        screen_width, screen_height = pag.size()
        print(f"Bildschirmgröße: {screen_width}x{screen_height}")

        # Check if the position is within the screen bounds
        if 0 <= pos[0] <= screen_width and 0 <= pos[1] <= screen_height:
            # Move the mouse to the center of the found image
            center_x = pos[0] + original_image.shape[1] // 2
            center_y = pos[1] + original_image.shape[0] // 2
            print(f"Maus bewegt zu: ({center_x}, {center_y})")
            pag.moveTo(center_x, center_y, duration=0.2)  # Move the mouse to the image

            # Simulate a visual effect (clicking the image)
            for i in range(3):
                pag.click(center_x, center_y)  # Click to mark the position
                time.sleep(0.2)
            break  # Exit the loop after finding the image
        else:
            print("Gefundene Position liegt außerhalb des Bildschirmbereichs")
    else:
        print("Bild nicht gefunden")

    time.sleep(0.05)

# Wait 10 seconds before closing the window
print("Das Programm wird in 10 Sekunden geschlossen...")
time.sleep(10)

# If no update is done, the program will exit
print("Beende das aktuelle Skript.")
os._exit(0)
