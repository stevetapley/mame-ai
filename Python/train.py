import time
import numpy as np
import model
import random
import tensorflow as tf
import utilities
from collections import deque
import json
import pandas as pd
import os.path
from utilities import RootFolder
from game import Game
from agent import Agent
import image

#
# main training module
# Parameters:
# * model => Keras Model to be trained
# * observe => flag to indicate whether the model is to be trained(weight updates), else just play


class Train:

    def __init__(self, agent: Agent, game: Game):

        self._agent = agent
        self._game = game

        self.loss_file_path = RootFolder + "objects/loss_df.csv"
        self.actions_file_path = RootFolder + "objects/actions_df.csv"
        self.scores_file_path = RootFolder + "objects/scores_df.csv"

        # initial variable caching, done only once
        if not utilities.FileExists("epsilon"):
            utilities.SaveObject(model.INITIAL_EPSILON, "epsilon")
            t = 0
            utilities.SaveObject(t, "time")
            D = deque()
            utilities.SaveObject(D, "D")

        # Intialize log structures from file if exists else create new
        self.loss_df = pd.read_csv(self.loss_file_path) if os.path.isfile(
            self.loss_file_path) else pd.DataFrame(columns=['loss'])
        self.scores_df = pd.read_csv(self.scores_file_path) if os.path.isfile(
            self.scores_file_path) else pd.DataFrame(columns=['scores'])
        self.actions_df = pd.read_csv(self.actions_file_path) if os.path.isfile(
            self.actions_file_path) else pd.DataFrame(columns=['actions'])

    def GetGameState(self, actions):
        # storing actions in a dataframe
        self.actions_df.loc[len(self.actions_df)] = actions[1]

        score = self._game.GetScore()
        reward = 0.1*score/10  # dynamic reward calculation
        is_over = False  # game over
        if actions[1] == 1:
            self._agent.MoveDown()
            reward = 0.1*score/11
        elif actions[2] == 1:
            self._agent.MoveUp()
            reward = 0.1*score/11
        elif actions[3] == 1:
            self._agent.MoveLeft()
            reward = 0.1*score/11
        elif actions[4] == 1:
            self._agent.MoveRight()
            reward = 0.1*score/11

        image = self.GetGameBoard()

        if self._agent.IsGameEnded():
            # log the score when game is over
            self.scores_df.loc[len(self.scores_df)] = score
            self._game.restart()
            reward = -11/score
            is_over = True

        return image, reward, is_over  # return the Experience tuple

    def GetGameBoard(self):
        boardframe = image.GetEdgeDetectedImage(image.GetLastImage()[60:950, 0:730])
        boardframe = np.array(boardframe).astype(np.float16)

        # cv2.imshow('boardframe', boardframe)
        return boardframe

    def trainNetwork(self, tensorModel, observe=False):
        last_time = time.time()
        # store the previous observations in replay memory
        D = utilities.LoadObject("D")  # load from file system
        # get the first state by doing nothing
        do_nothing = np.zeros(model.ACTIONS)
        do_nothing[0] = 1  # 0 => do nothing,

        # get next step after performing the action
        gameImage, reward, isGameOver = self.GetGameState(do_nothing)

        # stack 4 images to create placeholder input
        s_t = np.stack((gameImage, gameImage, gameImage, gameImage), axis=2)

        s_t = s_t.reshape(1, s_t.shape[0], s_t.shape[1], s_t.shape[2])

        initial_state = s_t

        if observe:
            OBSERVE = 999999999  # We keep observe, never train
            epsilon = model.FINAL_EPSILON
            print("Now we load weight")
            tensorModel.load_weights("model_final.h5")
            adam = tf.keras.optimizers.Adam(lr=model.LEARNING_RATE)
            tensorModel.compile(loss='mse', optimizer=adam)
            print("Weight load successfully")
        else:  # We go to training mode
            OBSERVE = model.OBSERVATION
            epsilon = utilities.LoadObject("epsilon")
            if (os.path.exists("model_final.h5")):
                tensorModel.load_weights("model_final.h5")
            adam = tf.keras.optimizers.Adam(lr=model.LEARNING_RATE)
            tensorModel.compile(loss='mse', optimizer=adam)

        # resume from the previous time step stored in file system
        t = utilities.LoadObject("time")
        while (True):  # endless running

            loss = 0
            Q_sa = 0
            action_index = 0
            r_t = 0  # reward at 4
            a_t = np.zeros([model.ACTIONS])  # action at t

            # choose an action epsilon greedy
            if t % model.FRAME_PER_ACTION == 0:  # parameter to skip frames for actions
                if random.random() <= epsilon:  # randomly explore an action
                    print("----------Random Action----------")
                    action_index = random.randrange(model.ACTIONS)
                    a_t[0] = 1
                else:  # predict the output
                    # input a stack of 4 images, get the prediction
                    q = tensorModel.predict(s_t)
                    # chosing index with maximum q value
                    max_Q = np.argmax(q)
                    action_index = max_Q
                    a_t[action_index] = 1 

            # We reduced the epsilon (exploration parameter) gradually
            if epsilon > model.FINAL_EPSILON and t > OBSERVE:
                epsilon -= (model.INITIAL_EPSILON - model.FINAL_EPSILON) / model.EXPLORE

            # run the selected action and observed next state and reward
            x_t1, r_t, isGameOver = self.GetGameState(a_t)
            # helpful for measuring frame rate
            print('loop took {} seconds'.format(time.time()-last_time))
            last_time = time.time()
            x_t1 = x_t1.reshape(1, x_t1.shape[0], x_t1.shape[1], 1)  # 1x20x40x1
            # append the new image to input stack and remove the first one
            s_t1 = np.append(x_t1, s_t[:, :, :, :3], axis=3)

            # store the transition in D
            D.append((s_t, action_index, r_t, s_t1, isGameOver))
            if len(D) > model.REPLAY_MEMORY:
                D.popleft()

            # only train if done observing
            if t > OBSERVE:

                # sample a minibatch to train on
                minibatch = random.sample(D, model.BATCH)
                # 32, 20, 40, 4
                inputs = np.zeros((model.BATCH, s_t.shape[1], s_t.shape[2], s_t.shape[3]))
                targets = np.zeros((inputs.shape[0], model.ACTIONS))  # 32, 2

                # Now we do the experience replay
                for i in range(0, len(minibatch)):
                    state_t = minibatch[i][0]    # 4D stack of images
                    action_t = minibatch[i][1]  # This is action index
                    # reward at state_t due to action_t
                    reward_t = minibatch[i][2]
                    state_t1 = minibatch[i][3]  # next state
                    # wheather the agent died or survided due the action
                    isGameOver = minibatch[i][4]

                    inputs[i:i + 1] = state_t

                    targets[i] = tensorModel.predict(
                        state_t)  # predicted q values
                    # predict q values for next step
                    Q_sa = tensorModel.predict(state_t1)

                    if isGameOver:
                        # if terminated, only equals reward
                        targets[i, action_t] = reward_t
                    else:
                        targets[i, action_t] = reward_t + \
                            model.GAMMA * np.max(Q_sa)

                loss += tensorModel.train_on_batch(inputs, targets)
                self.loss_df.loc[len(self.loss_df)] = loss
            else:
                # artificial time delay as training done with this delay
                time.sleep(0.12)
            # reset game to initial frame if terminate
            s_t = initial_state if isGameOver else s_t1
            t = t + 1

            # save progress every 1000 iterations
            if t % 1000 == 0:
                print("Now we save model")

                tensorModel.save_weights("model_final.h5", overwrite=True)
                utilities.SaveObject(D, "D")  # saving episodes
                utilities.SaveObject(t, "time")  # caching time steps
                # cache epsilon to avoid repeated randomness in actions
                utilities.SaveObject(epsilon, "epsilon")
                self.loss_df.to_csv(self.loss_file_path, index=False)
                self.scores_df.to_csv(self.scores_file_path, index=False)
                self.actions_df.to_csv(self.actions_file_path, index=False)
                with open("model.json", "w+") as outfile:
                    json.dump(tensorModel.to_json(), outfile)

            # print info
            state = ""
            if t <= OBSERVE:
                state = "observe"
            elif t > OBSERVE and t <= OBSERVE + model.EXPLORE:
                state = "explore"
            else:
                state = "train"

            print("TIMESTEP", t, "/ STATE", state,             "/ EPSILON", epsilon, "/ ACTION",
                  action_index, "/ REWARD", r_t,             "/ Q_MAX ", np.max(Q_sa), "/ Loss ", loss)

        print("Episode finished!")
        print("************************")
