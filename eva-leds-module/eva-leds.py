#!/usr/bin/env python
# -*- coding: utf-8 -*-

from paho.mqtt import client as mqtt_client

import os
import signal
import subprocess

import sys
sys.path.append('/home/pi/EVA_ROBOT')
import config # Module with network device configurations.

broker = config.MQTT_BROKER_ADRESS # Broker address.
port = config.MQTT_PORT # Broker Port.
topic_base = config.EVA_TOPIC_BASE


p = "" # Variable that stores the subprocess that runs the Martix Voice animation.

# MQTT
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # Reconnect then subscriptions will be renewed.
    client.subscribe(topic=[(topic_base + '/leds', 1), ])
    
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global p # process
    if msg.topic == topic_base + '/leds':
        if msg.payload.decode() != "STOP": # Only prints for commands other than STOP
            client.publish(topic_base + '/log', "Leds Animation: " + msg.payload.decode()) 
        if msg.payload.decode() == "ANGRY": 
            p = subprocess.Popen("eva-leds-module/leds-animation/angry", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        elif msg.payload.decode() == "ANGRY2":
            p = subprocess.Popen("eva-leds-module/leds-animation/angry2", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        elif msg.payload.decode() == "HAPPY":
            p = subprocess.Popen("eva-leds-module/leds-animation/happy", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        elif msg.payload.decode() == "LISTEN":
            p = subprocess.Popen("eva-leds-module/leds-animation/listen", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        elif msg.payload.decode() == "PROCESS":
            p = subprocess.Popen("eva-leds-module/leds-animation/process", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        elif msg.payload.decode() == "RAINBOW":
            p = subprocess.Popen("eva-leds-module/leds-animation/rainbow", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        elif msg.payload.decode() == "SAD":
            p = subprocess.Popen("eva-leds-module/leds-animation/sad", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        elif msg.payload.decode() == "SAD2":
            p = subprocess.call("eva-leds-module/leds-animation/sad2", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        elif msg.payload.decode() == "SURPRISE":
            p = subprocess.Popen("eva-leds-module/leds-animation/surprise", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        elif msg.payload.decode() == "SPEAK":
            p = subprocess.Popen("eva-leds-module/leds-animation/speak", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        elif msg.payload.decode() == "WHITE":
            p = subprocess.Popen("eva-leds-module/leds-animation/white", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        elif msg.payload.decode() == "STOP":
            if p != "":
                os.killpg(os.getpgid(p.pid), signal.SIGTERM)
                os.system("eva-leds-module/leds-animation/stop")

           

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
