import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, TimeDistributed, BatchNormalization, Reshape, Dense, Flatten, Activation, \
    Dropout
from tensorflow.keras.optimizers import RMSprop
import datetime
import enums

print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))

epochs = 1500

dropout_rate = 0.1
momentum = 0.9

num_bars = 16
num_notes = 96
num_time_samples = 96

midi_matrices = np.load(enums.ALL_SAMPLES_FILEPATH)
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

# tensorboard logging for model details
print(model.summary())
log_directory = "..\logs\\" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_directory, histogram_freq=1)

# Train model and save trained model
model.fit(midi_matrices, midi_matrices, batch_size=100, epochs=epochs, validation_split=0.05,
          callbacks=[tensorboard_callback])
model.save('../saved models/autoencoder ' + str(epochs) + '.h5')
model.save_weights('../saved models/autoencoder ' + str(epochs) + ' weights.h5')
