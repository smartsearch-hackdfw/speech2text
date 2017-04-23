from flask import Blueprint, render_template, request, jsonify
from google.cloud import speech
import subprocess
import json
import base64
from os import path


speech_app = Blueprint('speech2text', __name__, template_folder='./templates',
                       static_folder='./static/speech2text')

sclient = speech.Client();

@speech_app.route('/', methods=['GET'])
def index():
    return render_template("speech2text/index.html")

@speech_app.route('/', methods=['POST'])
def save_audio():

    # Decode base64
    data = request.form['audioBase64']
    data = base64.b64decode(data)

    # Write data to file
    webmPath = path.abspath('recording.webm')
    wavePath = path.abspath('recording.wav')

    file = open(webmPath, 'wb')
    file.write(data)
    file.close

    command = "ffmpeg -i %s -ab 160k -ac 1 -ar 48000 -vn %s -y" % (webmPath, wavePath)
    proc = subprocess.call(command, shell=True)

    ## Read back data
    file = open(wavePath)
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

    return json.dumps(transcripts)
