import sys

import serial.tools.list_ports
from CAR import Car, CarMode

from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import (
      QApplication, QMainWindow, QWidget
    , QHBoxLayout, QGridLayout
    , QLabel, QPushButton

)

class CarControlUI(QMainWindow):

    def btnDFN( self, btn, img, rw, cl, press =None
    ):
        btn.setIconSize(QtCore.QSize(60, 60))
        btn.setFixedSize(QSize(64, 64))
        btn.setIcon(QtGui.QIcon('./imgCtrl/btn/btn'+img+'.png'))
        self.layout_button.addWidget(btn, rw, cl)
        if press is not None:
            btn.pressed.connect(press)
            btn.released.connect(self.btn_releaseEvent)
    # def btnDFN

    def btn1DFN( self, btn, img, press =None
    ):
        btn.setIconSize(QtCore.QSize(30, 60))
        btn.setFixedSize(QSize(32, 64))
        btn.setIcon(QtGui.QIcon('./imgCtrl/btn/btn'+img+'.png'))
        self.layout_rotate.addWidget(btn)
        if press is not None:
            btn.pressed.connect(press)
            btn.released.connect(self.btn_releaseEvent)
    # def btn1DFN

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Car Control")
        self.setGeometry(100, 100, 400, 64*3+10)

        central_widget = QWidget(self)
        central_widget.setFixedSize(64*3,64*3)
        self.setCentralWidget(central_widget)

        self.layout_ctrl = QHBoxLayout(central_widget)
        self.layout_ctrl.setContentsMargins(10, 10, 10, 10)

        self.layout_button = QGridLayout()
        self.layout_button.cellRect(3, 3)

        self.btn_fl = QPushButton()
        self.btnDFN( self.btn_fl, 'FL', 1, 1)

        self.btn_fw = QPushButton()
        self.btnDFN( self.btn_fw, 'FW', 1, 2, self.btn_fw_pressEvent)

        self.btn_fr = QPushButton()
        self.btnDFN( self.btn_fr, 'FR', 1, 3)
#
        self.btn_lf = QPushButton()
        self.btnDFN( self.btn_lf, 'LF', 2, 1, self.btn_lf_pressEvent)

        self.btn_rt = QPushButton()
        self.btnDFN( self.btn_rt, 'RT', 2, 3, self.btn_rt_pressEvent)
#
        self.btn_bl = QPushButton()
        self.btnDFN( self.btn_bl, 'BL', 3, 1)

        self.btn_bw = QPushButton()
        self.btnDFN( self.btn_bw, 'BW', 3, 2, self.btn_bw_pressEvent)

        self.btn_br = QPushButton()
        self.btnDFN( self.btn_br, 'BR', 3, 3)

        self.layout_rotate = QHBoxLayout()

        self.btn_ccw = QPushButton()
        self.btn1DFN( self.btn_ccw, 'CCW', self.btn_ccw_pressEvent)

        self.btn_cw = QPushButton()
        self.btn1DFN( self.btn_cw, 'CW', self.btn_cw_pressEvent)

        self.layout_button.addLayout(self.layout_rotate, 2,2)
        self.layout_ctrl.addLayout(self.layout_button)

#        self.label = QLabel()
#        self.layout_ctrl.addWidget(self.label)
#        self.label.move(64*3, 10)
#        self.image_path = "./imgCtrl/move/stop.png"
#        self.image = QImage(self.image_path)
#        self.label.setPixmap(QPixmap.fromImage(self.image))
    # def __init__

    def btn_releaseEvent(self):
        carMecanum.CarRun(CarMode.stop)
# forward
    def btn_fw_pressEvent(self):
        carMecanum.CarRun(CarMode.forward)
# left
    def btn_lf_pressEvent(self):
        carMecanum.CarRun(CarMode.left)

# right
    def btn_rt_pressEvent(self):
        carMecanum.CarRun(CarMode.right)
# backward
    def btn_bw_pressEvent(self):
        carMecanum.CarRun(CarMode.backward)
# clockwise
    def btn_cw_pressEvent(self):
        carMecanum.CarRun(CarMode.clockwise)
# counterclockwise
    def btn_ccw_pressEvent(self):
        carMecanum.CarRun(CarMode.counterclockwise)

# end class  CarControlUI

if __name__=="__main__":
    portNo = ''

    ports = serial.tools.list_ports.comports()
    for port in ports:
#        print(port.device)
#        print(f"description: {port.description}")
#        print(f"manufacturer: {port.manufacturer}\n")
#        print(f"hwid: {port.hwid}\n")
        if port.hwid=='BTHENUM\\{00001101-0000-1000-8000-00805F9B34FB}_LOCALMFG&0002\\8&39341452&0&98DA600ACB1E_C00000000':
            portNo = port.device
            print('!' + portNo)
    if (portNo != ''):
        global carMecanum
        carMecanum = Car(portNo)
        print("board install")
    else:
        print("not found!!!")

    app = QApplication([])
    window = CarControlUI()
    window.show()
    sys.exit(app.exec())

#print(f"hwid: {port.hwid}\n")
#COM7
#name: BTHENUM\{00001101-0000-1000-8000-00805F9B34FB}_LOCALMFG&0002\8&39341452&0&98DA600ACB1E_C00000000

#COM8
#name: BTHENUM\{00001101-0000-1000-8000-00805F9B34FB}_LOCALMFG&0000\8&39341452&0&000000000000_00000014
