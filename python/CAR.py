import enum
import pyfirmata

#https://habr.com/ru/articles/137415/


MotorMode = enum.Enum(
    value='MotorMode',
    names=('forward backward stop brake'),
)
#end MotorMode

HIGH = True # Create a high state
LOW = False # Create a low state

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
        print('>>'+portNo)
        self.board = pyfirmata.Arduino(portNo)

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

if __name__=="__main__":
    pass