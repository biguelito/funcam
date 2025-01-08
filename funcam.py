#!/home/gabriel/funcam/venv/bin/python3
# ONLY TESTED ON LINUX
# To run using ./run.py [args] on your terminal (without python3)
# point the first line to some python interpreter containing the requirements
# or create a venv inside this project.
# Or delete this to use another method.

from cam import Cam
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--video', help='choose video input', type=int, default=0)
    parser.add_argument('--maxhands', help='set max hands for detection', type=int, default=1)
    parser.add_argument('-d', help='enable draw for marks and functional areas', action='store_true')
    parser.add_argument('--finger', help='choose the finger for control', type=int, default=8, choices=[4, 8, 12, 16, 20])
    args = parser.parse_args()

    cam = Cam(video=args.video, mxhand=args.maxhands, du=args.d, f=args.finger)
    cam.open()
