from flask import Flask, jsonify, request, send_file, send_from_directory
# from flask_cors import CORS
import model_output
import enums
import objects.PCASliderComponent

app = Flask(__name__,
            static_url_path='',
            static_folder='./webapp/')
# CORS(app)


@app.route("/generateRandomMusic", methods=['GET'])
def generate_random_music():
    user_input_text = request.args.get('userInput')
    instrument_number = request.args.get('instrumentNumber')
    display_sheet_music = request.args.get('displaySheetMusic')
    # minor_tonality = request.args.get('minorTonality')
    note_density = request.args.get('noteDensity')
    tempo = request.args.get('tempo')
    slider_values = request.args.get('slider_values')

    slider_components = model_output.generate_song(user_input_text, display_sheet_music, instrument_number, note_density, tempo)

    first_10_slider_components_serialised = []
    for i in range(10):
        first_10_slider_components_serialised.append(objects.PCASliderComponent.serialize(slider_components[i]))

    return jsonify(first_10_slider_components_serialised)
    # send_file(enums.EnvVars.LIVE_SONG_OUTPUT_DIRECTORY_FILEPATH + 'livesong.mid')


@app.route("/", methods=['GET'])
def default():
    return send_from_directory('../src/webapp/html/', 'music_player.html')


if __name__ == "__main__":
    app.run()
