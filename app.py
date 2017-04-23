from flask import Flask
from . import speech_app

app = Flask(__name__)
app.register_blueprint(speech_app)

if __name__ == '__main__':
    app.run(debug=True)
