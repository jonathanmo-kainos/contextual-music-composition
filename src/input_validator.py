import objects.UserInput


def validate_user_input(text, instrument_number, note_certainty, note_speed):
    text = validate_text(text)
    instrument_number = validate_instrument_number(instrument_number)
    note_certainty = validate_note_certainty(note_certainty)
    note_speed = validate_note_speed(note_speed)

    return objects.UserInput.define_user_input(text, instrument_number, note_certainty, note_speed)


def validate_text(text):
    if not text or type(text) is not str:
        text = ''
    return text


def validate_instrument_number(instrument_number):
    if not instrument_number or type(instrument_number) is not int or int(instrument_number) > 127 or int(instrument_number) < 0:
        instrument_number = 0
    return int(instrument_number)


def validate_note_certainty(note_certainty):
    if not note_certainty or type(note_certainty) is not int or int(note_certainty) < 98 or int(note_certainty) > 100:
        note_certainty = 99.9
    return int(note_certainty)


def validate_note_speed(note_speed):
    if not note_speed or type(note_speed) is not int or int(note_speed) > 5 or int(note_speed) < 0.2:
        note_speed = 1
    return int(note_speed)
