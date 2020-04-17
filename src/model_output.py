from tensorflow.compat.v1.keras.models import load_model
import shutil
import midi_preprocessing
import enums
import pca_utils
import sentiment_analysis
import objects.UserInput


def generate_random_song(user_input_text, current_uuid, previous_uuid):
    delete_old_song_directory(previous_uuid)
    decoder = load_model(enums.EnvVars.DECODER_2000_FILEPATH)

    sample_type = get_sample_type(user_input_text)

    default_volume = 63
    default_black_with_white = True
    default_instrument = 0
    default_randomise_on_screen_sliders = True
    default_randomise_off_screen_sliders = True
    if sample_type == enums.EnvVars.MINOR_SAMPLE_TYPE:
        default_note_length = 100
        default_note_certainty = 99.94
        default_playback_speed = 0.7
    else:
        default_note_length = 75
        default_note_certainty = 99.9
        default_playback_speed = 1

    random_input, slider_components = pca_utils.convert_pca_components_to_random_decoder_input(sample_type)
    if enums.EnvVars.DEBUG_MODE:
        print('Random music seed: ' + str(random_input))
    song_name = 'autoencoder 2000 ' + str(random_input[0]) + ' ' + user_input_text + ' 0'

    samples = decoder.predict(random_input.reshape(-1, 120))
    midi_preprocessing.samples_to_midi(current_uuid, samples, song_name, default_instrument, default_note_length,
                                       default_black_with_white, default_note_certainty, default_playback_speed,
                                       default_volume)
    initial_input = objects.UserInput.define_user_input(user_input_text, default_black_with_white,
                                                        default_instrument, default_note_certainty,
                                                        default_playback_speed, default_volume, default_note_length,
                                                        default_randomise_on_screen_sliders,
                                                        default_randomise_off_screen_sliders, slider_components)
    return initial_input


def generate_user_context_song(user_input, current_uuid, previous_uuid):
    delete_old_song_directory(previous_uuid)
    decoder = load_model(enums.EnvVars.DECODER_2000_FILEPATH)

    specified_input, slider_components = pca_utils.get_decoder_input_from_slider_configs(
        get_sample_type(user_input.text),
        user_input.randomise_on_screen_sliders,
        user_input.randomise_off_screen_sliders,
        user_input.pca_slider_components)
    if enums.EnvVars.DEBUG_MODE:
        print('Random music seed: ' + str(specified_input))
    song_name = 'autoencoder 2000 ' + str(specified_input[0]) + ' ' + user_input.text + ' ' + str(
        user_input.instrument_number)

    samples = decoder.predict(specified_input.reshape(-1, 120))
    midi_preprocessing.samples_to_midi(current_uuid, samples, song_name, user_input.instrument_number, user_input.note_length,
                                       user_input.black_with_white, user_input.note_certainty,
                                       user_input.playback_speed, user_input.volume)
    return slider_components


def get_sample_type(user_input_text):
    if user_input_text != '':
        return sentiment_analysis.get_sample_type_based_on_user_input(user_input_text)
    else:
        return 'all'


def delete_old_song_directory(previous_uuid):
    shutil.rmtree(enums.EnvVars.LIVE_SONG_OUTPUT_DIRECTORY_FILEPATH + previous_uuid)
