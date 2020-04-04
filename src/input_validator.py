import objects.UserInput


def validate_user_input(text, black_with_white, instrument_number, note_length, note_certainty, playback_speed, slider_values):
    text = validate_text(text)
    black_with_white = validate_black_with_white(black_with_white)
    instrument_number = validate_instrument_number(instrument_number)
    note_certainty = validate_note_certainty(note_certainty)
    playback_speed = validate_playback_speed(playback_speed)
    note_length = validate_note_length(note_length)
    slider_values = validate_slider_values(slider_values)

    return objects.UserInput.define_user_input(text, black_with_white, instrument_number, note_certainty, playback_speed, note_length, slider_values)


def validate_text(text):
    if not text or type(text) is not str:
        text = ''
    return text


def validate_black_with_white(black_with_white):
    if not black_with_white or black_with_white == 'false':
        black_with_white = False
    else:
        black_with_white = True
    return black_with_white


def validate_instrument_number(instrument_number):
    if not instrument_number or int(instrument_number) > 127 or int(instrument_number) < 0:
        instrument_number = 0
    return int(instrument_number)


def validate_note_certainty(note_certainty):
    if not note_certainty or float(note_certainty) < 99 or float(note_certainty) > 100:
        note_certainty = 99.9
    return float(note_certainty)


def validate_playback_speed(playback_speed):
    if not playback_speed or float(playback_speed) > 5 or float(playback_speed) < 0.2:
        playback_speed = 1
    return float(playback_speed)


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
