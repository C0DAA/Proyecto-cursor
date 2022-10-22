from funciones import * 

#razon de proporcionalidad + 0.1 para evitar cortes de pantalla
r = RazonDeProporcionalidad()

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
        ret,frame = lecturaVideo(cap)
        if not ret:
            break

        #escala de grises para mediapipe
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        img_h, img_w = frame.shape[:2]
        results = face_mesh.process(rgb_frame)
       
        #DIBUJO DE LINEAS
        if results.multi_face_landmarks:

            mesh_points= np.array([np.multiply([p.x, p.y], [img_w, img_h]).astype(int) for p in results.multi_face_landmarks[0].landmark])
           
            #circulos iris
            (l_cx, l_cy), l_radius =cv.minEnclosingCircle(mesh_points[IRIS_IZQUIERDO])
            (r_cx, r_cy), r_radius =cv.minEnclosingCircle(mesh_points[IRIS_DERECHO])
           
            #coordenadas centro de iris
            CENTRO_IZQUIERDO= np.array([l_cx, l_cy], dtype = np.int32)
            CENTRO_DERECHO= np.array([r_cx, r_cy], dtype = np.int32)

            #control de mouse con coordenadas de centro del ojo IZQUIERDO * razon de proporcion
            pyautogui.moveTo(int(CENTRO_IZQUIERDO[0])*r,int(CENTRO_IZQUIERDO[1])*r)   
            
            #dibujar lineas
            dibujar(mesh_points, frame, CENTRO_IZQUIERDO, CENTRO_DERECHO,l_radius)
           
            
            
        cv.imshow('control', frame) 
        key = cv.waitKey(1)
        if key == ord('q'):
            break

cap.release()
cv.destroyAllWindows()