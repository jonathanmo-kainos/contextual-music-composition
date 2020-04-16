class UserInput(object):
    text = ''
    black_with_white = True
    instrument_number = 0
    note_certainty = 99.9
    playback_speed = 1
    volume = 1
    note_length = 50
    randomise_on_screen_sliders = True
    randomise_off_screen_sliders = True
    pca_slider_components = []

    def __init__(self, text, black_with_white, instrument_number, note_certainty, playback_speed, volume, note_length,
                 randomise_on_screen_sliders, randomise_off_screen_sliders, pca_slider_components):
        self.text = text
        self.black_with_white = black_with_white
        self.instrument_number = instrument_number
        self.note_certainty = note_certainty
        self.playback_speed = playback_speed
        self.volume = volume
        self.note_length = note_length
        self.randomise_on_screen_sliders = randomise_on_screen_sliders
        self.randomise_off_screen_sliders = randomise_off_screen_sliders
        self.pca_slider_components = pca_slider_components


def define_user_input(text, black_with_white, instrument_number, note_certainty, playback_speed, volume, note_length,
                      randomise_on_screen_sliders, randomise_off_screen_sliders, pca_slider_components):
    return UserInput(text, black_with_white, instrument_number, note_certainty, playback_speed, volume, note_length,
                     randomise_on_screen_sliders, randomise_off_screen_sliders, pca_slider_components)
