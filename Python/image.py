
import mss
import numpy
import cv2

# stores the last image captured so that it can be used by multiple modules
lastCapturedImage = None

def CaptureImage():
    with mss.mss() as sct:
        monitor_number = 1
        mon = sct.monitors[monitor_number]
        monitor = {
            "top": mon["top"]+33,
            "left": mon["left"] + 604,
            "width": 732,
            "height": 1180,
            "mon": monitor_number,
        }

        global lastCapturedImage
        lastCapturedImage = numpy.array(sct.grab(monitor))

        cv2.imshow('frame', lastCapturedImage)

        return lastCapturedImage
    
def GetLastImage():
    return lastCapturedImage