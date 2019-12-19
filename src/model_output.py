from tensorflow.compat.v1.keras.models import load_model
import numpy as np
import midi_preprocessing

midi_matrices = np.load('samples bool.npy')
midi_matrices = midi_matrices[0].reshape(1, 16, 96, 96)
model = load_model(r"C:\Users\Jonny\PycharmProjects\contextual-music-composition\saved models\autoencoder 10 2.h5")

samples = model.predict(midi_matrices)

midi_preprocessing.samples_to_midi(samples, 0)