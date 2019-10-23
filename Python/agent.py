import time
import image
from game import Game

class Agent:
    def __init__(self, game: Game):
        self._game = game
        self.StartGame()

    def StartGame(self):
        self._game.InsertCoin()
        time.sleep(0.1)
        self._game.StartGame()
        time.sleep(0.2)
        image.CaptureImage()
        while self._game.IsGameInitializing(image.lastCapturedImage):
            time.sleep(0.2)
            image.CaptureImage()

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
    

    