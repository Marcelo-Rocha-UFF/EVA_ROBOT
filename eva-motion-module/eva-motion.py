# Software developed by Marcelo Marques da Rocha
# MidiaCom Laboratory - Universidade Federal Fluminense
# This work was funded by CAPES and Google Research

import serial

from paho.mqtt import client as mqtt_client

import sys
sys.path.append('/home/pi/EVA_ROBOT')
import config # Module with network device configurations.

broker = config.MQTT_BROKER_ADRESS # Broker address.
port = config.MQTT_PORT # Broker Port.
topic_base = config.EVA_TOPIC_BASE

EVA_SERIAL_PORT = config.EVA_SERIAL_PORT # Name of the Arduino serial port that controls the EVA servomotors.
BAUD_RATE = config.BAUD_RATE # Serial transmission speed.

EVA_arduino_serial_obj = serial.Serial(EVA_SERIAL_PORT, BAUD_RATE)


# MQTT
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    # Reconnect then subscriptions will be renewed.
    client.subscribe(topic=[(topic_base + '/motion/head', 1), ])
    client.subscribe(topic=[(topic_base + '/motion/arm/left', 1), ])
    client.subscribe(topic=[(topic_base + '/motion/arm/right', 1), ])
    print("Motion Module - Connected.")



# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if msg.topic == topic_base + '/motion/head':
        client.publish(topic_base + '/syslog', 'Moving the head: ' + msg.payload.decode())
        # Keeping compatibility with the old version.
        if msg.payload.decode() == "CENTER":
            EVA_arduino_serial_obj.write("c".encode())
        elif msg.payload.decode() == "RIGHT":
            EVA_arduino_serial_obj.write("r".encode())
        elif msg.payload.decode() == "2RIGHT":
            EVA_arduino_serial_obj.write("R".encode())
        elif msg.payload.decode() == "LEFT":
            EVA_arduino_serial_obj.write("l".encode())
        elif msg.payload.decode() == "2LEFT":
            EVA_arduino_serial_obj.write("L".encode())
        elif msg.payload.decode() == "UP":
            EVA_arduino_serial_obj.write("u".encode())
        elif msg.payload.decode() == "2UP":
            EVA_arduino_serial_obj.write("U".encode())
        elif msg.payload.decode() == "DOWN":
            EVA_arduino_serial_obj.write("d".encode())
        elif msg.payload.decode() == "2DOWN":
            EVA_arduino_serial_obj.write("D".encode())
        elif msg.payload.decode() == "NO":
            EVA_arduino_serial_obj.write("s".encode())
        elif msg.payload.decode() == "2NO":
            EVA_arduino_serial_obj.write("S".encode())
        elif msg.payload.decode() == "YES":
            EVA_arduino_serial_obj.write("n".encode())
        elif msg.payload.decode() == "2YES":
            EVA_arduino_serial_obj.write("N".encode())
        elif msg.payload.decode() == "UP_LEFT":
            EVA_arduino_serial_obj.write("q".encode())
        elif msg.payload.decode() == "2UP_LEFT":
            EVA_arduino_serial_obj.write("Q".encode())
        elif msg.payload.decode() == "UP_RIGHT":
            EVA_arduino_serial_obj.write("e".encode())
        elif msg.payload.decode() == "2UP_RIGHT":
            EVA_arduino_serial_obj.write("E".encode())
        elif msg.payload.decode() == "DOWN_RIGHT":
            EVA_arduino_serial_obj.write("x".encode())
        elif msg.payload.decode() == "2DOWN_RIGHT":
            EVA_arduino_serial_obj.write("X".encode())
        elif msg.payload.decode() == "DOWN_LEFT":
            EVA_arduino_serial_obj.write("z".encode())
        elif msg.payload.decode() == "2DOWN_LEFT":
            EVA_arduino_serial_obj.write("Z".encode())
        # Using the new version of head movement protocol.
        elif msg.payload.decode() == "UP1":
            EVA_arduino_serial_obj.write("hu1".encode())
        elif msg.payload.decode() == "UP2":
            EVA_arduino_serial_obj.write("hu2".encode())
        elif msg.payload.decode() == "DOWN1":
            EVA_arduino_serial_obj.write("hd1".encode())
        elif msg.payload.decode() == "DOWN2":
            EVA_arduino_serial_obj.write("hd2".encode())

        elif msg.payload.decode() == "LEFT1":
            EVA_arduino_serial_obj.write("hl1".encode())
        elif msg.payload.decode() == "LEFT2":
            EVA_arduino_serial_obj.write("hl2".encode())
        elif msg.payload.decode() == "LEFT3":
            EVA_arduino_serial_obj.write("hl3".encode())
        elif msg.payload.decode() == "RIGHT1":
            EVA_arduino_serial_obj.write("hr1".encode())
        elif msg.payload.decode() == "RIGHT2":
            EVA_arduino_serial_obj.write("hr2".encode())
        elif msg.payload.decode() == "RIGHT3":
            EVA_arduino_serial_obj.write("hr3".encode())

        elif msg.payload.decode() == "LEFT_UP1":
            EVA_arduino_serial_obj.write("h11".encode())
        elif msg.payload.decode() == "LEFT_UP2":
            EVA_arduino_serial_obj.write("h12".encode())
        elif msg.payload.decode() == "LEFT_UP3":
            EVA_arduino_serial_obj.write("h13".encode())
        elif msg.payload.decode() == "RIGHT_UP1":
            EVA_arduino_serial_obj.write("h21".encode())
        elif msg.payload.decode() == "RIGHT_UP2":
            EVA_arduino_serial_obj.write("h22".encode())
        elif msg.payload.decode() == "RIGHT_UP3":
            EVA_arduino_serial_obj.write("h23".encode())
        elif msg.payload.decode() == "LEFT_DOWN1":
            EVA_arduino_serial_obj.write("h41".encode())
        elif msg.payload.decode() == "LEFT_DOWN2":
            EVA_arduino_serial_obj.write("h42".encode())
        elif msg.payload.decode() == "LEFT_DOWN3":
            EVA_arduino_serial_obj.write("h43".encode())
        elif msg.payload.decode() == "RIGHT_DOWN1":
            EVA_arduino_serial_obj.write("h31".encode())
        elif msg.payload.decode() == "RIGHT_DOWN2":
            EVA_arduino_serial_obj.write("h32".encode())
        elif msg.payload.decode() == "RIGHT_DOWN3":
            EVA_arduino_serial_obj.write("h33".encode())

        elif msg.payload.decode() == "CENTER_X":
            EVA_arduino_serial_obj.write("hcx".encode())
        elif msg.payload.decode() == "CENTER_Y":
            EVA_arduino_serial_obj.write("hcy".encode())

    # Movements of the robot's arms.
    if msg.topic == topic_base + '/motion/arm/left':
        client.publish(topic_base + '/syslog', 'Moving the left arm: ' + msg.payload.decode())
        if msg.payload.decode() == "UP":
            EVA_arduino_serial_obj.write("alu".encode())
        elif msg.payload.decode() == "DOWN":
            EVA_arduino_serial_obj.write("ald".encode())
        elif msg.payload.decode() == "POSITION 0":
            EVA_arduino_serial_obj.write("al0".encode())
        elif msg.payload.decode() == "POSITION 1":
            EVA_arduino_serial_obj.write("al1".encode())
        elif msg.payload.decode() == "POSITION 2":
            EVA_arduino_serial_obj.write("al2".encode())
        elif msg.payload.decode() == "POSITION 3":
            EVA_arduino_serial_obj.write("al3".encode())
        elif msg.payload.decode() == "SHAKE1":
            EVA_arduino_serial_obj.write("als".encode())
        elif msg.payload.decode() == "SHAKE2":
            EVA_arduino_serial_obj.write("alS".encode())

    if msg.topic == topic_base + '/motion/arm/right':
        client.publish(topic_base + '/syslog', 'Moving the right arm: ' + msg.payload.decode())
        if msg.payload.decode() == "UP":
            EVA_arduino_serial_obj.write("aru".encode())
        elif msg.payload.decode() == "DOWN":
            EVA_arduino_serial_obj.write("ard".encode())
        elif msg.payload.decode() == "POSITION 0":
            EVA_arduino_serial_obj.write("ar0".encode())
        elif msg.payload.decode() == "POSITION 1":
            EVA_arduino_serial_obj.write("ar1".encode())
        elif msg.payload.decode() == "POSITION 2":
            EVA_arduino_serial_obj.write("ar2".encode())
        elif msg.payload.decode() == "POSITION 3":
            EVA_arduino_serial_obj.write("ar3".encode())
        elif msg.payload.decode() == "SHAKE1":
            EVA_arduino_serial_obj.write("ars".encode())
        elif msg.payload.decode() == "SHAKE2":
            EVA_arduino_serial_obj.write("arS".encode())


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
