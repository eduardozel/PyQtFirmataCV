#Chip 'n Dale: Rescue Rangers
#Чип и Дейл: Спешат на помощь
#https://habr.com/ru/companies/wunderfund/articles/716740/
#https://habr.com/ru/articles/337420/
import tkinter as tk
from tkinter.constants import DISABLED, NORMAL, SUNKEN, RAISED
import asyncio
import serial.tools.list_ports
from CAR import Car, CarMode
import pythoncom # pip install pywin32



class App:
    async def exec(self):
        self.window = Window(asyncio.get_event_loop())

        await self.window.show()

class Window(tk.Tk):

    def mkBTN(self, rw, cl, fnm):
        self.img = tk.PhotoImage(file='btn/btn'+fnm+'.png')
        btn = tk.Button( self.frameCTRL, image=self.img)
        btn.grid(row=rw, column=cl, padx=1, pady=1)
        return btn
    # end mkBTN

    def __init__(self, loop):
        self.loop = loop
        self.root = tk.Tk()

        self.lblBattery = tk.Label(text="Battery", width=5, borderwidth=2, font=("Helvetica 14 bold"), bg="White", highlightthickness=4, highlightbackground="#37d3ff")
        self.lblBattery.place(x=170, y=10)

        self.lblIRsensor = tk.Label(text="IR", width=2, borderwidth=2, font=("Helvetica 14 bold"), bg="White", highlightthickness=4, highlightbackground="#37d3ff")
        self.lblIRsensor.place(x=120, y=10)


        self.frameSPEED = tk.Frame(bd=2, bg='white')
        self.frameSPEED.pack(expand=True)
        self.frameSPEED.place(x=270, y=60)

        self.btnSP1 = tk.Button(self.frameSPEED, command=self.car_SP1, text= "1", font=("Helvetica 12 bold"), width=2, relief=SUNKEN)
        self.btnSP1.grid(row=0, column=0, padx=1, pady=1)

        self.btnSP2 = tk.Button(self.frameSPEED, command=self.car_SP2, text= "2", font=("Helvetica 12 bold"), width=2, relief=RAISED)
        self.btnSP2.grid(row=1, column=0, padx=1, pady=1)

        self.frameCTRL = tk.Frame(bd=2, bg='red')
        self.frameCTRL.pack(expand=True)
        self.frameCTRL.place(x=140, y=60)

        self.imgFL = tk.PhotoImage(file='btn/btnFL.png')
        self.btnFL = tk.Button(self.frameCTRL, image=self.imgFL)
        self.btnFL.grid(row=0, column=0, padx=1, pady=1)

        self.imgFW = tk.PhotoImage(file='btn/btnFW.png')
        self.btnFW = tk.Button(self.frameCTRL, image=self.imgFW)
        self.btnFW.grid(row=0, column=1, padx=1, pady=1)
        self.btnFW.bind("<ButtonPress>", self.btnFW_press)
        self.btnFW.bind("<ButtonRelease>", self.btnFW_release)

        self.imgFR = tk.PhotoImage(file='btn/btnFR.png')
        self.btnFR = tk.Button(self.frameCTRL, image=self.imgFR)
        self.btnFR.grid(row=0, column=2, padx=1, pady=1)#

        self.imgLF = tk.PhotoImage(file='btn/btnLF.png')
        btnLF = tk.Button(self.frameCTRL, image=self.imgLF)
        btnLF.grid(row=1, column=0, padx=1, pady=1)

        self.imgRT = tk.PhotoImage(file='btn/btnRT.png')
        btnRT = tk.Button(self.frameCTRL, image=self.imgRT)
        btnRT.grid(row=1, column=2, padx=1, pady=1)

        self.imgCCW = tk.PhotoImage(file='btn/btnCCW.png')
        self.btnCCW = tk.Button(self.frameCTRL, image=self.imgCCW)
        self.btnCCW.grid(row=2, column=0, padx=1, pady=1)
        self.btnCCW.bind("<ButtonPress>", self.btnCCW_press)
        self.btnCCW.bind("<ButtonRelease>", self.btnCCW_release)

        self.imgBW = tk.PhotoImage(file='btn/btnBW.png')
        btnBW = tk.Button(self.frameCTRL, image=self.imgBW)
        btnBW.grid(row=2, column=1, padx=1, pady=1)

        self.btnCW = self.mkBTN( 2, 2, 'CW')
        self.btnCW.bind("<ButtonPress>", self.btnCW_press)
        self.btnCW.bind("<ButtonRelease>", self.btnCW_release)

        self.imgST = tk.PhotoImage(file='btn/btnSTOP.png')
        self.btnST = tk.Button(self.frameCTRL, command=self.btn_stop, image=self.imgST)
        self.btnST.grid(row=1, column=1, padx=1, pady=1)
