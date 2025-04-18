# Software developed by Marcelo Marques da Rocha
# MidiaCom Laboratory - Universidade Federal Fluminense
# This work was funded by CAPES and Google Research

from paho.mqtt import client as mqtt_client

import tkinter as tk
from PIL import Image, ImageTk
from itertools import count

import random
import time

import sys

sys.path.append('/home/pi/EVA_ROBOT')

import config # Module with network device configurations.

broker = config.MQTT_BROKER_ADRESS # Broker address.
port = config.MQTT_PORT # Broker Port.
topic_base = config.EVA_TOPIC_BASE


class ImageLabel(tk.Label):
    """a label that displays images and plays them if they are gifs"""
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.frames = []
        self.currentstate = "null"
        self.targetstate = "neutral"
        self.stopped = True
        self.frame = 0
        self.bind('<Key>', self.key_press)
        self.init_time = time.time()
        self.interval_pisca = 2

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100 # Controls the display speed of frames.

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.config(image=self.frames[self.frame])
            self.next_frame()


    def next_frame(self):
        current_time = time.time()
        if (self.currentstate == "neutral") and (self.targetstate == "neutral"):
            if current_time - self.init_time > self.interval_pisca:
                self.init_time = time.time()
                self.targetstate = "blink"
                self.interval_pisca = random.randint(0,8)

        elif self.currentstate != self.targetstate:

            if self.currentstate == "null":
                self.currentstate = "neutral"

            elif self.currentstate == "neutral": # State changes starting from "neutral".
                if self.targetstate == "blink":
                    if self.stopped:
                        self.frame = 1 # Initial frame of the animation.
                        self.stopped = False
                    else:
                        if self.frame > 2:
                            self.frame = 0
                            self.currentstatestate = "neutral"
                            self.targetstate = "neutral"
                            self.stopped = True
                        else: 
                            self.config(image=self.frames[self.frame])
                            self.frame += 1
                
                elif self.targetstate == "inlove":
                    if self.stopped:
                        self.frame = 27 # Initial frame of the animation.
                        self.stopped = False
                    else:
                        if self.frame > 28:
                            self.frame = 28
                            self.currentstate = "inlove"
                            self.stopped = True
                        else: 
                            self.config(image=self.frames[self.frame])
                            self.frame += 1

                elif self.targetstate == "disgust":
                    if self.stopped:
                        self.frame = 23 # Initial frame of the animation.
                        self.stopped = False
                    else:
                        if self.frame > 24:
                            self.frame = 24
                            self.currentstate = "disgust"
                            self.stopped = True
                        else: 
                            self.config(image=self.frames[self.frame])
                            self.frame += 1

                elif self.targetstate == "surprise":
                    if self.stopped:
                        self.frame = 19 # Initial frame of the animation.
                        self.stopped = False
                    else:
                        if self.frame > 20:
                            self.frame = 20
                            self.currentstate = "surprise"
                            self.stopped = True
                        else: 
                            self.config(image=self.frames[self.frame])
                            self.frame += 1

                elif self.targetstate == "fear":
                    if self.stopped:
                        self.frame = 15 # Initial frame of the animation.
                        self.stopped = False
                    else:
                        if self.frame > 16:
                            self.frame = 16
                            self.currentstate = "fear"
                            self.stopped = True
                        else: 
                            self.config(image=self.frames[self.frame])
                            self.frame += 1

                elif self.targetstate == "happy":
                    if self.stopped:
                        self.frame = 11 # Initial frame of the animation.
                        self.stopped = False
                    else:
                        if self.frame > 12:
                            self.frame = 12
                            self.currentstate = "happy"
                            self.stopped = True
                        else: 
                            self.config(image=self.frames[self.frame])
                            self.frame += 1

                elif self.targetstate == "sad":
                    if self.stopped:
                        self.frame = 7 # Initial frame of the animation.
                        self.stopped = False
                    else:
                        if self.frame > 8:
                            self.frame = 8
                            self.currentstate = "sad"
                            self.stopped = True
                        else: 
                            self.config(image=self.frames[self.frame])
                            self.frame += 1

                elif self.targetstate == "angry":
                    if self.stopped:
                        self.frame = 3 # Initial frame of the animation.
                        self.stopped = False
                    else:
                        if self.frame > 4:
                            self.frame = 4
                            self.currentstate = "angry"
                            self.stopped = True
                        else: 
                            self.config(image=self.frames[self.frame])
                            self.frame += 1

                

            # Transitions all states to "neutral".
            elif self.targetstate == "blink": # Should not work when not in "neutral".
                pass
            
            elif self.currentstate == "inlove":
                if self.stopped:
                        self.frame = 29 # Initial frame of the animation.
                        self.stopped = False
                else:
                    if self.frame > 30:
                        self.frame = 30
                        self.currentstate = "neutral"
                        self.stopped = True
                    else: 
                        self.config(image=self.frames[self.frame])
                        self.frame += 1

            elif self.currentstate == "disgust":
                if self.stopped:
                        self.frame = 25 # Initial frame of the animation.
                        self.stopped = False
                else:
                    if self.frame > 26:
                        self.frame = 26
                        self.currentstate = "neutral"
                        self.stopped = True
                    else: 
                        self.config(image=self.frames[self.frame])
                        self.frame += 1

            elif self.currentstate == "surprise":
                if self.stopped:
                        self.frame = 21 # Initial frame of the animation.
                        self.stopped = False
                else:
                    if self.frame > 22:
                        self.frame = 22
                        self.currentstate = "neutral"
                        self.stopped = True
                    else: 
                        self.config(image=self.frames[self.frame])
                        self.frame += 1

            elif self.currentstate == "fear":
                if self.stopped:
                        self.frame = 17 # Initial frame of the animation.
                        self.stopped = False
                else:
                    if self.frame > 18:
                        self.frame = 18
                        self.currentstate = "neutral"
                        self.stopped = True
                    else: 
                        self.config(image=self.frames[self.frame])
                        self.frame += 1

            elif self.currentstate == "happy":
                if self.stopped:
                        self.frame = 13 # Initial frame of the animation.
                        self.stopped = False
                else:
                    if self.frame > 14:
                        self.frame = 14
                        self.currentstate = "neutral"
                        self.stopped = True
                    else: 
                        self.config(image=self.frames[self.frame])
                        self.frame += 1

            elif self.currentstate == "sad":
                if self.stopped:
                        self.frame = 9 # Initial frame of the animation.
                        self.stopped = False
                else:
                    if self.frame > 10:
                        self.frame = 10
                        self.currentstate = "neutral"
                        self.stopped = True
                    else: 
                        self.config(image=self.frames[self.frame])
                        self.frame += 1

            elif self.currentstate == "angry":
                if self.stopped:
                        self.frame = 5 # Initial frame of the animation.
                        self.stopped = False
                else:
                    if self.frame > 6:
                        self.frame = 6
                        self.currentstate = "neutral"
                        self.stopped = True
                    else: 
                        self.config(image=self.frames[self.frame])
                        self.frame += 1
        
        self.after(50, self.next_frame)


    def key_press(self, event):
        key = event.char
        print(f"'{key}' is pressed")
        if key == 'n':
            self.targetstate = "neutral"
        elif key == 'a':
            self.targetstate = "angry"
        elif key == 's':
            self.targetstate = "sad"
        elif key == 'h':
            self.targetstate = "happy"
        elif key == 'f':
            self.targetstate = "fear"
        elif key == 'r':
            self.targetstate = "surprise"
        elif key == 'd':
            self.targetstate = "disgust"
        elif key == 'i':
            self.targetstate = "inlove"
        elif key == 'p':
            self.targetstate = "blink"
        elif key == 'q':
            exit(0)


