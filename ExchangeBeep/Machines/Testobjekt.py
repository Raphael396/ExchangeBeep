import winsound
import pyautogui as pag
import time
from python_imagesearch.imagesearch import imagesearch
import cv2  # OpenCV zum Laden des Bildes

# frequency is set to 500Hz
freq = 500

# duration is set to 100 milliseconds
dur = 500

# Pfad zum Bild
image_path = "Machines/Image assets/Testobjekt.png"
# Lade das Bild mit OpenCV
original_image = cv2.imread(image_path)

# Überprüfen, ob das Bild geladen wurde
if original_image is None:
   print(f"Fehler: Das Bild konnte nicht geladen werden. Überprüfe den Pfad: {image_path}")
   exit()  # Beende das Programm

# Funktion zur Suche nach dem Bild auf dem Bildschirm
def search_image(image_path):
    # Suche das Bild auf dem Bildschirm
    pos = imagesearch(image_path)
    return pos

while True:
   pos = search_image(image_path)
   if pos[0] != -1:  # Wenn das Bild gefunden wird
      winsound.Beep(freq, dur)
      
      # Debug-Ausgabe der Position
      print(f"Bild gefunden bei: {pos}")
      
      # Bildschirmgröße abrufen
      screen_width, screen_height = pag.size()
      print(f"Bildschirmgröße: {screen_width}x{screen_height}")
      
      # Prüfe, ob die Position innerhalb des Bildschirmbereichs liegt
      if 0 <= pos[0] <= screen_width and 0 <= pos[1] <= screen_height:
         # Bewege die Maus zur gefundenen Bildposition
         center_x = pos[0]
         center_y = pos[1]
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