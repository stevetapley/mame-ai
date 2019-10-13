
# assume mame has started
# assume someone has selected the game
# assume the game has booted up

# move mouse to mame window, start game - press '5' to give a credit, then press '1' to start the game
import pyautogui
pyautogui.moveTo(3000, 500)
pyautogui.click()
pyautogui.typewrite("55555", 1)

# screenshotting
import time
import cv2
import mss
import numpy
with mss.mss() as sct:
    # Screen cap the board
    monitor_number = 1
    mon = sct.monitors[monitor_number]
    monitor = {
        "top": mon["top"],
        "left": mon["left"] + 550,
        "width": 820,
        "height":1200,
        "mon": monitor_number,
    }

    while "Screen capturing":
        last_time = time.time()

        # Get raw pixels from the screen, save it to a Numpy array
        img = numpy.array(sct.grab(monitor))

        # Display the picture
        cv2.imshow("OpenCV/Numpy normal", img)

        # Display the picture in grayscale
        # cv2.imshow('OpenCV/Numpy grayscale',
        #            cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))

        print("fps: {}".format(1 / (time.time() - last_time)))

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break