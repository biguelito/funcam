import pyvirtualcam
import cv2
from basicsfilters import BasicsFilters


class VCam:

    def __init__(self):
        cv2.namedWindow("preview")
        self.vc = cv2.VideoCapture(0)
        if not self.vc.isOpened():
            raise RuntimeError('Could not open video source')

        pref_width = 1280
        pref_height = 720
        pref_fps_in = 30
        self.vc.set(cv2.CAP_PROP_FRAME_WIDTH, pref_width)
        self.vc.set(cv2.CAP_PROP_FRAME_HEIGHT, pref_height)
        self.vc.set(cv2.CAP_PROP_FPS, pref_fps_in)

        # Query final capture device values (may be different from preferred settings).
        self.width = int(self.vc.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.vc.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps_in = self.vc.get(cv2.CAP_PROP_FPS)
        print(f'Webcam capture started ({self.width}x{self.height} @ {self.fps_in}fps)')

        self.fps_out = 20

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
                    cv2.imshow("feedback", self.frame)
                    # Send to virtual cam.
                    cam.send(self.frame)

        except RuntimeError:
            print('Virtual cam closed')

    def camInputs(self):
        key = cv2.waitKey(20)
        if key == 27:  # exit on ESC
            cv2.destroyWindow("preview")
            self.vc.release()
        elif key == 91:
            self.filterIndex = (self.filterIndex - 1) % len(self.filterList)
        elif key == 93:
            self.filterIndex = (self.filterIndex + 1) % len(self.filterList)
        filter = self.filterList[self.filterIndex]
        self.frame = getattr(BasicsFilters, filter)(self.frame)