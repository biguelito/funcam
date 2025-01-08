import cv2
from filters import Filters
import Tracking.HandTracking as htm
import math
from datetime import datetime


class Cam:

    def __init__(self, mxhand, video, f, detCon=0.5, cw=640, ch=480, du=True):
        # Basics
        cv2.namedWindow("ESC to close")
        self.videocap = video
        self.filterList = ['normal', 'negative', 'bgr2gray']
        self.filterIndex = 0
        self.filter = 'normal'
        self.inputKey = -1

        # Utils
        self.toDU = du
        self.nextX, self.nextY = cw-40, ch//2
        self.prevX, self.prevY = 40, ch//2
        self.escX, self.escY = cw-40, 40
        self.radius = 40

        # Hand tracking
        self.detector = htm.HandDetector(detectionCon=detCon, maxHands=mxhand)
        self.finger = f
        self.pressing = False
        self.initialTime = datetime.timestamp(datetime.now())

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

            # Hand track control
            self.handCommands()

            # Receiving input from keyboard
            self.inputKey = cv2.waitKey(1)
            if self.inputKey != -1:
                self.camInputs()

            # Apllying filter on frame
            self.filter = self.filterList[self.filterIndex]
            self.frame = getattr(Filters, self.filter)(self.frame)

            # Putting extra info on frame
            cTime = datetime.timestamp(datetime.now())
            fps = int(1 / (cTime - pTime))
            pTime = cTime
            cv2.putText(self.frame, str(fps), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            
            if self.toDU:
                self.drawUtils()
                self.detector.drawMarks(self.frame, drawFingerMark=[self.finger])

            # Showing frame
            cv2.imshow("ESC to close", self.frame)

        print("camera closed")

    def handCommands(self):
        self.detector.findHands(self.frame)
        lmList, bbox = self.detector.findPosition(self.frame)

        if lmList:
            fingerX, fingerY = lmList[self.finger][1], lmList[self.finger][2]

            init = datetime.timestamp(datetime.now())

            # next filter
            if math.hypot(fingerX - self.nextX, fingerY - self.nextY) <= 30:
                actual = datetime.timestamp(datetime.now())

                if not self.pressing:
                    self.pressing = True
                    self.initialTime = init

                else:
                    presstime = int(actual - self.initialTime)
                    if presstime == 1:
                        self.filterIndex = (self.filterIndex + 1) % len(self.filterList)
                        self.pressing = False

            # previus filter
            elif math.hypot(fingerX - self.prevX, fingerY - self.prevY) <= 30:
                actual = datetime.timestamp(datetime.now())

                if not self.pressing:
                    self.pressing = True
                    self.initialTime = init

                else:
                    presstime = int(actual - self.initialTime)

                    if presstime == 1:
                        self.filterIndex = (self.filterIndex - 1) % len(self.filterList)
                        self.pressing = False

            # close cam
            elif math.hypot(fingerX - self.escX, fingerY - self.escY) <= 30:
                actual = datetime.timestamp(datetime.now())

                if not self.pressing:
                    self.pressing = True
                    self.initialTime = init

                else:
                    presstime = int(actual - self.initialTime)

                    if presstime == 2:
                        self.cam.release()
                        self.display = False
                        self.pressing = False

            else:
                self.pressing = False
                self.initialTime = init

    def camInputs(self):
        # Using input keyboard
        # ESC
        if self.inputKey == 27:
            self.close()

        # [
        elif self.inputKey == 91:
            self.filterIndex = (self.filterIndex - 1) % len(self.filterList)

        # ]
        elif self.inputKey == 93:
            self.filterIndex = (self.filterIndex + 1) % len(self.filterList)

    def drawUtils(self):
        # Drawing area for hand tracker commands
        cv2.circle(self.frame, (self.nextX, self.nextY), self.radius, (255, 0, 0))
        cv2.circle(self.frame, (self.prevX, self.prevY), self.radius, (255, 0, 0))
        cv2.circle(self.frame, (self.escX, self.escY), self.radius, (255, 0, 0))

    def close(self):
        cv2.destroyWindow('ESC to close')
        self.cam.release()
        self.display = False