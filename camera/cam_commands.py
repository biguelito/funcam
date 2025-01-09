from tracking.hand_tracking import HandTracking
import math
from camera.cam_marks import CamMarks
from datetime import datetime
from utils.input_keys import InputKeys

class CamCommands:
    def __init__(self, cam_width, cam_height, enabled=True):
        self.enabled = enabled
        self.radius = 40
        self.nextX, self.nextY = cam_width-self.radius, cam_height//2
        self.prevX, self.prevY = self.radius, cam_height//2
        self.escX, self.escY = cam_width-self.radius, self.radius

        self.camMarks = CamMarks()

        return
    
    def drawCommands(self, frame):
        self.camMarks.drawCircle(frame, self.nextX, self.nextY, self.radius)
        self.camMarks.drawCircle(frame, self.prevX, self.prevY, self.radius)
        self.camMarks.drawCircle(frame, self.escX, self.escY, self.radius)

        return 
    
    def doInputKey(self, input_key):
        if input_key == InputKeys.ESC:
            self.close()

        elif input_key == InputKeys.LEFT_BRACKET:
            self.filterIndex = (self.filterIndex - 1) % len(self.filterList)

        elif input_key == InputKeys.RIGHT_BRACKET:
            self.filterIndex = (self.filterIndex + 1) % len(self.filterList)

    def handCommands(self):
        self.detector.findHands(self.frame)
        lmList, bbox = self.detector.findPosition(self.frame)

        if lmList:
            fingerX, fingerY = lmList[self.finger][1], lmList[self.finger][2]

            init = datetime.timestamp(datetime.now())

            # next filter
            if math.hypot(fingerX - self.nextX, fingerY - self.nextY) <= 30:
                actual = datetime.timestamp(datetime.now())

                if not self.pressing:
                    self.pressing = True
                    self.initialTime = init

                else:
                    presstime = int(actual - self.initialTime)
                    if presstime == 1:
                        self.filterIndex = (self.filterIndex + 1) % len(self.filterList)
                        self.pressing = False

            # previus filter
            elif math.hypot(fingerX - self.prevX, fingerY - self.prevY) <= 30:
                actual = datetime.timestamp(datetime.now())

                if not self.pressing:
                    self.pressing = True
                    self.initialTime = init

                else:
                    presstime = int(actual - self.initialTime)

                    if presstime == 1:
                        self.filterIndex = (self.filterIndex - 1) % len(self.filterList)
                        self.pressing = False

            # close cam
            elif math.hypot(fingerX - self.escX, fingerY - self.escY) <= 30:
                actual = datetime.timestamp(datetime.now())

                if not self.pressing:
                    self.pressing = True
                    self.initialTime = init

                else:
                    presstime = int(actual - self.initialTime)

                    if presstime == 2:
                        self.cam.release()
                        self.display = False
                        self.pressing = False

            else:
                self.pressing = False
                self.initialTime = init
    