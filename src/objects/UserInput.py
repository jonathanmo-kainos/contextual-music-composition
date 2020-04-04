class UserInput(object):
    text = ''
    black_with_white = False
    instrument_number = 0
    note_certainty = 99.9
    playback_speed = 1
    note_length = 50
    slider_values = []

    def __init__(self, text, black_with_white, instrument_number, note_certainty, playback_speed, note_length, slider_values):
        self.text = text
        self.black_with_white = black_with_white
        self.instrument_number = instrument_number
        self.note_certainty = note_certainty
        self.playback_speed = playback_speed
        self.note_length = note_length
        self.slider_values = slider_values


def define_user_input(text, black_with_white, instrument_number, note_certainty, playback_speed, note_length, slider_values):
    return UserInput(text, black_with_white, instrument_number, note_certainty, playback_speed, note_length, slider_values)
