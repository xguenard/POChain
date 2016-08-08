import sys
from PySide import QtGui, QtCore
import threading
import time

class BlockchainWindow(QtGui.QWidget):
    
    def __init__(self, size):
        super(BlockchainWindow, self).__init__()
        self.blocks = []
        self.setGeometry(size.width()/2, 0, size.width()/2, size.height())
        
    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawRectangles(qp)
        qp.end()

    def add_elem(self, elem):
        self.blocks.append(elem)
        self.update()

        
        
    def drawRectangles(self, qp):
      
        color = QtGui.QColor(0, 0, 0)
        color.setNamedColor('#d4d4d4')
        qp.setPen(color)
        size = self.size()

        try:
            self.draw_rectangle(qp, self.blocks[-1]\
                    , size.height()/10)
        except:
            pass

        try:
            y = 2*size.height()/6 + size.height()/10
            self.draw_rectangle(qp, self.blocks[-2], y)
        except:
            pass

        try:
            y = 4 *size.height()/6 + size.height()/10
            self.draw_rectangle(qp, self.blocks[-3], y)
        except:
            pass

    def draw_rectangle(self, qp, elems, y):
        elems_txt = "\n".join([e.short_str() \
                for e in elems])
        size = self.size()
        rect = QtCore.QRectF(size.width()/10, y\
                ,size.width()/1.1, size.height()/6)
        qp.setBrush(QtGui.QColor(36, 145, 181))
        qp.drawRect(rect)
        qp.drawText(rect, QtCore.Qt.AlignCenter, elems_txt)
