class Speech:

    def __init__(self, speech, language, processor, *args, **kwargs):
        self.speech = speech
        self.language = language                
        self.processor = processor


    def processed(self):
        return self.processor.process(self.speech)