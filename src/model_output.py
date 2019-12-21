from tensorflow.compat.v1.keras.models import load_model
import numpy as np
import midi_preprocessing

midi_matrices = np.load('samples bool.npy')
model = load_model(r"C:\Users\Jonny\PycharmProjects\contextual-music-composition\saved models\autoencoder 2000.h5")

random_music_seed = 1
song_name = 'autoencoder 2000 new ' + str(random_music_seed)

midi_matrix = midi_matrices[random_music_seed].reshape(1, 16, 96, 96)
samples = model.predict(midi_matrix)

midi_preprocessing.samples_to_midi(samples, 0, song_name)
