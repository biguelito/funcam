import cv2
import mediapipe as mp
from math import hypot

class HandTracking():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode,
                                        max_num_hands=self.maxHands,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.lmList = []
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img):
        self.results = None
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

    def findPosition(self, img,):
        bbox = []
        self.lmList = []

        if self.results.multi_hand_landmarks:
            for myHand in self.results.multi_hand_landmarks:
                xlist = []
                ylist = []
                lml = []
                for id, lm in enumerate(myHand.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    xlist.append(cx)
                    ylist.append(cy)
                    lml.append([id, cx, cy])

                xmin, xmax = min(xlist), max(xlist)
                ymin, ymax = min(ylist), max(ylist)
                bbox = [xmin, ymin, xmax, ymax] + bbox
                self.lmList = lml + self.lmList

        return self.lmList, bbox

    def calcDistance(self, img, f1,f2, draw=False):

        x1, y1 = self.lmList[f1][1], self.lmList[f1][2]
        x2, y2 = self.lmList[f2][1], self.lmList[f2][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)

        length = hypot(x2 - x1, y2 - y1)
        return length, img, [x1, y1, x2, y2, cx, cy]

    def fingersUp(self):
        self.fingers = []

        if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0] - 1][1]:
            self.fingers.append(1)
        else:
            self.fingers.append(0)

        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                self.fingers.append(1)
            else:
                self.fingers.append(0)

        return self.fingers

    def drawMarks(self, img, drawFingerMark=[]):
        if self.lmList:
            for myHand in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, myHand, self.mpHands.HAND_CONNECTIONS)
                xlist = []
                ylist = []

                for id, lm in enumerate(myHand.landmark):
                    h, w, c = img.shape
                    wx, hy = int(lm.x * w), int(lm.y * h)
                    xlist.append(wx)
                    ylist.append(hy)

                    if id in drawFingerMark:
                        cv2.circle(img, (wx, hy), 10, (255, 0, 0), cv2.FILLED)

                xmin, xmax = min(xlist), max(xlist)
                ymin, ymax = min(ylist), max(ylist)
                cv2.rectangle(img, (xmin - 15, ymin - 15), (xmax + 15, ymax + 15), (255, 0, 0), 2)


