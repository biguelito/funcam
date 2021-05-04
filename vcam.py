import pyvirtualcam
import cv2
from basicsfilters import BasicsFilters


class VCam:

    def __init__(self):
        cv2.namedWindow('feedback')
        self.filterList = ['normal', 'negative', 'bgr2gray']
        self.filterIndex = 0
        self.videocap = 0

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

        with pyvirtualcam.Camera(self.width, self.height, self.fps_out, print_fps=True, fmt=pyvirtualcam.PixelFormat.BGR,) as cam:
            print(f'Virtual cam started: {cam.device} ({cam.width}x{cam.height} @ {cam.fps}fps)')

            while self.display:
                # Read frame from webcam.
                self.ret, self.frame = self.vc.read()
                if not self.ret:
                    raise RuntimeError('Error fetching frame')

                self.camInputs()

                self.frame = cv2.flip(self.frame, 1)
                cv2.imshow('feedback', self.frame)
                cam.send(self.frame)

        print('Virtual camera closed')

    def camInputs(self):
        key = cv2.waitKey(5)

        # ESC
        if key == 27:
            cv2.destroyWindow('feedback')
            self.vc.release()
            self.display = False

        # [
        elif key == 91:
            self.filterIndex = (self.filterIndex - 1) % len(self.filterList)

        # ]
        elif key == 93:
            self.filterIndex = (self.filterIndex + 1) % len(self.filterList)

        filter = self.filterList[self.filterIndex]
        self.frame = getattr(BasicsFilters, filter)(self.frame)