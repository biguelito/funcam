#!/home/gabriel/funcam/funcam-venv/bin/python3.8

from cam import Cam
from vcam import VCam
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--virtual',
                        help='enable virtual cam',
                        action='store_true')
    args = parser.parse_args()

    if args.virtual:
        # virtual cam
        vc = VCam()
        vc.start()

    else:
        # own cam
        vc = Cam()
        vc.open()
