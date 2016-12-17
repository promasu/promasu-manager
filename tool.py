# -*- coding: utf-8 -*-

import os
import sys
import xml.etree.ElementTree as eT

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class myListWidget(QListWidget):
    def doubleClickedSlot(self,item):
        #TODO: Add edit screen
        database = ex.getDatabase()
        QMessageBox.information(self,
                                     "Item Double Click Detected!",
                                      "You clicked: " + database[item.text()][1])
        return True

class Tool(QMainWindow):
    def __init__(self):
        super().__init__()

        self.database = ""
        self.filename = ""
        self.initUI()

        if len(sys.argv) >= 2:
            self.importHandlerInit(self.frameLeft, self.frameRight)

    def initUI(self):
        exitAction = QAction('&Schließen', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(qApp.quit)

        openAction = QAction('&Öffnen', self)
        openAction.setShortcut('Ctrl+O')
        openAction.triggered.connect(lambda: self.importHandler(self.frameLeft, self.frameRight))

        addAction = QAction('&Eintrag anlegen', self)
        addAction.setShortcut('Ctrl+N')
        addAction.triggered.connect(lambda: self.addHandler(self.frameLeft))

        saveAction = QAction('&Speichern', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(lambda: self.saveProjectfile())

        saveasAction = QAction('&Speichern unter', self)
        saveasAction.setShortcut('Ctrl+Shift+S')
        saveasAction.triggered.connect(lambda: self.saveAsProjectfile())

        #editmodeAction = QAction('&Bearbeitungsmodus', self)
        #editmodeAction.setShortcut('Ctrl+E')
        #editmodeAction.triggered.connect(lambda: self.editmodeHandler(self.frameRight))

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Datei')
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveasAction)
        fileMenu.addAction(exitAction)

        editMenu = menubar.addMenu('&Bearbeiten')
        editMenu.addAction(addAction)
        #editMenu.addAction(editmodeAction)

        screenbox = QWidget()

        hbox = QHBoxLayout(self)
        screenbox.setLayout(hbox)

        self.frameLeft = myListWidget()
        self.frameLeft.setMaximumWidth(self.frameLeft.sizeHintForColumn(0))
        self.frameLeft.currentItemChanged.connect(lambda: self.displayInfo(self.frameLeft, self.frameRight))
        self.frameLeft.itemDoubleClicked[QListWidgetItem].connect(self.frameLeft.doubleClickedSlot)

        self.frameRight = QLabel()
        self.frameRight.setTextFormat(Qt.RichText)
        self.frameRight.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.frameRight.setOpenExternalLinks(True)

        screenSplitter = QSplitter(Qt.Horizontal)
        screenSplitter.addWidget(self.frameLeft)
        screenSplitter.addWidget(self.frameRight)

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
            self.database = self.listDictParser(root)
            self.filename = str(filename[0])
            self.setWindowTitle('Promasu Manager - ' + self.filename)
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
    
    def importHandlerInit(self, listView, labelView):
        filename = sys.argv[1]
        try:
            tree = eT.parse(filename)
            root = tree.getroot()
            listView.clear()
            for child in root:
                listView.addItem(child[0].text)
            listView.setMaximumWidth(listView.sizeHintForColumn(0) + 10)
            listView.setMinimumWidth(listView.sizeHintForColumn(0) + 10)
            self.database = self.listDictParser(root)
            self.filename = str(filename)
            self.setWindowTitle('Promasu Manager - ' + os.path.abspath(self.filename))
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

        saveString = "Speicherort: <a href=\"file:///" + root[itemNumber][1].text + "\">" + root[itemNumber][1].text + "</a><br>" if root[itemNumber][1].text != "NONE" else ""
        buildString = "Build: <a href=\"file:///" + root[itemNumber][2].text + "\">" + root[itemNumber][2].text + "</a><br>" if root[itemNumber][2].text != "NONE" else ""
        gitString = "Git: <a href=\"" + root[itemNumber][3].text + "\">" + root[itemNumber][3].text + "</a><br>" if root[itemNumber][3].text != "NONE" else ""
        docString = "Dokumentation: <a href=\"" + root[itemNumber][4].text + "\">" + root[itemNumber][4].text + "</a><br>" if root[itemNumber][4].text != "NONE" else ""
        designString = "Designs: <a href=\"file:///" + root[itemNumber][5].text + "\">" + root[itemNumber][5].text + "</a><br>" if root[itemNumber][5].text != "NONE" else ""
        imageString = "Bilder: <a href=\"file:///" + root[itemNumber][6].text + "\">" + root[itemNumber][6].text + "</a><br>" if root[itemNumber][6].text != "NONE" else ""
        langString = "Sprache: " + root[itemNumber][8].text + "<br>" if root[itemNumber][8].text != "NONE" else ""
        versionString = "Version: " + root[itemNumber][9].text if root[itemNumber][9].text != "NONE" else ""

        labelView.setText(saveString+buildString+gitString+docString+designString+imageString+langString+versionString)
        return True

    def addHandler(self, listView):
        pass

    def editmodeHandler(self, labelView):
        pass

    def testBox(self, msg):
        msgBox = QMessageBox()
        msgBox.setText(msg)
        msgBox.setWindowTitle("Promasu Manager")
        return True

    def editDialog(self, dictKey):
        return True

    def listDictParser(self, xmlList):
        dict = {}
        for child in xmlList:
            dict[child[0].text] = child[0:len(child)]
        for entry in dict:
            for i in range(10):
                dict[entry][i] = dict[entry][i].text
        return dict

    def onChanged(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()

    def getDatabase(self):
        database = self.database
        return database

    def saveProjectfile(self):
        try:
            fileContent = self.xmlWriter()
            f = open(self.filename, 'w+')
            f.write(fileContent)
            f.close()
            return True
        except FileNotFoundError:
            return False
        except:
            self.saveAsProjectfile()
            return True

    def saveAsProjectfile(self):
        try:
            fileDialog = QFileDialog()
            fileDialog.setFileMode(QFileDialog.ExistingFile)
            filename = fileDialog.getSaveFileName(self, 'Promasu Datenbank speichern', '.', 'Promasu Projectdatabase (*.pmdx)')
            fileContent = self.xmlWriter()
            f = open(filename[0], 'w+')
            f.write(fileContent)
            f.close()
            self.filename = filename[0]
            self.setWindowTitle(self.filename)
            return True
        except FileNotFoundError:
            return False
        except:
            self.saveAsProjectfile()
            return True

    def xmlWriter(self):
        dict = self.database
        fileContent = ""
        fileContent += "<database>\n"
        for entry in dict:
            fileContent += "    <project>\n"
            fileContent += "        <name>"+dict[entry][0]+"</name>\n"
            fileContent += "        <code>"+dict[entry][1]+"</code>\n"
            fileContent += "        <build>"+dict[entry][2]+"</build>\n"
            fileContent += "        <git>"+dict[entry][3]+"</git>\n"
            fileContent += "        <documentation>"+dict[entry][4]+"</documentation>\n"
            fileContent += "        <design>"+dict[entry][5]+"</design>\n"
            fileContent += "        <image>"+dict[entry][6]+"</image>\n"
            fileContent += "        <logo>"+dict[entry][7]+"</logo>\n"
            fileContent += "        <language>"+dict[entry][8]+"</language>\n"
            fileContent += "        <version>"+dict[entry][9]+"</version>\n"
            fileContent += "    </project>\n"
        fileContent += "</database>"
        return fileContent

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Tool()
    sys.exit(app.exec_())
