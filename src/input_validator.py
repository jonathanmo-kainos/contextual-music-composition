import objects.UserInput


def validate_user_input(text, instrument_number, note_length, note_certainty, note_speed, slider_values):
    text = validate_text(text)
    instrument_number = validate_instrument_number(instrument_number)
    note_certainty = validate_note_certainty(note_certainty)
    note_speed = validate_note_speed(note_speed)
    note_length = validate_note_length(note_length)
    slider_values = validate_slider_values(slider_values)

    return objects.UserInput.define_user_input(text, instrument_number, note_certainty, note_speed, note_length, slider_values)


def validate_text(text):
    if not text or type(text) is not str:
        text = ''
    return text


def validate_instrument_number(instrument_number):
    if not instrument_number or int(instrument_number) > 127 or int(instrument_number) < 0:
        instrument_number = 0
    return int(instrument_number)


def validate_note_certainty(note_certainty):
    if not note_certainty or float(note_certainty) < 99 or float(note_certainty) > 100:
        note_certainty = 99.9
    return float(note_certainty)


def validate_note_speed(note_speed):
    if not note_speed or float(note_speed) > 5 or float(note_speed) < 0.2:
        note_speed = 1
    return float(note_speed)


def validate_note_length(note_length):
    if not note_length or int(note_length) > 500 or int(note_length) < 5:
        note_length = 50
    return int(note_length)


def validate_slider_values(slider_values):
    validated_slider_values = []

    if not slider_values or len(slider_values) != 10:
        return []
    for slider_value in slider_values:
        if float(slider_value) < -1000 or float(slider_value) > 1000:
            return []
        else:
            validated_slider_values.append(float(slider_value))
    return validated_slider_values
