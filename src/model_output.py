from tensorflow.compat.v1.keras.models import load_model
import numpy as np
import midi_preprocessing
import enums
import sentiment_analysis
from random import randrange, uniform

model = load_model(enums.AUTOENCODER_2000_FILEPATH)

certainty_for_note_to_be_played = 99.9
user_input_text = 'joyful'
instrument_number = 0

# if sentiment_analysis.is_sentiment_negative(user_input_text):
#    midi_matrices = np.load('../samples/minor samples.npy')
#else:
#    midi_matrices = np.load('../samples/major samples.npy')

# midi_matrices = np.load('../samples/ttfaf.npy')
# midi_matrix = midi_matrices[0].reshape(1, 16, 96, 96)

randomInput = [[]]
first_layer_weights = model.layers[0].getWeights()
first_layer_weights_shape = randrange(0, np.array(first_layer_weights[0]).shape[1] - 1)
for i in range(120):
    bottom_limit = np.percentile(first_layer_weights[i][first_layer_weights_shape], 25)
    top_limit = np.percentile(model.layers[0].get_weights()[i][first_layer_weights_shape], 75)
    randomInput[0].append(uniform(bottom_limit, top_limit))

np.save(enums.RANDOM_INPUT_FILEPATH, randomInput)
midi_matrix = np.load(enums.RANDOM_INPUT_FILEPATH)

random_music_seed = 0#randrange(0, midi_matrices.shape[0] - 1)
print('Random music seed: ' + str(random_music_seed))
song_name = 'autoencoder 2000 ' + str(random_music_seed) + ' ' + user_input_text + ' ' + str(instrument_number)

samples = model.predict(midi_matrix)
print(model.summary())
print(model.layers[0].get_weights())
midi_preprocessing.samples_to_midi(samples, instrument_number, song_name, certainty_for_note_to_be_played)

