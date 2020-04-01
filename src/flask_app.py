from flask import Flask, jsonify, request, send_file, send_from_directory
import json
import model_output
import enums
import objects.PCASliderComponent

app = Flask(__name__,
            static_url_path='',
            static_folder='./webapp/')


@app.route("/generateRandomMusic", methods=['GET'])
def generate_random_music():
    user_input_text = request.args.get('userInput')

    slider_components = model_output.generate_random_song(user_input_text)

    first_10_slider_components_serialised = []
    for i in range(10):
        first_10_slider_components_serialised.append(objects.PCASliderComponent.serialize(slider_components[i]))

    return jsonify(first_10_slider_components_serialised)


@app.route("/generateSpecifiedMusic", methods=['GET'])
def generate_specified_music():
    user_input_text = request.args.get('userInput')
    display_sheet_music = request.args.get('displaySheetMusic')
    instrument_number = request.args.get('instrumentNumber')
    note_length = request.args.get('noteLength')
    note_certainty = request.args.get('noteCertainty')
    tempo = request.args.get('tempo')
    slider_values = json.loads(request.args.get('sliderValues'))

    model_output.generate_user_context_song(user_input_text, display_sheet_music, instrument_number, note_length, note_certainty, tempo, slider_values)

    return send_file(enums.EnvVars.LIVE_SONG_OUTPUT_DIRECTORY_FILEPATH + 'livesong.mid')


@app.route("/", methods=['GET'])
def default():
    return send_from_directory('../src/webapp/html/', 'music_player.html')


if __name__ == "__main__":
    app.run()
