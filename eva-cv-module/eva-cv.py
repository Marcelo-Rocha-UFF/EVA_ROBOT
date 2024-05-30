import argparse

import time
import os

import sys
sys.path.append('/home/pi/EVA_ROBOT')
import config # Module with network device configurations.

broker = config.MQTT_BROKER_ADRESS # Broker address.
port = config.MQTT_PORT # Broker Port.
topic_base = config.EVA_TOPIC_BASE

from paho.mqtt import client as mqtt_client

from picamera.array import PiRGBArray
from picamera import PiCamera

import cv2
import numpy as np

import face_recognition as fr

from tensorflow.keras.layers import (Conv2D, Dense, Dropout, Flatten, MaxPooling2D)
from tensorflow.keras.models import Sequential



# Initialize the camera
camera = PiCamera()

# Time required for the camera to initialize
time.sleep(0.1)
print("The camera was initialized.")

# Input arg parsing
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
    # Reconnect then subscriptions will be renewed.
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
        # This resolution showed good results in the expression recognition process
        camera.resolution = (640, 480)
        camera.framerate = 10
        rawCapture = PiRGBArray(camera, size=(640, 480)) # 
        print("Capturing a facial expression.")
        client.publish(topic_base + '/log', "Computer Vision: " + "Eva will try to identify the user emotion.") 
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
                client.publish(topic_base + '/log', "Inferred User Emotion: " + emotion_label)
                # Clears the stream preparing to capture the next frame.
                rawCapture.truncate(0)
                stop_FER = True
                break
            if stop_FER:
                break
            # Shows the video capture window.
            if args.video:
                cv2.imshow("Frame", image)

                key = cv2.waitKey(1) & 0xFF

                # The 'q' key breaks the loop.
                if key == ord("q"):
                    break
            # Clears the stream preparing to capture the next frame.
            rawCapture.truncate(0)
        client.publish(topic_base + "/state", "FREE - (CV_FACIAL_EXPRESSION_RECOGNITION)")


###################################################################################
# Face recognition Submodule ######################################################
###################################################################################
    elif msg.topic == topic_base + '/userID':
        # This resolution showed good results in the facial recognition process
        camera.resolution = (400, 400)
        camera.framerate = 10
        rawCapture = PiRGBArray(camera, size=(400, 400)) # 
        client.publish(topic_base + '/log', "Computer Vision: " + "Eva will try to IDENTIFY the user.") 
        print("Capturing a face.")
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            image = frame.array
            facecasc = cv2.CascadeClassifier('eva-cv-module/haarcascade_frontalface_default.xml')  
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = facecasc.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
            # ########################## Expression ##########################################
            for (x, y, w, h) in faces:
                print("Encoding a face...")
                user_photo_encoded = fr.face_encodings(image)[0] # A numpy array
                file_list = os.listdir('eva-cv-module/users')
                id_usuario = "unknown"
                min_distance = 100 # Long distance to initialize the variable
                for file_name in file_list:
                    if file_name.endswith(".npy"): # Only numpy arrays
                        user_file_encoded = np.load('eva-cv-module/users/' + file_name)
                        distance = fr.face_distance([user_photo_encoded], user_file_encoded)
                        print("Comparing current user with:", file_name, " Distance:", distance)
                        if distance < min_distance:
                            min_distance = distance
                            id_usuario = file_name.split('_')[0]
                rawCapture.truncate(0)
                ########################################
                if min_distance > 0.42: # An estimated value
                    id_usuario = "unknown"
                client.publish(topic_base + "/var/dollar", id_usuario)
                client.publish(topic_base + '/log', "User ID: " + id_usuario) 
                break
            break
        client.publish(topic_base + "/state", "FREE - (CV_FACE_RECOGNITION)")



###################################################################################
# QR Code Reader Submodule ########################################################
###################################################################################
    elif msg.topic == topic_base + '/qrRead':
        client.publish(topic_base + '/log', "Computer Vision: " + "Eva will try to read a QR Code.") 
        camera.resolution = (1920, 1080) # This resolution showed improvements in QR recognition
        camera.framerate = 10
        rawCapture = PiRGBArray(camera)
        print("Trying to read a QR Code...")
        qrCodeDetector = cv2.QRCodeDetector() # QRCode detector
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            image = frame.array
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            decodedText, points, _ = qrCodeDetector.detectAndDecode(gray)  
            if (decodedText != ""):
                print("QR Code content: " + decodedText)
                client.publish(topic_base + "/var/dollar", decodedText)
                # Clears the stream preparing to capture the next frame.
                rawCapture.truncate(0)
                client.publish(topic_base + '/log', "QR Code content: " + decodedText)
                break
            else:
                print("A empty string was read...")
                client.publish(topic_base + "/log", "A EMPTY string was read...")
            
            # Shows the video capture window.
            if args.video:
                cv2.imshow("Frame", gray)

                key = cv2.waitKey(1) & 0xFF

                # The 'q' key breaks the loop.
                if key == ord("q"):
                    break
            # Clears the stream preparing to capture the next frame.
            rawCapture.truncate(0)
        client.publish(topic_base + "/state", "FREE - (CV_QR_CODE)")


# Creates the 7 layers for the model.
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

# Load the model with its weights.
model.load_weights('eva-cv-module/model.h5')

# Associate classes with their names
emotion_dict = {0: "ANGRY", 1: "DISGUST", 2: "FEAR", 3: "HAPPY", 4: "NEUTRAL", 5: "SAD", 6: "SURPRISE"}


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