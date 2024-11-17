# Software developed by Marcelo Marques da Rocha
# MidiaCom Laboratory - Universidade Federal Fluminense
# This work was funded by CAPES and Google Research

from deep_translator import GoogleTranslator
from paho.mqtt import client as mqtt_client
import time

import sys
sys.path.append('/home/pi/EVA_ROBOT')
import config # Module with network device configurations.

broker = config.MQTT_BROKER_ADRESS # Broker address.
port = config.MQTT_PORT # Broker Port.
topic_base = config.EVA_TOPIC_BASE

print("Loading the model into RAM...")
now = time.time()
from transformers import pipeline
classifier = pipeline("sentiment-analysis", model="michellejieli/emotion_text_classifier", top_k=1)

print("Loading time (s): ", (time.time() - now))


# MQTT
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    # Reconnect then subscriptions will be renewed.
    client.subscribe(topic=[(topic_base + '/textEmotion', 1), ])
    print("Text-Emotion-Recognition Module - Connected.")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic == topic_base + '/textEmotion':
        msg.payload = msg.payload.decode()
        source_lang = msg.payload.split("|")[0].lower()
        if source_lang != 'en': # It will be translated
            tradutor = GoogleTranslator(source=source_lang, target='en') # The target will be always 'en' because this is the language of the model.
            texto = (msg.payload).split("|")[1] # This is the text to translate.
            print("Translating from '" + source_lang + "' to 'en' (english).")
            traducao = tradutor.translate(texto)
            msg.payload = traducao
        else:
            msg.payload = (msg.payload).split("|")[1] # This is the text to classify
        print("Using the LLM model to extract emotion from the sentence: " + msg.payload)
        emotion = str(classifier(msg.payload)[0][0]["label"])
        # mapping emotions to defalt names
        remaping_emotions = {
            "joy" : "HAPPY",
            "sadness" : "SAD",
            "fear" : "FEAR",
            "disgust" : "DISGUST",
            "neutral" : "NEUTRAL",
            "surprise" : "SURPRISE",
            "anger" : "ANGRY"
        }
        emotion = remaping_emotions[emotion]
        print("The LLM model guess that emotion from text is: " + emotion)
        client.publish(topic_base + "/var/dollar", emotion) # This publish will pass the value to the EvaSIM, so the EvaSIM will also unblock itself



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