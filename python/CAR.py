import enum
import pyfirmata

#https://habr.com/ru/articles/137415/


MotorMode = enum.Enum(
    value='MotorMode',
    names=('forward backward stop free'),
)
#end MotorMode

HIGH = True # Create a high state
LOW = False # Create a low state

MotorPos = enum.Enum(
    value='MotorStatus',
    names=('LF RF RB LB'),
)
#end MotorPos


class Motor:
    def __init__(self, status  = None):
        self.__status = status

class Car:
    def __init__(self, portNo, board):
        self.__port = portNo
        print('>>'+portNo)
        self.board = board

    def __del__(self):
        pass
#        self.board.exit()

    def motorRun(self, motor, mode):
        if ( mode == 1 ):
            self.board.digital[12].write(1)
        else:
            self.board.digital[12].write(0)
            pass

if __name__=="__main__":
    pass