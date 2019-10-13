from enum import Enum
import pyautogui
import mss
import numpy
import cv2
import imagehash
from PIL import Image


class States(Enum):
    WaitingForMameShellStartup = 1
    WaitingForGameShellStartup = 2
    WaitingForGameToStart = 3


def InsertCoin():
    pyautogui.moveTo(3000, 500)
    pyautogui.click()
    pyautogui.typewrite("5")


def StartGame():
    pyautogui.moveTo(3000, 500)
    pyautogui.click()
    pyautogui.typewrite("1")


def SampleScreen():
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
        img = numpy.array(sct.grab(monitor))
        return img


def TransformScreenCapture():
    # gray scale?
    return 0


def GetScore(frame):
    DIGIT_WIDTH = 27
    DIGIT_TOP = 30
    DIGIT_BOTTOM = 54
    ONES_RIGHT = 169

    hashes = {
        "1c2663636363341c": 0,
        "1c2663636363361c": 0,
        "0c1c0c0c0c0c1e3f": 1,
        "0c1c0c0c0c0c3e3f": 1,
        "3e63071e3c38707f": 2,
        "3f060c1e0703673e": 3,
        "3f060c1e0303633e": 3,
        "0e1e36667f7f0606": 4,
        "7e607e060303663e": 5,
        "7e607e030303633e": 5,
        "1e30607c6663663e": 6,
        "1e30607e6663663e": 6,
        "1e30607e6763623e": 6,
        "ffe7060c18181818": 7,
        "7f67060c18181818": 7,
        "7f63060c18181818": 7,
        "3c6272384ecf463e": 8,
        "3c62723c4e4f463e": 8,
        "3c62723c0e4f463e": 8,
        "3c62723c4e4f423e": 8,
        "3e63637f07060c3c": 9,
        "0000000000000000": 0
    }
    value = 0

    multiplier = 1
    for digit in range(4):
        digitframe = frame[DIGIT_TOP:DIGIT_BOTTOM, ONES_RIGHT -
                           (DIGIT_WIDTH * (digit+1)):ONES_RIGHT-(DIGIT_WIDTH*digit)]
        digithash = str(imagehash.average_hash(Image.fromarray(digitframe)))

        if digithash == "0000000000000000":
            break

        if digithash in hashes:
            value += multiplier * hashes[digithash]
        else:
            # cv2.imshow('ones', digitframe)
            print("unexpected hash for digit: " + str(digit) + " = " + digithash)

        multiplier = multiplier * 10

    return value


# ******************* main loop *******************
while True:
    frame = SampleScreen()

    scores = GetScore(frame)
    print(scores)

    # Press "q" to quit
    if cv2.waitKey(25) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break
