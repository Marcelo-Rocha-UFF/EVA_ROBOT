#!/usr/bin/env python3

from paho.mqtt import client as mqtt_client

import speech_recognition as sr

import sys
sys.path.append('/home/pi/EVA_ROBOT')
import config # Module with network device configurations.


broker = config.MQTT_BROKER_ADRESS # Broker address.
port = config.MQTT_PORT # Broker Port
topic_base = config.EVA_TOPIC_BASE


# Audio will come from the microphone.
r = sr.Recognizer()

for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f'{index}, {name}')

# The Matrix Voice is the default.
mic = sr.Microphone(chunk_size = 64) # The smaller chunk_size helps capture smaller words. The default is 1024, but it fails for "yes", "no", "suzy"

threshold = 980 # Regulates the sensitivity between speech and silence. A good value tested in my house was 980.
# timeout = 10

# r.dynamic_energy_threshold = False
r.energy_threshold = threshold # Audio capture sensitivity.


# MQTT
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    # Reconnect then subscriptions will be renewed.
    client.subscribe(topic=[(topic_base + '/listen', 1), ])
    print("Speech-To-Text Module - Connected.")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic == topic_base + '/listen':
        with mic as source:
            print("EVA is listening!")
            audio = r.listen(source)
            print("The audio was recorded!")
            try:
                # Recognizes speech using Google Speech Recognition.
                # *** Nora, I think there is an option to use Whisper instead of Google *** 
                response = r.recognize_google(audio, language="pt-BR")
                print("Google Speech Recognition guess you said: " + response)
                client.publish(topic_base + "/var/dollar", response)
                client.publish(topic_base + "/log", "Google Speech Recognition guess you said: " + response)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand your audio...")
            except sr.RequestError as e:
                print("Unable to request the results from Google Speech Recognition: {0}".format(e))
            
        client.publish(topic_base + "/state", "FREE_LISTEN")



# Run the MQTT client thread.
client = mqtt_client.Client()
client.on_connect = on_connect
client.on_message = on_message
try:
    client.connect(broker, port)
except:
    print ("Unable to connect to Broker.")
    exit(1)

client.loop_forever()