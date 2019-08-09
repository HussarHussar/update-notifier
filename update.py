#!/usr/bin/python3

from PySide2.QtWidgets import (QApplication, QLabel,
                               QPushButton, QSlider,
                               QLineEdit, QWidget, QVBoxLayout, QHBoxLayout,
                               QDialog, QGroupBox, QTabWidget, QErrorMessage,
                               QListWidgetItem, QGridLayout, QTextEdit,
                               QComboBox, QToolBar, QInputDialog, QAction,
                               QStackedWidget, QTextBrowser)
from PySide2.QtCore import (Qt, QThread, Signal, QDir, QProcess,
                            QCoreApplication)
from PySide2.QtGui import (QIcon, QMovie)
import sys, subprocess, trio

class UpdatePrompt(QDialog):

    def __init__(self):
        super().__init__()
        self.makeView()
        return

    def makeView(self):
        layout = QVBoxLayout()
        btnLayout = QHBoxLayout()
        self.centStack = QStackedWidget()
        self.updateButton = QPushButton('Update')
        self.cancelButton = QPushButton('Cancel')
        notifyLabel = QLabel('There are upgrades scheduled')
        self.inputBox = QLineEdit()
        self.outputBox = QTextBrowser()
        #refreshIcon = QIcon.fromTheme('process-working')
        self.refreshIcon = QMovie('assets/spin3.gif')
        refreshAnimation = QLabel()

        layout.addWidget(notifyLabel)
        layout.addWidget(self.centStack)
        layout.addWidget(self.inputBox)
        layout.addLayout(btnLayout)
        btnLayout.addWidget(self.cancelButton)
        btnLayout.addWidget(self.updateButton)

        self.centStack.addWidget(refreshAnimation)
        self.centStack.addWidget(self.outputBox)
        refreshAnimation.setMovie(self.refreshIcon)
        refreshAnimation.setAlignment(Qt.AlignCenter)
        self.refreshIcon.start()

        self.inputBox.setEchoMode(QLineEdit.Password)
        self.inputBox.setFocus()
        self.inputBox.returnPressed.connect(self.pkgUpdates)
        self.updateButton.clicked.connect(self.pkgUpdates)
        self.cancelButton.clicked.connect(self.cancelUpdates)
        self.updateButton.setDefault(True)

        self.centStack.setCurrentIndex(1)
        notifyLabel.setAlignment(Qt.AlignTop)
        self.outputBox.setReadOnly(True)
        #self.outputBox.setAlignment(Qt.AlignTop)
        self.setWindowTitle('Package Upgrades')
        self.setLayout(layout)
        self.resize(450, 250)
        return

    async def asetup(self, password):
        async with trio.open_nursery() as nursery:
            finishedState = trio.Event()
            nursery.start_soon(self.upProc, password, 'update', finishedState)
            #nursery.start_soon(self.KEAlive, finishedState)
        return

    async def upProc(self, password, cmd, finishedState):
        proc = await trio.open_process(['sudo', '-S', 'apt-get', cmd, '-y'],
                       stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT)
        await proc.stdin.send_all((password + '\n').encode())

        while (proc.poll() == None):
            QCoreApplication.processEvents()
            await trio.sleep(0.1)

        result = ''
        result = await self.pullOutput(proc)
        self.appendToOutput(result)
        proc.terminate()

        if (cmd == 'update'):
            await self.upProc(password, 'upgrade', finishedState)
            finishedState.set()
        return

    async def pullOutput(self, proc):
        x = await proc.stdout.receive_some()
        x = x.decode()
        result = ''
        while (x != ''):
            QCoreApplication.processEvents()
            result = result + x
            x = await proc.stdout.receive_some()
            x = x.decode()
        return result

    async def KEAlive(self, finishedState):
        while finishedState.is_set():
            QCoreApplication.processEvents()
            trio.sleep(0.1)
        return

        return

    def appendToOutput(self, add):
        currentText = self.outputBox.toPlainText()
        self.outputBox.setText(currentText + 'Running updates\n' + add + '\n')
        print (add)
        return

    def pkgUpdates(self):
        self.centStack.setCurrentIndex(0)
        self.refreshIcon.start()
        QCoreApplication.processEvents()

        password = self.inputBox.text()

        if (password == ''):
            self.passError('The password field cannot be empty')
            return

        self.inputBox.clear()
        self.inputBox.setDisabled(True)
        self.updateButton.setDisabled(True)
        trio.run(self.asetup, password)
        self.centStack.setCurrentIndex(1)
        self.refreshIcon.stop()
        self.updateButton.setDisabled(False)
        self.inputBox.setDisabled(False)
        return

    def passError(self, s):
        passError = QDialog(self)
        msg = QLabel(s)
        layout = QVBoxLayout()
        layout.addWidget(msg)
        passError.setLayout(layout)

        okBtn = QPushButton('OK')
        okBtn.clicked.connect(passError.reject)
        layout.addWidget(okBtn)

        passError.exec_()
        return

    def cancelUpdates(self):
        #Needs way of closing subprocess during async run
        self.reject()
        return



if __name__ == '__main__':
    app = QApplication([])
    view = UpdatePrompt()
    view.show()
    sys.exit(app.exec_())
