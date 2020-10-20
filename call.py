from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.rest import Client
from googletrans import Translator

from langauge import Language
from util import read_config


def get_other_caller_type(caller_type):
    if caller_type == 'receiver':
        return 'caller'
    else:
        return 'receiver'


def get_other_caller_uri(uri, caller_type):
    return uri + '/{}'.format(get_other_caller_type(caller_type))


def get_caller_uri(uri, caller_type):
    return uri + '/{}'.format(caller_type)


def is_speech_available(queued, caller_type):
    if caller_type == 'receiver' and queued['caller'] != None:
        return True
    elif caller_type == 'caller' and queued['receiver'] != None:
        return True
    else:
        False


class Call:
    def __init__(self, request, listen_uri, store_speech_uri, speak_uri):
        self.request = request
        self.language = Language()
        self.translator = Translator()
        self.LISTEN_URI = listen_uri
        self.STORE_SPEECH_URI = store_speech_uri
        self.SPEAK_URI = speak_uri
        self.CALLER_NUMBER = read_config('caller')['number']
        self.RECEIVER_NUMBER = read_config('receiver')['number']
        self.URL = read_config('url')

        TWILIO_ACCOUNT_SID = read_config('twilio_account_sid')
        TWILIO_AUTH_TOKEN = read_config('twilio_auth_token')
        self.twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        self.queued = {
            'receiver': None,
            'caller': None,
        }

    def answer(self, caller_type):
        response = VoiceResponse()
        call = self.twilio_client.calls.create(
            to=self.RECEIVER_NUMBER, from_=self.CALLER_NUMBER, url=self.URL + get_other_caller_uri(self.LISTEN_URI, caller_type))
        response.redirect(get_caller_uri(self.LISTEN_URI, caller_type))
        return response

    def listen(self, caller_type):
        """listen for speech and store"""
        response = VoiceResponse()
        gather = Gather(input='speech', language=self.language.get_twilio_lang_from_caller_type(caller_type),
                        timeout=1, action=get_caller_uri(self.STORE_SPEECH_URI, caller_type))
        response.append(gather)
        if is_speech_available(self.queued, caller_type):
            response.redirect(get_caller_uri(self.SPEAK_URI, caller_type))
        else:
            response.redirect(get_caller_uri(self.LISTEN_URI, caller_type))
        return response

    def store_speech(self, caller_type):
        """store speech to text then resume listening"""
        response = VoiceResponse()
        if 'SpeechResult' in self.request.values:
            native_speech = self.request.values['SpeechResult']
            self.queued[caller_type] = native_speech
            print('{}: {}'.format(caller_type, native_speech))
        response.redirect(get_caller_uri(self.LISTEN_URI, caller_type))
        return response

    def speak(self, caller_type):
        response = VoiceResponse()
        # translate and play if other caller caller_type has speech queued
        if self.queued[get_other_caller_type(caller_type)] != None:
            to_lang = self.language.get_google_lang_from_caller_type(
                caller_type)
            translated_speech = self.translator.translate(
                self.queued[get_other_caller_type(caller_type)], to_lang).text
            print('{}: {}: {}'.format(caller_type, to_lang, translated_speech))
            response.say(translated_speech,
                         language=self.language.get_twilio_lang_from_caller_type(caller_type))
            # reset once spoken
            self.queued[get_other_caller_type(caller_type)] = None

        response.redirect(get_caller_uri(self.LISTEN_URI, caller_type))
        return response
