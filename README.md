# Translation app using Twilio, Google Translate

## Requirements
* Python - 3.8+ with requirements.txt
* ngrok - https://ngrok.com/download

## Launch
* `python app.py` - launches flask app
* `ngrok http 5000` - launches ngrok
* Find and copy forwarding https address for localhost from ngrok e.g. `https://xxxxxx.ngrok.io -> http://localhost:5000`
* Use address above and enter in Twilio "A Calls Comes In - Webhook" followed by `/answer` e.g. `https://xxxxxx.ngrok.io/answer`

## Use
* When call comes in to Twilio number, local Python logic via Flask server will be used.
