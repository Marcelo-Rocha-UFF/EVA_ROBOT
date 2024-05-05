from paho.mqtt import client as mqtt_client
import subprocess


import sys
sys.path.append('/home/pi/EVA_ROBOT')
import config # Módulo com as configurações dos dispositivos de rede.

broker = config.MQTT_BROKER_ADRESS # Endereço do Broker.
port = config.MQTT_PORT # Porta do Broker.
topic_base = config.EVA_TOPIC_BASE


# 
def playsound(file_path, audio_file, type, block = True):
        print(type)
        if type == "audio":
            audio_format = config.AUDIO_EXTENSION
        elif type == "speech":
            audio_format = config.WATSON_AUDIO_EXTENSION
            client.publish(topic_base + "/log", "EVA spoke the text and is free now.")
        
        if block == True:
            print('Playing audio in BLOCKING mode.')
            play = subprocess.Popen(['play', file_path + audio_file + audio_format], stdout=subprocess.PIPE)
            play.communicate()[0]
        else:
            print('Playing audio in NON-BLOCKING mode.')
            play = subprocess.Popen(['play', file_path + audio_file + audio_format], stdout=subprocess.PIPE)

        

# A fala é sempre do tipo (Blocking). A função playsound é responsável por colocar o estado do robô como "FREE".
def speech(audio_file, block = True):
        file_path = "eva-tts-module/tts_cache_files/"
        playsound(file_path, audio_file, "speech", block)
        client.publish(topic_base + "/state", "FREE - (AUDIO_SPEAK)") 


# MQTT
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    #print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
    client.subscribe(topic=[(topic_base + '/audio', 1), ])
    client.subscribe(topic=[(topic_base + '/speech', 1), ])
    print("Audio Module - Connected.")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic == topic_base + '/audio':
        file_name = msg.payload.decode().split("|")[0]
        block = msg.payload.decode().split("|")[1]
        if block == "TRUE":
            playsound("eva-audio-module/audio_files/", file_name, "audio", True)
            client.publish(topic_base + "/state", "FREE - (AUDIO_SOUND)") # Libera o robô
        else:
            playsound("eva-audio-module/audio_files/", file_name, "audio", False) 

    if msg.topic == topic_base + '/speech':
        file_name = msg.payload.decode()
        speech(file_name, True) # A fala roda sempre no modo "Blocking".


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