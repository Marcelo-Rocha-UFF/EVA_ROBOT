from paho.mqtt import client as mqtt_client
import subprocess
import time

import sys
sys.path.append('/home/pi/EVA_ROBOT')
import config # Modulo com as configurações dos dispositivos de rede

broker = config.MQTT_BROKER_ADRESS # broker adress
port = config.MQTT_PORT # broker port
topic_base = config.EVA_TOPIC_BASE


# 
def playsound(file_path, audio_file, type, block = True):
        print(type)
        if type == "audio":
            audio_format = config.AUDIO_EXTENSION
        elif type == "speech":
            audio_format = config.WATSON_AUDIO_EXTENSION
            client.publish(topic_base + "/log", "EVA spoke the text and is FREE now.")
        
        # sound = pygame.mixer.Sound(file_path + audio_file + audio_format)
        # playing = sound.play()
        if block == True:
            print("Blocking audio.")
            play = subprocess.Popen(['play', file_path + audio_file + audio_format], stdout=subprocess.PIPE)
            play.communicate()[0]
        else:
            print("No-blocking audio.")
            play = subprocess.Popen(['play', file_path + audio_file + audio_format], stdout=subprocess.PIPE)

        

# speaking is always bloking. The function is responsable to FREE the robot state
def speech(audio_file, block = True):
        file_path = "eva-tts-module/tts_cache_files/"
        playsound(file_path, audio_file, "speech", block)
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
        if block == "TRUE":
            playsound("eva-audio-module/audio_files/", file_name, "audio", True)
            client.publish(topic_base + "/state", "FREE") # libera o robô
        else:
            playsound("eva-audio-module/audio_files/", file_name, "audio", False) 

    if msg.topic == topic_base + '/speech':
        file_name = msg.payload.decode()
        speech(file_name, True) # It's always blocking

    
client = mqtt_client.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port)


client.loop_forever()