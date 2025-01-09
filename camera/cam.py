import cv2
from camera.cam_commands import CamCommands
from filters import Filters
from datetime import datetime

class Cam:
    def __init__(self, mxhand, video, f, detCon=0.5, cam_width=640, cam_height=480, markCommands=False):
        # Basics
        self.videocap = video
        self.filterList = ['normal', 'negative', 'bgr2gray']
        self.filterIndex = 0
        self.filter = 'normal'
        self.cam_width = cam_width
        self.cam_height = cam_height
        self.markCommands = markCommands

        self.camCommands = CamCommands(self.cam_width, self.cam_height)

        # # Hand tracking
        # self.detector = htm.HandTracking(detectionCon=detCon, maxHands=mxhand)
        # self.finger = f
        # self.pressing = False
        # self.initialTime = datetime.timestamp(datetime.now())

    def open(self):
        cv2.namedWindow("ESC to close")
        
        self.cam = cv2.VideoCapture(self.videocap)
        if not self.cam.isOpened():
            raise RuntimeError('Can\'t open your camera, please check if videocap is validy device, try using "v4l2-ctl --list-device"')

        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.cam_width)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cam_height)
        self.cam.set(cv2.CAP_PROP_FPS, 30)

        self.ret, self.frame = self.cam.read()
        if not self.ret:
            raise RuntimeError('Error fetching frame')

        self.display = True

        self.pTime, self.cTime = 0, 0
        while self.display:
            # Get and check video
            self.ret, self.frame = self.cam.read()
            self.frame = cv2.flip(self.frame, 1)
            if not self.ret:
                raise RuntimeError('Error fetching frame')

            # Hand track control
            # self.handCommands()

            self.camCommands.doInputKey(cv2.waitKey(1))

            # Apllying filter on frame
            # self.filter = self.filterList[self.filterIndex]
            # self.frame = getattr(Filters, self.filter)(self.frame)

            if self.markCommands:
                self.camCommands.drawCommands(self.frame)

            #     self.detector.drawMarks(self.frame, drawFingerMark=[self.finger])

            self.drawFPS()
            cv2.imshow("ESC to close", self.frame)

            self.checkEnd()

        return

    def drawFPS(self):
        self.cTime = datetime.timestamp(datetime.now())
        fps = int(1 / (self.cTime - self.pTime))
        self.pTime = self.cTime
        cv2.putText(self.frame, str(fps), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        return

    def end(self):
        cv2.destroyWindow('ESC to close')
        self.cam.release()

    def close(self):
        self.display = False

    def checkEnd(self):
        if not self.display:
            self.end()