import cv2
from basicsfilters import BasicsFilters


class Cam:

    def __init__(self):
        cv2.namedWindow("ESC to close")
        self.videocap = 0
        self.filterList = ['normal', 'negative', 'bgr2gray']
        self.filterIndex = 0

        self.cam = cv2.VideoCapture(self.videocap)
        if not self.cam.isOpened():
            raise RuntimeError('Can\'t open your camera, please check if videocap is validy device, try using "v4l2-ctl --list-device"')

        self.ret, self.frame = self.cam.read()
        if not self.ret:
            raise RuntimeError('Error fetching frame')

        self.display = True

    def open(self):
        while self.display:
            self.ret, self.frame = self.cam.read()
            if not self.ret:
                raise RuntimeError('Error fetching frame')

            self.camInputs()

            self.frame = cv2.flip(self.frame, 1)
            cv2.imshow("ESC to close", self.frame)

        print('Camera closed')

    def camInputs(self):
        key = cv2.waitKey(5)

        # ESC
        if key == 27:  # exit on ESC
            cv2.destroyWindow("ESC to close")
            self.cam.release()
            self.display = False
            return

        # [
        elif key == 91:
            self.filterIndex = (self.filterIndex - 1) % len(self.filterList)

        # ]
        elif key == 93:
            self.filterIndex = (self.filterIndex - 1) % len(self.filterList)

        filter = self.filterList[self.filterIndex]
        self.frame = getattr(BasicsFilters, filter)(self.frame)