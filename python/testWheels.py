from PyQt6 import QtGui
from PyQt6.QtGui import QIcon, QPixmap, QImage
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMainWindow

import sys

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
        self.btn_forward.setIcon(QtGui.QIcon('./imgWheels/btnForward.png'))
        self.btn_forward.setGeometry(130, 10, 64, 32)

        self.btn_forward = QPushButton(self)
        self.btn_forward.setIcon(QtGui.QIcon('./imgWheels/btnBackward.png'))
        self.btn_forward.setGeometry(130, 50, 64, 32)


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

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())