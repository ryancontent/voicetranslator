from flask import Flask, request

from call import Call


app = Flask(__name__)

call = Call(request=request, listen_uri='/listen',
            store_speech_uri='/storespeech', speak_uri='/speak')


@app.route("/answer", methods=['GET', 'POST'])
def answer():
    return str(call.answer('caller'))


@app.route("/listen/<caller_type>", methods=['GET', 'POST'])
def listen(caller_type):
    return str(call.listen(caller_type))


@app.route("/storespeech/<caller_type>", methods=['GET', 'POST'])
def store_speech(caller_type):
    return str(call.store_speech(caller_type))


@app.route("/speak/<caller_type>", methods=['GET', 'POST'])
def speak(caller_type):
    return str(call.speak(caller_type))


if __name__ == "__main__":
    app.run(debug=True)
