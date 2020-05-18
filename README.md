# Requirements
1. Python 3
2. pip
3. [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
4. [Google API Client](https://github.com/googleapis/google-api-python-client)

# How to...

Check the `trigger_map.json`, it's self explanatory how to add triggers, speeches and the language that the voice will speak.

If you want more customized speech, implement your own `SpeechProcessor` and add it to the `processors` package. The custom processor file name __MUST__ be exactly the same as the processor __class name__.

# run
```bash
$ pip install requirements.txt
$ python main.py
```

# Troubleshooting
On MacOs give permission to the terminal to use the microphone.

Check if the microfone index is ok in the main.py line 45