#!/usr/bin/python3

from PySide2.QtWidgets import (QApplication, QLabel,
                               QPushButton, QSlider,
                               QLineEdit, QWidget, QVBoxLayout, QHBoxLayout,
                               QDialog, QGroupBox, QTabWidget, QErrorMessage,
                               QListWidgetItem, QGridLayout, QTextEdit,
                               QComboBox, QToolBar, QInputDialog, QAction,
                               QStackedWidget, QTextBrowser)
from PySide2.QtCore import (Qt, QThread, Signal, QDir)
from PySide2.QtGui import (QIcon, QMovie)
import sys, subprocess

class UpdatePrompt(QDialog):

    def __init__(self):
        super().__init__()
        self.makeView()
        return

    def makeView(self):
        layout = QVBoxLayout()
        btnLayout = QHBoxLayout()
        self.centStack = QStackedWidget()
        updateButton = QPushButton('Update')
        cancelButton = QPushButton('Cancel')
        notifyLabel = QLabel('There are updates scheduled')
        self.inputBox = QLineEdit()
        self.outputBox = QTextBrowser()
        #refreshIcon = QIcon.fromTheme('process-working')
        self.refreshIcon = QMovie('assets/spin3.gif')
        refreshAnimation = QLabel()

        layout.addWidget(notifyLabel)
        layout.addWidget(self.centStack)
        layout.addWidget(self.inputBox)
        layout.addLayout(btnLayout)
        btnLayout.addWidget(cancelButton)
        btnLayout.addWidget(updateButton)

        self.centStack.addWidget(refreshAnimation)
        self.centStack.addWidget(self.outputBox)
        refreshAnimation.setMovie(self.refreshIcon)
        refreshAnimation.setAlignment(Qt.AlignCenter)
        self.refreshIcon.start()

        self.inputBox.setEchoMode(QLineEdit.Password)
        self.inputBox.setFocus()
        self.inputBox.returnPressed.connect(self.pkgUpdates)
        updateButton.clicked.connect(self.pkgUpdates)
        cancelButton.clicked.connect(self.cancelUpdates)

        self.centStack.setCurrentIndex(1)
        notifyLabel.setAlignment(Qt.AlignTop)
        self.outputBox.setReadOnly(True)
        #self.outputBox.setAlignment(Qt.AlignTop)
        self.setWindowTitle('Package Updates')
        self.setLayout(layout)
        self.resize(450, 250)
        return

    def pkgUpdates(self):
        self.centStack.setCurrentIndex(0)
        self.refreshIcon.start()

        password = self.inputBox.text()

        if (password == ''):
            self.passError('The password field cannot be empty')
            return

        password = password.encode()
        result = subprocess.run(['sudo', '-S', 'apt-get', 'update'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, input=password)
        stdout = result.stdout.decode()
        currentText = self.outputBox.toPlainText()
        self.outputBox.setText('Running updates\n' + stdout)

        result = subprocess.run(['sudo', '-S', 'apt-get', 'upgrade', '-y'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, input=password)
        stdout = result.stdout.decode()
        currentText = self.outputBox.toPlainText()
        self.outputBox.setText(currentText + '\nRunning upgrades\n' + stdout)
       # result = subprocess.run(['sudo', 'apt', 'upgrade', '-y'],
       #                         stdout=subprocess.PIPE,
       #                         stderr=subprocess.STDOUT, input=password)
       # currentText = self.outputBox.toPlainText()
       # self.outputBox.setText(currentText + '\n' + stdout)

        #self.refreshIcon.stop()
        self.centStack.setCurrentIndex(1)
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
        self.reject()
        return



if __name__ == '__main__':
    app = QApplication([])
    view = UpdatePrompt()
    view.show()
    sys.exit(app.exec_())
