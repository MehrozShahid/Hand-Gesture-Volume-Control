import cv2
import mediapipe as mp
import time
import math


class handDetector():

    def __init__(
        self,
        mode=False,
        maxHands=2,
        detectionCon=0.5,
        trackCon=0.5
    ):

        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands

        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon,
            model_complexity=1
        )

        self.prev_landmarks = None
        self.smooth_factor = 0.4

        self.connections = (
            mp.solutions.hands.HAND_CONNECTIONS
        )

        # Store detected hand type
        self.handType = "Right"


    def fingerAngle(self, p1, p2, p3):

        a = math.dist(p2, p3)
        b = math.dist(p1, p3)
        c = math.dist(p1, p2)

        denominator = 2 * c * a

        if denominator == 0:
            return 0

        value = (
            (c * c + a * a - b * b)
            / denominator
        )

        value = max(-1, min(1, value))

        angle = math.degrees(
            math.acos(value)
        )

        return angle


    def countFingers(self, lmList):

        if len(lmList) == 0:
            return 0

        fingers = []

        # ==================================
        # THUMB
        # ==================================

        thumb_tip_x = lmList[4][1]
        thumb_ip_x = lmList[3][1]

        if self.handType == "Right":

            if thumb_tip_x < thumb_ip_x:
                fingers.append(1)
            else:
                fingers.append(0)

        else:

            if thumb_tip_x > thumb_ip_x:
                fingers.append(1)
            else:
                fingers.append(0)


        # ==================================
        # INDEX, MIDDLE, RING, PINKY
        # ==================================

        fingerTips = [8, 12, 16, 20]
        fingerPips = [6, 10, 14, 18]

        for tip, pip in zip(
            fingerTips,
            fingerPips
        ):

            tip_y = lmList[tip][2]
            pip_y = lmList[pip][2]

            if tip_y < pip_y:
                fingers.append(1)
            else:
                fingers.append(0)


        return sum(fingers)


    def drawSkeleton(self, img, lmList):

        color = (255, 255, 255)
        thickness = 3

        for connection in self.connections:

            start = lmList[connection[0]]
            end = lmList[connection[1]]

            cv2.line(
                img,
                (start[1], start[2]),
                (end[1], end[2]),
                color,
                thickness
            )


    def findHands(self, img):

        imgRGB = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2RGB
        )

        self.results = self.hands.process(
            imgRGB
        )

        return img


    def findPosition(
        self,
        img,
        handNo=0
    ):

        lmList = []

        if self.results.multi_hand_landmarks:

            if handNo >= len(
                self.results.multi_hand_landmarks
            ):
                return lmList, img

            myHand = (
                self.results.multi_hand_landmarks[
                    handNo
                ]
            )

            # ==================================
            # DETECT LEFT / RIGHT HAND
            # ==================================

            if self.results.multi_handedness:

                self.handType = (
                    self.results
                    .multi_handedness[handNo]
                    .classification[0]
                    .label
                )


            # ==================================
            # LANDMARKS
            # ==================================

            for id, lm in enumerate(
                myHand.landmark
            ):

                h, w, c = img.shape

                cx = int(lm.x * w)
                cy = int(lm.y * h)

                if self.prev_landmarks is None:

                    smooth_x = cx
                    smooth_y = cy

                else:

                    px, py = (
                        self.prev_landmarks[id]
                    )

                    smooth_x = int(
                        px
                        + self.smooth_factor
                        * (cx - px)
                    )

                    smooth_y = int(
                        py
                        + self.smooth_factor
                        * (cy - py)
                    )

                lmList.append(
                    [id, smooth_x, smooth_y]
                )


            # ==================================
            # SAVE PREVIOUS LANDMARKS
            # ==================================

            self.prev_landmarks = {
                i: (lm[1], lm[2])
                for i, lm in enumerate(lmList)
            }


            # ==================================
            # DRAW SKELETON
            # ==================================

            self.drawSkeleton(
                img,
                lmList
            )


            # ==================================
            # DRAW FINGERTIPS
            # ==================================

            for id, x, y in lmList:

                if id in [
                    4,
                    8,
                    12,
                    16,
                    20
                ]:

                    cv2.circle(
                        img,
                        (x, y),
                        10,
                        (255, 255, 255),
                        -1
                    )

                    cv2.circle(
                        img,
                        (x, y),
                        20,
                        (255, 255, 255),
                        2
                    )


            # ==================================
            # BOUNDING BOX
            # ==================================

            x_vals = [
                lm[1]
                for lm in lmList
            ]

            y_vals = [
                lm[2]
                for lm in lmList
            ]

            xmin = min(x_vals)
            xmax = max(x_vals)

            ymin = min(y_vals)
            ymax = max(y_vals)


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


            # ==================================
            # FINGER COUNT
            # ==================================

            fingers = self.countFingers(
                lmList
            )

            cv2.putText(
                img,
                f"Fingers: {fingers}",
                (xmin - 20, ymin - 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )


        return lmList, img


# ==========================================
# TEST PROGRAM
# ==========================================

def main():

    pTime = 0

    cap = cv2.VideoCapture(0)

    cap.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        1280
    )

    cap.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        720
    )

    detector = handDetector()

    while True:

        success, img = cap.read()

        if not success:
            break

        img = detector.findHands(img)

        lmList, img = detector.findPosition(
            img
        )

        cTime = time.time()

        if pTime != 0:

            fps = 1 / (
                cTime - pTime
            )

        else:

            fps = 0

        pTime = cTime

        cv2.putText(
            img,
            f"FPS: {int(fps)}",
            (10, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )

        cv2.imshow(
            "Hand Tracking",
            img
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
