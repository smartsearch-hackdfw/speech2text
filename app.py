from flask import Flask, render_template, request, json
import soundfile as sf
from google.cloud import speech
import subprocess


app = Flask(__name__)
sclient = speech.Client();

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/', methods=['POST'])
def save_audio():

    # Decode base64
    data = request.form['audioBase64']
    data = decode_base64(data)

    # Write data to file
    file = open('recording.webm', 'w+')
    file.write(data)
    file.close

    command = "ffmpeg -i recording.webm -ab 160k -ac 1 -ar 44100 -vn audio.wav -y"
    proc = subprocess.call(command, shell=True)

    ## Read back data
    file = open('audio.wav')
    fdata = file.read()
    file.close()

    sample = sclient.sample(
        content=fdata,
        encoding='LINEAR16')

    alternatives = sample.recognize('en-US')
    for alternative in alternatives:
        print('Transcript: {}'.format(alternative.transcript))

    return ('', 200)

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
    app.run(debug=True)
