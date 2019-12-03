# import the necessary packages
import argparse
import cv2
import numpy as np
import pyautogui


# Funcion para seleccionar la ROI

def nothing(x):
    pass

def click_and_crop(event, x, y, flags, param):
    global puntos, Recortado
    # Mira si se ha pulsado el boton izquierdo. Lo que pasa entonces es que en la variable puntos se guarda la posicion x,y del mouse
    if event == cv2.EVENT_LBUTTONDOWN:
        puntos = [(x, y)]
        Recortado = True
    # Aqui se mira si se ha soltado el boton izquierdo, si es asi se guarda la posicion x,y del mouse y se muestra un rectangulo desde el punto donde se presiono click izquierdo, hasta le punto donde se solto
    elif event == cv2.EVENT_LBUTTONUP:

        puntos.append((x, y))
        Recortado = False
        cv2.rectangle(cuadro_param, puntos[0], puntos[1], (0, 255, 0), 2)
        cv2.imshow("cuadro_param", cuadro_param)


puntos = []
Recortado = False

# Aqui se crean las Trackbar que sirvenn para poder delimitar un rango de valores en HSV que permitan obtener una mascara apropiada

vent0 = "Ventana"
cv2.namedWindow(vent0, cv2.WINDOW_NORMAL)
lim_inf_h = 0
cv2.createTrackbar("Limite inferior: matiz", vent0, lim_inf_h, 255, nothing)
lim_sup_h = 29
cv2.createTrackbar("Limite superior: matiz", vent0, lim_sup_h, 255, nothing)
lim_inf_s = 80
cv2.createTrackbar("Limite inferior: saturacion", vent0, lim_inf_s, 255, nothing)
lim_sup_s = 239
cv2.createTrackbar("Limite superior: saturacion", vent0, lim_sup_s, 255, nothing)
lim_inf_v = 8
cv2.createTrackbar("Limite inferior: valor", vent0, lim_inf_v, 255, nothing)
lim_sup_v = 255
cv2.createTrackbar("Limite superior: valor", vent0, lim_sup_v, 255, nothing)


# The video source can change
video = cv2.VideoCapture(1)

while True:

    #para camara normal
    _, cuadro_param = video.read()
    cuadro_param = cv2.flip(cuadro_param, 1)

    # Se obtienen las posiciones actuales de las Trackbar
    lim_inf_h = cv2.getTrackbarPos("Limite inferior: matiz", vent0)
    lim_sup_h = cv2.getTrackbarPos("Limite superior: matiz", vent0)
    lim_inf_s = cv2.getTrackbarPos("Limite inferior: saturacion", vent0)
    lim_sup_s = cv2.getTrackbarPos("Limite superior: saturacion", vent0)
    lim_inf_v = cv2.getTrackbarPos("Limite inferior: valor", vent0)
    lim_sup_v = cv2.getTrackbarPos("Limite superior: valor", vent0)

    # Se halla una mascara con los valores determinados por las Trackbar. Lo que sucede es que inRange solo deja la parte de la imagen que este en los rangos de parametros HSV (al menos en este caso), porque tambien se puede decir que mire en el espectro RGB
    mascara_rango_hsv = cv2.inRange(cv2.cvtColor(cuadro_param, cv2.COLOR_BGR2HSV), np.array((float(lim_inf_h), float(lim_inf_s), float(lim_inf_v))), np.array((float(lim_sup_h), float(lim_sup_s), float(lim_sup_v))))

    copia = cuadro_param.copy()
    cv2.namedWindow("Seleccion de ROI")
    cv2.setMouseCallback("Seleccion de ROI", click_and_crop)

    cv2.imshow("Seleccion de ROI", cuadro_param)
    cv2.imshow(vent0, mascara_rango_hsv)

    key = cv2.waitKey(1) & 0xFF
    # Si se presiona z entonces se reinicia el ROI
    if key == ord("z"):
        cuadro_param = copia.copy()
    # Si se presiona q se rompe el ciclo para dar paso a la parte que obtiene el ROI con base en los puntos del mouse
    elif key == ord("q"):
        break


if len(puntos) == 2:
    roi = copia[puntos[0][1]:puntos[1][1], puntos[0][0]:puntos[1][0]]
    mascara_rango_hsv = mascara_rango_hsv[puntos[0][1]:puntos[1][1], puntos[0][0]:puntos[1][0]]


cv2.destroyAllWindows()

HSV_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
Hist_roi = cv2.calcHist([HSV_roi], [0], mascara_rango_hsv, [180], [0, 180])
term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)


camx = 640
camy = 480

fgbg = cv2.createBackgroundSubtractorMOG2()

