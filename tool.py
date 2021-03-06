# -*- coding: utf-8 -*-

import os
import sys
import xml.etree.ElementTree as eT
import time
from collections import OrderedDict

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class myListWidget(QListWidget):
    def doubleClickedSlot(self,item):
        database = ex.getDatabase()
        Tool.editDialog(ex, database[item.text()][0])
        return True

class Tool(QMainWindow):
    def __init__(self):
        super().__init__()

        self.database = OrderedDict
        self.filename = ""
        self.initUI()

        if len(sys.argv) >= 2:
            self.importHandlerInit(self.frameLeft, sys.argv[1])

    def initUI(self):
        exitAction = QAction('&Schließen', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(qApp.quit)

        openAction = QAction('&Öffnen', self)
        openAction.setShortcut('Ctrl+O')
        openAction.triggered.connect(lambda: self.importHandler(self.frameLeft))

        addAction = QAction('&Eintrag anlegen', self)
        addAction.setShortcut('Ctrl+N')
        addAction.triggered.connect(lambda: self.newDialog())

        saveAction = QAction('&Speichern', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(lambda: self.saveProjectfile())

        saveasAction = QAction('&Speichern unter', self)
        saveasAction.setShortcut('Ctrl+Shift+S')
        saveasAction.triggered.connect(lambda: self.saveAsProjectfile())

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Datei')
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveasAction)
        fileMenu.addAction(exitAction)

        editMenu = menubar.addMenu('&Bearbeiten')
        editMenu.addAction(addAction)

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
        self.setWindowIcon(QIcon('Promasu_manager.ico'))
        self.show()

    def importHandler(self, listView):
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
            self.warnBox("Die Datei hat kein gültiges Format.")
            self.importHandler(listView)
            return False
        except FileNotFoundError:
            if not filename[0] == "":
                self.importHandler(listView)
            self.warnBox("Die Datei wurde nicht gefunden.")
            return False
        except IndexError:
            self.warnBox("Die Datei ist nicht im richtigen Format.")
            self.importHandler(listView)
            return False
        except PermissionError:
            self.warnBox("Sie besitzen nicht die Berechtigung um diese Datei zu öffnen.")
            self.importHandler(listView)
            return False
        return True

    def importHandlerInit(self, listView, filename):
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
            self.warnBox("Die Datei hat kein gültiges Format.")
            return False
        except FileNotFoundError:
            self.warnBox("Die Datei wurde nicht gefunden.")
            return False
        except IndexError:
            self.warnBox("Die Datei ist nicht im richtigen Format.")
            return False
        except PermissionError:
            self.warnBox("Sie besitzen nicht die Berechtigung um diese Datei zu öffnen.")
            return False
        return True

    def displayInfo(self, listView, labelView):
        tree = eT.parse(self.filename)
        root = tree.getroot()
        itemNumber = listView.currentRow()
        saveString = "Speicherort: <a href=\"file:///" + root[itemNumber][1].text + "\">" + root[itemNumber][1].text + "</a><br>" if root[itemNumber][1].text != "NONE" and root[itemNumber][1].text is not None else ""
        buildString = "Build: <a href=\"file:///" + root[itemNumber][2].text + "\">" + root[itemNumber][2].text + "</a><br>" if root[itemNumber][2].text != "NONE" and root[itemNumber][2].text is not None else ""
        gitString = "Git: <a href=\"" + root[itemNumber][3].text + "\">" + root[itemNumber][3].text + "</a><br>" if root[itemNumber][3].text != "NONE" and root[itemNumber][3].text is not None else ""
        docString = "Dokumentation: <a href=\"" + root[itemNumber][4].text + "\">" + root[itemNumber][4].text + "</a><br>" if root[itemNumber][4].text != "NONE" and root[itemNumber][4].text is not None else ""
        designString = "Designs: <a href=\"file:///" + root[itemNumber][5].text + "\">" + root[itemNumber][5].text + "</a><br>" if root[itemNumber][5].text != "NONE" and root[itemNumber][5].text is not None else ""
        imageString = "Bilder: <a href=\"file:///" + root[itemNumber][6].text + "\">" + root[itemNumber][6].text + "</a><br>" if root[itemNumber][6].text != "NONE" and root[itemNumber][6].text is not None else ""
        langString = "Sprache: " + root[itemNumber][8].text + "<br>" if root[itemNumber][8].text != "NONE" and root[itemNumber][8].text is not None else ""
        versionString = "Version: " + root[itemNumber][9].text if root[itemNumber][9].text != "NONE" and root[itemNumber][9].text is not None else ""
        labelView.setText(saveString+buildString+gitString+docString+designString+imageString+langString+versionString)
        return True

    def warnBox(self, msg):
        msgBox = QMessageBox()
        msgBox.setText(str(msg))
        msgBox.setWindowTitle("Warnung")
        msgBox.exec()

    def testBox(self, msg):
        msgBox = QMessageBox()
        msgBox.setText(str(msg))
        msgBox.setWindowTitle("Test")
        return True

    def newDialog(self):
        window = QDialog()
        window.setWindowTitle("Neu...")
        formLayout = QFormLayout()

        submit = QPushButton()
        submit.setText("Hinzufügen")
        submit.clicked.connect(lambda: self.applyChanges([name.text(),code.text(),build.text(),git.text(),documentation.text(),design.text(),image.text(),logo.text(),language.text(),version.text()],window))

        abord = QPushButton()
        abord.setText("Abbrechen")
        abord.clicked.connect(lambda: window.close())

        window.setLayout(formLayout)

        name = QLineEdit()
        code = QLineEdit()
        build = QLineEdit()
        git = QLineEdit()
        documentation = QLineEdit()
        design = QLineEdit()
        image = QLineEdit()
        logo = QLineEdit()
        language = QLineEdit()
        version = QLineEdit()

        formLayout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)

        formLayout.addRow("Name: ", name)
        formLayout.addRow("Code: ", code)
        formLayout.addRow("Build: ", build)
        formLayout.addRow("Git: ", git)
        formLayout.addRow("Dokumentation: ", documentation)
        formLayout.addRow("Design: ", design)
        formLayout.addRow("Bilder: ", image)
        formLayout.addRow("Logo: ", logo)
        formLayout.addRow("Sprache: ", language)
        formLayout.addRow("Version: ", version)

        formLayout.addRow(abord, submit)

        window.exec()

    def editDialog(self, dictKey):
        window = QDialog()
        window.setWindowTitle("Ändern...")
        formLayout = QFormLayout()

        submit = QPushButton()
        submit.setText("Ändern")
        submit.clicked.connect(lambda: self.applyChanges([name.text(),code.text(),build.text(),git.text(),documentation.text(),design.text(),image.text(),logo.text(),language.text(),version.text()],window,dictKey))

        abord = QPushButton()
        abord.setText("Abbrechen")
        abord.clicked.connect(lambda: window.close())

        delete = QPushButton()
        delete.setText("Löschen")
        delete.clicked.connect(lambda: self.database.pop(dictKey) and self.refreshViews() and window.close())

        window.setLayout(formLayout)

        name = QLineEdit()
        name.setText(self.database[dictKey][0])
        code = QLineEdit()
        code.setText(self.database[dictKey][1])
        build = QLineEdit()
        build.setText(self.database[dictKey][2])
        git = QLineEdit()
        git.setText(self.database[dictKey][3])
        documentation = QLineEdit()
        documentation.setText(self.database[dictKey][4])
        design = QLineEdit()
        design.setText(self.database[dictKey][5])
        image = QLineEdit()
        image.setText(self.database[dictKey][6])
        logo = QLineEdit()
        logo.setText(self.database[dictKey][7])
        language = QLineEdit()
        language.setText(self.database[dictKey][8])
        version = QLineEdit()
        version.setText(self.database[dictKey][9])

        formLayout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)

        formLayout.addRow("Name: ", name)
        formLayout.addRow("Code: ", code)
        formLayout.addRow("Build: ", build)
        formLayout.addRow("Git: ", git)
        formLayout.addRow("Dokumentation: ", documentation)
        formLayout.addRow("Design: ", design)
        formLayout.addRow("Bilder: ", image)
        formLayout.addRow("Logo: ", logo)
        formLayout.addRow("Sprache: ", language)
        formLayout.addRow("Version: ", version)

        formLayout.addRow(delete)
        formLayout.addRow(abord, submit)

        window.exec()

    def applyChanges(self, entryList, window, dictKey=None):
        if dictKey != None:
            if entryList[0] == self.database[dictKey][0]:
                self.database[entryList[0]] = entryList
            else:
                del self.database[dictKey]
                self.database[entryList[0]] = entryList
        else:
            if entryList[0] == "":
                self.warnBox("Der Projektname darf nicht leer sein!")
                return False
            else:
                self.database[entryList[0]] = []
                for i in range(len(entryList)):
                    appendString = entryList[i] if entryList[i] != "" else "NONE"
                    self.database[entryList[0]].append(appendString)
        if not self.filename == "":
            self.saveProjectfile()
            self.refreshViews()
        else:
            self.saveAsProjectfile()
            self.importHandlerInit(self.frameLeft,self.filename)
        window.close()

    def refreshViews(self):
        self.displayInfo(self.frameLeft, self.frameRight)
        self.frameLeft.clear()
        for key in self.database:
            self.frameLeft.addItem(key)
        self.saveProjectfile()
        self.frameLeft.setMinimumWidth(self.frameLeft.sizeHintForColumn(0) + 10)
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
            f = open(self.filename, 'w+', 1000, 'utf-8')
            f.write(fileContent)
            f.close()
            return True
        except FileNotFoundError:
            self.saveAsProjectfile()
            return True
        except Exception as e:
            self.warnBox(e)
            return True

    def saveAsProjectfile(self):
        try:
            fileDialog = QFileDialog()
            fileDialog.setFileMode(QFileDialog.AnyFile)
            fileDialog.setDefaultSuffix(".pmdx")
            dialogFilename = fileDialog.getSaveFileName(self, 'Promasu Datenbank speichern', '.', 'Promasu Projectdatabase (*.pmdx)')
            fileContent = self.xmlWriter()
            if dialogFilename[0][-5:] != ".pmdx":
                filename = dialogFilename[0] + ".pmdx"
            else:
                filename = dialogFilename[0]
            f = open(filename, 'w+', 1000, 'utf-8')
            f.write(fileContent)
            f.close()
            self.filename = filename
            self.setWindowTitle("Promasu Manager - " + self.filename)
            return True
        except FileNotFoundError:
            self.saveAsProjectfile()
            return False
        except Exception as e:
            self.warnBox(e)
            return True

    def xmlWriter(self):
        dict = self.database
        fileContent = ""
        fileContent += "<database>\n"
        for entry in dict:
            fileContent += "    <project>\n"
            fileContent += "        <name>"+dict[entry][0]+"</name>\n" if dict[entry][0] != "NONE" and dict[entry][0] is not None else "        <name>NONE</name>\n"
            fileContent += "        <code>"+dict[entry][1]+"</code>\n" if dict[entry][1] != "NONE" and dict[entry][1] is not None else "        <code>NONE</code>\n"
            fileContent += "        <build>"+dict[entry][2]+"</build>\n" if dict[entry][2] != "NONE" and dict[entry][2] is not None else "        <build>NONE</build>\n"
            fileContent += "        <git>"+dict[entry][3]+"</git>\n" if dict[entry][3] != "NONE" and dict[entry][3] is not None else "        <git>NONE</git>\n"
            fileContent += "        <documentation>"+dict[entry][4]+"</documentation>\n" if dict[entry][4] != "NONE" and dict[entry][4] is not None else "        <documentation>NONE</documentation>\n"
            fileContent += "        <design>"+dict[entry][5]+"</design>\n" if dict[entry][5] != "NONE" and dict[entry][5] is not None else "        <design>NONE</design>\n"
            fileContent += "        <image>"+dict[entry][6]+"</image>\n" if dict[entry][6] != "NONE" and dict[entry][6] is not None else "        <image>NONE</image>\n"
            fileContent += "        <logo>"+dict[entry][7]+"</logo>\n" if dict[entry][7] != "NONE" and dict[entry][7] is not None else "        <logo>NONE</logo>\n"
            fileContent += "        <language>"+dict[entry][8]+"</language>\n" if dict[entry][8] != "NONE" and dict[entry][8] is not None else "        <language>NONE</language>\n"
            fileContent += "        <version>"+dict[entry][9]+"</version>\n" if dict[entry][9] != "NONE" and dict[entry][9] is not None else "        <version>NONE</version>\n"
            fileContent += "    </project>\n"
        fileContent += "</database>"
        return fileContent

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Tool()
    sys.exit(app.exec_())
