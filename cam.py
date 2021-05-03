import cv2
from basicsfilters import BasicsFilters


class Cam:

    def __init__(self):
        cv2.namedWindow("preview")
        self.videocap = 0

        self.cam = cv2.VideoCapture(self.videocap)
        if not self.cam.isOpened():
            raise RuntimeError('Can\'t open your camera, please check if videocap is validy device using "v4l2-ctl --list-device"')

        self.ret, self.frame = self.cam.read()
        self.filterList = ['normal', 'negative', 'bgr2gray']
        self.filterIndex = 0

    def open(self):
        while self.ret:
            self.camInputs()

            cv2.imshow("preview", self.frame)
            self.ret, self.frame = self.cam.read()

        cv2.destroyWindow("preview")
        self.cam.release()
        print('camera closed')

    def camInputs(self):
        key = cv2.waitKey(20)

        # ESC
        if key == 27:  # exit on ESC
            cv2.destroyWindow("preview")
            self.cam.release()
            return
        # [
        elif key == 91:
            self.filterIndex = (self.filterIndex - 1) % len(self.filterList)

        # ]
        elif key == 93:
            self.filterIndex = (self.filterIndex - 1) % len(self.filterList)
        filter = self.filterList[self.filterIndex]
        self.frame = getattr(BasicsFilters, filter)(self.frame)