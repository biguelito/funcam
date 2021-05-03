import pyvirtualcam
import cv2
from basicsfilters import BasicsFilters


class VCam:

    def __init__(self):
        cv2.namedWindow('feedback')
        self.camerror = True

        self.vc = cv2.VideoCapture(0)
        if not self.vc.isOpened():
            raise RuntimeError('Can\'t open your camera, please check if videocap is validy device using "v4l2-ctl --list-device"')

        self.vc.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.vc.set(cv2.CAP_PROP_FPS, 30)

        # Query final capture device values (may be different from preferred settings).
        self.width = int(self.vc.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.vc.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps_out = self.vc.get(cv2.CAP_PROP_FPS)

        self.filterList = ['normal', 'negative', 'bgr2gray']
        self.filterIndex = 0

    def start(self):
        try:
            with pyvirtualcam.Camera(self.width, self.height, self.fps_out, print_fps=True, fmt=pyvirtualcam.PixelFormat.BGR,) as cam:
                print(f'Virtual cam started: {cam.device} ({cam.width}x{cam.height} @ {cam.fps}fps)')

                while True:
                    # Read frame from webcam.
                    ret, self.frame = self.vc.read()
                    if not ret:
                        raise RuntimeError('Error fetching frame')

                    self.camInputs()

                    # See feedback
                    cv2.imshow('feedback', self.frame)
                    # Send to virtual cam.
                    cam.send(self.frame)

        except RuntimeError:
            if self.camerror:
                print('Can\'t use virtual camera, please try "sudo modprobe v4l2loopback"')
            print('Virtual camera closed')

    def camInputs(self):
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            cv2.destroyWindow('feedback')
            self.camerror = False
            self.vc.release()
        elif key == 91:
            self.filterIndex = (self.filterIndex - 1) % len(self.filterList)
        elif key == 93:
            self.filterIndex = (self.filterIndex + 1) % len(self.filterList)
        filter = self.filterList[self.filterIndex]
        self.frame = getattr(BasicsFilters, filter)(self.frame)