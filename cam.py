import cv2
from basicsfilters import BasicsFilters


class Cam:

    def __init__(self):
        cv2.namedWindow("preview")
        self.cam = cv2.VideoCapture(0)
        self.rval, self.frame = self.cam.read()

        self.filterList = ['normal', 'negative', 'bgr2gray']
        self.filterIndex = 0

    def open(self):
        while self.rval:
            cv2.imshow("preview", self.frame)
            self.rval, self.frame = self.cam.read()

            self.camInputs()

        cv2.destroyWindow("preview")
        self.cam.release()

    def camInputs(self):
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            cv2.destroyWindow("preview")
            self.cam.release()
        elif key == 91:
            self.filterIndex = (self.filterIndex - 1) % len(self.filterList)
        elif key == 93:
            self.filterIndex = (self.filterIndex - 1) % len(self.filterList)
        filter = self.filterList[self.filterIndex]
        self.frame = getattr(BasicsFilters, filter)(self.frame)