# from playsound import playsound as ps
import hashlib
import os
from paho.mqtt import client as mqtt_client

import time

# from ibm_watson.text_to_speech_v1 import Voice
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


import sys
sys.path.append('/home/pi/EVA_ROBOT')
import config # Modulo com as configurações dos dispositivos de rede

broker = config.MQTT_BROKER_ADRESS # broker adress
port = config.MQTT_PORT # broker port
topic_base = config.EVA_TOPIC_BASE

voice_tone = config.VOICE_TONE


# watson config api key
with open("eva-tts-module/ibm_cred.txt", "r") as ibm_cred: 
    ibm_config = ibm_cred.read().splitlines()
apikey = ibm_config[0]
url = ibm_config[1]
# setup watson service
authenticator = IAMAuthenticator(apikey)
# tts service
tts = TextToSpeechV1(authenticator = authenticator)
tts.set_service_url(url)

# def playsound(audio_file, block = True):
#     file_path = "eva-tts-module/tts_cache_files/"
#     ps(file_path + audio_file, block)


# MQTT
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    #print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
    client.subscribe(topic=[(topic_base + '/talk', 1), ])
    print("TTS module CONNECTED.")
    
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global voice_tone
    if msg.topic == topic_base + '/talk':
        print("Usando o IBM Watson para converter o texto em audio...")
        # Assume the default UTF-8 (Gera o hashing do arquivo de audio)
        # Also, uses the voice tone attribute in file hashing
        if len(msg.payload.decode().split("|")) == 2:
            voice_tone = msg.payload.decode().split("|")[0]
            msg.payload = (msg.payload.decode()).split("|")[1]
            msg.payload = msg.payload.encode()

        print("Voice:", voice_tone, "Message:", msg.payload.decode())
        hash_object = hashlib.md5(msg.payload)
        file_name = "_audio_"  + voice_tone + hash_object.hexdigest()
        
        audio_file_is_ok = False
        while(not audio_file_is_ok):
            # verifica se o audio da fala já existe na pasta cache
            if not (os.path.isfile("eva-tts-module/tts_cache_files/" + file_name + config.WATSON_AUDIO_EXTENSION)): # se nao existe chama o watson
                print("O arquivo não está em cache... Vamos tentar gerá-lo!")
                tts_start = time.time()
                while(not audio_file_is_ok):
                    # Eva tts functions
                    with open("eva-tts-module/tts_cache_files/" + file_name + config.WATSON_AUDIO_EXTENSION, 'wb') as audio_file:
                        try:
                            print("Gerando o res...")
                            res = tts.synthesize(msg.payload.decode(), accept = config.ACCEPT_AUDIO_EXTENSION, voice = voice_tone).get_result()
                            print("gravando conteudo no disco...")
                            audio_file.write(res.content)
                            file_size = os.path.getsize("eva-tts-module/tts_cache_files/" + file_name + config.WATSON_AUDIO_EXTENSION)
                            print("File size:", file_size, " bytes.")
                            if file_size == 0: # arquivo corrompido
                                print("#### Arquivo corrompido....")
                                os.remove("eva-tts-module/tts_cache_files/" + file_name + config.WATSON_AUDIO_EXTENSION)
                            else:
                                tts_ending = time.time()
                                client.publish(topic_base + "/log", "The audio was generated correctly in (s): " + str(tts_ending - tts_start))
                                print("O arquivo foi gerado corretamente e será tocado!")
                                client.publish(topic_base + "/log", "EVA is BUSY trying to speak the text.")
                                client.publish(topic_base + "/speech", file_name)
                                audio_file_is_ok = True  
                        except:
                            print("Voice exception")
                            exit(1)
            else:
                print("O arquivo está em cache!")
                if (os.path.getsize("eva-tts-module/tts_cache_files/" + file_name + config.WATSON_AUDIO_EXTENSION)) == 0: # arquivo corrompido
                    print("O arquivo de audio gerado tem 0 bytes, está corrompido e será removido!")
                    os.remove("eva-tts-module/tts_cache_files/" + file_name + config.WATSON_AUDIO_EXTENSION)
                else:
                    print("O arquivo tem mais que 0 bytes e será tocado agora!")
                    client.publish(topic_base + "/log", "The audio was found in cache.")
                    client.publish(topic_base + "/log", "EVA is BUSY trying to speak the text.")
                    client.publish(topic_base + "/speech", file_name)
                    audio_file_is_ok = True  
        
        
        
        
client = mqtt_client.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port)


client.loop_forever()

