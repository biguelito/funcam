import cv2
import numpy as np


class Filters:

    def normal(frame):
        return frame

    def negative(frame):
        return 255 - frame

    def bgr2gray(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        grayframe = np.zeros_like(frame)
        grayframe[:, :, 0] = gray
        grayframe[:, :, 1] = gray
        grayframe[:, :, 2] = gray
        return grayframe
