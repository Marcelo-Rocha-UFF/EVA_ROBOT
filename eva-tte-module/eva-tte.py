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
    print("Text-To-Emotion Module - Connected.")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic == topic_base + '/textEmotion':
        print("Using the LLM model to extract emotion from text.")
        emotion = str(classifier(msg.payload.decode())[0][0]["label"])
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
        client.publish(topic_base + "/var/dollar", emotion)
        client.publish(topic_base + "/state", "FREE_TEXT_EMOTION")



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