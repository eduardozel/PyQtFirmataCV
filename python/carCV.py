#https://robotclass.ru/tutorials/opencv-detect-rectangle-angle/
#https://datahacker.rs/012-blending-and-pasting-images-using-opencv/
#https://docs.opencv.org/3.4/d4/d15/group__videoio__flags__base.html
#https://www.youtube.com/watch?v=yuOPSRyBY0Y
#https://www.youtube.com/watch?v=olLOP5_L8-Y

import numpy as np
import tkinter as tk
from tkinter.constants import DISABLED, NORMAL
import time
from PIL import Image, ImageTk#  pip install Pillow
import cv2 as cv
import math
import serial.tools.list_ports
from CAR import Car, CarMode
import pythoncom # pip install pywin32

color_blue = (255,0,0)
color_yellow = (0,255,255)


class App:
    def __init__(self, master) -> None:
        # Instantiating master i.e toplevel Widget
        self.master = master


def findRectangle1( img ):
    pythoncom.PumpWaitingMessages()
    hsv_min = np.array(( 65,  95, 110), np.uint8)
    hsv_max = np.array((125, 255, 255), np.uint8)
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    thresh = cv.inRange(hsv, hsv_min, hsv_max)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    if ( len(contours) > 4 ):
        pass
        return
    global maxArea
    maxArea = 0
    for cnt in contours:
        rect = cv.minAreaRect(cnt)
        box = cv.boxPoints(rect)
        area = int(rect[1][0] * rect[1][1])
#        if area > maxArea:
#            maxArea = area
#            print("max")
#            print(maxArea)
        if area > 20500 and area < 45000:
            box = np.int64(box)
            x = int(rect[0][0])
            y = int(rect[0][1])
            center = ( x, y)
            cv.circle(img, center, 5, color_yellow, 2)
            cv.drawContours(img, [box], 0, (255, 0, 0), 2)

#            print("-----------------")
#            print(x)
#            print(y)
            if (x> 400):
                flarr = 'mvRT'
                carMecanum.CarRun(CarMode.right)
            elif (x < 200):
                flarr = 'mvLF'
                carMecanum.CarRun(CarMode.left)
            else:
                if (y< 90):
                    flarr = 'mvFW'
                    carMecanum.CarRun(CarMode.forward)
                elif (y>300):
                    flarr = 'mvBW'
                    carMecanum.CarRun(CarMode.backward)
                else:
                    flarr = 'mvSTOP'
                    carMecanum.CarRun(CarMode.stop)

            imgArrow = cv.imread('./imgTurtle/move/'+flarr+'.jpg')

            img1 = cv.resize(img, (800, 600))
            img2 = cv.resize(imgArrow, (800, 600))
            global imgRes
            imgRes = cv.addWeighted(img1, 0.5, img2, 0.5, 0.0)
            edge1 = np.int64((box[1][0] - box[0][0], box[1][1] - box[0][1]))
            edge2 = np.int64((box[2][0] - box[1][0], box[2][1] - box[1][1]))

            usedEdge = edge1
            if cv.norm(edge2) > cv.norm(edge1):
                usedEdge = edge2
            reference = (1, 0)  # vector horizont

            angle = 180.0 / math.pi * math.acos(
                (reference[0] * usedEdge[0] + reference[1] * usedEdge[1]) / (cv.norm(reference) * cv.norm(usedEdge)))
            win_ctrl = 'direction'
            w = 640
            h = 480
            cv.imshow(win_ctrl, cv.resize(imgRes, (w, h)))
            cv.resizeWindow(win_ctrl, w, h)
            cv.moveWindow(win_ctrl, 340, 0)
        else: # if area >
            win_epmty = 'empty'
            cv.imshow(win_epmty, cv.resize(img, (320, 240)))
            cv.resizeWindow(win_epmty, 320, 240)
            cv.moveWindow(win_epmty, 0, 0)
            carMecanum.CarRun(CarMode.stop)
#            print("empty")
#            print(area)
#def findRectangle1

