class Speech:

    def __init__(self, trigger_key, trigger_speech,
                speech, language,*args, **kwargs):
        self.trigger_key = trigger_key
        self.trigger_speech = trigger_speech
        self.speech = speech
        self.language = language                        


    def processed(self, processor):
        return processor.process(self)