from cam import Cam
from fakecam import MyVideoSource

import virtualvideo


if __name__ == '__main__':

    """fakecam"""
    # print('fakecam on')
    # vidsrc = MyVideoSource()
    # fvd = virtualvideo.FakeVideoDevice()
    # fvd.init_input(vidsrc)
    # fvd.init_output(4, 640, 480)
    # fvd.run()

    """own cam"""
    cv = Cam()
    cv.open()
