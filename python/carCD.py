#Chip 'n Dale: Rescue Rangers
#Чип и Дейл: Спешат на помощь

#https://habr.com/ru/articles/337420/
import tkinter as tk
from tkinter.constants import DISABLED, NORMAL
import asyncio
import serial.tools.list_ports
from CAR import Car, CarMode
import pythoncom # pip install pywin32



class App:
    async def exec(self):
        self.window = Window(asyncio.get_event_loop())

        await self.window.show()

class Window(tk.Tk):
    def __init__(self, loop):
        self.loop = loop
        self.root = tk.Tk()

        self.lblBattery = tk.Label(text="Battery", borderwidth=2, bg="White", highlightthickness=4, highlightbackground="#37d3ff")
        self.lblBattery.place(x=170, y=10)

        self.lblIRsensor = tk.Label(text="IR", borderwidth=2, bg="White", highlightthickness=4, highlightbackground="#37d3ff")
        self.lblIRsensor.place(x=120, y=10)

        self.loop.create_task(self.getIRsensor())
        self.loop.create_task(self.getBattery())
    # end init

    async def show(self):
        while True:
            self.root.update()
            await asyncio.sleep(.1)
    # end show
    async def getIRsensor(self):
        while True:
            tmp = carMecanum.getIRsensor()
            self.lblIRsensor["text"] = tmp
            self.root.update()
            await asyncio.sleep(0.1)
    # end getIRsensor
    async def getBattery(self):
        while True:
            tmp = carMecanum.getBattery()
            self.lblBattery["text"] = tmp
            self.root.update()
            await asyncio.sleep(0.1)
    # end getBattery
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

def on_closing():
    print("exit")
    car_stop()
    app.destroy()

if __name__ == '__main__':

    app = tk.Tk()
    app.title("Chip 'n Dale: Rescue Rangers")
    app.geometry("320x240")
    app.resizable(width=False, height=False)

#    win = App(app)


    flcam = 'camera'


    global carPort
    carPort = ''
    carPort = carSearch()

    imgStop = tk.PhotoImage(file='C:/ed/api/prog/imgTurtle/move/mvSTOP.png')
    btnStop = tk.Button(app, text="STOP", command=car_stop, image=imgStop)
    btnStop.place(x=10, y=60)
    btnStop['state'] = DISABLED

    lblPort = tk.Label( text=carPort, borderwidth=2, bg="White", highlightthickness=4, highlightbackground="#37d3ff")
    lblPort.place(x=10, y=10)

    app.protocol("WM_DELETE_WINDOW", on_closing)
#    app.mainloop()

    asyncio.run(App().exec())
    print("ex")