def carRun():

    cameraIP = '192.168.100.4'
    cap = cv.VideoCapture("http://"+cameraIP+":8080/video")
    cap.set(cv.CAP_PROP_FPS,3)
    if cap.isOpened():
        print("camera oK")
        while cap.isOpened():
            pythoncom.PumpWaitingMessages()
            ret, frame = cap.read()
            if frame is None:
                break
            if ret:
                frameBGR = cv.resize( cv.flip(cv.cvtColor(frame, cv.COLOR_BGR2RGBA) , 0), (320, 240))
                imgBGR = Image.fromarray(frameBGR)
                ph1 = ImageTk.PhotoImage(imgBGR)
                lblCamera.image = ph1
                lblCamera.configure(image=ph1)
                app.update()
                print("img")
                image = cv.flip(frame, 0) # 0 around the x; > 0 around the y;
#                cv.imshow('direction', frame)
#                findRectangle1(image)

    else:
        print("Cannot open camera")

# end def carRun

def carSearch():
    """
    Return a com port string.
    """
    ports = serial.tools.list_ports.comports()
    portNo = ''
    for port in ports:
            print(port.device)
            print(f"description: {port.description}")
            print(f"manufacturer: {port.manufacturer}\n")
            print(f"hwid: {port.hwid}\n")
            if port.hwid == 'BTHENUM\\{00001101-0000-1000-8000-00805F9B34FB}_VID&0001000E_PID&3412\\8&39341452&0&98DA600ACB1E_C00000000':
                portNo = port.device
                print('!' + portNo)
    portNo = 'COM9'
    if (portNo != ''):
        global carMecanum
        carMecanum = Car(portNo)
        time.sleep(5)
        tmp = carMecanum.getBattery()
        print(tmp)
        print("board install")
        return portNo
    else:
        print("board not found!!!")
        return ''
# end carSearch


def car_stop():
    carMecanum.CarRun(CarMode.stop)
# end car_stop

def camera_run():
    btnCamera['state'] = DISABLED
    if len(carPort)>0:
        btnStop['state'] = NORMAL
    carRun()
# end camera_run

if __name__ == '__main__':

    app = tk.Tk()
    app.title("car control= openCV")
    app.geometry("1200x640")
    app.resizable(width=False, height=False)

    win = App(app)

    frame = cv.imread("./imgTurtle/carTest.jpg")
    tmp = cv.imread("./imgTurtle/box.png")
    img_box  = cv.cvtColor(tmp, cv.COLOR_BGR2RGB)

    image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    image = Image.fromarray(frame)
    edged = Image.fromarray(img_box)
    ph1 = ImageTk.PhotoImage(edged)
    photo = ImageTk.PhotoImage(image)

    panelA = tk.Label(image=photo, width = 800, height = 600, borderwidth=2, bg="White", highlightthickness=4, highlightbackground="#37d3ff")
    panelA.image = image
    panelA.place( x = 20, y = 20) #anchor=n, ne, e, se, s, sw, w, nw, or center

    lblCamera = tk.Label(image=ph1, width = 320, height = 240, bg="White", highlightthickness=4, highlightbackground="#37d3ff")
    lblCamera.place(x=840, y=20)
    lblCamera.image = ph1

    flcam = 'camera'


    global carPort
    carPort = ''
    #tmp = carSearch()
    imgCamera = tk.PhotoImage(file='D:/tartaruga/python/imgTurtle/move/camera.png')
    btnCamera = tk.Button(app, text="camera", command=camera_run, image=imgCamera)
    btnCamera.place(x=850, y=340)

    imgStop = tk.PhotoImage(file='D:/tartaruga/python/imgTurtle/move/mvSTOP.png')
    btnStop = tk.Button(app, text="STOP", command=car_stop, image=imgStop)
    btnStop.place(x=1000, y=340)
    btnStop['state'] = DISABLED

    lblPort = tk.Label( text=carPort, borderwidth=2, bg="White", highlightthickness=4, highlightbackground="#37d3ff")
    lblPort.place(x=1000, y=300)

    app.mainloop()
    print("ex")

