import cv2
import numpy as np
import imutils
import pandas as pd
from datetime import datetime

cap = cv2.VideoCapture('video/carros.mp4')

fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
car_counter = 0

centers= []
dx = 0
diccionario = dict()
while True:

    ret, frame = cap.read()
    if ret == False: break
    frame = imutils.resize(frame, width=640)
    # Especificamos los puntos extremos del área a analizar
    area_pts = np.array([[0, 0], [frame.shape[1]-80, 0], [frame.shape[1]-80, 640], [0, 640]])
    # Con ayuda de una imagen auxiliar, determinamos el área
    # sobre la cual actuará el detector de movimiento
    imAux = np.zeros(shape=(frame.shape[:2]), dtype=np.uint8)
    imAux = cv2.drawContours(imAux, [area_pts], -1, (255), -1)
    image_area = cv2.bitwise_and(frame, frame, mask=imAux)

    # Obtendremos la imagen binaria donde la región en blanco representa
    # la existencia de movimiento
    fgmask = fgbg.apply(image_area)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
    fgmask = cv2.dilate(fgmask, None, iterations=5)

    # Encontramos los contornos presentes de fgmask, para luego basándonos
    # en su área poder determinar si existe movimiento (autos)
    cnts = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    # print(len(cnts))
    # print(cnts)
    for cnt in cnts:
        if cv2.contourArea(cnt) > 1000:
            #today = date.now()
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,255), 1)
            center_x = (x+w)/2
            centers.append(center_x)
            if len(centers) > 2:
                dx  = centers[len(centers)-2]-centers[len(centers)-1]

            # Si el auto ha cruzado entre 440 y 460 abierto, se incrementará
            # en 1 el contador de autos
            if (300 < (x + w) < 320):
                car_counter = car_counter + 1
                cv2.line(frame, (310, 0), (310, 640), (0, 255, 0), 3)
                diccionario[datetime.now().strftime("%d-%m-%Y %H:%M:%S")] = car_counter

            #elif (300 < (x + w) < 320):
            #    car_counter = car_counter - 1
            #    cv2.line(frame, (310, 0), (310, 640), (0, 255, 0), 3)
            dataset = pd.DataFrame()
            dataset["ID"] = np.arange(len(diccionario))
            dataset["Datetime"] = diccionario.keys()
            dataset["Aforo"] = diccionario.values()
            dataset["Oficina"] = 123
            
            # Visualización del conteo de autos
            dataset.to_csv("datasets/real_time.csv",index=None)
    
    cv2.drawContours(frame, [area_pts], -1, (255, 0, 255), 2)
    cv2.line(frame, (310, 0), (310, 640), (0, 255, 255), 1)
    cv2.rectangle(frame, (frame.shape[1]-70, 215), (frame.shape[1]-5, 270), (0, 255, 0), 2)
    cv2.putText(frame, str(car_counter), (frame.shape[1]-55, 250),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,0), 2)
    cv2.imshow('frame', frame)

    
    k = cv2.waitKey(70) & 0xFF
    if k ==27:
        break

cap.release()
cv2.destroyAllWindows()
print(diccionario)