import time
import image
from game import Game

class Agent:
    def __init__(self, game: Game):
        print ("Initialising Agent")
        self._game = game
        self.StartGame()

    def StartGame(self):
        print ("Inserting Coin")
        self._game.InsertCoin()
        time.sleep(0.1)

        print ("Starting Game")
        self._game.StartGame()
        time.sleep(0.2)

        print ("Capturing Initial Image")
        image.CaptureImage()

        print ("Waiting for Game Initialisation")
        while self._game.IsGameInitializing(image.lastCapturedImage):
            time.sleep(0.2)
            image.CaptureImage()
        print ("Game Initialisation Detected")

    def MoveUp(self):
        self._game.MoveUp()
    
    def MoveDown(self):
        self._game.MoveDown()

    def MoveLeft(self):
        self._game.MoveLeft()

    def MoveRight(self):
        self._game.MoveRight()

    def IsGameEnded(self):
        return self._game.IsGameEnded(image.lastCapturedImage)
    
    def IsPacDead(self):
        # after he dies, but before he regenerates
        # we should stop the model running so it doesnt train stupid shit
        return False
    

    