import pyautogui
import sendkeys
import ctypes
import mss
import numpy
import cv2
import imagehash
from PIL import Image
import image
from game import Game
from agent import Agent

class GameState:
    def __init__(self, agent: Agent, game: Game):
        self._agent = agent
        self._game = game

    def get_state(self, actions):
        actions_df.loc[len(actions_df)] = actions[1] # storing actions in a dataframe
        score = self._game.GetScore() 
        reward = 0.1*score/10 # dynamic reward calculation
        is_over = False #game over
        if actions[1] == 1:
            self._agent.jump()
            reward = 0.1*score/11
        image = self.GetGameBoard() 
        self._display.send(image) #display the image on screen

        if self._agent.is_crashed():
            scores_df.loc[len(loss_df)] = score # log the score when game is over
            self._game.restart()
            reward = -11/score
            is_over = True
        return image, reward, is_over #return the Experience tuple

    def GetGameBoard(self):
        boardframe = image.lastCapturedImage[60:950, 0:730]
        # cv2.imshow('boardframe', boardframe)
        return boardframe
