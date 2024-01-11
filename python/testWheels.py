from PyQt6 import QtGui, QtCore
from PyQt6.QtGui import QIcon, QPixmap, QImage
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMainWindow

import sys
import pyfirmata
#pip install pyFirmata2==2.4.2
#https://codingwithfun.com/pip/pyfirmata2/526240/
#https://codingwithfun.com/pip/pyfirmata/526239/
#https://coder-studio.ru/q-2504690/pyfirmata-vydayet-oshibku-posle-sozdaniya-ob-yekta-arduino#a_74572258
#https://www.pythonguis.com/tutorials/pyqt6-signals-slots-events/

import time
import serial
import serial.tools.list_ports
from CAR import Car

#https://lora-grig.ru/how-to-fix-missing-image-and-button-in-pyqt6-application/

portNo =''
class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(QSize(200, 150))
        self.setWindowTitle("test wheels")
        self.setWindowIcon(QIcon('./imgWheels/wheel.png'))

        self.image_path = "./imgWheels/carL1.png"
        self.image = QImage(self.image_path)


        self.label = QLabel(self)
        pixmap = QPixmap('./imgWheels/carL1.png')
#        label.setPixmap(pixmap)
        self.label.setPixmap(QPixmap.fromImage(self.image))

        self.btn_forward = QPushButton(self)
#        self.btn_forward.setScaledContents(True)
        self.btn_forward.setIcon(QtGui.QIcon('./imgWheels/btnForward.png'))
        self.btn_forward.setIconSize(QtCore.QSize(64, 32))
#        self.btn_forward.setGeometry(130, 10, 64, 32)
        self.btn_forward.move(130, 10)
        self.btn_forward.setFixedSize(QSize(64, 32))
#        self.btn_forward.toggled.connect(self.btn_forward_Clicked)
        self.btn_forward.setCheckable(True)
        self.btn_forward.clicked.connect(self.btn_forward_was_toggled)
        self.btn_forward.setEnabled(portNo != '')
        #button.setShortcut(tr("Alt+F7"))


        self.btn_backward = QPushButton(self)
        self.btn_backward.setIcon(QtGui.QIcon('./imgWheels/btnBackward.png'))
        self.btn_backward.setIconSize(QtCore.QSize(64, 32))
        self.btn_backward.setGeometry(130, 50, 64, 32)
        self.btn_backward.setEnabled(portNo != '')
    @QtCore.pyqtSlot(bool)
    def btn_forward_was_toggled(self, checked):
        if checked:
            print('+++++')
            carMecanum.motorRun( 1, 1)
            self.rowOverride = True
        elif not checked:
            print('-----')
            carMecanum.motorRun(1, 0)
            self.rowOverride = False

    def btn_forward_Clicked(self):
        print("down")


    def mousePressEvent(self, event):
        pos = event.pos()
        x = pos.x()
        y = pos.y()
        if ( x < 120 ) & ( y < 135):
            if ( y < 60 ):
                if ( x < 60 ):
                    pixmap = QPixmap('./imgWheels/carL1.png')
                else:
                    pixmap = QPixmap('./imgWheels/carR1.png')
            else:
                if ( x < 60 ):
                    pixmap = QPixmap('./imgWheels/carL2.png')
                else:
                    pixmap = QPixmap('./imgWheels/carR2.png')
            self.label.setPixmap(pixmap)
    #end mousePressEvent
#end class window

app = QApplication(sys.argv)

#portNo = 'COM4'# Windows
#port = '/dev/ttyACM3' # Linux

ports = serial.tools.list_ports.comports()
for port in ports:
    #    print(port.device)
    #    print(f"description: {port.description}")
    #    print(f"manufacturer: {port.manufacturer}\n")
        if 'USB-SERIAL CH340' == port.description[:16]:
            portNo = port.device
            print('!' + portNo)
#    if 'wch.cn'==port.manufacturer:
#        portNo = port.device
#        print('+'+portNo)
# end for port
board = pyfirmata.Arduino(portNo)
print("board install")
if (portNo !=''):
    pass
    global carMecanum
    carMecanum = Car(portNo, board)


#for i in range(1, 10):
#    board.digital[12].write(1)
#    time.sleep(1)
#    board.digital[12].write(0)
#    time.sleep(1)
#board.exit()

window = Window()
window.show()
print('quit')
sys.exit(app.exec())