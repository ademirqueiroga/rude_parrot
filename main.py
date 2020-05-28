import speech_recognition as sr
import random
import json
import importlib
import os
from processors.SpeechProcessor import SpeechProcessor
from Speech import Speech
from gtts import gTTS
from playsound import playsound
from pathlib import Path


TRIGGERS_KEY = 'triggers'
TRIGGER_KEY = 'trigger'
SPEECHES_KEY = 'speeches'
SPEECH_KEY = 'speech'
LANG_KEY = 'language'
PROCESSOR_KEY = 'processor'


def load_trigger_map():
        trigger_map = {}
        with open('trigger_map.json', 'r') as file:
            trigger_json = json.load(file)
            for entry in trigger_json:
                try:
                    triggers = entry.get(TRIGGERS_KEY)
                    speeches = entry.get(SPEECHES_KEY)
                    processor = entry.get(PROCESSOR_KEY)
                    for trigger in triggers:                
                        trigger_map.setdefault(trigger, {})[PROCESSOR_KEY] = processor
                        for speech in speeches:
                            trigger_map[trigger].setdefault(SPEECHES_KEY, list()).append(speech)                            
                        
                except Exception as e:
                    print(e)                
        # print('Trigger map:', json.dumps(trigger_map, indent=2))
        return trigger_map

def main(): 
    recog = sr.Recognizer()        
    trigger_map = load_trigger_map()
    triggers = sorted(trigger_map.keys(), key=lambda key: -len(key))                

    with sr.Microphone(device_index=0) as source:        
        print("Adjusting energy_threshold")
        recog.adjust_for_ambient_noise(source)
        print(recog.energy_threshold)        

        print("Listening...")        
        # obtain audio from the microphone
        audio = recog.listen(source)
        print("Thinking...")

        try:
            recognized_speech = recog.recognize_google(audio)
            print("I think I heard " + recognized_speech)

            speech = None
            for trigger in triggers:
                if trigger in recognized_speech.lower():
                    entry = trigger_map[trigger]
                    print('Entry', entry)                                        
                    processor = entry.get(PROCESSOR_KEY)                    

                    processor_module = importlib.import_module(f'processors.{processor}')
                    processor_class = getattr(processor_module, processor)

                    if not issubclass(processor_class, SpeechProcessor):
                        continue

                    trigger_speech = random.choice(entry.get(SPEECHES_KEY))
                    speech = Speech(
                        trigger_key=trigger,
                        trigger_speech=recognized_speech,
                        speech=trigger_speech.get(SPEECH_KEY),
                        language=trigger_speech.get(LANG_KEY),                        
                    )        

            if speech:
                # text to speech            
                tts = speech.processed(processor_class())                
                filename = f'media/{hash((speech.trigger_key, speech.speech, processor_class))}.mp3'
                if not Path(filename).is_file():
                    gTTS(tts, lang=speech.language).save(filename)

                playsound(filename)

        except sr.UnknownValueError:
            print("I could not understand the audio")
        except sr.RequestError as e:
            print("Error; {0}".format(e))
        # except Exception as e:
        #     print(e)
    

if __name__ == "__main__":

    if not Path('media').is_dir():
        os.mkdir('media')

    while True:
        main()