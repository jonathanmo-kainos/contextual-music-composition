from tensorflow.compat.v1.keras.models import load_model
import input_validator
import midi_preprocessing
import enums
import utils
import sentiment_analysis


def generate_song(user_input_text, instrument_number, note_certainty, note_speed):
    decoder = load_model(enums.DECODER_2000_FILEPATH)

    user_input = input_validator.validate_user_input(instrument_number, note_certainty, note_speed)

    if user_input.text is not '':
        sample_type = sentiment_analysis.get_sample_type_based_on_user_input(user_input_text)
    else:
        sample_type = 'all'

    random_input = utils.convert_pca_components_to_random_decoder_input(sample_type)

    if enums.DEBUG_MODE:
        print('Random music seed: ' + str(random_input))
    song_name = 'autoencoder 2000 ' + str(random_input[0]) + ' ' + user_input_text + ' ' + str(instrument_number)

    samples = decoder.predict(random_input.reshape(-1, 120))
    return midi_preprocessing.samples_to_midi(samples, instrument_number, song_name, note_certainty)

