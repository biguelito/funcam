import pyvirtualcam
import cv2
import time
from filters import Filters
import math
import time
import ML.HandTrackingModule as htm

class VCam:

    def __init__(self, video=0, f=8, detCon=0.5, du=True):
        cv2.namedWindow('feedback')
        self.videocap = video
        self.filterList = ['normal', 'negative', 'bgr2gray']
        self.filterIndex = 0
        self.key = -1

        # Utils
        self.toDU = du
        self.nextX, self.nextY = 600, 240
        self.prevX, self.prevY = 40, 240
        self.radius = 40

        # Hand tracking
        self.detector = htm.HandDetector(detectionCon=detCon)
        self.finger = f
        self.pressing = False
        self.initialTime = time.time()

        self.vc = cv2.VideoCapture(self.videocap)
        if not self.vc.isOpened():
            raise RuntimeError('Can\'t open your camera, please check if videocap is validy device, try using "v4l2-ctl --list-device"')

        self.vc.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
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

                self.key = cv2.waitKey(1)
                if self.key != -1:
                    self.camInputs()

                filter = self.filterList[self.filterIndex]
                self.frame = getattr(Filters, filter)(self.frame)

                cTime = time.time()
                fps = int(1 / (cTime - pTime))
                pTime = cTime
                cv2.putText(self.frame, str(fps), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                if self.toDU:
                    self.drawUtils()

                cv2.imshow('feedback', self.frame)
                cam.send(self.frame)

        print('Virtual camera closed')

    def handCommands(self):
        self.frame = self.detector.findHands(self.frame, draw=True)
        lmList = self.detector.findPosition(self.frame, drawOn=[self.finger])

        if lmList:
            fingerX, fingerY = lmList[self.finger][1], lmList[self.finger][2]
            init = time.time()

            if math.hypot(fingerX - self.nextX, fingerY - self.nextY) <= 30:
                actual = time.time()

                if not self.pressing:
                    self.pressing = True
                    self.initialTime = init

                else:
                    presstime = actual - self.initialTime

                    if presstime >= 1:
                        self.filterIndex = (self.filterIndex + 1) % len(self.filterList)
                        self.pressing = False

            elif math.hypot(fingerX - self.prevX, fingerY - self.prevY) <= 30:
                actual = time.time()

                if not self.pressing:
                    self.pressing = True
                    self.initialTime = init

                else:
                    presstime = actual - self.initialTime

                    if presstime >= 1:
                        self.filterIndex = (self.filterIndex - 1) % len(self.filterList)
                        self.pressing = False

            else:
                self.pressing = False
                self.initialTime = init

    def camInputs(self):

        # ESC
        if self.key == 27:
            cv2.destroyWindow('feedback')
            self.vc.release()
            self.display = False

        # [
        elif self.key == 91:
            self.filterIndex = (self.filterIndex - 1) % len(self.filterList)

        # ]
        elif self.key == 93:
            self.filterIndex = (self.filterIndex + 1) % len(self.filterList)

    def drawUtils(self):
        # Drawing area for hand tracker commands
        cv2.circle(self.frame, (self.nextX, self.nextY), self.radius, (255, 0, 0))
        cv2.circle(self.frame, (self.prevX, self.prevY), self.radius, (255, 0, 0))