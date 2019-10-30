
import mss
import numpy
import cv2
import utilities

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
        # cv2.imshow('frame', lastCapturedImage)

        lastCapturedImage = cv2.Canny(lastCapturedImage, threshold1 = 100, threshold2 = 200)

        cv2.imshow('canny frame', lastCapturedImage)
        cv2.waitKey(delay=1)
        
        return lastCapturedImage
    
def GetLastImage():
    return lastCapturedImage

# def GetEdgeDetectedImage(daImage):
#     canny = cv2.Canny(daImage, threshold1 = 100, threshold2 = 200)
#     cv2.imshow('canny', canny)
#     cv2.waitKey(delay=1)
#     return canny

def IsImageMatch(image_array, template_file_name):
    # write the numpy array to a file
    # TODO: do in memory!
    cv2.imwrite(utilities.GetImageFilePath('image_match_test'), image_array)
    test_img = cv2.imread(utilities.GetImageFilePath('image_match_test'))

    # if template doesnt exist, create it!
    if not utilities.ImageFileExists(template_file_name):
        cv2.imwrite(utilities.GetImageFilePath(template_file_name), image_array)

    template_image = cv2.imread(utilities.GetImageFilePath(template_file_name))
    res = cv2.matchTemplate(test_img, template_image,cv2.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    return max_val > 0.5