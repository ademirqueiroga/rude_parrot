from processors.SpeechProcessor import SpeechProcessor

class DefaultSpeechProcessor(SpeechProcessor):

    def process(self, speech):
        return speech.speech
    