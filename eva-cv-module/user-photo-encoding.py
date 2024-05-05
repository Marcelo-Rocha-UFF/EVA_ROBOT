from datetime import datetime
import time

import sys
sys.path.append('/home/pi/EVA_ROBOT')

from picamera.array import PiRGBArray
from picamera import PiCamera

import cv2
import numpy as np

import face_recognition as fr

# Codifica a foto epecificada no diretŕotio corrente gerando uma cópia para o diretório users. 
# formato: python3 user-photo-encoding.py luiza.jpg 
# A foto copiada para a pasta users terá o seguinte formato: nome_do_arquivo_original_data_hora.jpg
# O array Numpy tera o mesmo nome, porém com outra extensão.

# Codifica a foto capturada da imagem da câmera, em real time.
# Os nomes dos arquivos seguem o mesmo padrão da explicação anterior. 
# formato: python3 user-photo-encoding.py marcelo.jpg -v

# Inicializa a câmera.
camera = PiCamera()

# Tempo necessário para a câmera inicializar.
time.sleep(0.1)
print("The camera was initialized.")


if len(sys.argv) == 1:
    print("The -v flag or file name is missing!")

elif (len(sys.argv) == 2) & (sys.argv[1] != '-v'): # Obtém a imagem a partir do arquivo.
    file_name = sys.argv[1]
    print("Importing the image file: ", file_name)
    user_photo = fr.load_image_file(file_name)
    user_photo = cv2.cvtColor(user_photo, cv2.COLOR_BGR2RGB)
    print('The image was imported!')
    print("Encoding the image: ", file_name)
    user_photo_encoded = fr.face_encodings(user_photo)[0] # Um array numpy.
    now = datetime.now()
    only_name = file_name.split('.')[0] # Pega somente o nome do arquivo.
    only_type = file_name.split('.')[1] # Pega somente a extensão (o tipo).
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

elif len(sys.argv) == 3: # Obtém a imagem da câmera.
    print("flag -v activated!")
    camera.resolution = (800, 800)
    camera.framerate = 10
    rawCapture = PiRGBArray(camera, size=(800, 800)) # 
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
        # A tecla 'q' quebra o loop.
        if key == ord("q"):
            break
        elif key == ord("s"): # Salva a foto e o vetor na pasta users.
            print("Saving the photo...")
            image = cv2.resize(image, (400, 400))
            file_name = sys.argv[1]
            print("Encoding an image: ", file_name)
            user_photo_encoded = fr.face_encodings(image)[0] # Um array numpy.
            now = datetime.now()
            only_name = file_name.split('.')[0] # Pega somente o nome do arquivo.
            only_type = file_name.split('.')[1] # Pega somente a extensão (o tipo).
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

