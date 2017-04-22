from flask import Flask
from speech2text import speech_app

app = Flask(__name__)
app.register_blueprint(speech_app)
app.run(debug=True)
