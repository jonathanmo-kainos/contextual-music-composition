from flask import Flask, jsonify, request, send_file, send_from_directory
# from flask_cors import CORS
import model_output
import enums

app = Flask(__name__,
            static_url_path='',
            static_folder='./')
# CORS(app)


@app.route("/getMusic/", methods=['GET'])
def return_song():
    user_input_text = request.args.get('user_input_text')
    instrument_number = request.args.get('instrument_number')
    note_certainty = request.args.get('note_certainty')
    note_speed = request.args.get('note_speed')

    model_output.generate_song(user_input_text, instrument_number, note_certainty, note_speed)
    return send_file(enums.LIVE_SONG_OUTPUT_DIRECTORY_FILEPATH + 'livesong.mid')


@app.route("/", methods=['GET'])
def default():
    return send_from_directory('./html/', 'music_player.html')


if __name__ == "__main__":
    app.run()
