from util import read_config


class Language:
    def __init__(self):
        RECEIVER = read_config('receiver')['langauge']
        CALLER = read_config('caller')['langauge']
        LANGUAGES = read_config('languages')
        self.RECEIVER_TWILIO = LANGUAGES[RECEIVER]['twilio']
        self.CALLER_TWILIO = LANGUAGES[CALLER]['twilio']
        self.RECEIVER_GOOGLE = LANGUAGES[RECEIVER]['google']
        self.CALLER_GOOGLE = LANGUAGES[CALLER]['google']

    def get_twilio_lang_from_caller_type(self, caller_type):
        if caller_type == 'receiver':
            return self.RECEIVER_TWILIO
        else:
            return self.CALLER_TWILIO

    def get_google_lang_from_caller_type(self, caller_type):
        if caller_type == 'receiver':
            return self.RECEIVER_GOOGLE
        else:
            return self.CALLER_GOOGLE
