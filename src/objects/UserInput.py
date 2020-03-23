class UserInput(object):
    text = ''
    instrument_number = 0
    note_certainty = 99.9
    note_speed = 1

    def __init__(self, text, instrument_number, note_certainty, note_speed):
        self.text = text
        self.instrument_number = instrument_number
        self.note_certainty = note_certainty
        self.note_speed = note_speed


def define_user_input(text, instrument_number, note_certainty, note_speed):
    user_input = UserInput(text, instrument_number, note_certainty, note_speed)
    return user_input
