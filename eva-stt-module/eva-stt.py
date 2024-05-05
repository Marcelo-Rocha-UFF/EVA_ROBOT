#!/usr/bin/env python3

from paho.mqtt import client as mqtt_client

import speech_recognition as sr

import sys
sys.path.append('/home/pi/EVA_ROBOT')
import config # Módulo com as configurações dos dispositivos de rede.


broker = config.MQTT_BROKER_ADRESS # Endereço do Broker.
port = config.MQTT_PORT # Porta do Broker
topic_base = config.EVA_TOPIC_BASE


# O áudio virá do microfone.
r = sr.Recognizer()

for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f'{index}, {name}')

# A Matrix Voice o padrão (default).
mic = sr.Microphone(chunk_size = 64) # O chunk_size menor ajuda a capturar palavras menores. O default é 1024, mas falha para "sim", "não", "suzy"

threshold = 980 # Regula a sensibilidade entre o que é fala e silêncio. Um bom valor testado na minha casa foi 980.
# timeout = 10

# r.dynamic_energy_threshold = False
r.energy_threshold = threshold # Sensibilidade da captação.


# MQTT
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic=[(topic_base + '/listen', 1), ])
    print("Speech-To-Text Module - Connected.")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic == topic_base + '/listen':
        with mic as source:
            #r.adjust_for_ambient_noise(source)  # listen for 1 second to calibrate the energy threshold for ambient noise levels
            print("EVA is listening!")
            audio = r.listen(source)
            print("The audio was recorded!")

            # Reconhece a fala usando o Google Speech Recognition.
            try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio)`
                response = r.recognize_google(audio, language="pt-BR")
                print("Google Speech Recognition guess you said: " + response)
                client.publish(topic_base + "/var/dollar", response)
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand your audio...")
            except sr.RequestError as e:
                print("Unable to request the results from Google Speech Recognition: {0}".format(e))
            
        client.publish(topic_base + "/state", "FREE_LISTEN")



# Executa a thread do cliente MQTT.
client = mqtt_client.Client()
client.on_connect = on_connect
client.on_message = on_message
try:
    client.connect(broker, port)
except:
    print ("Unable to connect to Broker.")
    exit(1)

client.loop_forever()