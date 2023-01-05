import cv2 as cv
import numpy as np
import mediapipe as mp
import pyautogui
import PIL
from PIL import Image 
from os import remove
import math
import time


################# DEFINICIONES GLOBALES ########################
ancho_pantalla, alto_pantalla = pyautogui.size()


################################################################




################# COORDENADAS MEDIAPIPE ########################
    #coordenadas ojos en malla
OJO_IZQUIERDO =[362,382,381,380,374,373,390,249,263,466,388,387,386,385,384,398]
OJO_DERECHO =[33,7,163,144,145,153,154,155,133,173,157,158,159,160,161,246]

    #coordenadas iris en malla
IRIS_IZQUIERDO = [474,475,476,477]
IRIS_DERECHO = [469,470,471,472]
################################################################





###################### MEDIAPIPE ###############################
#objeto de malla de mediapipe
MALLA_FACIAL = mp.solutions.face_mesh

################################################################






################### FUNCIONES ##################################
#OBTIENE LA RAZON DE PROPORCIONALIDAD
def RazonDeProporcionalidad(ancho_frame):

    r = (ancho_pantalla/ancho_frame)*2

    return r

#LECTURA DE VIDEO
def lecturaVideo(cap):
    
    ret, frame = cap.read()
    frame = cv.flip(frame, 1)

    return ret, frame

#DIBUJAR LINEAS
def dibujar(mesh_points, frame, CENTRO_IZQUIERDO,CENTRO_DERECHO,l_radius):

    #lineas ojos
    cv.polylines(frame, [mesh_points[OJO_IZQUIERDO]], True, (0,0,255),1,cv.LINE_AA)
    cv.polylines(frame, [mesh_points[OJO_DERECHO]], True, (0,0,255),1,cv.LINE_AA)
    
    #dibujo circulo iris
    cv.circle(frame, CENTRO_IZQUIERDO, int(l_radius),(255,0,255),1,cv.LINE_AA)
    cv.circle(frame, CENTRO_DERECHO, int(l_radius),(255,0,255),1,cv.LINE_AA)
    cv.circle(frame, CENTRO_DERECHO,1,(0,255,0),1,cv.LINE_AA)
    cv.circle(frame, CENTRO_IZQUIERDO,1,(0,255,0),1,cv.LINE_AA)
    
def calcular_rectangulo_interior(ancho,alto):   

     X1 = int(ancho / 3)
     X2 = int(X1 * 2)
     Y1 = int(alto / 3)
     Y2 = int(Y1 * 2)
     
     return X1,X2,Y1,Y2

def pestañeo(coordinates_left_eye):

    distancia= math.sqrt((coordinates_left_eye[12][0]-coordinates_left_eye[4][0])**2 + (coordinates_left_eye[12][1]-coordinates_left_eye[4][1])**2)
    
    return distancia

def calcular_centro_pantalla():
   
    x = int(ancho_pantalla/2)
    y = int(alto_pantalla/2)

    return x,y

def centros_ojos(mesh_points):
   
    #circulos iris
    (l_cx, l_cy), l_radius =cv.minEnclosingCircle(mesh_points[IRIS_IZQUIERDO])
    (r_cx, r_cy), r_radius =cv.minEnclosingCircle(mesh_points[IRIS_DERECHO])

    #coordenadas centro de iris
    CENTRO_IZQUIERDO= np.array([l_cx, l_cy], dtype = np.int32)
    CENTRO_DERECHO= np.array([r_cx, r_cy], dtype = np.int32)

    return CENTRO_IZQUIERDO,CENTRO_DERECHO, l_radius

def calcular_vector(centro_izquierda_aux, centro_izquierda):
    
    vectorX = centro_izquierda[0] - centro_izquierda_aux[0]
    vectorY = centro_izquierda[1] - centro_izquierda_aux[1]


    return vectorX,vectorY

def distancia_Entre_ojos(centro_izquierda,centro_derecha):

    centro_Ojos = math.sqrt((centro_izquierda[0]-centro_derecha[0])**2 + (centro_izquierda[1]-centro_derecha[1])**2)
    print(centro_Ojos)
    return centro_Ojos


def punto_medio(punto1, punto2):

    result1 = (punto1[0]+punto2[0])/2
    result2 = (punto1[1]+punto2[1])/2    

    return result1, result2
################################################################

# puntos facemesh para rectangulo
# 285 y 261


def eye_aspect_ratio(coordinates):
     d_A = np.linalg.norm(np.array(coordinates[1]) - np.array(coordinates[5]))
     d_B = np.linalg.norm(np.array(coordinates[2]) - np.array(coordinates[4]))
     d_C = np.linalg.norm(np.array(coordinates[0]) - np.array(coordinates[3]))
     return (d_A + d_B) / (2 * d_C)




def drawing_output(frame, coordinates_left_eye, coordinates_right_eye, blink_counter):
     aux_image = np.zeros(frame.shape, np.uint8)
     contours1 = np.array([coordinates_left_eye])
     contours2 = np.array([coordinates_right_eye])
     cv.fillPoly(aux_image, pts=[contours1], color=(255, 0, 0))
     cv.fillPoly(aux_image, pts=[contours2], color=(255, 0, 0))
     output = cv.addWeighted(frame, 1, aux_image, 0.7, 1)
     cv.rectangle(output, (0, 0), (200, 50), (255, 0, 0), -1)
     cv.rectangle(output, (202, 0), (265, 50), (255, 0, 0),2)
     cv.putText(output, "Num. Parpadeos:", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
     cv.putText(output, "{}".format(blink_counter), (220, 35), cv.FONT_HERSHEY_SIMPLEX, 0.9, (128, 0, 250), 2)
     
     return output



def calcular_distancia(coordinates_left_eye, coordinates_right_eye):

    distancia_izquierda = math.sqrt((coordinates_left_eye[12][0]-coordinates_left_eye[4][0])**2 + (coordinates_left_eye[12][1]-coordinates_left_eye[4][1])**2)
    distancia_derecha = math.sqrt((coordinates_right_eye[12][0]-coordinates_right_eye[4][0])**2 + (coordinates_right_eye[12][1]-coordinates_right_eye[4][1])**2)
    return distancia_izquierda, distancia_derecha


def calcular_distancia2(coordenadas1, coordenadas2):
    resultado =  math.sqrt((coordenadas2[0]-coordenadas1[0])**2 + (coordenadas2[1]-coordenadas1[1])**2)
    return resultado


