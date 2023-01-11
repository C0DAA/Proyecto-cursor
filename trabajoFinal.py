from funciones import * 


#Variables globales
i = 0
line1 = []
pts_ear = deque(maxlen = 64)
EAR_THRESH = 10
NUM_FRAMES = 2
aux_counter = 0
blink_counter = 0
coordenadas_Nuevas = []
x_aux,y_aux = calcular_centro_pantalla()

#Contador de bucle global
CONTADOR = 1

#Captura de video
cap = cv.VideoCapture(0)

#Objeto facemesh
with MALLA_FACIAL.FaceMesh(
    max_num_faces= 1,
    refine_landmarks=True,
    min_detection_confidence = 0.5,
    min_tracking_confidence=0.5
) as face_mesh:

    #Inicio bucle
    while True:

                                            ###### Bloque 1 ######
        if (CONTADOR == 1):
            
            #Captura del primer frame
            ret,frame = lecturaVideo(cap)
            if not ret:
              break

            #Escala de grises para mediapipe
            rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            img_h, img_w = frame.shape[:2]
            results = face_mesh.process(rgb_frame)
            height, width, _ = frame.shape

            #Razon de proporcionalidad
            r = RazonDeProporcionalidad(img_w)


            if results.multi_face_landmarks:
                    mesh_points= np.array([np.multiply([p.x, p.y], [img_w, img_h]).astype(int) for p in results.multi_face_landmarks[0].landmark])
                    
                    #Se busca el centro de iris
                    CENTRO_IZQUIERDO_AUX,CENTRO_DERECHO_AUX,l_radius= centros_ojos(mesh_points)
                    

                    #listas que seran llenadas con coordenadas
                    coordinates_left_eye = [] 
                    coordinates_right_eye= []
                    coordenadas_iris_izquierdo = []

                    #Captura de coordenadas puntos de ojos
                    for face_landmarks in results.multi_face_landmarks:
                        for index in OJO_IZQUIERDO:
                            x1 = int(face_landmarks.landmark[index].x * width)
                            y1 = int(face_landmarks.landmark[index].y * height)
                            coordinates_left_eye.append([x1,y1])
            
                    for face_landmarks in results.multi_face_landmarks:
                        for index in OJO_DERECHO:
                            x2 = int(face_landmarks.landmark[index].x * width)
                            y2 = int(face_landmarks.landmark[index].y * height)
                            coordinates_right_eye.append([x2,y2])

                    #Distancia parpados
                    distancia_izquierda_AUX , distancia_derecha_AUX = calcular_distancia(coordinates_left_eye, coordinates_right_eye)
                    
                    #Punto medio de ojos
                    finalX, finalY = punto_medio(CENTRO_IZQUIERDO_AUX,CENTRO_DERECHO_AUX)

                    CONTADOR += 1

                                #################### Bloque 2 #################
        elif (CONTADOR == 2):
                
                #Captura de video del frame siguiente
                ret,frame_dos = lecturaVideo(cap)
                if not ret:
                    break

                #Escala de grises para mediapipe
                rgb_frame = cv.cvtColor(frame_dos, cv.COLOR_BGR2RGB)
                img_h, img_w = frame_dos.shape[:2]
                results = face_mesh.process(rgb_frame)
                height, width, _ = frame_dos.shape


                if results.multi_face_landmarks:
                    mesh_points= np.array([np.multiply([p.x, p.y], [img_w, img_h]).astype(int) for p in results.multi_face_landmarks[0].landmark])
                    
                    #Se busca el centro de iris
                    CENTRO_IZQUIERDO,CENTRO_DERECHO,l_radius= centros_ojos(mesh_points)
                    
                    #Listas que seran llenadas con coordenadas
                    coordinates_left_eye = [] 
                    coordinates_right_eye= []
                    coordenadas_iris_izquierdo = []

                    #Coordenadas ojos nuevas
                    for face_landmarks in results.multi_face_landmarks:
                        for index in OJO_IZQUIERDO:
                            x1 = int(face_landmarks.landmark[index].x * width)
                            y1 = int(face_landmarks.landmark[index].y * height)
                            coordinates_left_eye.append([x1,y1])


                    for face_landmarks in results.multi_face_landmarks:
                        for index in OJO_DERECHO:
                            x2 = int(face_landmarks.landmark[index].x * width)
                            y2 = int(face_landmarks.landmark[index].y * height)
                            coordinates_right_eye.append([x2,y2])

                    #Coordenadas de iris para medir distancia de monitor
                    for face_landmarks in results.multi_face_landmarks:
                        for index in IRIS_IZQUIERDO:    
                            x3 = int(face_landmarks.landmark[index].x * width)
                            y3 = int(face_landmarks.landmark[index].y * height)
                            coordenadas_iris_izquierdo.append([x3,y3])

                    #Distancia parpados
                    distancia_izquierda , distancia_derecha = calcular_distancia(coordinates_left_eye,coordinates_right_eye)

                    #Distancia respecto monitor
                    distancia_iris = calcular_distancia2(coordenadas_iris_izquierdo[0], coordenadas_iris_izquierdo[2])
                    
                    finalX_comp = finalX
                    finalY_comp = finalY

                    #Calculo de vectores de movimiento    
                    vectorX, vectorY= calcular_vector(CENTRO_IZQUIERDO_AUX,CENTRO_IZQUIERDO)
                        
                    finalX, finalY = punto_medio(CENTRO_IZQUIERDO,CENTRO_DERECHO)

                    comparacionX = abs(finalX_comp-finalX)
                    comparacionY = abs(finalY_comp-finalY)

                    #Control de camara    
                    #cv.imshow("frame", frame_dos)

                    CONTADOR += 1


                                        ###### Bloque 3 #########
        elif (CONTADOR == 3):
            
            #Condicionales 
            if(comparacionX > 1.5 or comparacionY > 1.5):
            
                CENTROX = (int(finalX)+int(vectorX))
                CENTROY = (int(finalY)+int(vectorY))

                #Condicionales para persona a mayor de 45 cm
                if(distancia_iris <= 25):
                    pyautogui.moveTo(((int(CENTROX))*(r*3))-(ancho_pantalla*2),(int(CENTROY))*(r*3)-(alto_pantalla*2)) 

                    if distancia_derecha >= 5 and distancia_izquierda <= 5 :
                        pyautogui.click()
                   
                    elif distancia_derecha <= 5 and distancia_izquierda >= 5:
                        pyautogui.click(button= 'right')
                             
                    CONTADOR -= 1


                else:
                    #Condicionales para persona a menos de 45 cm
                    pyautogui.moveTo(((int(CENTROX))*(r*1))-(ancho_pantalla/2),(int(CENTROY))*(r*1)-(alto_pantalla/2))

                    if distancia_derecha >= 12 and distancia_izquierda <= 12 :
                        pyautogui.click()              
                    
                    elif distancia_derecha <= 12 and distancia_izquierda >= 12:
                        pyautogui.click(button= 'right')
                     
                    CONTADOR -= 1





                
            else:
                CONTADOR -= 1
    
        else: 
            print("ERROR, INTENTALO DENUEVO")

        key = cv.waitKey(1)
        if key == ord('q'):
            break

        
cap.release()
cv.destroyAllWindows()