while True:
    
    _, cuadro = video.read()
    cuadro = cv2.flip(cuadro, 1)
    cuadro1 = cuadro.copy()

    HSV_cuadro = cv2.cvtColor(cuadro, cv2.COLOR_BGR2HSV)
    mascara = cv2.calcBackProject([HSV_cuadro], [0], Hist_roi, [0, 180], 1)

    ini_track = (puntos[0][0], puntos[0][1], puntos[1][0] - puntos[0][0], puntos[1][1] - puntos[0][1])
    ret, track_window = cv2.meanShift(mascara, ini_track, term_crit)
    x, y, w, h = track_window

    mascara_rango_hsv_1 = cv2.inRange(cv2.cvtColor(cuadro, cv2.COLOR_BGR2HSV), np.array((float(lim_inf_h), float(lim_inf_s), float(lim_inf_v))), np.array((float(lim_sup_h), float(lim_sup_s), float(lim_sup_v))))
    roi_conteo = mascara_rango_hsv_1[int(y * 0.95): (y + h), x: int(x * 1.25 + w)]

    cont_img, contornos, _ = cv2.findContours(roi_conteo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contornos) != 0:
        max_c = max(contornos, key=cv2.contourArea)
        max_c[:, :, 0] = max_c[:, :, 0] + x
        max_c[:, :, 1] = max_c[:, :, 1] + y

        cascara = cv2.convexHull(max_c, returnPoints=False)
        defectos = cv2.convexityDefects(max_c, cascara)

        xi = 0
        yi = 0

        if defectos is not None:
            dis_a = 0
            cnt = 0

            for i in range(defectos.shape[0]):
                _, _, f, dis = defectos[i, 0]
                if abs(dis - dis_a) > 8000:
                    cnt = cnt + 1
                far = tuple(max_c[f][0])
                xi = xi + far[0]
                yi = yi + far[1]
                dis_a = dis

            xi = x / defectos.shape[0]
            yi = y / defectos.shape[0]
            cv2.circle(cuadro1, (x + int(w / 2), y + int(h / 2)), 3, (0, 0, 255), 3)

            xc = x + int(w / 2)
            yc = y + int(h / 2)

            if xc < 3 * camx / 8 and yc > 3 * camy / 8 and yc < 5 * camy / 8:
                if xc < 1.5 * camx / 8:
                    pyautogui.moveRel(-15, 0)
                else:
                    pyautogui.moveRel(-5, 0)
            if xc > 5 * camx / 8 and yc > 3 * camy / 8 and yc < 5 * camy / 8:
                if xc > 6.5 * camx / 8:
                    pyautogui.moveRel(+15, 0)
                else:
                    pyautogui.moveRel(+5, 0)
            if yc < 3 * camy / 8 and xc > 3 * camx / 8 and xc < 5 * camx / 8:
                if yc > 6.5 * camy / 8:
                    pyautogui.moveRel(0, -15)
                else:
                    pyautogui.moveRel(0, -5)
            if yc > 5 * camy / 8 and xc > 3 * camx / 8 and xc < 5 * camx / 8:
                if xc < 1.5 * camx / 8:
                    pyautogui.moveRel(0, +15)
                else:
                    pyautogui.moveRel(0, +5)

            cv2.line(cuadro1, (int(3 * camx / 8), 0), (int(3 * camx / 8), camy), (255, 0, 0), 5)
            cv2.line(cuadro1, (int(5 * camx / 8), 0), (int(5 * camx / 8), camy), (255, 0, 0), 5)
            cv2.line(cuadro1, (0, int(3 * camy / 8)), (camx, int(3 * camy / 8)), (255, 0, 0), 5)
            cv2.line(cuadro1, (0, int(5 * camy / 8)), (camx, int(5 * camy / 8)), (255, 0, 0), 5)
            if cnt == 0:
                area_cls = cv2.contourArea(max_c)
                accion = area_opn / area_cls
            else:
                area_opn = cv2.contourArea(max_c)
                accion = 0

    if accion == 0:
        print("-o-")
    if accion >= 1.30:
        ini_track = (x, y, w, h)

        if (3 * camx / 8 < xc < 5 * camx / 8) and (3 * camy / 8 < yc < 5 * camy / 8):
            print("--ok--")
            pyautogui.click(interval=1)
        print("-->")
    if accion > 0.5 and accion < 1.30:
        ini_track = (x, y, w, h)

        if (3 * camx / 8 < xc < 5 * camx / 8) and (3 * camy / 8 < yc < 5 * camy / 8):
            pyautogui.click(button='right', clicks=1, interval=1)
            print("--ok--")
        print("<--")
    cv2.imshow("mascara_rango_hsv", cuadro1)
    # cv2.imshow("cuadro", roi_conteo)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
video.release()
cv2.destroyAllWindows()
