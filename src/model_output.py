from tensorflow.compat.v1.keras.models import load_model
import midi_preprocessing
import enums
import utils
import sentiment_analysis

decoder = load_model(enums.DECODER_2000_FILEPATH)

certainty_for_note_to_be_played = 99.9
user_input_text = 'joyful'
instrument_number = 0

# sample_type = sentiment_analysis.get_sample_type_based_on_user_input(user_input_text)
sample_type = 'major'

random_input = utils.convert_pca_components_to_random_decoder_input(sample_type)

print('Random music seed: ' + str(random_input))
song_name = 'autoencoder 2000 ' + str(random_input[0]) + ' ' + user_input_text + ' ' + str(instrument_number)

samples = decoder.predict(random_input.reshape(-1, 120))
midi_preprocessing.samples_to_midi(samples, instrument_number, song_name, certainty_for_note_to_be_played)

