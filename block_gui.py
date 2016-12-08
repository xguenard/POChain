import sys
from PyQt5 import QtGui, QtCore, QtWidgets
import threading
import time

class BlockchainWindow(QtWidgets.QWidget):
    
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
                    , size.height()/10, len(self.blocks)-1)
        except:
            pass

        try:
            y = 2*size.height()/6 + size.height()/10
            self.draw_rectangle(qp, self.blocks[-2], y, len(self.blocks)-2)
        except:
            pass

        try:
            y = 4 *size.height()/6 + size.height()/10
            self.draw_rectangle(qp, self.blocks[-3], y, len(self.blocks)-3)
        except:
            pass

    def draw_rectangle(self, qp, elems, y, blk_id):
        size = self.size()
        rect1 = QtCore.QRectF(0, y, size.width()/5.1, size.height()/6)

        elems_txt = "\n".join([e.short_str() \
                for e in elems])
        if not elems:
            elems_txt = "EMPTY BLOCK"
        rect = QtCore.QRectF(size.width()/5, y\
                ,size.width()/1.2, size.height()/6)

        qp.setBrush(QtGui.QColor(36, 145, 181))
        qp.drawRect(rect)
        qp.setBrush(QtGui.QColor(8, 67, 92))
        qp.drawRect(rect1)
        qp.drawText(rect, QtCore.Qt.AlignCenter, elems_txt)
        qp.drawText(rect1, QtCore.Qt.AlignCenter, "block : {}".format(blk_id))
