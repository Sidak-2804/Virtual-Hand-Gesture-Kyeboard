import cv2
import mediapipe as mp
import numpy as np
from time import sleep
import math
from pynput.keyboard import Controller

mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mpdraw = mp.solutions.drawing_utils

keyboard = Controller()

cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Set width
cap.set(4, 720)   # Set height

text = ""
tx = ""

class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "CL"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "SP"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "APR"]]
keys1 = [["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "CL"],
         ["a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "SP"],
         ["z", "x", "c", "v", "b", "n", "m", ",", ".", "/", "APR"]]

def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        # Draw rounded rectangle for the key
        cv2.rectangle(img, (x, y), (x + w, y + h), (200, 200, 200), cv2.FILLED)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 2)
        cv2.putText(img, button.text, (x + 20, y + 60),
                    cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)
    return img

buttonList = []
buttonList1 = []
list = []

for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))
for i in range(len(keys1)):
    for j, key in enumerate(keys1[i]):
        buttonList1.append(Button([100 * j + 50, 100 * i + 50], key))

app = 0
delay = 0
last_y = 0  # To track the last y position of the finger

def calculate_distance(x1, y1, x2, y2):
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coff = np.polyfit(x, y, 2)

while True:
    success, frame = cap.read()
    frame = cv2.resize(frame, (1280, 720))
    frame = cv2.flip(frame, 1)
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img)
    lanmark = []

    if app == 0:
        frame = drawAll(frame, buttonList)
        list = buttonList
        r = "up"
    if app == 1:
        frame = drawAll(frame, buttonList1)
        list = buttonList1
        r = "down"

    if results.multi_hand_landmarks:
        for hn in results.multi_hand_landmarks:
            for id, lm in enumerate(hn.landmark):
                hl, wl, cl = frame.shape
                cx, cy = int(lm.x * wl), int(lm.y * hl)
                lanmark.append([id, cx, cy])

    if lanmark:
        try:
            x8, y8 = lanmark[8][1], lanmark[8][2]  # Index finger tip
            x6, y6 = lanmark[6][1], lanmark[6][2]  # Index finger PIP

            cv2.circle(frame, (x8, y8), 20, (255, 0, 255), cv2.FILLED)

            # Check if the finger is moving forward (y-coordinate decreasing)
            if y8 < last_y - 10:  # Threshold to detect forward movement
                for button in list:
                    xb, yb = button.pos
                    wb, hb = button.size

                    if (xb < x8 < xb + wb) and (yb < y8 < yb + hb):
                        cv2.rectangle(frame, (xb - 5, yb - 5), (xb + wb + 5, yb + hb + 5), (160, 160, 160), cv2.FILLED)
                        cv2.putText(frame, button.text, (xb + 20, yb + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)

                        k = button.text
                        if k == "SP":
                            tx = ' '
                            text += tx
                            keyboard.press(tx)
                        elif k == "CL":
                            tx = text[:-1]
                            text = ""
                            text += tx
                            keyboard.press('\b')
                        elif k == "APR" and r == "up":
                            app = 1
                        elif k == "APR" and r == "down":
                            app = 0
                        else:
                            text += k
                            keyboard.press(k)
                        sleep(0.2)  # Add a small delay to avoid multiple presses

            last_y = y8  # Update the last y position

        except:
            pass

    cv2.rectangle(frame, (20, 500), (1260, 600), (255, 255, 255), cv2.FILLED)
    cv2.putText(frame, text, (30, 550), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)
    cv2.imshow('Virtual Keyboard', frame)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()