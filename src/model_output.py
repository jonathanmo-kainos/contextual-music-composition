from tensorflow.compat.v1.keras.models import load_model
import input_validator
import midi_preprocessing
import enums
import pca_utils
import sentiment_analysis


def generate_random_song(user_input_text):
    decoder = load_model(enums.EnvVars.DECODER_2000_FILEPATH)

    user_input = input_validator.validate_text(user_input_text)

    if user_input is not '':
        sample_type = 'minor'
        # sample_type = sentiment_analysis.get_sample_type_based_on_user_input(user_input_text)
    else:
        sample_type = 'all'

    random_input, slider_components = pca_utils.convert_pca_components_to_random_decoder_input(sample_type)
    if enums.EnvVars.DEBUG_MODE:
        print('Random music seed: ' + str(random_input))
    song_name = 'autoencoder 2000 ' + str(random_input[0]) + ' ' + user_input + ' 0'

    samples = decoder.predict(random_input.reshape(-1, 120))
    midi_preprocessing.samples_to_midi(samples, 0, song_name, 99.9)
    return slider_components


def generate_user_context_song(user_input_text, display_sheet_music, instrument_number, note_certainty, note_speed, slider_values):
    decoder = load_model(enums.EnvVars.DECODER_2000_FILEPATH)

    user_input = input_validator.validate_user_input(user_input_text, instrument_number, note_certainty, note_speed, slider_values)

    if user_input.text is not '':
        sample_type = 'minor'
        # sample_type = sentiment_analysis.get_sample_type_based_on_user_input(user_input_text)
    else:
        sample_type = 'all'

    specified_input = pca_utils.convert_specified_slider_values_to_decoder_input(sample_type, user_input.slider_values)
    if enums.EnvVars.DEBUG_MODE:
        print('Random music seed: ' + str(specified_input))
    song_name = 'autoencoder 2000 ' + str(specified_input[0]) + ' ' + user_input.text + ' ' + str(user_input.instrument_number)

    samples = decoder.predict(specified_input.reshape(-1, 120))
    midi_preprocessing.samples_to_midi(samples, user_input.instrument_number, song_name, user_input.note_certainty)
    return
