from flask import Flask, jsonify, request, send_file, send_from_directory
# from flask_cors import CORS
import model_output
import enums

app = Flask(__name__,
            static_url_path='',
            static_folder='./')
# CORS(app)


@app.route("/generateRandomMusic", methods=['GET'])
def return_song():
    user_input_text = request.args.get('user_input_text')

    model_output.generate_song(user_input_text, 0, 99.9, 1)
    return send_file(enums.EnvVars.LIVE_SONG_OUTPUT_DIRECTORY_FILEPATH + 'livesong.mid')


@app.route("/", methods=['GET'])
def default():
    return send_from_directory('../src/webapp/html/', 'music_player.html')


if __name__ == "__main__":
    app.run()
