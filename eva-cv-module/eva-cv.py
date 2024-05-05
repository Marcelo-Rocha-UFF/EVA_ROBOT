import argparse

import time
import os

import sys
sys.path.append('/home/pi/EVA_ROBOT')
import config # Módulo com as configurações dos dispositivos de rede.

broker = config.MQTT_BROKER_ADRESS # Endereço do Broker.
port = config.MQTT_PORT # Porta do Broker.
topic_base = config.EVA_TOPIC_BASE

from paho.mqtt import client as mqtt_client

from picamera.array import PiRGBArray
from picamera import PiCamera

import cv2
import numpy as np

import face_recognition as fr

from tensorflow.keras.layers import (Conv2D, Dense, Dropout, Flatten, MaxPooling2D)
from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense, Dropout, Flatten
# from tensorflow.keras.layers import Conv2D
# from tensorflow.keras.layers import MaxPooling2D



# Inicializa a câmera
camera = PiCamera()

# Tempo necessário para a camera inicializar
time.sleep(0.1)
print("The camera was initialized.")

# input arg parsing
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--fullscreen',
                    help='Display window in full screen', action='store_true')
parser.add_argument('-v', '--video', help='Display video capture window', action='store_true')
parser.add_argument('-fl', '--flip', help='Flip incoming video signal', action='store_true')
args = parser.parse_args()


# MQTT
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic=[(topic_base + '/userEmotion', 1), ])
    client.subscribe(topic=[(topic_base + '/userID', 1), ])
    client.subscribe(topic=[(topic_base + '/qrRead', 1), ])
    print("Computer Vision Module - Connected.")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

######################################################################################################
# Face Expression Recognition Submodule ##############################################################
######################################################################################################
    if msg.topic == topic_base + '/userEmotion':
        # Essa resolução apresentou bons resultados no processo de reconhecimento de expressões
        camera.resolution = (640, 480)
        camera.framerate = 10
        rawCapture = PiRGBArray(camera, size=(640, 480)) # 
        print("Capturing a facial expression.")
        stop_FER = False
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            image = frame.array
            facecasc = cv2.CascadeClassifier('eva-cv-module/haarcascade_frontalface_default.xml')  
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = facecasc.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
            # ########################## Expression ##########################################
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
                roi_gray = gray[y:y + h, x:x + w]
                cropped_img = np.expand_dims(np.expand_dims(
                cv2.resize(roi_gray, (48, 48)), -1), 0)
                prediction = model.predict(cropped_img)
                maxindex = int(np.argmax(prediction))
                emotion_label = emotion_dict[maxindex]
                print(emotion_label)
                cv2.putText(image, emotion_label, (x+20, y-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                client.publish(topic_base + "/var/dollar", emotion_label)
                # Limpa o fluxo preparando para capturar o próximo frame.
                rawCapture.truncate(0)
                stop_FER = True
                break
            if stop_FER:
                break
            # Mostra a janela de captura do vídeo.
            if args.video:
                cv2.imshow("Frame", image)

                key = cv2.waitKey(1) & 0xFF

                # A tecla 'q' quebra o loop.
                if key == ord("q"):
                    break
            # Limpa o fluxo preparando para capturar o próximo frame.
            rawCapture.truncate(0)
        client.publish(topic_base + "/state", "FREE - (CV_FACIAL_EXPRESSION_RECOGNITION)")


###################################################################################
# Face recognition Submodule ######################################################
###################################################################################
    elif msg.topic == topic_base + '/userID':
        # Essa resolução apresentou bons resultados no processo de reconhecimento facial
        user_recognized = False
        camera.resolution = (400, 400)
        camera.framerate = 10
        rawCapture = PiRGBArray(camera, size=(400, 400)) # 
        print("Capturing a face.")
        stop_FR = False
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            image = frame.array
            facecasc = cv2.CascadeClassifier('eva-cv-module/haarcascade_frontalface_default.xml')  
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = facecasc.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
            # ########################## Expression ##########################################
            for (x, y, w, h) in faces:
                print("Encoding a face...")
                #image = cv2.resize(image, (200, 200))
                user_photo_encoded = fr.face_encodings(image)[0] # A numpy array
                file_list = os.listdir('eva-cv-module/users')
                for file_name in file_list:
                    if file_name.endswith(".npy"): # somente numpy arrays
                        print("Comparing current user with: ", file_name)
                        user_file_encoded = np.load('eva-cv-module/users/' + file_name)
                        comparacao = fr.compare_faces([user_photo_encoded], user_file_encoded, 0.35)
                        #distancia = fr.face_distance([user_photo_encoded], user_file_encoded)
                        if comparacao[0] == True:
                            user_recognized = True
                            print("User identified: ", file_name)
                            client.publish(topic_base + "/var/dollar", file_name.split('_')[0])
                            break
                # Limpa o fluxo preparando para capturar o próximo frame.
                rawCapture.truncate(0)
                if user_recognized == False:
                    print("The user could not be identified!")
                    client.publish(topic_base + "/var/dollar", "unknown")
                stop_FR = True
                break
            if stop_FR:
                break
            # Mostra a janela de captura do vídeo.
            if args.video:
                cv2.imshow("Frame", image)

                key = cv2.waitKey(1) & 0xFF

                # A tecla 'q' quebra o loop.
                if key == ord("q"):
                    break
            # Limpa o fluxo preparando para capturar o próximo frame.
            rawCapture.truncate(0)
        client.publish(topic_base + "/state", "FREE - (CV_FACE_RECOGNITION)")



###################################################################################
# QR Code Reader Submodule ########################################################
###################################################################################
    elif msg.topic == topic_base + '/qrRead':
        camera.resolution = (1920, 1080) # esta resulução apresentou melhoras no reconhecimento do QR
        camera.framerate = 10
        rawCapture = PiRGBArray(camera)
        print("Trying to read a QR Code...")
        qrCodeDetector = cv2.QRCodeDetector() # detector de QRCode
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            image = frame.array
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            decodedText, points, _ = qrCodeDetector.detectAndDecode(gray)  
            if (decodedText != ""):
                print(decodedText)
                client.publish(topic_base + "/var/dollar", decodedText)
                # Limpa o fluxo preparando para capturar o próximo frame.
                rawCapture.truncate(0)
                break
            else:
                pass
            
            # Mostra a janela de captura do vídeo.
            if args.video:
                cv2.imshow("Frame", gray)

                key = cv2.waitKey(1) & 0xFF

                # A tecla 'q' quebra o loop.
                if key == ord("q"):
                    break
            # Limpa o fluxo preparando para capturar o próximo frame.
            rawCapture.truncate(0)
        client.publish(topic_base + "/state", "FREE - (CV_QR_CODE)")


# Cria as 7 camadas para o modelo.
model = Sequential()

model.add(Conv2D(32, kernel_size=(3, 3),
                 activation='relu', input_shape=(48, 48, 1)))
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(7, activation='softmax'))

# Carrega o modelo com seus pesos.
model.load_weights('eva-cv-module/model.h5')

# Associa as classes aos seus nomes
emotion_dict = {0: "ANGRY", 1: "DISGUST", 2: "FEARFUL", 3: "HAPPY", 4: "NEUTRAL", 5: "SAD", 6: "SUSPRISED"}


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