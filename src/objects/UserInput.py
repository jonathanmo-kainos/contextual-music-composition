class UserInput(object):
    text = ''
    instrument_number = 0
    note_certainty = 99.9
    note_speed = 1
    note_length = 50
    slider_values = []

    def __init__(self, text, instrument_number, note_certainty, note_speed, note_length, slider_values):
        self.text = text
        self.instrument_number = instrument_number
        self.note_certainty = note_certainty
        self.note_speed = note_speed
        self.note_length = note_length
        self.slider_values = slider_values


def define_user_input(text, instrument_number, note_certainty, note_speed, note_length, slider_values):
    return UserInput(text, instrument_number, note_certainty, note_speed, note_length, slider_values)
