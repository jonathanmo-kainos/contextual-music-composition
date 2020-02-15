from tensorflow.compat.v1.keras.models import load_model
import numpy as np
import midi_preprocessing
import sentiment_analysis
from random import randrange, uniform
from tensorflow.keras.models import Sequential

model = load_model(r"C:\Users\Jonny\PycharmProjects\contextual-music-composition\saved models\autoencoder 2000.h5")

certainty_for_note_to_be_played = 99.9
user_input_text = 'joyful'
instrument_number = 0

# if sentiment_analysis.is_sentiment_negative(user_input_text):
#    midi_matrices = np.load('../samples/minor samples.npy')
#else:
#    midi_matrices = np.load('../samples/major samples.npy')

# midi_matrix = midi_matrices[random_music_seed].reshape(1, 16, 96, 96)

randomInput = [[]]
for i in range(120):
    randomInput[0].append(uniform(0, 1))

np.save('../samples/randomInput.npy', randomInput)
midi_matrix = np.load('../samples/randomInput.npy')

random_music_seed = 0#randrange(0, midi_matrices.shape[0] - 1)
print('Random music seed: ' + str(random_music_seed))
song_name = 'autoencoder 2000 ' + str(random_music_seed) + ' ' + user_input_text + ' ' + str(instrument_number)

model2 = Sequential()
for layer in model.layers[7:]:
    model2.add(layer)
samples = model2.predict(midi_matrix.reshape(1, 120))

midi_preprocessing.samples_to_midi(samples, instrument_number, song_name, certainty_for_note_to_be_played)

