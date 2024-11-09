import winsound
import pyautogui as pag
import time
import cv2  # OpenCV zum Laden und Vergleichen von Bildern
import numpy as np
import os  # Importiere os für das Neustarten des Batch-Skripts

# frequency is set to 500Hz
freq = 500

# duration is set to 100 milliseconds
dur = 500

# Pfad zum Bild
image_path = "Machines/Image assets/Soeldner.png"
# Lade das Bild mit OpenCV
original_image = cv2.imread(image_path)

# Überprüfen, ob das Bild geladen wurde
if original_image is None:
    print(f"Fehler: Das Bild konnte nicht geladen werden. Überprüfe den Pfad: {image_path}")
    exit()  # Beende das Programm

# Funktion zur Suche nach dem exakten Bild auf dem Bildschirm
def search_image_exact(image, threshold=0.99):
    # Screenshot des Bildschirms machen
    screenshot = pag.screenshot()

    # Screenshot in ein OpenCV-kompatibles Format konvertieren (von PIL zu OpenCV)
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Führe das Template Matching durch
    result = cv2.matchTemplate(screenshot, image, cv2.TM_CCOEFF_NORMED)

    # Suche nach dem besten Treffer
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Wenn der beste Treffer über dem Schwellenwert liegt, gibt es eine Übereinstimmung
    if max_val >= threshold:
        return max_loc  # Rückgabe der Position (linke obere Ecke des Bildes)
    else:
        return None  # Keine Übereinstimmung

while True:
    pos = search_image_exact(original_image)
    if pos:  # Wenn das Bild gefunden wird
        winsound.Beep(freq, dur)

        # Debug-Ausgabe der Position
        print(f"Bild gefunden bei: {pos}")

        # Bildschirmgröße abrufen
        screen_width, screen_height = pag.size()
        print(f"Bildschirmgröße: {screen_width}x{screen_height}")

        # Prüfe, ob die Position innerhalb des Bildschirmbereichs liegt
        if 0 <= pos[0] <= screen_width and 0 <= pos[1] <= screen_height:
            # Bewege die Maus zur gefundenen Bildposition
            center_x = pos[0] + original_image.shape[1] // 2  # Berechne die Mitte des Bildes
            center_y = pos[1] + original_image.shape[0] // 2
            print(f"Maus bewegt zu: ({center_x}, {center_y})")
            pag.moveTo(center_x, center_y, duration=0.2)  # Maus zum Bild bewegen

            # Simuliere visuellen Effekt (z.B. durch Klick)
            for i in range(3):
                pag.click(center_x, center_y)  # Klicken, um die Position zu markieren
                time.sleep(0.2)
            break  # Beende die Schleife, wenn das Bild gefunden wird
        else:
            print("Gefundene Position liegt außerhalb des Bildschirmbereichs")
    else:
        print("Bild nicht gefunden")
    time.sleep(0.05)

# Warte 10 Sekunden, bevor das Fenster geschlossen wird
print("Das Programm wird in 10 Sekunden geschlossen...")
time.sleep(10)

# Beende das aktuelle Skript
os._exit(0)
