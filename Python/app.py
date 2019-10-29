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
    game = Game()
    agent = Agent(game)
    tensorModel = buildModel()
    train = Train(agent,game)

    try:
        train.trainNetwork(tensorModel,observe=observe)
    except StopIteration:
        game.End()

playGame(False)



# ******************* main loop *******************
# a = 1
# img_queue = deque()

# while True:
#     frame = gamestate.SampleScreen()
    
#     gamestate.GetGameBoard(frame)

#     scores = gamestate.GetScore(frame)
#     print('Score = ' + str(scores))
#     if gamestate.IsGameEnded(frame):
#         print('game ended')
#         gamestate.InsertCoin()
#         if gamestate.HasCredit(frame):
#             gamestate.StartGame()
#     else:
#         if not gamestate.WaitingForStartup(frame):

#             # sample initial boards
#             for x in range(model.IMG_CHANNELS)
#                 img_queue.append(gamestate.GetGameBoard(frame))

