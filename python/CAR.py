import enum
import pyfirmata

#https://habr.com/ru/articles/137415/


MotorStatus = enum.Enum(
    value='MotorStatus',
    names=('forward backward stop free'),
)
#end MotorStatus

MotorPos = enum.Enum(
    value='MotorStatus',
    names=('LF RF RB LB'),
)
#end MotorPos


class Motor:
    def __init__(self, status  = None):
        self.__status = status

class Car:
    def __init__(self, mLF  = None):
        self.__mLF = mLF

if __name__=="__main__":
    pass