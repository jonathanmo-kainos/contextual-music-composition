from tensorflow.compat.v1.keras.models import load_model
import midi_preprocessing
import enums
import pca_utils
import sentiment_analysis

default_instrument = 0
default_note_length = 50
default_note_certainty = 99.9
default_black_with_white = False
default_playback_speed = 1


def generate_random_song(user_input_text):
    decoder = load_model(enums.EnvVars.DECODER_2000_FILEPATH)

    random_input, slider_components = pca_utils.convert_pca_components_to_random_decoder_input(get_sample_type(user_input_text))
    if enums.EnvVars.DEBUG_MODE:
        print('Random music seed: ' + str(random_input))
    song_name = 'autoencoder 2000 ' + str(random_input[0]) + ' ' + user_input_text + ' 0'

    samples = decoder.predict(random_input.reshape(-1, 120))
    midi_preprocessing.samples_to_midi(samples, song_name, default_instrument, default_note_length, default_black_with_white, default_note_certainty, default_playback_speed)
    return slider_components


def generate_user_context_song(user_input):
    decoder = load_model(enums.EnvVars.DECODER_2000_FILEPATH)

    specified_input = pca_utils.convert_specified_slider_values_to_decoder_input(get_sample_type(user_input.text), user_input.slider_values)
    if enums.EnvVars.DEBUG_MODE:
        print('Random music seed: ' + str(specified_input))
    song_name = 'autoencoder 2000 ' + str(specified_input[0]) + ' ' + user_input.text + ' ' + str(user_input.instrument_number)

    samples = decoder.predict(specified_input.reshape(-1, 120))
    midi_preprocessing.samples_to_midi(samples, song_name, user_input.instrument_number, user_input.note_length, user_input.black_with_white, user_input.note_certainty, user_input.playback_speed)
    return


def get_sample_type(user_input):
    if user_input != '':
        return 'minor'
        # sample_type = sentiment_analysis.get_sample_type_based_on_user_input(user_input_text)
    else:
        return 'all'
