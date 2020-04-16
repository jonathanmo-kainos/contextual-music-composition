import objects.UserInput


class InputValidator:

    @staticmethod
    def validate_user_input(user_input_text, black_with_white, instrument_number, note_length, note_certainty,
                            playback_speed, volume, randomise_on_screen_sliders, randomise_off_screen_sliders,
                            pca_slider_components):
        text = InputValidator.validate_text(user_input_text)
        black_with_white = InputValidator.validate_black_with_white(black_with_white)
        instrument_number = InputValidator.validate_instrument_number(instrument_number)
        note_certainty = InputValidator.validate_note_certainty(note_certainty)
        playback_speed = InputValidator.validate_playback_speed(playback_speed)
        volume = InputValidator.validate_volume(volume)
        note_length = InputValidator.validate_note_length(note_length)
        randomise_on_screen_sliders = InputValidator.validate_randomise_on_screen_sliders(randomise_on_screen_sliders)
        randomise_off_screen_sliders = InputValidator.validate_randomise_off_screen_sliders(
            randomise_off_screen_sliders)
        pca_slider_components = InputValidator.validate_pca_slider_components(pca_slider_components)

        return objects.UserInput.define_user_input(text, black_with_white, instrument_number, note_certainty,
                                                   playback_speed, volume, note_length, randomise_on_screen_sliders,
                                                   randomise_off_screen_sliders, pca_slider_components)

    @staticmethod
    def validate_text(text):
        if not text or type(text) is not str:
            text = ''
        return text

    @staticmethod
    def validate_black_with_white(black_with_white):
        if not black_with_white or black_with_white == 'false':
            black_with_white = False
        else:
            black_with_white = True
        return black_with_white

    @staticmethod
    def validate_instrument_number(instrument_number):
        if not instrument_number or int(instrument_number) > 127 or int(instrument_number) < 0:
            instrument_number = 0
        return int(instrument_number)

    @staticmethod
    def validate_note_certainty(note_certainty):
        if not note_certainty or float(note_certainty) < 99 or float(note_certainty) > 100:
            note_certainty = 99.9
        return float(note_certainty)

    @staticmethod
    def validate_playback_speed(playback_speed):
        if not playback_speed or float(playback_speed) > 5 or float(playback_speed) < 0.2:
            playback_speed = 1
        return float(playback_speed)

    @staticmethod
    def validate_volume(volume):
        if not volume or int(volume) < 1 or int(volume) > 127:
            volume = 63
        return int(volume)

    @staticmethod
    def validate_note_length(note_length):
        if not note_length or int(note_length) > 150 or int(note_length) < 1:
            note_length = 75
        return int(note_length)

    @staticmethod
    def validate_randomise_on_screen_sliders(randomise_on_screen_sliders):
        if not randomise_on_screen_sliders or randomise_on_screen_sliders == 'false':
            randomise_on_screen_sliders = False
        else:
            randomise_on_screen_sliders = True
        return randomise_on_screen_sliders

    @staticmethod
    def validate_randomise_off_screen_sliders(randomise_off_screen_sliders):
        if not randomise_off_screen_sliders or randomise_off_screen_sliders == 'false':
            randomise_off_screen_sliders = False
        else:
            randomise_off_screen_sliders = True
        return randomise_off_screen_sliders

    @staticmethod
    def validate_pca_slider_components(pca_slider_components):
        validated_pca_slider_components = []

        if not pca_slider_components:
            return []
        for slider_component in pca_slider_components:
            if float(slider_component.number) < -1000 or float(slider_component.number) > 1000:
                return []
            else:
                validated_pca_slider_components.append(slider_component)
        return validated_pca_slider_components
