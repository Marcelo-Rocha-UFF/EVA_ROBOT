#!/usr/bin/env python3

import speech_recognition as sr


# obtain audio from the microphone
r = sr.Recognizer()


# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print(f'{index}, {name}')


# # Matrix Voice is 3 or 4
mic = sr.Microphone(1)
r.energy_threshold = 300


with mic as source:
    #r.adjust_for_ambient_noise(source)  # listen for 1 second to calibrate the energy threshold for ambient noise levels
    print("EVA is listening!")
    audio = r.listen(source)

    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        response = r.recognize_google(audio, language="pt-BR")
        print("Google Speech Recognition thinks you said " + response)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
            



# harvard = sr.AudioFile('eva-stt-module/audio_files_harvard.wav')
# with harvard as source:
#     audio = r.record(source)
# print(type(audio))
# r.recognize_google(audio)

# st = "{'alternative': [{'confidence': 0.82141513, 'transcript': 'Fala Que Eu Te Escuto'}], 'final': True}"

# json_object = json.loads(st)

# import speech_recognition as sr
# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

