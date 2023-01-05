from funciones2 import * 

NUM_FRAMES = 2
aux_counter = 0
blink_counter = 0
coordenadas_Nuevas = []

x_aux,y_aux = calcular_centro_pantalla()

#captura de video
cap = cv.VideoCapture(0)

CONTADOR = 1

#objeto facemesh
with MALLA_FACIAL.FaceMesh(
    max_num_faces= 1,
    refine_landmarks=True,
    min_detection_confidence = 0.5,
    min_tracking_confidence=0.5
) as face_mesh:

    
    while True:

                                            ###### bloque de control ######
        if (CONTADOR == 1):

            ret,frame = lecturaVideo(cap)
            if not ret:
              break
            #escala de grises para mediapipe
            rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            img_h, img_w = frame.shape[:2]
            results = face_mesh.process(rgb_frame)
            height, width, _ = frame.shape

            r = RazonDeProporcionalidad(img_w)
                
            if results.multi_face_landmarks:
                    mesh_points= np.array([np.multiply([p.x, p.y], [img_w, img_h]).astype(int) for p in results.multi_face_landmarks[0].landmark])
                    
                    #centro de ojos
                    CENTRO_IZQUIERDO_AUX,CENTRO_DERECHO_AUX,l_radius= centros_ojos(mesh_points)
                    
                    #dibujar lineas ojos
                    #dibujar(mesh_points, frame,CENTRO_IZQUIERDO_AUX,CENTRO_DERECHO_AUX,l_radius)
                    
                    coordinates_left_eye = [] 
                    coordinates_right_eye= []
                    coordenadas_iris_izquierdo = []
    
                    for face_landmarks in results.multi_face_landmarks:
                        for index in OJO_IZQUIERDO:
                            x1 = int(face_landmarks.landmark[index].x * width)
                            y1 = int(face_landmarks.landmark[index].y * height)
                            coordinates_left_eye.append([x1,y1])
                        #  cv.circle(frame,(x1,y1),2,(0,255,255),1)
                        # cv.circle(frame,(x1,y1),1,(128,0,250),1)

                    for face_landmarks in results.multi_face_landmarks:
                        for index in OJO_DERECHO:
                            x2 = int(face_landmarks.landmark[index].x * width)
                            y2 = int(face_landmarks.landmark[index].y * height)
                            coordinates_right_eye.append([x2,y2])
                        #  cv.circle(frame,(x2,y2),2,(0,255,255),1)
                        # cv.circle(frame,(x2,y2),1,(128,0,250),1)
                

                    #Distancia parpados
                    distancia_izquierda_AUX , distancia_derecha_AUX = calcular_distancia(coordinates_left_eye, coordinates_right_eye)
                    finalX, finalY = punto_medio(CENTRO_IZQUIERDO_AUX,CENTRO_DERECHO_AUX)

                    CONTADOR += 1

                                #################### bloque principal #################
        elif (CONTADOR == 2):
                
                ret,frame_dos = lecturaVideo(cap)
                if not ret:
                    break
                #escala de grises para mediapipe
                rgb_frame = cv.cvtColor(frame_dos, cv.COLOR_BGR2RGB)
                img_h, img_w = frame_dos.shape[:2]
                results = face_mesh.process(rgb_frame)
                height, width, _ = frame_dos.shape
                if results.multi_face_landmarks:
                    mesh_points= np.array([np.multiply([p.x, p.y], [img_w, img_h]).astype(int) for p in results.multi_face_landmarks[0].landmark])
                    
                    #centro de ojos
                    CENTRO_IZQUIERDO,CENTRO_DERECHO,l_radius= centros_ojos(mesh_points)
                    
                    #dibujar lineas ojos
                    # dibujar(mesh_points, frame_dos,CENTRO_IZQUIERDO,CENTRO_DERECHO,l_radius)
                    
                    coordinates_left_eye = [] 
                    coordinates_right_eye= []
                    coordenadas_iris_izquierdo = []

                    #coordenadas iris y dibujo de circulo interior del ojo
                    for face_landmarks in results.multi_face_landmarks:
                        for index in OJO_IZQUIERDO:
                            x1 = int(face_landmarks.landmark[index].x * width)
                            y1 = int(face_landmarks.landmark[index].y * height)
                            coordinates_left_eye.append([x1,y1])
                        # cv.circle(frame_dos,(x1,y1),2,(0,255,255),1)
                        # cv.circle(frame_dos,(x1,y1),1,(128,0,250),1)

                    for face_landmarks in results.multi_face_landmarks:
                        for index in OJO_DERECHO:
                            x2 = int(face_landmarks.landmark[index].x * width)
                            y2 = int(face_landmarks.landmark[index].y * height)
                            coordinates_right_eye.append([x2,y2])
                            cv.circle(frame_dos,(x2,y2),2,(0,255,255),1)
                        #  cv.circle(frame_dos,(x2,y2),1,(128,0,250),1)

                    for face_landmarks in results.multi_face_landmarks:
                        for index in IRIS_IZQUIERDO:    
                            x3 = int(face_landmarks.landmark[index].x * width)
                            y3 = int(face_landmarks.landmark[index].y * height)
                            coordenadas_iris_izquierdo.append([x3,y3])
                            cv.circle(frame_dos,(x3,y3),1,(128,0,250),1)
                            cv.circle(frame_dos,(x3,y3),2,(128,0,250),1)

                    #Distancia parpados
                    distancia_izquierda , distancia_derecha = calcular_distancia(coordinates_left_eye,coordinates_right_eye)

                        #Distancia iris 
                        #print(coordenadas_iris_izquierdo)
                    distancia_iris = calcular_distancia2(coordenadas_iris_izquierdo[0], coordenadas_iris_izquierdo[2])
                    

                    #print(distancia_iris)
                   # print(" ")

                    finalX_comp = finalX
                    finalY_comp = finalY
                        
                    vectorX, vectorY= calcular_vector(CENTRO_IZQUIERDO_AUX,CENTRO_IZQUIERDO)
                        
                    finalX, finalY = punto_medio(CENTRO_IZQUIERDO,CENTRO_DERECHO)

                    comparacionX = abs(finalX_comp-finalX)
                    comparacionY = abs(finalY_comp-finalY)

                        
                    #cv.imshow("frame", frame_dos)

                    CONTADOR += 1


                                        ###### comparaciones y movimientos ######
        elif (CONTADOR == 3):
            
            #cv.imshow("control", frame_dos)
            if(comparacionX > 1.5 or comparacionY > 1.5):
            
                CENTROX = (int(finalX)+int(vectorX))
                CENTROY = (int(finalY)+int(vectorY))

                if(distancia_iris <= 25):
                    pyautogui.moveTo(((int(CENTROX))*(r*3))-(ancho_pantalla*2),(int(CENTROY))*(r*3)-(alto_pantalla*2)) 

                else:
                    pyautogui.moveTo(((int(CENTROX))*(r*1))-(ancho_pantalla/2),(int(CENTROY))*(r*1)-(alto_pantalla/2))


                #condicional para el conteo de parpadeos
                #print('derecha: ' , distancia_derecha, ' izquierda: ', distancia_izquierda )
                if distancia_derecha >= 10 and distancia_izquierda <= 10 :
                    pyautogui.click()
                    #print(" ")
                    
                
                elif distancia_derecha <= 10 and distancia_izquierda >= 10:
                    pyautogui.click(button= 'right')
                    #print(" ")
                
                CONTADOR -= 1
            else:
                CONTADOR -= 1
    
        else: 
            print("ERROR, EL CONTADOR SE VOLVIO LOQUITO, INTENTALO DENUEVO")

        key = cv.waitKey(1)
        if key == ord('q'):
            break

        
cap.release()
cv.destroyAllWindows()

