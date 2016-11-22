# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import xml.etree.ElementTree as et

class tool(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        exitAction = QAction('&Schließen', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(qApp.quit)

        openAction = QAction('&Öffnen', self)
        openAction.setShortcut('Ctrl+O')
        filename = openAction.triggered.connect(lambda: self.importHandler(frameLeft))

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Datei')
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)

        screenbox = QWidget()

        hbox = QHBoxLayout(self)
        screenbox.setLayout(hbox)

        frameLeft = QListWidget()
        frameLeft.setMaximumWidth(frameLeft.sizeHintForColumn(0))

        frameRight = QFrame(self)
        frameRight.setFrameShape(QFrame.StyledPanel)

        screenSplitter = QSplitter(Qt.Horizontal)
        screenSplitter.addWidget(frameLeft)
        screenSplitter.addWidget(frameRight)

        hbox.addWidget(screenSplitter)

        self.setCentralWidget(screenbox)
        self.showMaximized()
        self.setWindowTitle('Promasu Manager')
        self.show()

    def importHandler(self, listView):
        fileDialog = QFileDialog()
        fileDialog.setFileMode(QFileDialog.ExistingFile)
        filename = fileDialog.getOpenFileName(self, 'Promasu Datenbank öffnen', '.', 'Promasu Projectdatabase (*.pmdx)')
        tree = et.parse(filename[0])
        root = tree.getroot()
        listView.clear()
        for child in root:
            listView.addItem(child[0].text)
        listView.setMaximumWidth(listView.sizeHintForColumn(0))
        self.setWindowTitle("Promasu Manager - " + filename[0])
        return filename[0]

    def onChanged(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = tool()
    sys.exit(app.exec_())
