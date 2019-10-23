import pyautogui
import sendkeys
import ctypes
import mss
import numpy
import cv2
import imagehash
from PIL import Image
import image

class Game:

    def __init__(self):
        # moves to the second monitor and gives the MAME window focus
        pyautogui.moveTo(3000, 500)
        pyautogui.click()

    def InsertCoin(self):
        sendkeys.SendScanCodeInput(0x06)

    def StartGame(self):
        sendkeys.SendScanCodeInput(0x02)

    def MoveUp(self):
        # todo check!
        sendkeys.SendScanCodeInput(0xCA)

    def MoveDown(self):
        # todo check!
        sendkeys.SendScanCodeInput(0xCC)

    def MoveLeft(self):
        # todo check!
        sendkeys.SendScanCodeInput(0xCD)

    def MoveRight(self):
        # todo check!
        sendkeys.SendScanCodeInput(0xCB)

    def Pause(self):
        # todo check!
        sendkeys.SendScanCodeInput(0xDD)

    def Resume(self):
        # todo check!
        sendkeys.SendScanCodeInput(0xDE)

    def GetScore(self):
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
            digitframe = image.lastCapturedImage[DIGIT_TOP:DIGIT_BOTTOM,
                            ONES_RIGHT - (DIGIT_WIDTH * (digit+1)):ONES_RIGHT-(DIGIT_WIDTH*digit)]
            digithash = str(imagehash.average_hash(Image.fromarray(digitframe)))

            if digithash == "0000000000000000":
                break

            if digithash in hashes:
                value += multiplier * hashes[digithash]
            else:
                # cv2.imshow('ones', digitframe)
                print("unexpected hash for digit: " +
                    str(digit) + " = " + digithash)

            multiplier = multiplier * 10

        return value

    def HasCredit(self, frame):
        # look for anything but zero in the first position
        creditcountframe = frame[969:997, 251:277]
        # cv2.imshow('creditcountarea', creditcountframe)
        credithash = str(imagehash.average_hash(Image.fromarray(creditcountframe)))
        if credithash == '0000000000000000':
            return False

        if credithash == '383c46c7c7e63c18':
            return False

        return True
        
    def IsGameEnded(self, frame):
        # look for word 'credit' at bottom of screen
        creditframe = frame[969:997, 35:198]
        # cv2.imshow('creditarea', creditframe)
        credithash = str(imagehash.average_hash(Image.fromarray(creditframe)))
        if credithash == '12ffa8307860fe10':
            return True

        # look for word 'game' in middle of screen
        # look for word 'over' in middle of screen
        return False

    def IsGameInitializing(self, frame):
        startupframe = frame[550:585, 278:440]
        # cv2.imshow('startupframe', startupframe)
        credithash = str(imagehash.average_hash(Image.fromarray(startupframe)))
        if credithash == '00ffdffebcf82000':
            return True

        return False

