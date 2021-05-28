#!/home/gabriel/funcam/funcam-venv/bin/python3.8
# ONLY TESTED ON UBUNTU
# To run using ./run.py [args] on your terminal
# point the first line to your virtual environment or some python interpreter
# containing the requirements


from cam import Cam
from vcam import VCam
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--virtual',help='enable virtual cam',action='store_true')
    parser.add_argument('--video', help='choose video input', type=int, default=0)
    parser.add_argument('--maxhands', help='set max hands for detection', type=int, default=1)
    parser.add_argument('-d', help='enable draw for marks and functional areas', action='store_true')
    parser.add_argument('--finger', help='choose the finger for control', type=int, default=8, choices=[4, 8, 12, 16, 20])
    parser.add_argument('-p', help='enable camera to take photos', action='store_true')
    args = parser.parse_args()

    if args.virtual:
        # virtual cam
        vc = VCam(video=args.video, mxhand=args.maxhands, du=args.d, f=args.finger)
        vc.start()

    else:
        # own cam
        cam = Cam(video=args.video, mxhand=args.maxhands, du=args.d, f=args.finger, p=args.p)
        cam.open()
