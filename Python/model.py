import tensorflow as tf

# model hyper parameters
LEARNING_RATE = 1e-4
IMAGE_ROWS_OFFSET = 100
IMAGE_ROWS = 920
IMAGE_COLS_OFFSET = 0
IMAGE_COLS = 710
IMG_CHANNELS = 4 #We stack 4 frames

# game parameters
ACTIONS = 5 # move 4 ways, do nothing
GAMMA = 0.99 # decay rate of past observations original 0.99
OBSERVATION = 50000. # timesteps to observe before training
EXPLORE = 100000  # frames over which to anneal epsilon
FINAL_EPSILON = 0.0001 # final value of epsilon
INITIAL_EPSILON = 0.1 # starting value of epsilon
REPLAY_MEMORY = 50000 # number of previous transitions to remember
BATCH = 32 # size of minibatch
FRAME_PER_ACTION = 1

def buildModel():
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Conv2D(32, (8, 8), strides=(4, 4), padding='same',input_shape=(IMAGE_ROWS-IMAGE_ROWS_OFFSET,IMAGE_COLS-IMAGE_COLS_OFFSET,IMG_CHANNELS)))
    model.add(tf.keras.layers.Activation('relu'))
    model.add(tf.keras.layers.Conv2D(64, (4, 4), strides=(2, 2), padding='same'))
    model.add(tf.keras.layers.Activation('relu'))
    model.add(tf.keras.layers.Conv2D(64, (3, 3), strides=(1, 1), padding='same'))
    model.add(tf.keras.layers.Activation('relu'))
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(512))
    model.add(tf.keras.layers.Activation('relu'))
    model.add(tf.keras.layers.Dense(ACTIONS))
    adam = tf.keras.optimizers.Adam(lr=LEARNING_RATE)
    model.compile(loss='mse',optimizer=adam)
    return model


