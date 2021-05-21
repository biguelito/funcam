import cv2
from filters import Filters
import ML.HandTrackingModule as htm
import time
import math


class Cam:

    def __init__(self, video=0, f=8, detCon=0.5, cw=640, ch=480, du=False):
        # Basics
        cv2.namedWindow("ESC to close")
        self.videocap = video
        self.filterList = ['normal', 'negative', 'bgr2gray']
        self.filterIndex = 0
        self.inputKey = 0

        # Utils
        self.toDU = du
        self.nextX, self.nextY = 600, 240
        self.prevX, self.prevY = 40, 240
        self.radius = 40

        # Hand tracking
        self.detector = htm.HandDetector(detectionCon=detCon)
        self.finger = f
        self.pressing = False

        # Creating camera
        self.cam = cv2.VideoCapture(self.videocap)
        if not self.cam.isOpened():
            raise RuntimeError('Can\'t open your camera, please check if videocap is validy device, try using "v4l2-ctl --list-device"')

        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, cw)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, ch)
        self.cam.set(cv2.CAP_PROP_FPS, 30)

        self.ret, self.frame = self.cam.read()
        if not self.ret:
            raise RuntimeError('Error fetching frame')

        self.display = True

    def open(self):
        pTime, cTime = 0, 0
        while self.display:
            # Get and check video
            self.ret, self.frame = self.cam.read()
            self.frame = cv2.flip(self.frame, 1)
            if not self.ret:
                raise RuntimeError('Error fetching frame')

            # Dealing with hand detection, from here ============================================
            self.frame = self.detector.findHands(self.frame)
            lmList = self.detector.findPosition(self.frame)

            if lmList:
                x8, y8 = lmList[self.finger][1], lmList[self.finger][2]

                if math.hypot(x8 - self.nextX, y8 - self.nextY) <= 30:
                    actual = time.time()

                    if not self.pressing:
                        self.pressing = True
                        init = time.time()

                    presstime = actual - init

                    if presstime >= 1:
                        self.filterIndex = (self.filterIndex + 1) % len(self.filterList)
                        self.pressing = False

                elif math.hypot(x8 - self.prevX, y8 - self.prevY) <= 30:
                    actual = time.time()

                    if not self.pressing:
                        self.pressing = True
                        init = time.time()

                    presstime = actual - init
                    
                    if presstime >= 1:
                        self.filterIndex = (self.filterIndex - 1) % len(self.filterList)
                        self.pressing = False

                else:
                    self.pressing = False
            # To here ===========================================================================

            # Receiving input from keyboard
            self.inputKey = cv2.waitKey(1)
            if self.inputKey != -1:
                self.camInputs()

            # Apllying filter on frame
            filter = self.filterList[self.filterIndex]
            self.frame = getattr(Filters, filter)(self.frame)

            # Putting extra info on frame
            cTime = time.time()
            fps = int(1 / (cTime - pTime))
            pTime = cTime
            cv2.putText(self.frame, str(fps), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            if self.toDU:
                self.drawUtils()

            # Showing frame
            cv2.imshow("ESC to close", self.frame)

        print("camera closed")

    def drawUtils(self):
        # Drawing area for hand tracker commands
        cv2.circle(self.frame, (self.nextX, self.nextY), self.radius, (255, 0, 0))
        cv2.circle(self.frame, (self.prevX, self.prevY), self.radius, (255, 0, 0))

    def camInputs(self):
        # Using input keyboard
        # ESC
        if self.inputKey == 27:
            cv2.destroyWindow('ESC to close')
            self.cam.release()
            self.display = False

        # [
        elif self.inputKey == 91:
            self.filterIndex = (self.filterIndex - 1) % len(self.filterList)

        # ]
        elif self.inputKey == 93:
            self.filterIndex = (self.filterIndex + 1) % len(self.filterList)