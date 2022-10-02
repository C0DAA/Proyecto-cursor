import cv2 as cv
import numpy as np
import mediapipe as mp
import autopy
from PIL import Image 
 
anchopanta, altopanta = autopy.screen.size()

MALLA_FACIAL = mp.solutions.face_mesh # objeto de mediapipe

#coordenadas ojos en malla
OJO_IZQUIERDO =[362,382,381,380,374,373,390,249,263,466,388,387,386,385,384,398]
OJO_DERECHO =[33,7,163,144,145,153,154,155,133,173,157,158,159,160,161,246]

#coordenadas iris en malla
IRIS_IZQUIERDO = [474,475,476,477]
IRIS_DERECHO = [469,470,471,472]

#captura de video
cap = cv.VideoCapture(0)

#objeto facemesh
with MALLA_FACIAL.FaceMesh(
    max_num_faces= 1,
    refine_landmarks=True,
    min_detection_confidence = 0.5,
    min_tracking_confidence=0.5
) as face_mesh:

    #lectura de video
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        #escala de grises para mediapipe
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        #cv.imshow('escala de grises', rgb_frame) #mostrar escala de gris para 
        
        img_h, img_w = frame.shape[:2]
        results = face_mesh.process(rgb_frame)
       
       
        ## recortar frame en parte del ojo 

       # rows,cols, _ = frame.shape

       # cut_image = frame[240: 480, 320: 640]
        
       # cv.imshow('foto cortada', cut_image)


        #DIBUJO DE LINEAS
        if results.multi_face_landmarks:
            #print(results.multi_face_landmarks[0].landmark) #muestra coordenadas de los landmarks
            mesh_points= np.array([np.multiply([p.x, p.y], [img_w, img_h]).astype(int) for p in results.multi_face_landmarks[0].landmark])
            #print(mesh_points.shape)
           
            #circulos iris
            (l_cx, l_cy), l_radius =cv.minEnclosingCircle(mesh_points[IRIS_IZQUIERDO])
            (r_cx, r_cy), r_radius =cv.minEnclosingCircle(mesh_points[IRIS_DERECHO])
    
            #coordenadas centro de iris
            CENTRO_IZQUIERDO= np.array([l_cx, l_cy], dtype = np.int32)
            CENTRO_DERECHO= np.array([r_cx, r_cy], dtype = np.int32)

            #control de mouse con coordenadas de centro del ojo IZQUIERDO
            #autopy.mouse.move(anchopanta - l_cx,l_cy)
 
            #dibujo circulo iris
            cv.circle(frame, CENTRO_IZQUIERDO, int(l_radius),(255,0,255),1,cv.LINE_AA)
            cv.circle(frame, CENTRO_DERECHO, int(l_radius),(255,0,255),1,cv.LINE_AA)
            cv.circle(frame, CENTRO_DERECHO,1,(255,0,255),1,cv.LINE_AA)
            cv.circle(frame, CENTRO_IZQUIERDO,1,(255,0,255),1,cv.LINE_AA)
           
           

            #lineas ojos
            cv.polylines(frame, [mesh_points[OJO_IZQUIERDO]], True, (0,0,255),1,cv.LINE_AA)
            cv.polylines(frame, [mesh_points[OJO_DERECHO]], True, (0,0,255),1,cv.LINE_AA)


            #print("IZQUIERDO: ",mesh_points[OJO_IZQUIERDO[0]] , " , ", mesh_points[OJO_IZQUIERDO[15]])
            #print("derecho: ",mesh_points[OJO_DERECHO[0]] , " , ", mesh_points[OJO_DERECHO[15]])
        cv.imshow('control', frame) 
        key = cv.waitKey(1)
        if key == ord('q'):
            break

cap.release()
cv.destroyAllWindows()
