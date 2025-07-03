# Tugas Besar Pengolahan Citra
# Nama :Agung Hadi Astanto
# NIM : 4.33.23.0.02
# Kelas : TI-2A
# AI Virtual Keyboard
import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller

# Inisialisasi kamera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Inisialisasi detektor tangan
detector = HandDetector(detectionCon=0.8, maxHands=1)
keyboard = Controller()
finalText = ""

# Definisi tombol keyboard (tanpa tombol "Open")
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
        ["Space", "Backspace", "Reset"]]

# Class tombol
class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

# Buat daftar tombol
buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        # Untuk baris terakhir tombol besar
        size = [200, 85] if key in ["Space", "Backspace", "Reset"] else [85, 85]
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key, size))

# Fungsi gambar tombol
def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (x, y, w, h), 20, rt=0)
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 3 if w < 150 else 2, (255, 255, 255), 3)
    return img

# Loop utama
while True:
    success, img = cap.read()
    
    # Jika kamera gagal membaca frame, lewati iterasi ini
    if not success:
        continue

    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img)

    img = drawAll(img, buttonList)

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        bbox = hand["bbox"]

        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65),
                            cv2.FONT_HERSHEY_PLAIN, 3 if w < 150 else 2, (255, 255, 255), 3)

                l, _, _ = detector.findDistance(lmList[8][:2], lmList[12][:2], img)

                # Ketika jari telunjuk dan tengah berdekatan (mengeklik)
                if l < 30:
                    key = button.text
                    if key == "Space":
                        finalText += " "
                    elif key == "Backspace":
                        finalText = finalText[:-1]
                    elif key == "Reset":
                        finalText = ""
                    else:
                        finalText += key
                        keyboard.press(key)
                    sleep(0.25) # Menambahkan jeda untuk menghindari input ganda

    # Tampilkan teks yang diketik
    cv2.rectangle(img, (50, 450), (1200, 550), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 520),
                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

    cv2.imshow("Virtual Keyboard", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
