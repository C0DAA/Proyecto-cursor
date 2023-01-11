import cv2 as cv
import numpy as np
import mediapipe as mp
import pyautogui
import math
import matplotlib.pyplot as plt
from collections import deque

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


def lecturaVideo(cap):
    
    ret, frame = cap.read()
    frame = cv.flip(frame, 1)

    return ret, frame


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


def punto_medio(punto1, punto2):

    result1 = (punto1[0]+punto2[0])/2
    result2 = (punto1[1]+punto2[1])/2    

    return result1, result2


def calcular_distancia(coordinates_left_eye, coordinates_right_eye):

    distancia_izquierda = math.sqrt((coordinates_left_eye[12][0]-coordinates_left_eye[4][0])**2 + (coordinates_left_eye[12][1]-coordinates_left_eye[4][1])**2)
    distancia_derecha = math.sqrt((coordinates_right_eye[12][0]-coordinates_right_eye[4][0])**2 + (coordinates_right_eye[12][1]-coordinates_right_eye[4][1])**2)
    return distancia_izquierda, distancia_derecha


def calcular_distancia2(coordenadas1, coordenadas2):
    resultado =  math.sqrt((coordenadas2[0]-coordenadas1[0])**2 + (coordenadas2[1]-coordenadas1[1])**2)
    return resultado


def plotting_ear(pts_ear, line1):
    global figure
    pts = np.linspace(0,1,64)
    if line1 == []:
        plt.style.use("ggplot")
        plt.ion()

        figure, ax = plt.subplots()
        line1, = ax.plot(pts,pts_ear)
        plt.ylim(1, 50)
        plt.xlim(0, 1)
        plt.ylabel("distancia en pixeles",fontsize = 16)
        plt.xlabel("tiempo en seg", fontsize = 16)
    else:
        line1.set_ydata(pts_ear)
        figure.canvas.draw()
        figure.canvas.flush_events()

    return line1
