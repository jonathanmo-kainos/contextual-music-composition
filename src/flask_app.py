from flask import Flask, jsonify, request, send_from_directory
import json
import model_output
import objects.PCASliderComponent
import input_validator

app = Flask(__name__,
            static_url_path='',
            static_folder='./webapp/')


@app.route("/generateRandomMusic", methods=['POST'])
def generate_random_music():
    user_input_text = request.values.get('userInput')
    current_uuid = request.values.get('currentUUID')
    previous_uuid = request.values.get('previousUUID')

    user_input = input_validator.validate_text(user_input_text)

    initial_input = model_output.generate_random_song(user_input, current_uuid, previous_uuid)
    initial_input.pca_slider_components = objects.PCASliderComponent.serialize(initial_input.pca_slider_components)
    initial_input = json.dumps(initial_input.__dict__)

    return initial_input


@app.route("/generateSpecifiedMusic", methods=['POST'])
def generate_specified_music():
    user_input_text = request.values.get('userInput')
    current_uuid = request.values.get('currentUUID')
    previous_uuid = request.values.get('previousUUID')
    black_with_white = request.values.get('blackWithWhite')
    instrument_number = request.values.get('instrumentNumber')
    note_length = request.values.get('noteLength')
    note_certainty = request.values.get('noteCertainty')
    playback_speed = request.values.get('playbackSpeed')
    volume = request.values.get('volume')
    randomise_on_screen_sliders = request.values.get('randomiseOnScreenSliders')
    randomise_off_screen_sliders = request.values.get('randomiseOffScreenSliders')
    pca_slider_components = json.loads(request.values.get('pcaSliderComponents'))

    deserialized_pca_slider_components = objects.PCASliderComponent.deserialize(pca_slider_components)

    user_input = input_validator.validate_user_input(
        user_input_text,
        black_with_white,
        instrument_number,
        note_length,
        note_certainty,
        playback_speed,
        volume,
        randomise_on_screen_sliders,
        randomise_off_screen_sliders,
        deserialized_pca_slider_components)

    slider_components = model_output.generate_user_context_song(user_input, current_uuid, previous_uuid)
    slider_components_serialised = objects.PCASliderComponent.serialize(slider_components)

    return jsonify(slider_components_serialised)


@app.route("/downloadMidi", methods=['GET'])
def download_midi():
    current_uuid = request.values.get('currentUUID')
    return send_from_directory('../outputs/live/' + current_uuid + '/', 'livesong.mid')


@app.route("/", methods=['GET'])
def default():
    return send_from_directory('../src/webapp/html/', 'music_player.html')


if __name__ == "__main__":
    app.run()