#        tk.CreateToolTip(self.btnST,"STOP CAR")

        self.imgStart = tk.PhotoImage(file='btn/btnCD.png')
        self.btnStart = tk.Button(app, command=self.mission_start, image=self.imgStart)
        self.btnStart.place(x=10, y=60)
        self.btnStart.config(height=120, width=120)

        self.car_SP1()
        global IR_task
        IR_task = self.loop.create_task(self.getIRsensor())
        global BAT_task
        BAT_task = self.loop.create_task(self.getBattery())

    # end init

    def btn_stop(self):
        if not mission_task.cancelled():
            was_cancelled = mission_task.cancel()
            while not was_cancelled:
                pass
            self.btnStart['state'] = NORMAL
        carMecanum.CarRun(CarMode.stop)
    # end btn_stop

    def car_SP1(self):
        self.btnSP2.config(relief=RAISED)
        self.btnSP1.config(relief=SUNKEN)
        carMecanum.carSpeed(1)
    # end car_SP1

    def car_SP2(self):
        self.btnSP1.config(relief=RAISED)
        self.btnSP2.config(relief=SUNKEN)
        carMecanum.carSpeed(2)
    # end car_SP2

    def btnCW_press(self, event):
        carMecanum.CarRun(CarMode.clockwise)
    def btnCW_release(self, event):
        carMecanum.CarRun(CarMode.stop)

    def btnCCW_press(self, event):
        carMecanum.CarRun(CarMode.counterclockwise)

    def btnCCW_release(self, event):
        carMecanum.CarRun(CarMode.stop)
    def btnFW_press(self, event):
        carMecanum.CarRun(CarMode.forward)
    def btnFW_release(self, event):
        carMecanum.CarRun(CarMode.stop)

    async def show(self):
        while True:
            self.root.update()
            await asyncio.sleep(.1)
    # end show
    async def getIRsensor(self):
        while True:
            tmp = carMecanum.getIRsensor()
            self.lblIRsensor["text"] = tmp
            global IRdetect
            IRdetect = tmp == 0
            if IRdetect :
                self.lblIRsensor.config(bg="orange")
            else :
                self.lblIRsensor.config(bg="#37d3ff")
            self.root.update()
            await asyncio.sleep(0.1)
    # end getIRsensor

    async def getBattery(self):
        while True:
            tmp = carMecanum.getBattery()
            self.lblBattery["text"] = f"{tmp:.{1}f}"+" V"
            self.root.update()
            await asyncio.sleep(10)
    # end getBattery

    def mission_start(self):
        self.btnStart['state'] = DISABLED
        global mission_task
        mission_task = self.loop.create_task(self.mission())
        #was_cancelled = task.cancel()
        #task.cancelled()
    # end mission_start
    async def mission(self):
        while not IRdetect:
            carMecanum.CarRun(CarMode.clockwise)
            await asyncio.sleep(0.2)
            carMecanum.CarRun(CarMode.stop)
            await asyncio.sleep(1.0)
        await asyncio.sleep(2.1)
        carMecanum.CarRun(CarMode.forward)
        await asyncio.sleep(0.5)
        carMecanum.CarRun(CarMode.stop)
        self.btnStart['state'] = NORMAL
        print("mission end")
    # end mission

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
    for port in ports:
            print(port.device)
#            print(f"description: {port.description}")
#            print(f"manufacturer: {port.manufacturer}\n")
#            print(f"hwid: {port.hwid}\n")
#            if port.hwid == 'BTHENUM\\{00001101-0000-1000-8000-00805F9B34FB}_VID&0001000E_PID&3412\\8&39341452&0&98DA600ACB1E_C00000000':
#                portNo = port.device
#                print('!' + portNo)
    portNo = 'COM7'
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
    if not mission_task.cancelled():
        was_cancelled = mission_task.cancel()
        while not was_cancelled:
            pass
    if not IR_task.cancelled():
        was_cancelled = IR_task.cancel()
        while not was_cancelled:
            pass
    if not BAT_task.cancelled():
        was_cancelled = BAT_task.cancel()
        while not was_cancelled:
            pass
    car_stop()
    print("exit")
    app.destroy()

if __name__ == '__main__':

    app = tk.Tk()
    app.title("Chip 'n Dale: Rescue Rangers")
    app.geometry("320x240")
    app.resizable(width=False, height=False)

#    win = App(app)

    global carPort
    carPort = ''
    carPort = carSearch()

    lblPort = tk.Label( text=carPort, borderwidth=2, bg="White", highlightthickness=4, highlightbackground="#37d3ff")
    lblPort.place(x=10, y=10)

    app.protocol("WM_DELETE_WINDOW", on_closing)
    asyncio.run(App().exec())
    carMecanum.CarRun(CarMode.stop)
    print("the end")


