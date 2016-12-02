# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import xml.etree.ElementTree as eT

class Tool(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        exitAction = QAction('&Schließen', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(qApp.quit)

        openAction = QAction('&Öffnen', self)
        openAction.setShortcut('Ctrl+O')
        openAction.triggered.connect(lambda: self.importHandler(frameLeft, frameRight))

        addAction = QAction('&Eintrag anlegen', self)
        addAction.setShortcut('Ctrl+N')
        addAction.triggered.connect(lambda: self.addHandler(frameLeft))

        editmodeAction = QAction('&Bearbeitungsmodus', self)
        editmodeAction.setShortcut('Ctrl+E')
        editmodeAction.triggered.connect(lambda: self.editmodeHandler(frameRight))

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Datei')
        fileMenu.addAction(openAction)
        fileMenu.addAction(addAction)
        fileMenu.addAction(exitAction)

        editMenu = menubar.addMenu('&Bearbeiten')
        editMenu.addAction(editmodeAction)

        screenbox = QWidget()

        hbox = QHBoxLayout(self)
        screenbox.setLayout(hbox)

        frameLeft = QListWidget()
        frameLeft.setMaximumWidth(frameLeft.sizeHintForColumn(0))
        frameLeft.currentItemChanged.connect(lambda: self.displayInfo(frameLeft, frameRight))
        #frameLeft.connect(frameLeft, QSignalMapper("itemDoubleClicked(QListWidgetItem*)"))
        #frameLeft.connect(frameLeft, QSignalMapper("itemDoubleClicked(QListWidgetItem*)", lambda: self.testBox()))


        frameRight = QLabel()
        frameRight.setTextFormat(Qt.RichText)
        frameRight.setTextInteractionFlags(Qt.TextBrowserInteraction)
        frameRight.setOpenExternalLinks(True)

        screenSplitter = QSplitter(Qt.Horizontal)
        screenSplitter.addWidget(frameLeft)
        screenSplitter.addWidget(frameRight)

        hbox.addWidget(screenSplitter)

        self.setCentralWidget(screenbox)
        self.showMaximized()
        self.setWindowTitle('Promasu Manager')
        self.show()

    def importHandler(self, listView, labelView):
        fileDialog = QFileDialog()
        fileDialog.setFileMode(QFileDialog.ExistingFile)
        filename = fileDialog.getOpenFileName(self, 'Promasu Datenbank öffnen', '.', 'Promasu Projectdatabase (*.pmdx)')
        try:
            tree = eT.parse(filename[0])
            root = tree.getroot()
            listView.clear()
            for child in root:
                listView.addItem(child[0].text)
            listView.setMaximumWidth(listView.sizeHintForColumn(0) + 10)
            listView.setMinimumWidth(listView.sizeHintForColumn(0) + 10)
            labelView.setText(filename[0])
            self.filename = str(filename[0])
        except eT.ParseError:
            msgBox = QMessageBox()
            msgBox.setText("Die Datei hat kein gültiges Format.")
            msgBox.setWindowTitle("Promasu Manager Warnung")
            msgBox.exec()
            return False
        except FileNotFoundError:
            msgBox = QMessageBox()
            msgBox.setText("Die Datei wurde nicht gefunden.")
            msgBox.setWindowTitle("Promasu Manager Warnung")
            msgBox.exec()
            return False
        except IndexError:
            msgBox = QMessageBox()
            msgBox.setText("Die Datei ist nicht im richtigen Format.")
            msgBox.setWindowTitle("Promasu Manager Warnung")
            msgBox.exec()
            return False
        except PermissionError:
            msgBox = QMessageBox()
            msgBox.setText("Sie besitzen nicht die Berechtigung um diese Datei zu öffnen.")
            msgBox.setWindowTitle("Promasu Manager Warnung")
            msgBox.exec()
            return False
        return True

    def displayInfo(self, listView, labelView):
        tree = eT.parse(self.filename)
        root = tree.getroot()
        itemNumber = listView.currentRow()
        saveString = "Speicherort: <a href=\"file:///" + root[itemNumber][1].text + "\">" + root[itemNumber][1].text + "</a><br>"
        buildString = "Build: <a href=\"file:///" + root[itemNumber][2].text + "\">" + root[itemNumber][2].text + "</a><br>"
        gitString = "Git: <a href=\"" + root[itemNumber][3].text + "\">" + root[itemNumber][3].text + "</a><br>"
        docString = "Dokumentation: <a href=\"" + root[itemNumber][4].text + "\">" + root[itemNumber][4].text + "</a><br>"
        designString = "Designs: <a href=\"file:///" + root[itemNumber][5].text + "\">" + root[itemNumber][5].text + "</a><br>"
        imageString = "Bilder: <a href=\"file:///" + root[itemNumber][6].text + "\">" + root[itemNumber][6].text + "</a><br>"
        langString = "Sprache: " + root[itemNumber][7].text + "<br>"
        versionString = "Version: " + root[itemNumber][8].text
        labelView.setText(saveString+buildString+gitString+docString+designString+imageString+langString+versionString)
        return True

    def addHandler(self, listView):
        pass

    def editmodeHandler(self, labelView):
        pass

    def testBox(self):
        msgBox = QMessageBox()
        msgBox.setText("Es klappt.")
        msgBox.setWindowTitle("Promasu Manager")
        return True

    def onChanged(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Tool()
    sys.exit(app.exec_())
