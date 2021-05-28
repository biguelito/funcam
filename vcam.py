import pyvirtualcam
import cv2
import time
from filters import Filters
import math
from datetime import datetime
import ML.HandTrackingModule as htm


class VCam:

    def __init__(self, mxhand, video, f, detCon=0.5, cw=640, ch=480, du=True):
        cv2.namedWindow('feedback')
        self.videocap = video
        self.filterList = ['normal', 'negative', 'bgr2gray']
        self.filterIndex = 0
        self.inputKey = -1

        # Utils
        self.toDU = du
        self.nextX, self.nextY = cw - 40, ch // 2
        self.prevX, self.prevY = 40, ch // 2
        self.escX, self.escY = cw - 40, 40
        self.radius = 40

        # Hand tracking
        self.detector = htm.HandDetector(detectionCon=detCon, maxHands=mxhand)
        self.finger = f
        self.pressing = False
        self.initialTime = datetime.timestamp(datetime.now())

        self.vc = cv2.VideoCapture(self.videocap)
        if not self.vc.isOpened():
            raise RuntimeError('Can\'t open your camera, please check if videocap is validy device, try using "v4l2-ctl --list-device"')

        self.vc.set(cv2.CAP_PROP_FRAME_WIDTH, cw)
        self.vc.set(cv2.CAP_PROP_FRAME_HEIGHT, ch)
        self.vc.set(cv2.CAP_PROP_FPS, 30)

        # Query final capture device values (may be different from preferred settings).
        self.width = int(self.vc.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.vc.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps_out = self.vc.get(cv2.CAP_PROP_FPS)

        self.ret, self.frame = self.vc.read()
        if not self.ret:
            raise RuntimeError('Error fetching frame')

        self.display = True

    def start(self):

        with pyvirtualcam.Camera(self.width, self.height, self.fps_out, print_fps=False, fmt=pyvirtualcam.PixelFormat.BGR,) as cam:
            print(f'Virtual cam started: {cam.device} ({cam.width}x{cam.height} @ {cam.fps}fps)')
            pTime, cTime = 0,0
            while self.display:
                # Read frame from webcam.
                self.ret, self.frame = self.vc.read()
                self.frame = cv2.flip(self.frame, 1)
                if not self.ret:
                    raise RuntimeError('Error fetching frame')

                # Hand track control
                self.handCommands()

                self.inputKey = cv2.waitKey(1)
                if self.inputKey != -1:
                    self.camInputs()

                filter = self.filterList[self.filterIndex]
                self.frame = getattr(Filters, filter)(self.frame)

                cTime = time.time()
                fps = int(1 / (cTime - pTime))
                pTime = cTime
                cv2.putText(self.frame, str(fps), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                cam.send(self.frame)
                if self.toDU:
                    self.drawUtils()
                    self.detector.drawMarks(self.frame, drawOn=[self.finger])
                cv2.imshow('feedback', self.frame)

        print('Virtual camera closed')

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
                    presstime = actual - self.initialTime

                    if presstime >= 1:
                        self.filterIndex = (self.filterIndex + 1) % len(self.filterList)
                        self.pressing = False

            # previus filter
            elif math.hypot(fingerX - self.prevX, fingerY - self.prevY) <= 30:
                actual = datetime.timestamp(datetime.now())

                if not self.pressing:
                    self.pressing = True
                    self.initialTime = init

                else:
                    presstime = actual - self.initialTime

                    if presstime >= 1:
                        self.filterIndex = (self.filterIndex - 1) % len(self.filterList)
                        self.pressing = False

            # close cam
            elif math.hypot(fingerX - self.escX, fingerY - self.escY) <= 30:
                actual = datetime.timestamp(datetime.now())

                if not self.pressing:
                    self.pressing = True
                    self.initialTime = init

                else:
                    presstime = actual - self.initialTime

                    if presstime >= 2:
                        self.vc.release()
                        self.display = False
                        self.pressing = False

            else:
                self.pressing = False
                self.initialTime = init

    def camInputs(self):

        # ESC
        if self.inputKey == 27:
            cv2.destroyWindow('feedback')
            self.vc.release()
            self.display = False

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