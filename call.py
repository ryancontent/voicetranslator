from twilio.twiml.voice_response import VoiceResponse, Gather
from googletrans import Translator

from utils import read_languages


class Call:
    def __init__(self, request, listen_uri, speak_uri):
        self.request = request
        self.listen_uri = listen_uri
        self.speak_uri = speak_uri
        self.languages = read_languages()
        self.caller_language = self.languages[0]
        self.receiver_language = self.languages[1]

    def listen(self):
        response = VoiceResponse()
        gather = Gather(input='speech', language=self.caller_language,
                        timeout=1, action=self.speak_uri)
        response.append(gather)
        response.say('I did not hear you.')
        response.redirect(self.listen_uri)
        return response

    def speak(self):
        response = VoiceResponse()
        if 'SpeechResult' in self.request.values:
            native_speech = self.request.values['SpeechResult']
            print(native_speech)
            translated_speech = translate_text_to_text(
                text=native_speech, dest_lang=self.receiver_language['google'])
            print(translated_speech)
            response.say(translated_speech,
                         language=self.receiver_language['twilio'])

        response.redirect(self.listen_uri)

        return response


def translate_text_to_text(text, dest_lang):
    translator = Translator()
    return translator.translate(text, dest=dest_lang).text
