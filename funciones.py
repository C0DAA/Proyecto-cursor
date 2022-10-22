import cv2 as cv
import numpy as np
import mediapipe as mp
import pyautogui
import PIL
from PIL import Image 
from os import remove

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
def RazonDeProporcionalidad():
    
    ancho_frame, alto_frame = obtenerTamañoFrame()
    ancho_pantalla, alto_pantalla = pyautogui.size()

    r = (ancho_pantalla/ancho_frame)+0.1

    return r


#OBTIENE EL TAMAÑO DE FRAME DE CAMARA
def obtenerTamañoFrame():
    respuesta = []
    cap = cv.VideoCapture(0)
    ret, frame = cap.read()
    frame = cv.flip(frame, 1)

    total_frames = cap.get(1)
    cv.imwrite("/Users/coda/Documents/universidad/pruebas proyecto/controlVisual/foto.jpg", frame)
    img = PIL.Image.open("/Users/coda/Documents/universidad/pruebas proyecto/controlVisual/foto.jpg")
    ancho, alto = img.size
    respuesta.append(ancho)
    respuesta.append(alto)
    remove("/Users/coda/Documents/universidad/pruebas proyecto/controlVisual/foto.jpg")
    
    return respuesta


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
    
################################################################