import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
import os

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER

# Webcam size
wCam, hCam = 1280, 720

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0

# Hand detector (matches your module)
detector = htm.handDetector()

# Audio device
devices = AudioUtilities.GetSpeakers()

interface = devices._dev.Activate(
    IAudioEndpointVolume._iid_,
    CLSCTX_ALL,
    None
)

volume = cast(
    interface,
    POINTER(IAudioEndpointVolume)
)

# Volume range
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

volBar = 400
volPer = 0

# Initial volume
volume.SetMasterVolumeLevel(-20.0, None)

while True:

    success, img = cap.read()

    if not success:
        break

    # Detect hands
    img = detector.findHands(img)

    # Get landmarks
    lmList, img = detector.findPosition(img)

    if len(lmList) != 0:

        # Thumb tip
        x1, y1 = lmList[4][1], lmList[4][2]

        # Index finger tip
        x2, y2 = lmList[8][1], lmList[8][2]

        # Center point
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # White fingertip glow
        cv2.circle(
            img,
            (x1, y1),
            12,
            (255, 255, 255),
            -1
        )

        cv2.circle(
            img,
            (x2, y2),
            12,
            (255, 255, 255),
            -1
        )

        # White connecting line
        cv2.line(
            img,
            (x1, y1),
            (x2, y2),
            (255, 255, 255),
            3
        )

        # Center glow
        cv2.circle(
            img,
            (cx, cy),
            15,
            (255, 255, 255),
            -1
        )

        # Distance between fingers
        length = math.hypot(
            x2 - x1,
            y2 - y1
        )

        # Convert distance → volume
        # Changed only the minimum distance from 120 to 50
        vol = np.interp(
            length,
            [50, 300],
            [minVol, maxVol]
        )

        volBar = np.interp(
            length,
            [50, 300],
            [400, 150]
        )

        volPer = np.interp(
            length,
            [50, 300],
            [0, 100]
        )

        # Set system volume
        volume.SetMasterVolumeLevel(
            vol,
            None
        )

        # Transparent highlight box
        xmin, xmax = min(x1, x2), max(x1, x2)
        ymin, ymax = min(y1, y2), max(y1, y2)

        overlay = img.copy()

        cv2.rectangle(
            overlay,
            (xmin - 20, ymin - 20),
            (xmax + 20, ymax + 20),
            (255, 255, 255),
            -1
        )

        img = cv2.addWeighted(
            overlay,
            0.15,
            img,
            0.85,
            0
        )

        cv2.rectangle(
            img,
            (xmin - 20, ymin - 20),
            (xmax + 20, ymax + 20),
            (255, 255, 255),
            2
        )

        # Glow when fingers close
        if length < 50:

            cv2.circle(
                img,
                (cx, cy),
                20,
                (0, 255, 0),
                -1
            )

    # Volume bar background
    cv2.rectangle(
        img,
        (50, 150),
        (85, 400),
        (30, 30, 30),
        -1
    )

    # Volume bar fill (white)
    cv2.rectangle(
        img,
        (50, int(volBar)),
        (85, 400),
        (255, 255, 255),
        -1
    )

    # Border
    cv2.rectangle(
        img,
        (50, 150),
        (85, 400),
        (255, 255, 255),
        3
    )

    # Percentage text
    cv2.putText(
        img,
        f'{int(volPer)} %',
        (40, 450),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

    # FPS
    cTime = time.time()

    fps = 1 / (cTime - pTime)

    pTime = cTime

    cv2.putText(
        img,
        f'FPS: {int(fps)}',
        (40, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        3
    )

    cv2.imshow(
        "img",
        img
    )

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()

cv2.destroyAllWindows()