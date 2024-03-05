import argparse
import time

import sys
sys.path.append('/home/pi/EVA_ROBOT')
import config # Modulo com as configurações dos dispositivos de rede

broker = config.MQTT_BROKER_ADRESS # broker adress
port = config.MQTT_PORT # broker port
topic_base = config.EVA_TOPIC_BASE

from paho.mqtt import client as mqtt_client

from picamera.array import PiRGBArray
from picamera import PiCamera

import cv2
import numpy as np

from tensorflow.keras.layers import (Conv2D, Dense, Dropout, Flatten, MaxPooling2D)
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D


broker = config.MQTT_BROKER_ADRESS # broker adress
port = config.MQTT_PORT # broker port
topic_base = config.EVA_TOPIC_BASE


 #initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 29
rawCapture = PiRGBArray(camera, size=(640, 480))
# allow the camera to warmup
time.sleep(0.1)
print("The camera was initialized...")

# input arg parsing
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--fullscreen',
                    help='Display window in full screen', action='store_true')
parser.add_argument('-v', '--video', help='Display video capture window', action='store_true')
parser.add_argument('-fl', '--flip', help='Flip incoming video signal', action='store_true')
args = parser.parse_args()

# input arg parsing
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--fullscreen',
                    help='Display window in full screen', action='store_true')
parser.add_argument('-v', '--video', help='Display video capture window', action='store_true')
parser.add_argument(
    '-fl', '--flip', help='Flip incoming video signal', action='store_true')
args = parser.parse_args()



# MQTT
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic=[(topic_base + '/userEmotion', 1), ])
    client.subscribe(topic=[(topic_base + '/userID', 1), ])
    client.subscribe(topic=[(topic_base + '/qrReader', 1), ])
    print("Computer Vision module CONNECTED.")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic == topic_base + '/userEmotion':
        print("Capturing an expression...")
        stop_FER = False
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            # time for fps
            start_time = time.time()
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
                # clear the stream in preparation for the next frame
                rawCapture.truncate(0)
                stop_FER = True
                break
            if stop_FER:
                break
            # Display video capture window
            if args.video:
                cv2.imshow("Frame", image)

                key = cv2.waitKey(1) & 0xFF

                # if the `q` key was pressed, break from the loop
                if key == ord("q"):
                    break
            # clear the stream in preparation for the next frame
            rawCapture.truncate(0)
        client.publish(topic_base + "/state", "FREE")


    if msg.topic == topic_base + '/userID':
        print("Recognizing a face...")


    if msg.topic == topic_base + '/qrReader':
        print("Trying to read a QR Code...")
        qrCodeDetector = cv2.QRCodeDetector() # detector de QRCode
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            image = frame.array
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            decodedText, points, _ = qrCodeDetector.detectAndDecode(gray)  
            if (decodedText != ""):
                print(decodedText)
                # clear the stream in preparation for the next frame
                rawCapture.truncate(0)
                break
            else:
                pass
            
            # Display video capture window
            if args.video:
                cv2.imshow("Frame", gray)

                key = cv2.waitKey(1) & 0xFF

                # if the `q` key was pressed, break from the loop
                if key == ord("q"):
                    break
            # clear the stream in preparation for the next frame
            rawCapture.truncate(0)



# create model
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

model.load_weights('eva-cv-module/model.h5')

# dictionary which assigns each label an emotion (alphabetical order)
emotion_dict = {0: "Angry", 1: "Disgust", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

qrCodeDetector = cv2.QRCodeDetector() # detector de QRCode

# #########################################################################################################
# for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
#     print("Entrou no FOR.............")
#     # time for fps
#     start_time = time.time()

# 	# grab the raw NumPy array representing the image, then initialize the timestamp
# 	# and occupied/unoccupied text


#     image = frame.array
#     #facecasc = cv2.CascadeClassifier('eva-cv-module/haarcascade_frontalface_default.xml')  
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     #faces = facecasc.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
	
# ########################## Expression ##########################################
#     # for (x, y, w, h) in faces:
#     #     cv2.rectangle(image, (x, y-50), (x+w, y+h+10), (255, 0, 0), 2)
#     #     roi_gray = gray[y:y + h, x:x + w]
#     #     cropped_img = np.expand_dims(np.expand_dims(
#     #         cv2.resize(roi_gray, (48, 48)), -1), 0)
#     #     prediction = model.predict(cropped_img)
#     #     maxindex = int(np.argmax(prediction))
#     #     emotion_label = emotion_dict[maxindex]
#     #     print(emotion_label)
#     #     cv2.putText(image, emotion_label, (x+20, y-60),
#     #         cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    
# ############ QR Reader ############################
#     decodedText, points, _ = qrCodeDetector.detectAndDecode(gray)  
#     if (decodedText != ""):
#         print(decodedText)  
#     else:
#         print("----------------------")
    


#     # Display video capture window
#     if args.video:
#         fps = str(int(1.0 / (time.time() - start_time)))
#         #cv2.putText(image, fps + " fps", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
#         cv2.putText(gray, fps + " fps", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        
#         # show the frame
#         #cv2.imshow("Frame", image)
#         cv2.imshow("Frame", gray)

#         key = cv2.waitKey(1) & 0xFF

#         # if the `q` key was pressed, break from the loop
#         if key == ord("q"):
#             break

#     # clear the stream in preparation for the next frame
#     rawCapture.truncate(0)
# #########################################################################################################


#cv2.destroyAllWindows()

client = mqtt_client.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port)


client.loop_forever()
