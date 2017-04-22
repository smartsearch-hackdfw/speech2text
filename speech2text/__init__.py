from flask import Blueprint, render_template, request, jsonify
import soundfile as sf
from google.cloud import speech
import subprocess
import json


speech_app = Blueprint('speech2text', __name__,
                template_folder='templates')

sclient = speech.Client();

@speech_app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@speech_app.route('/', methods=['POST'])
def save_audio():

    # Decode base64
    data = request.form['audioBase64']
    data = decode_base64(data)

    # Write data to file
    file = open('recording.webm', 'w+')
    file.write(data)
    file.close

    command = "ffmpeg -i recording.webm -ab 160k -ac 1 -ar 48000 -vn audio.wav -y"
    proc = subprocess.call(command, shell=True)

    ## Read back data
    file = open('audio.wav')
    fdata = file.read()
    file.close()

    sample = sclient.sample(
        content=fdata,
        encoding='LINEAR16')

    responses = sample.recognize('en-US')
    transcripts = []
    for response in responses:
        res = {
            'text': response.transcript,
            'confidence': response.confidence
        }
        transcripts.append(res);


    print transcripts
    return json.dumps(transcripts)

def decode_base64(data):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += b'='* (4 - missing_padding)
    return data.decode('base64')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
