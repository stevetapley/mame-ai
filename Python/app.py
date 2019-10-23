# 3rd party modules
from collections import deque

# my modules
import sendkeys
import gamestate
import model
import train
from game import Game
from agent import Agent
from gamestate import GameState
#######################################

def playGame(observe=False):
    game = Game()
    agent = Agent(game)
    game_state = GameState(agent,game)
    model = model.buildmodel()
    try:
        train.trainNetwork(model,game_state,observe=observe)
    except StopIteration:
        game.end()

train.Initialise()
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

