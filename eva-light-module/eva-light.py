# De vez em quando, parece que a lâmpada se desconecta e não responde a um comando, falhando...
# Só respondendo ao comando seguinte...

import socket
from paho.mqtt import client as mqtt_client
import time

import sys
sys.path.append('/home/pi/EVA_ROBOT')
import config # Módulo com as configurações dos dispositivos de rede.

broker = config.MQTT_BROKER_ADRESS # Endereço do Broker.
port = config.MQTT_PORT # Porta do Broker.
topic_base = config.EVA_TOPIC_BASE

SMARTBULB_IP = config.SMART_BULB_IP_ADRESS
SMARTBULB_PORT = config.SMART_BULB_PORT

COLOR_TABLE = {
    "RED"   : "FF0000",
    "GREEN" : "00FF00",
    "BLUE"  : "0000FF",
    "YELLOW": "FFFF00",
    "PINK"  : "FF00FF",
    "WHITE" : "FFFFFF",
    "BLACK" : "000000"
}


# MQTT
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic=[(topic_base + '/light', 1), ])
    print("Smart Bulb Module - Connected.")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    bulb_color = ""
    if msg.topic == topic_base + '/light':
        client.publish(topic_base + '/log', 'Controlling the Smart Bulb (color|state): ' + msg.payload.decode())
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((SMARTBULB_IP, SMARTBULB_PORT))
                print("TCP connection with the Smart Bulb established.")
                color = msg.payload.decode().split("|")[0]
                if color == "": color = "000000"
                state = msg.payload.decode().split("|")[1]

                if color in COLOR_TABLE:
                    bulb_color = str(int(COLOR_TABLE[color], 16))
                else:
                    bulb_color = str(int(color, 16))
                    
                if state == "OFF":
                    # off command
                    s.sendall('{"id":1, "method":"set_power","params":["off", "smooth", 0]}\r\n'.encode())
                elif state == "ON":
                    # on command
                    s.sendall('{"id":1, "method":"set_power","params":["on", "smooth", 0]}\r\n'.encode())
                    time.sleep(0.1) # parece precisar de um tempo para enviar os dois comandos seguidos
                    s.sendall(('{"id":1,"method":"set_rgb","params":[' + bulb_color + ', "smooth", 0]}\r\n').encode())

            except socket.error:
                print ("Unable to connect to Smart Bulb. \nTurn on the device and configure its IP address correctly.")
                
        

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