# Tk Window
root = tk.Tk()
root.attributes("-fullscreen", True)
lbl = ImageLabel(root)
lbl.grid(column=0, row=0, padx= 150, pady=150)
lbl.load("eva-display-module/eva-expressions.gif")
root.bind('<Key>', lbl.key_press)


# # Opening of EVA (Can be commented)
# from vlc import *
# media_player = MediaPlayer()
# media = Media("eva-abertura-logo.mp4")
# media_player.set_media(media)
# media_player.toggle_fullscreen()
# media_player.play()
# time.sleep(0.1) # Time to start the video using VLC
# while media_player.is_playing():
#             time.sleep(.1)



# MQTT
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    # Reconnect then subscriptions will be renewed.
    client.subscribe(topic=[(topic_base + '/evaEmotion', 1), ])
    print("Display Module - Connected.")
    

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic == topic_base + '/evaEmotion':
        client.publish(topic_base + '/syslog', "EVA's facial expression: " + msg.payload.decode()) 
        if msg.payload.decode() == "NEUTRAL":
            lbl.targetstate = "neutral"
        elif msg.payload.decode() == "HAPPY":
            lbl.targetstate = "happy"
        elif msg.payload.decode() == "ANGRY":
            lbl.targetstate = "angry"
        elif msg.payload.decode() == "SAD":
            lbl.targetstate = "sad"
        elif msg.payload.decode() == "FEAR":
            lbl.targetstate = "fear"
        elif msg.payload.decode() == "SURPRISE":
            lbl.targetstate = "surprise"
        elif msg.payload.decode() == "DISGUST":
            lbl.targetstate = "disgust"
        elif msg.payload.decode() == "INLOVE":
            lbl.targetstate = "inlove"
        elif msg.payload.decode() == "BLINK":
            lbl.targetstate = "blink"

            
# Run the MQTT client thread.
client = mqtt_client.Client()
client.on_connect = on_connect
client.on_message = on_message
try:
    client.connect(broker, port)
except:
    print ("Unable to connect to Broker.")
    exit(1)

# You cannot use the "forever" method (as in other modules) because it blocks not allowing
# for the graphical interface thread loop to execute.
client.loop_start()


# Executes the graphical interface thread.
root.mainloop()
