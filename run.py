from cam import Cam
from vcam import VCam
import sys

if __name__ == '__main__':

    mode = sys.argv[1]

    if mode == 'c':
        # own cam
        vc = Cam()
        vc.open()

    elif mode == 'v':
        # virtual cam
        vc = VCam()
        vc.start()

    else:
        print('please run "python3 run.py [c/v]"')
        print('c for see your cam')
        print('v for activate virtual cam')