import cv2

class CamMarks:
    def __init__(self, enabled=False):
        self.enabled = enabled
        
        return
    
    def drawCircle(self, frame, x, y, r, color=(255, 0, 0)):
        cv2.circle(frame, (x, y), r, color)
        return