import unittest
from input_validator import InputValidator


class InputValidatorTest(unittest.TestCase):

    def test_black_with_white_empty_string_validation(self):
        input_validator = InputValidator()
        black_with_white = ''
        result = input_validator.validate_black_with_white(black_with_white)
        self.assertFalse(result)

    def test_black_with_white_true_string_validation(self):
        input_validator = InputValidator()
        black_with_white = 'true'
        result = input_validator.validate_black_with_white(black_with_white)
        self.assertTrue(result)

    def test_black_with_white_True_string_validation(self):
        input_validator = InputValidator()
        black_with_white = 'True'
        result = input_validator.validate_black_with_white(black_with_white)
        self.assertTrue(result)

    def test_black_with_white_notvalid_string_validation(self):
        input_validator = InputValidator()
        black_with_white = 'notValid'
        result = input_validator.validate_black_with_white(black_with_white)
        self.assertTrue(result)

    def test_black_with_white_number_validation(self):
        input_validator = InputValidator()
        black_with_white = 123
        result = input_validator.validate_black_with_white(black_with_white)
        self.assertTrue(result)

    def test_instrument_number_empty_string_validation(self):
        input_validator = InputValidator()
        instrument_number = ''
        result = input_validator.validate_instrument_number(instrument_number)
        self.assertFalse(result)

    def test_instrument_number_negative_int_validation(self):
        input_validator = InputValidator()
        instrument_number = -1
        result = input_validator.validate_instrument_number(instrument_number)
        self.assertFalse(result)

    def test_instrument_number_large_int_validation(self):
        input_validator = InputValidator()
        instrument_number = 3000
        result = input_validator.validate_instrument_number(instrument_number)
        self.assertFalse(result)

    def test_instrument_number_notvalid_string_validation(self):
        input_validator = InputValidator()
        instrument_number = 'notValid'
        with self.assertRaises(ValueError) as cm:
            input_validator.validate_instrument_number(instrument_number)

    def test_instrument_number_valid_int_validation(self):
        instrument_number = 123
        result = input_validator.validate_instrument_number(instrument_number)
        self.assertTrue(result)

    def test_note_certainty_empty_string_validation(self):
        note_certainty = ''
        result = input_validator.validate_note_certainty(note_certainty)
        self.assertEqual(result, 99.9)

    def test_note_certainty_negative_int_validation(self):
        note_certainty = -1
        result = input_validator.validate_note_certainty(note_certainty)
        self.assertEqual(result, 99.9)

    def test_note_certainty_large_int_validation(self):
        note_certainty = 3000
        result = input_validator.validate_note_certainty(note_certainty)
        self.assertEqual(result, 99.9)

    def test_note_certainty_notvalid_string_validation(self):
        note_certainty = 'notValid'
        with self.assertRaises(ValueError) as cm:
            input_validator.validate_note_certainty(note_certainty)

    def test_note_certainty_valid_float_validation(self):
        note_certainty = 99.636487568782635
        result = input_validator.validate_note_certainty(note_certainty)
        self.assertEqual(result, note_certainty)

    def test_playback_speed_empty_string_validation(self):
        playback_speed = ''
        result = input_validator.validate_playback_speed(playback_speed)
        self.assertEqual(result, 1)

    def test_playback_speed_negative_int_validation(self):
        playback_speed = -1
        result = input_validator.validate_playback_speed(playback_speed)
        self.assertEqual(result, 1)

    def test_playback_speed_large_int_validation(self):
        playback_speed = 3000
        result = input_validator.validate_playback_speed(playback_speed)
        self.assertEqual(result, 1)

    def test_playback_speed_notvalid_string_validation(self):
        playback_speed = 'notValid'
        with self.assertRaises(ValueError) as cm:
            input_validator.validate_playback_speed(playback_speed)

    def test_playback_speed_valid_float_validation(self):
        playback_speed = 3.5324
        result = input_validator.validate_playback_speed(playback_speed)
        self.assertEqual(result, playback_speed)

    def test_volume_empty_string_validation(self):
        volume = ''
        result = input_validator.validate_volume(volume)
        self.assertEqual(result, 63)

    def test_volume_negative_int_validation(self):
        volume = -1
        result = input_validator.validate_volume(volume)
        self.assertEqual(result, 63)

    def test_volume_large_int_validation(self):
        volume = 3000
        result = input_validator.validate_volume(volume)
        self.assertEqual(result, 63)

    def test_volume_notvalid_string_validation(self):
        volume = 'notValid'
        with self.assertRaises(ValueError) as cm:
            input_validator.validate_volume(volume)

    def test_volume_valid_int_validation(self):
        volume = 102
        result = input_validator.validate_volume(volume)
        self.assertEqual(result, volume)

    def test_note_length_empty_string_validation(self):
        note_length = ''
        result = input_validator.validate_note_length(note_length)
        self.assertEqual(result, 75)

    def test_note_length_negative_int_validation(self):
        note_length = -1
        result = input_validator.validate_note_length(note_length)
        self.assertEqual(result, 75)

    def test_note_length_large_int_validation(self):
        note_length = 3000
        result = input_validator.validate_note_length(note_length)
        self.assertEqual(result, 75)

    def test_note_length_notvalid_string_validation(self):
        note_length = 'notValid'
        with self.assertRaises(ValueError) as cm:
            input_validator.validate_note_length(note_length)

    def test_note_length_valid_int_validation(self):
        note_length = 140
        result = input_validator.validate_note_length(note_length)
        self.assertEqual(result, note_length)

    def test_randomise_on_screen_sliders_empty_string_validation(self):
        randomise_on_screen_sliders = ''
        result = input_validator.validate_randomise_on_screen_sliders(randomise_on_screen_sliders)
        self.assertFalse(result)

    def test_randomise_on_screen_sliders_true_string_validation(self):
        randomise_on_screen_sliders = 'true'
        result = input_validator.validate_randomise_on_screen_sliders(randomise_on_screen_sliders)
        self.assertTrue(result)

    def test_randomise_on_screen_sliders_True_string_validation(self):
        randomise_on_screen_sliders = 'True'
        result = input_validator.validate_randomise_on_screen_sliders(randomise_on_screen_sliders)
        self.assertTrue(result)

    def test_randomise_on_screen_sliders_notvalid_string_validation(self):
        randomise_on_screen_sliders = 'notValid'
        result = input_validator.validate_randomise_on_screen_sliders(randomise_on_screen_sliders)
        self.assertTrue(result)

    def test_randomise_on_screen_sliders_int_validation(self):
        randomise_on_screen_sliders = 123
        result = input_validator.validate_randomise_on_screen_sliders(randomise_on_screen_sliders)
        self.assertTrue(result)

    def test_randomise_off_screen_sliders_empty_string_validation(self):
        randomise_off_screen_sliders = ''
        result = input_validator.validate_randomise_off_screen_sliders(randomise_off_screen_sliders)
        self.assertFalse(result)

    def test_randomise_off_screen_sliders_true_string_validation(self):
        randomise_off_screen_sliders = 'true'
        result = input_validator.validate_randomise_off_screen_sliders(randomise_off_screen_sliders)
        self.assertTrue(result)

    def test_randomise_off_screen_sliders_True_string_validation(self):
        randomise_off_screen_sliders = 'True'
        result = input_validator.validate_randomise_off_screen_sliders(randomise_off_screen_sliders)
        self.assertTrue(result)

    def test_randomise_off_screen_sliders_notvalid_string_validation(self):
        randomise_off_screen_sliders = 'notValid'
        result = input_validator.validate_randomise_off_screen_sliders(randomise_off_screen_sliders)
        self.assertTrue(result)

    def test_randomise_off_screen_sliders_int_validation(self):
        randomise_off_screen_sliders = 123
        result = input_validator.validate_randomise_off_screen_sliders(randomise_off_screen_sliders)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
