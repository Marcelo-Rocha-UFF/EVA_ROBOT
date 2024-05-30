from datetime import datetime
import time

import sys
sys.path.append('/home/pi/EVA_ROBOT')

from picamera.array import PiRGBArray
from picamera import PiCamera

import cv2
import numpy as np

import face_recognition as fr

# Encodes the photo specified in the current directory, generating a copy in the users directory.
# format: python3 user-photo-encoding.py luiza.jpg
# The photo copied to the users folder will have the following format: original_filename_date_time.jpg
# The Numpy array will have the same name, but with a different extension.

# Using the flag -v, you can encode the captured photo from the camera image, in real time.
# The file names follow the same pattern as the previous explanation.
# format: python3 user-photo-encoding.py luiza.jpg -v

# Initialize the camera.
camera = PiCamera()

# Time required for the camera to initialize.
time.sleep(0.1)
print("The camera was initialized.")


if len(sys.argv) == 1:
    print("The -v flag or file name is missing!")

elif (len(sys.argv) == 2) & (sys.argv[1] != '-v'): # Get the image from the file.
    file_name = sys.argv[1]
    print("Importing the image file: ", file_name)
    user_photo = fr.load_image_file(file_name)
    user_photo = cv2.cvtColor(user_photo, cv2.COLOR_BGR2RGB)
    print('The image was imported!')
    print("Encoding the image: ", file_name)
    user_photo_encoded = fr.face_encodings(user_photo)[0] # A numpy array.
    now = datetime.now()
    only_name = file_name.split('.')[0] # Get only the file name.
    only_type = file_name.split('.')[1] # Get only the extension (the type).
    _day = str(now.day)
    _month = str(now.month)
    _year = str(now.year)
    _hour = str(now.hour)
    _minute = str(now.minute)
    _second = str(now.second)
    new_photo_file_name = 'eva-cv-module/users/' + only_name + '_' + _day + '-' + _month + '-' + _year + '-' + _hour + '-' + _minute + '-' + _second + '.' + only_type
    cv2.imwrite(new_photo_file_name, user_photo)
    array_file_name = 'eva-cv-module/users/' + only_name + '_' + _day + '-' + _month + '-' + _year + '-' + _hour + '-' + _minute + '-' + _second + '.' + 'npy'
    np.save(array_file_name, user_photo_encoded)

elif len(sys.argv) == 3: # Get the image from the camera.
    print("flag -v activated!")
    camera.resolution = (800, 800)
    camera.framerate = 10
    rawCapture = PiRGBArray(camera, size=(800, 800)) # 
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
        # The 'q' key breaks the loop.
        if key == ord("q"):
            break
        elif key == ord("s"): # Save the photo and vector in the users folder.
            print("Saving the photo...")
            image = cv2.resize(image, (400, 400))
            file_name = sys.argv[1]
            print("Encoding an image: ", file_name)
            user_photo_encoded = fr.face_encodings(image)[0] # A numpy array.
            now = datetime.now()
            only_name = file_name.split('.')[0] # Get only the file name.
            only_type = file_name.split('.')[1] # Get only the extension (the type).
            _day = str(now.day)
            _month = str(now.month)
            _year = str(now.year)
            _hour = str(now.hour)
            _minute = str(now.minute)
            _second = str(now.second)
            new_photo_file_name = 'eva-cv-module/users/' + only_name + '_' + _day + '-' + _month + '-' + _year + '-' + _hour + '-' + _minute + '-' + _second + '.' + only_type
            cv2.imwrite(new_photo_file_name, image)
            array_file_name = 'eva-cv-module/users/' + only_name + '_' + _day + '-' + _month + '-' + _year + '-' + _hour + '-' + _minute + '-' + _second + '.' + 'npy'
            np.save(array_file_name, user_photo_encoded)
            break
        rawCapture.truncate(0)

