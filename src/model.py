import matplotlib.pyplot as plt
import numpy as np
from keras.backend.tensorflow_backend import set_session
import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Input, TimeDistributed, BatchNormalization, Reshape, Dense, Flatten, Activation, \
    Dropout
from tensorflow.keras.losses import binary_crossentropy
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.utils import plot_model
from tensorflow.keras import backend
import datetime

config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
config.gpu_options.per_process_gpu_memory_fraction = 0.9
config.allow_soft_placement = True
sess = tf.compat.v1.Session(config=config)
set_session(sess)

print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

dropout_rate = 0.1
momentum = 0.9

num_bars = 16
num_notes = 96
num_time_samples = 96

midi_matrices = np.load('samples bool.npy')
midi_matrices = midi_matrices.reshape(-1, num_bars, num_notes, num_time_samples)

model = Sequential()

# Input is 16 bars of 96 notes over 96 samples
model.add(Input(shape=midi_matrices[0].shape))
model.add(Reshape((num_bars, num_notes * num_time_samples)))

# Convert each bar to a usable vector
model.add(TimeDistributed(Dense(2000, activation='relu')))
model.add(TimeDistributed(Dense(200, activation='relu')))
model.add(Flatten())

# Reduce number of nodes to generate key principle components
model.add(Dense(1600, activation='relu'))
model.add(Dense(120))
model.add(BatchNormalization(momentum=momentum, name='encoder1'))

model.add(Dense(1600, name='encoder2'))
model.add(BatchNormalization(momentum=momentum))
model.add(Activation('relu'))
if dropout_rate > 0:
    model.add(Dropout(dropout_rate))

# Start decoding back to higher dimensions
model.add(Dense(num_bars * 200))
model.add(Reshape((num_bars, 200)))
model.add(TimeDistributed(BatchNormalization(momentum=momentum)))
model.add(Activation('relu'))
if dropout_rate > 0:
    model.add(Dropout(dropout_rate))

model.add(TimeDistributed(Dense(2000)))
model.add(TimeDistributed(BatchNormalization(momentum=momentum)))
model.add(Activation('relu'))
if dropout_rate > 0:
    model.add(Dropout(dropout_rate))

# Decode back to 16 bars of 96 notes by 96 time samples
model.add(TimeDistributed(Dense(num_notes * num_time_samples, activation='sigmoid')))
model.add(Reshape((num_bars, num_notes, num_time_samples)))

model.compile(optimizer=RMSprop(lr=0.001), loss='binary_crossentropy')

# plot_model(model, to_file='model.png', show_shapes=True)
print(model.summary())

log_directory = "..\logs\\" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_directory, histogram_freq=1)

model.fit(midi_matrices, midi_matrices, batch_size=400, epochs=2000, validation_split=0.05,
          callbacks=[tensorboard_callback])
model.save(r"C:\Users\Jonny\PycharmProjects\contextual-music-composition\saved models\autoencoder 2000.h5")
