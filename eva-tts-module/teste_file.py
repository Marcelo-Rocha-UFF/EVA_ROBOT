import os

import sys
sys.path.append('/home/pi/EVA_ROBOT')

import config

file_size = os.path.getsize("eva-tts-module/tts_cache_files/_audio_en-US_MichaelExpressive77a89cadba7b9778d80c9178b80947f8.mp3")

print("File size: ", file_size)