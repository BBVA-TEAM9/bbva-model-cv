import cv2
import numpy as np
import math
import imutils
#import pandas as pd
#from datetime import datetime
from object_detection import ObjectDetection

# Initialize Object Detection
od = ObjectDetection()

cap = cv2.VideoCapture(0)

#cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

#fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
#kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))


car_counter = 0
center_point_hist = {}
frame_id = 0

while True:
    frame_id += 1
    ret, frame = cap.read()
    print(frame.shape)
    if ret == False: break

    (class_ids, scores, cnts) = od.detect(frame)
    print((class_ids, scores, cnts))
    #frame = imutils.resize(frame, width=640)
    # Especificamos los puntos extremos del área a analizar
    area_pts = np.array([[0, 0], [frame.shape[1], 0], [frame.shape[1], 640], [0, 640]])
    # Con ayuda de una imagen auxiliar, determinamos el área
    # sobre la cual actuará el detector de movimiento
    #imAux = np.zeros(shape=(frame.shape[:2]), dtype=np.uint8)
    #imAux = cv2.drawContours(imAux, [area_pts], -1, (255), -1)
    #image_area = cv2.bitwise_and(frame, frame, mask=imAux)

    
    # Obtendremos la imagen binaria donde la región en blanco representa
    # la existencia de movimiento
    #fgmask = fgbg.apply(image_area)
    #fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    #fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
    #fgmask = cv2.dilate(fgmask, None, iterations=5)

    # Encontramos los contornos presentes de fgmask, para luego basándonos
    # en su área poder determinar si existe movimiento (autos)
    #cnts = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    # print(len(cnts))
    # print(cnts)
    center_point_cur_frame = []
    for cnt in cnts:
        
        (x, y, w, h) = cnt
        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,255), 1)
        center_x = int((x+x+w)/2)
        center_y = int((y+y+h)/2)
        center_point_cur_frame.append((center_x,center_y))
        # Si el auto ha cruzado entre 440 y 460 abierto, se incrementará
        # en 1 el contador de autos
        if (250 < (x + w) < 320) & (frame_id>=3) & (0 in list(class_ids)):
            for pt_act in center_point_hist[frame_id-1]:
                if (math.hypot(pt_act[0]-center_x,pt_act[1]-center_y)<25) & (pt_act[0]-center_x>0):
                    car_counter += 1
                elif (math.hypot(pt_act[0]-center_x,pt_act[1]-center_y)<25) & (pt_act[0]-center_x<0):
                    car_counter -= 1
    
                #diccionario[datetime.now().strftime("%d-%m-%Y %H:%M:%S")] = car_counter
    
    center_point_hist[frame_id] = center_point_cur_frame
            #elif (300 < (x + w) < 320):
            #    car_counter = car_counter - 1
            #    cv2.line(frame, (310, 0), (310, 640), (0, 255, 0), 3)
            #dataset = pd.DataFrame()
            #dataset["ID"] = np.arange(len(diccionario))
            #dataset["Datetime"] = diccionario.keys()
            #dataset["Aforo"] = diccionario.values()
            #dataset["Oficina"] = 123
            
            # Visualización del conteo de autos
            #dataset.to_csv("datasets/real_time.csv",index=None)
    
    cv2.drawContours(frame, [area_pts], -1, (255, 0, 255), 2)
    cv2.line(frame, (310, 0), (310, 640), (0, 0, 255), 1)
    cv2.rectangle(frame, (frame.shape[1]-70, 215), (frame.shape[1]-5, 270), (0, 255, 0), 2)
    cv2.putText(frame, str(car_counter), (frame.shape[1]-55, 250),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0,255), 2)
    cv2.imshow('frame', frame)
    
    #if frame_id % 180 == 0:


    
    k = cv2.waitKey(70) & 0xFF
    if k ==27:
        break

cap.release()
cv2.destroyAllWindows()
