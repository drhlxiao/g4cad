#!/usr/bin/python
from utils import printf
import os
import os.path
from PySide.QtGui import *
from PySide.QtCore import *
import sys
__author__ = 'Hualin Xiao'
__date__ = 'Sept. 10th, 2017'

__dir__ = os.path.dirname(__file__)


class MainWidget(QDialog):

    def __init__(self, parent):
        super(MainWidget, self).__init__(parent)
        self.setGeometry(200, 200, 340, 440)
        self.setWindowTitle("Measurements")
        self.layoutMain = QVBoxLayout(self)

        self.layoutDataBrowser = QHBoxLayout()

        self.buttonCopyClipBoard = QPushButton('Copy')
        self.buttonClose = QPushButton('Close')
        self.buttonClose.clicked.connect(self.close)

        self.textEdit = QTextEdit()
        self.textEdit.setGeometry(QRect(330, 50, 241, 222))

        # self.buttonNewRecord.clicked.connect(self.openAddRecordDialog)

        # self.layoutDataBrowser.addWidget(self.textEdit)
        self.layoutDataBrowser.addWidget(self.buttonCopyClipBoard)
        self.layoutDataBrowser.addWidget(self.buttonClose)

        self.buttonCopyClipBoard.clicked.connect(self.copyToClipBoard)

        self.layoutMain.addWidget(self.textEdit)
        self.layoutMain.addLayout(self.layoutDataBrowser)

        self.setLayout = self.layoutMain

    def copyToClipBoard(self):
        text = self.textEdit.toPlainText()
        clipboard = QApplication.clipboard()
        clipboard.setText(text)

    def measurePart(self, measurements):
        self.textEdit.clear()
        cursor = QTextCursor(self.textEdit.document())

        template = '''<h3>{name}</h3> <br>
                   <b>Volume:  <br> {vol} mm^3  <br> <br>
                   <b>Centres </b> <br> 
                   <b>&nbsp;&nbsp; Barycentre: </b> <br>  ({wx:0.3f},{wy:0.3f},{wz:0.3f}) mm<br>
                   <b>&nbsp;&nbsp;  Geometric Centre: </b> <br> ({cx:0.3f},{cy:0.3f},{cz:0.3f}) mm<br>

                    <h4> Bound Box</h4> <br>
                   <b>&nbsp;&nbsp;   Length: </b>   {xLen:0.3f} mm <br>
                   <b> &nbsp;&nbsp;  Width: </b>   {yLen:0.3f} mm <br>
                   <b>&nbsp;&nbsp;   Height: </b>   {zLen:0.3f} mm <br>
                   <b>&nbsp;&nbsp; x-range: </b>  ({xmin:0.3f},{xmax:0.3f}) mm<br>
                   <b>&nbsp;&nbsp; y-range: </b>  ({ymin:0.3f},{ymax:0.3f}) mm<br>
                   <b>&nbsp;&nbsp; z-range: </b>  ({zmin:0.3f},{zmax:0.3f}) mm<br>
                   '''

        html = template.format(**measurements)
        cursor.insertHtml(html)
        self.textEdit.setReadOnly(True)
        # self.textEdit.setEnabled(False);

    @staticmethod
    def run(parent=None, measurements=None):
        dialog = MainWidget(parent)
        dialog.measurePart(measurements)
        dialog.exec_()


def main():
    app = QApplication([])
    MainWidget.run()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
