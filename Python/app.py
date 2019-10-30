# 3rd party modules
from collections import deque

# my modules
import sendkeys
from model import buildModel
from game import Game
from agent import Agent
from train import Train

#######################################

def playGame(observe=False):
    tensorModel = buildModel()
    game = Game()
    agent = Agent(game)
    train = Train(agent, game)

    try:
        train.trainNetwork(tensorModel, observe=observe)
    except StopIteration:
        game.End()


# playGame(False)

import time
import image
game = Game()

while True:
    image.CaptureImage()
    game.IsGameEnded(image.GetLastImage())
    game.HasCredit(image.GetLastImage())
    time.sleep(0.3)
    

# debug code to get the image
# import image
# import model
# import cv2
# while True:
#     image.CaptureImage()
#     canny = image.GetEdgeDetectedImage(image.GetLastImage())
#     boardframe = canny[100:model.IMAGE_ROWS, 0:model.IMAGE_COLS]
#     cv2.imshow("gameboard", boardframe)
