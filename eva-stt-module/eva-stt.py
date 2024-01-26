#!/usr/bin/env python3

from paho.mqtt import client as mqtt_client
import time

import speech_recognition as sr


import sys
sys.path.append('/home/pi/EVA_ROBOT')
import config # Modulo com as configurações dos dispositivos de rede


broker = config.MQTT_BROKER_ADRESS # broker adress
port = config.MQTT_PORT # broker port
topic_base = config.EVA_TOPIC_BASE

# obtain audio from the microphone
r = sr.Recognizer()


for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f'{index}, {name}')


# # Matrix Voice is default
mic = sr.Microphone()
r.energy_threshold = 1000 # sensibilidade da captação


# MQTT
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    #print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
    client.subscribe(topic=[(topic_base + '/listen', 1), ])
    print("STT module CONNECTED.")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic == topic_base + '/listen':
        #file_name = msg.payload.decode().split("|")[0]
        with mic as source:
            #r.adjust_for_ambient_noise(source)  # listen for 1 second to calibrate the energy threshold for ambient noise levels
            print("EVA is listening!")
            audio = r.listen(source)
            print("The audio was recorded!")

            # recognize speech using Google Speech Recognition
            try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio)`
                response = r.recognize_google(audio, language="pt-BR")
                print("Google Speech Recognition thinks you said " + response)
                client.publish(topic_base + "/var/dollar", response)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
            
        client.publish(topic_base + "/state", "FREE")



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

client = mqtt_client.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port)


client.loop_forever()

# import speech_recognition as sr
# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
