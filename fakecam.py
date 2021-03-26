import virtualvideo
import cv2
from basicsfilters import BasicsFilters


class MyVideoSource(virtualvideo.VideoSource):
    def __init__(self):
        cv2.namedWindow("preview")
        self.cam = cv2.VideoCapture(0)
        _, self.frame = self.cam.read()
        size = self.frame.shape
        #opencv's shape is y,x,channels
        self._size = (size[1],size[0])

        self.filterList = ['normal', 'negative']
        self.filterIndex = 0

    def img_size(self):
        return self._size

    def fps(self):
        return 30

    def generator(self):
        while True:
            _, self.frame = self.cam.read()
            self.camInputs()
            yield self.frame

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