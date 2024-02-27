#Chip 'n Dale: Rescue Rangers
#Чип и Дейл: Спешат на помощь

import numpy as np
import tkinter as tk
from tkinter.constants import DISABLED, NORMAL
import time
from PIL import Image, ImageTk#  pip install Pillow
import math
import serial.tools.list_ports
from CAR import Car, CarMode
import pythoncom # pip install pywin32


class App:
    def __init__(self, master) -> None:
        # Instantiating master i.e toplevel Widget
        self.master = master


def cmd2car(mode):
    print(mode)
    if len(carPort)>0:
        carMecanum.CarRun(mode)
#end def cmd2car




def carSearch():
    """
    Return a com port pyfirmata.
    """
    ports = serial.tools.list_ports.comports()
    portNo = ''
#    for port in ports:
#            print(port.device)
#            print(f"description: {port.description}")
#            print(f"manufacturer: {port.manufacturer}\n")
#            print(f"hwid: {port.hwid}\n")
#            if port.hwid == 'BTHENUM\\{00001101-0000-1000-8000-00805F9B34FB}_VID&0001000E_PID&3412\\8&39341452&0&98DA600ACB1E_C00000000':
#                portNo = port.device
#                print('!' + portNo)
    portNo = 'COM6'
    if (portNo != ''):
        global carMecanum
        carMecanum = Car(portNo)
        print("board install")
 #       time.sleep(5)
        tmp = carMecanum.getBattery()
        print(tmp)
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
# end camera_run

def on_closing():
    print("exit")
    car_stop()
    app.destroy()

if __name__ == '__main__':

    app = tk.Tk()
    app.title("Chip 'n Dale: Rescue Rangers")
    app.geometry("1200x640")
    app.resizable(width=False, height=False)

    win = App(app)


    flcam = 'camera'


    global carPort
    carPort = ''
    carPort = carSearch()
    imgCamera = tk.PhotoImage(file='C:/ed/api/prog/imgTurtle/move/camera.png')
    btnCamera = tk.Button(app, text="camera", command=camera_run, image=imgCamera)
    btnCamera.place(x=850, y=340)

    imgStop = tk.PhotoImage(file='C:/ed/api/prog/imgTurtle/move/mvSTOP.png')
    btnStop = tk.Button(app, text="STOP", command=car_stop, image=imgStop)
    btnStop.place(x=1000, y=340)
    btnStop['state'] = DISABLED

    lblPort = tk.Label( text=carPort, borderwidth=2, bg="White", highlightthickness=4, highlightbackground="#37d3ff")
    lblPort.place(x=1000, y=300)

    lblX =  tk.Label( text="posX", borderwidth=2, bg="White", highlightthickness=4, highlightbackground="#37d3ff")
    lblX.place(x=1070, y=300)

    lblY =  tk.Label( text="posY", borderwidth=2, bg="White", highlightthickness=4, highlightbackground="#37d3ff")
    lblY.place(x=1120, y=300)

    app.protocol("WM_DELETE_WINDOW", on_closing)
    app.mainloop()
    print("ex")

