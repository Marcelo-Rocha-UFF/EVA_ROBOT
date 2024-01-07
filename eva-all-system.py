import subprocess
import os
import threading

print("1- Running Text-To-Speech (TTS) module")
subprocess.Popen(["python3", "eva-tts-module/eva-tts.py"])

print("2- Running Leds module")
subprocess.Popen(["python3", "eva-leds-module/eva-leds.py"])

print("3- Running Light module")
subprocess.Popen(["python3", "eva-light-module/eva-light.py"])

print("4- Running Audio module")
subprocess.Popen(["python3", "eva-audio-module/eva-audio.py"])

print("5- Running Motion module")
subprocess.Popen(["python3", "eva-motion-module/eva-motion.py"])

# print("6- Running Speech-To-Text (STT) module")
# subprocess.Popen(["python3", "eva-stt-module/eva-stt.py"])

print("7- Running Display module")
subprocess.Popen(["python3", "eva-display-module/eva-display.py"])




