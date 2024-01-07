import serial
import time

from paho.mqtt import client as mqtt_client

import sys
sys.path.append('/home/pi/EVA_ROBOT')
import config # Modulo com as configurações dos dispositivos de rede

broker = config.MQTT_BROKER_ADRESS # broker adress
port = config.MQTT_PORT # broker port
topic_base = config.EVA_TOPIC_BASE

EVA_SERIAL_PORT = config.EVA_SERIAL_PORT
BAUD_RATE = config.BAUD_RATE



EVA_head_serial = serial.Serial(EVA_SERIAL_PORT, BAUD_RATE)

time.sleep(7) # waiting for serial board intializing process

# MQTT
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    #print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
    client.subscribe(topic=[(topic_base + '/motion', 1), ])
    print("Motion module CONNECTED.")



# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic == topic_base + '/motion':
        client.publish(topic_base + '/log', 'Moving the head: ' + msg.payload.decode())
        if msg.payload.decode() == "CENTER":
            EVA_head_serial.write("c".encode())
        elif msg.payload.decode() == "RIGHT":
            EVA_head_serial.write("r".encode())
        elif msg.payload.decode() == "2RIGHT":
            EVA_head_serial.write("R".encode())
        elif msg.payload.decode() == "LEFT":
            EVA_head_serial.write("l".encode())
        elif msg.payload.decode() == "2LEFT":
            EVA_head_serial.write("L".encode())
        elif msg.payload.decode() == "UP":
            EVA_head_serial.write("u".encode())
        elif msg.payload.decode() == "2UP":
            EVA_head_serial.write("U".encode())
        elif msg.payload.decode() == "DOWN":
            EVA_head_serial.write("d".encode())
        elif msg.payload.decode() == "2DOWN":
            EVA_head_serial.write("D".encode())
        elif msg.payload.decode() == "NO":
            EVA_head_serial.write("s".encode())
        elif msg.payload.decode() == "YES":
            EVA_head_serial.write("n".encode())
        elif msg.payload.decode() == "UP_LEFT":
            EVA_head_serial.write("q".encode())
        elif msg.payload.decode() == "2UP_LEFT":
            EVA_head_serial.write("Q".encode())
        elif msg.payload.decode() == "UP_RIGHT":
            EVA_head_serial.write("e".encode())
        elif msg.payload.decode() == "2UP_RIGHT":
            EVA_head_serial.write("E".encode())
        elif msg.payload.decode() == "DOWN_RIGHT":
            EVA_head_serial.write("x".encode())
        elif msg.payload.decode() == "2DOWN_RIGHT":
            EVA_head_serial.write("X".encode())
        elif msg.payload.decode() == "DOWN_LEFT":
            EVA_head_serial.write("z".encode())
        elif msg.payload.decode() == "2DOWN_LEFT":
            EVA_head_serial.write("Z".encode())


client = mqtt_client.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port)


client.loop_forever()
