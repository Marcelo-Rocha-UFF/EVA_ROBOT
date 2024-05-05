# from playsound import playsound as ps
import hashlib
import os
from paho.mqtt import client as mqtt_client

import time

from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import ApiException


import sys
sys.path.append('/home/pi/EVA_ROBOT')
import config # Módulo com as configurações dos dispositivos de rede.

broker = config.MQTT_BROKER_ADRESS # Endereço do Broker.
port = config.MQTT_PORT # Porta do Broker.
topic_base = config.EVA_TOPIC_BASE

voice_tone = config.VOICE_TONE


# Chave de configuração da API do Watson.
with open("eva-tts-module/ibm_cred.txt", "r") as ibm_cred: 
    ibm_config = ibm_cred.read().splitlines()
apikey = ibm_config[0]
url = ibm_config[1]

# Setup watson service.
authenticator = IAMAuthenticator(apikey)

# TTS service.
tts = TextToSpeechV1(authenticator = authenticator)
tts.set_service_url(url)

auth_start_time = time.time() # Momento da autenticação.
first_requisition = True; # Indica que é a primeira requisição do serviço do Watson.

# MQTT
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic=[(topic_base + '/talk', 1), ])
    print("Text-To-Speech Module - Connected.")
    
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global voice_tone, auth_start_time, apikey, url, authenticator, tts, first_requisition
    if msg.topic == topic_base + '/talk':
        print("Using IBM Watson to convert text to audio...")
        # Assume the default UTF-8 (Gera o hashing do arquivo de audio).
        # Além disso, usa o atributo de timbre de voz no hash de arquivo.
        if len(msg.payload.decode().split("|")) == 2:
            voice_tone = msg.payload.decode().split("|")[0]
            msg.payload = (msg.payload.decode()).split("|")[1]
            msg.payload = msg.payload.encode()

        print("Voice:", voice_tone, "Message:", msg.payload.decode())
        hash_object = hashlib.md5(msg.payload)
        file_name = "_audio_"  + voice_tone + hash_object.hexdigest()
        
        audio_file_is_ok = False
        while(not audio_file_is_ok):
            # Verifica se o áudio da fala já existe na pasta cache.
            if not (os.path.isfile("eva-tts-module/tts_cache_files/" + file_name + config.WATSON_AUDIO_EXTENSION)): # Se não existe, chama o Watson.
                print("The file is not cached... Let's try to generate it!")

                # Testes com a primeira requisição a partir de um reset no módulo.
                # =======================================================================================
                # O Watson parece impor um tempo de conexão limitado a partir da primeira requisição.
                # 1min de inatividade -> OK
                # 2min de inatividade -> OK
                # 8min de inatividade -> OK 

                # Testes com uma requisição a partir de outra, sem o reset do módulo.
                # =======================================================================================
                # 3min de inatividade a partir da primeira req.-> OK
                # 3,30min de inatividade a partir da primeira req.-> OK
                # 4min de inatividade a partir de uma primeira req. -> Travou!
                # 5min de inatividade a partir da uma primeira req.-> Travou!

                # Verifica se o módulo esteve inativo por mais 3min (180s) a partir da primeira requisição.
                print(first_requisition, (time.time() - auth_start_time))
                if (not(first_requisition) and (time.time() - auth_start_time >= 180)):
                    #global apikey, url, authenticator, tts
                    print("The module has been inactive for more than 3 minutes (since the first request) and a new authentication will be performed.")
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
                    first_requisition = False
                    auth_start_time = time.time() # Momento da autenticação.

                # Incia o processo de TTS
                tts_start = time.time() # Variável utilizada para marcar o tempo de processamento do serviço de TTS.
                while(not audio_file_is_ok):
                    # Funções do serviço de TTS dpara o EVA
                    with open("eva-tts-module/tts_cache_files/" + file_name + config.WATSON_AUDIO_EXTENSION, 'wb') as audio_file:
                        try:
                            res = tts.synthesize(msg.payload.decode(), accept = config.ACCEPT_AUDIO_EXTENSION, voice = voice_tone).get_result()
                            print("Writing content to disk...")
                            audio_file.write(res.content)
                            file_size = os.path.getsize("eva-tts-module/tts_cache_files/" + file_name + config.WATSON_AUDIO_EXTENSION)
                            print("File size:", file_size, " bytes.")
                            if file_size == 0: # Arquivo corrompido!
                                print("#### Corrupted file....")
                                os.remove("eva-tts-module/tts_cache_files/" + file_name + config.WATSON_AUDIO_EXTENSION)
                            else:
                                tts_ending = time.time()
                                client.publish(topic_base + "/log", "The audio was generated correctly in (s): %.2f" % (tts_ending - tts_start))
                                print("The file will be played!")
                                client.publish(topic_base + "/log", "EVA is busy trying to speak the text.")
                                client.publish(topic_base + "/speech", file_name)
                                audio_file_is_ok = True
                                first_requisition = False
                        except ApiException as ex:
                            print ("The function failed with the following error code: " + str(ex.code) + ": " + ex.message)
                            exit(1)
            else:
                print("The file is cached!")
                if (os.path.getsize("eva-tts-module/tts_cache_files/" + file_name + config.WATSON_AUDIO_EXTENSION)) == 0: # arquivo corrompido
                    print("The generated audio file is 0 bytes, corrupt and will be removed!")
                    os.remove("eva-tts-module/tts_cache_files/" + file_name + config.WATSON_AUDIO_EXTENSION)
                else:
                    print("The file is more than 0 bytes and will be played now!")
                    client.publish(topic_base + "/log", "The audio was found in the cache.")
                    client.publish(topic_base + "/log", "EVA is busy trying to speak the text.")
                    client.publish(topic_base + "/speech", file_name)
                    audio_file_is_ok = True  
        
        
        
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

