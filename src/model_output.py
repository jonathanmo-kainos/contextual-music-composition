from tensorflow.compat.v1.keras.models import load_model
import numpy as np
import midi_preprocessing
import sentiment_analysis
from random import randrange

model = load_model(r"C:\Users\Jonny\PycharmProjects\contextual-music-composition\saved models\autoencoder 2000.h5")

certainty_for_note_to_be_played = 99.9
user_input_text = 'dark moody scary ominous'

if sentiment_analysis.is_sentiment_negative(user_input_text):
    midi_matrices = np.load('../samples/minor samples.npy')
else:
    midi_matrices = np.load('../samples/major samples.npy')

random_music_seed = randrange(0, midi_matrices.shape[0] - 1)
print('Random music seed: ' + str(random_music_seed))
song_name = 'autoencoder 2000 new ' + str(random_music_seed)

midi_matrix = midi_matrices[random_music_seed].reshape(1, 16, 96, 96)
samples = model.predict(midi_matrix)

midi_preprocessing.samples_to_midi(samples, 0, song_name, certainty_for_note_to_be_played)
