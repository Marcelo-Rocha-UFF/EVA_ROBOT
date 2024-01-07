from playsound import playsound as ps
from paho.mqtt import client as mqtt_client


import sys
sys.path.append('/home/pi/EVA_ROBOT')
import config # Modulo com as configurações dos dispositivos de rede

broker = config.MQTT_BROKER_ADRESS # broker adress
port = config.MQTT_PORT # broker port
topic_base = config.EVA_TOPIC_BASE


# 
def playsound(audio_file, block = True):
        file_path = "eva-audio-module/audio_files/"
        ps(file_path + audio_file + config.AUDIO_EXTENSION , block)

# speaking is always bloking. The function is responsable to FREE the robot state
def speech(audio_file, block = True):
        file_path = "eva-tts-module/tts_cache_files/"
        ps(file_path + audio_file, block)
        client.publish(topic_base + "/log", "EVA spoke the text and is FREE now.")
        client.publish(topic_base + "/state", "FREE")


# MQTT
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    #print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
    client.subscribe(topic=[(topic_base + '/audio', 1), ])
    client.subscribe(topic=[(topic_base + '/speech', 1), ])
    print("Audio module CONNECTED.")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic == topic_base + '/audio':
        file_name = msg.payload.decode().split("|")[0]
        block = msg.payload.decode().split("|")[1]
        playsound(file_name, block)
        if block == "TRUE":
            client.publish(topic_base + "/state", "FREE") # libera o robô

    if msg.topic == topic_base + '/speech':
        file_name = msg.payload.decode()
        speech(file_name, True) # It's always bloking

    
client = mqtt_client.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port)


client.loop_forever()