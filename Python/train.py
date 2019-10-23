import time
import numpy as np
import model
import random
import tensorflow as tf
import utilities
from collections import deque
from gamestate import GameState
import json
import pandas as pd
import os.path

loss_file_path = "./objects/loss_df.csv"
actions_file_path = "./objects/actions_df.csv"
scores_file_path = "./objects/scores_df.csv"
loss_df = None
scores_df = None
actions_df = None

def Initialise():
    # initial variable caching, done only once
    if not utilities.FileExists("epsilon"):
        utilities.SaveObject(model.INITIAL_EPSILON,"epsilon")
        t = 0
        utilities.SaveObject(t,"time")
        D = deque()
        utilities.SaveObject(D,"D")

    # Intialize log structures from file if exists else create new
    global loss_df
    loss_df = pd.read_csv(loss_file_path) if os.path.isfile(loss_file_path) else pd.DataFrame(columns =['loss'])

    global scores_df
    scores_df = pd.read_csv(scores_file_path) if os.path.isfile(loss_file_path) else pd.DataFrame(columns = ['scores'])

    global actions_df
    actions_df = pd.read_csv(actions_file_path) if os.path.isfile(actions_file_path) else pd.DataFrame(columns = ['actions'])

#
# main training module
# Parameters:
# * model => Keras Model to be trained
# * game_state => Game State module with access to game environment and dino
# * observe => flag to indicate wherther the model is to be trained(weight updates), else just play
def trainNetwork(model,game_state: GameState,observe=False):
    last_time = time.time()
    # store the previous observations in replay memory
    D = utilities.LoadObject("D") #load from file system
    # get the first state by doing nothing
    do_nothing = np.zeros(model.ACTIONS)
    do_nothing[0] =1 #0 => do nothing,
                     #1=> jump
    
    x_t, r_0, terminal = game_state.get_state(do_nothing) # get next step after performing the action
    

    s_t = np.stack((x_t, x_t, x_t, x_t), axis=2) # stack 4 images to create placeholder input
    

    
    s_t = s_t.reshape(1, s_t.shape[0], s_t.shape[1], s_t.shape[2])  #1*20*40*4
    
    initial_state = s_t 

    if observe :
        OBSERVE = 999999999    #We keep observe, never train
        epsilon = model.FINAL_EPSILON
        print ("Now we load weight")
        model.load_weights("model_final.h5")
        adam = tf.keras.optimizers.Adam(lr=model.LEARNING_RATE)
        model.compile(loss='mse',optimizer=adam)
        print ("Weight load successfully")    
    else:                       #We go to training mode
        OBSERVE = model.OBSERVATION
        epsilon = utilities.LoadObject("epsilon") 
        model.load_weights("model_final.h5")
        adam = tf.keras.optimizers.Adam(lr=model.LEARNING_RATE)
        model.compile(loss='mse',optimizer=adam)

    t = utilities.LoadObject("time") # resume from the previous time step stored in file system
    while (True): #endless running
        
        loss = 0
        Q_sa = 0
        action_index = 0
        r_t = 0 #reward at 4
        a_t = np.zeros([model.ACTIONS]) # action at t
        
        #choose an action epsilon greedy
        if t % model.FRAME_PER_ACTION == 0: #parameter to skip frames for actions
            if  random.random() <= epsilon: #randomly explore an action
                print("----------Random Action----------")
                action_index = random.randrange(model.ACTIONS)
                a_t[0] = 1
            else: # predict the output
                q = model.predict(s_t)       #input a stack of 4 images, get the prediction
                max_Q = np.argmax(q)         # chosing index with maximum q value
                action_index = max_Q 
                a_t[action_index] = 1        # o=> do nothing, 1=> jump
                
        #We reduced the epsilon (exploration parameter) gradually
        if epsilon > model.FINAL_EPSILON and t > OBSERVE:
            epsilon -= (model.INITIAL_EPSILON - model.FINAL_EPSILON) / model.EXPLORE 

        #run the selected action and observed next state and reward
        x_t1, r_t, terminal = game_state.get_state(a_t)
        print('loop took {} seconds'.format(time.time()-last_time)) # helpful for measuring frame rate
        last_time = time.time()
        x_t1 = x_t1.reshape(1, x_t1.shape[0], x_t1.shape[1], 1) #1x20x40x1
        s_t1 = np.append(x_t1, s_t[:, :, :, :3], axis=3) # append the new image to input stack and remove the first one
        
        
        # store the transition in D
        D.append((s_t, action_index, r_t, s_t1, terminal))
        if len(D) > model.REPLAY_MEMORY:
            D.popleft()

        #only train if done observing
        if t > OBSERVE: 
            
            #sample a minibatch to train on
            minibatch = random.sample(D, model.BATCH)
            inputs = np.zeros((model.BATCH, s_t.shape[1], s_t.shape[2], s_t.shape[3]))   #32, 20, 40, 4
            targets = np.zeros((inputs.shape[0], model.ACTIONS))                         #32, 2

            #Now we do the experience replay
            for i in range(0, len(minibatch)):
                state_t = minibatch[i][0]    # 4D stack of images
                action_t = minibatch[i][1]   #This is action index
                reward_t = minibatch[i][2]   #reward at state_t due to action_t
                state_t1 = minibatch[i][3]   #next state
                terminal = minibatch[i][4]   #wheather the agent died or survided due the action
                

                inputs[i:i + 1] = state_t    

                targets[i] = model.predict(state_t)  # predicted q values
                Q_sa = model.predict(state_t1)      #predict q values for next step
                
                if terminal:
                    targets[i, action_t] = reward_t # if terminated, only equals reward
                else:
                    targets[i, action_t] = reward_t + model.GAMMA * np.max(Q_sa)

            loss += model.train_on_batch(inputs, targets)
            loss_df.loc[len(loss_df)] = loss
        else:
            # artificial time delay as training done with this delay
            time.sleep(0.12)
        s_t = initial_state if terminal else s_t1 #reset game to initial frame if terminate
        t = t + 1
        
        # save progress every 1000 iterations
        if t % 1000 == 0:
            print("Now we save model")
            
            model.save_weights("model_final.h5", overwrite=True)
            utilities.SaveObject(D,"D") #saving episodes
            utilities.SaveObject(t,"time") #caching time steps
            utilities.SaveObject(epsilon,"epsilon") #cache epsilon to avoid repeated randomness in actions
            loss_df.to_csv("./objects/loss_df.csv",index=False)
            scores_df.to_csv("./objects/scores_df.csv",index=False)
            actions_df.to_csv("./objects/actions_df.csv",index=False)
            with open("model.json", "w") as outfile:
                json.dump(model.to_json(), outfile)

        # print info
        state = ""
        if t <= OBSERVE:
            state = "observe"
        elif t > OBSERVE and t <= OBSERVE + model.EXPLORE:
            state = "explore"
        else:
            state = "train"

        print("TIMESTEP", t, "/ STATE", state,             "/ EPSILON", epsilon, "/ ACTION", action_index, "/ REWARD", r_t,             "/ Q_MAX " , np.max(Q_sa), "/ Loss ", loss)

    print("Episode finished!")
    print("************************")