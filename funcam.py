from time import sleep
from camera.cam import Cam
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--video', help='choose video input', type=int, default=0)
    parser.add_argument('--maxhands', help='set max hands for detection', type=int, default=1)
    parser.add_argument('-d', help='enable draw for marks and functional areas', action='store_true')
    parser.add_argument('--finger', help='choose the finger for control', type=int, default=8, choices=[4, 8, 12, 16, 20])
    args = parser.parse_args()

    cam = Cam(video=args.video, mxhand=args.maxhands, markCommands=args.d, f=args.finger)
    cam.open()