from flask import Flask, request

from call import Call


app = Flask(__name__)

call = Call(request=request, listen_uri='/listen', speak_uri='/speak')


@app.route("/listen", methods=['GET', 'POST'])
def listen():
    return str(call.listen())


@app.route("/speak", methods=['POST'])
def speak():
    return str(call.speak())


if __name__ == "__main__":
    app.run(debug=True)
