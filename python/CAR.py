import enum
import pyfirmata


#https://habr.com/ru/articles/137415/
#https://python.hotexamples.com/examples/pyfirmata/Arduino/get_pin/python-arduino-get_pin-method-examples.html
#https://jethrojeff.com/


MotorMode = enum.Enum(
    value='MotorMode',
    names=('forward backward stop brake'),
)

CarMode = enum.Enum(
    value='CarMode',
    names=('forward backward left right clockwise counterclockwise stop brake'),
)
#end MotorMode

#MotorPos = enum.Enum(
#    value='MotorPos',
#    names=('LF RF RB LB'),
# 5 9 11 7
#)
class MotorPos(enum.IntEnum):
    LF = 0
    RF = 1
    RB = 2
    LB = 3

#end MotorPos

class Motor:
    def __init__(self, status = None):
        self.__status = status

class Car:
    def __init__(self, portNo):
        self.__port = portNo
        print('!>>'+portNo)
        PORT = ''#pyfirmata.Arduino.AUTODETECT
        print("PORT>>"+PORT)
        self.board = pyfirmata.Arduino(portNo)
        it = pyfirmata.util.Iterator(self.board)
        it.start()
        self.curMode = CarMode.stop
        self.ir_pin = self.board.get_pin('d:2:i')
        self.ir_pin.enable_reporting()
        self.bt_pin = self.board.get_pin('a:5:i')
        self.sp_pin = self.board.get_pin('d:3:p')

        self.motorpins = [[5, 6]
            , [9, 10]
            , [11, 12]
            , [7, 8]
        ]

#            self.motorpins = {MotorPos.LF: [5, 6]
#            , MotorPos.RF: [9, 10]
#            , MotorPos.RB: [11, 12]
#            , MotorPos.LB: [7, 8]
#        }

    def __del__(self):
        print("del")
        self.board.exit()

    def getIRsensor(self
    ):
        ir = self.ir_pin.read()
        while ir is None:
            ir = self.ir_pin.read()
        return ir
    # end getIRsensor
    def getBattery(self
    ):
        motorBattery = self.bt_pin.read()
        while motorBattery is None:
            motorBattery = self.bt_pin.read()
        return motorBattery
    # end getBattery

    def carSpeed(self, speed):

        if speed == 1:
            print("1")
            self.sp_pin.write(50)
        else:
            print("2")
            self.sp_pin.write(10)
    #end carSpeed
    def motorRun(self, motor, mode):
        pin1 = self.motorpins[motor][0]
        pin0 = self.motorpins[motor][1]
        if ( mode == MotorMode.forward ):
            self.board.digital[pin0].write(0)
            self.board.digital[pin1].write(1)
        elif ( mode == MotorMode.backward ):
            self.board.digital[pin0].write(1)
            self.board.digital[pin1].write(0)
        elif ( mode == MotorMode.stop ):
            self.board.digital[pin0].write(0)
            self.board.digital[pin1].write(0)
        elif ( mode == MotorMode.brake ):
            self.board.digital[pin0].write(1)
            self.board.digital[pin1].write(1)

    def CarRun(self, mode
    ):
        """
        Move car
        """
        if (self.curMode == mode):
            pass
            return
        else:
            self.curMode = mode
        print("mode")
        print(mode)
        if ( mode == CarMode.stop ):
            print("stop")
            self.motorRun(0, MotorMode.stop)
            self.motorRun(1, MotorMode.stop)
            self.motorRun(2, MotorMode.stop)
            self.motorRun(3, MotorMode.stop)
        elif (mode == CarMode.forward):
            print("forward")
            self.motorRun(0, MotorMode.forward)
            self.motorRun(1, MotorMode.forward)
            self.motorRun(2, MotorMode.forward)
            self.motorRun(3, MotorMode.forward)
        elif ( mode == CarMode.backward ):
            self.motorRun(0, MotorMode.backward)
            self.motorRun(1, MotorMode.backward)
            self.motorRun(2, MotorMode.backward)
            self.motorRun(3, MotorMode.backward)
        elif (mode == CarMode.left):
            self.motorRun(0, MotorMode.backward) #FL
            self.motorRun(1, MotorMode.forward)  #FR
            self.motorRun(2, MotorMode.backward) #BR
            self.motorRun(3, MotorMode.forward)  #BL
        elif (mode == CarMode.right):
            self.motorRun(0, MotorMode.forward)   #FL
            self.motorRun(1, MotorMode.backward)  #FR
            self.motorRun(2, MotorMode.forward)   #BR
            self.motorRun(3, MotorMode.backward)  #BL
        elif (mode == CarMode.clockwise):
            self.motorRun(0, MotorMode.forward)   #FL
            self.motorRun(1, MotorMode.backward)  #FR
            self.motorRun(2, MotorMode.backward)  #BR
            self.motorRun(3, MotorMode.forward)   #BL
        elif (mode == CarMode.counterclockwise):
            self.motorRun(0, MotorMode.backward)  # FL
            self.motorRun(1, MotorMode.forward)   # FR
            self.motorRun(2, MotorMode.forward)   # BR
            self.motorRun(3, MotorMode.backward)  # BL

if __name__=="__main__":
    pass