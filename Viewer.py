# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ViewerUI.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from OpenGLWidget import OpenGLWidget
from PyQt5 import QtCore, QtGui, QtWidgets

from Particles import *

class Ui_Motion_Viewer(object):
	def __init__(self, Motion_Viewer):
		Motion_Viewer.setObjectName("Motion_Viewer")
		Motion_Viewer.resize(800, 640)
		self.centralwidget = QtWidgets.QWidget(Motion_Viewer)
		self.centralwidget.setObjectName("centralwidget")
		self.openGLWidget = OpenGLWidget(self.centralwidget)
		self.openGLWidget.setGeometry(QtCore.QRect(40, 30, 720, 480))
		self.openGLWidget.setObjectName("openGLWidget")
		self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
		self.groupBox.setGeometry(QtCore.QRect(40, 510, 721, 101))
		self.groupBox.setTitle("")
		self.groupBox.setObjectName("groupBox")
		self.playButton = QtWidgets.QPushButton(self.groupBox)
		self.playButton.setGeometry(QtCore.QRect(20, 60, 80, 25))
		self.playButton.setObjectName("playButton")
		self.pauseButton = QtWidgets.QPushButton(self.groupBox)
		self.pauseButton.setGeometry(QtCore.QRect(110, 60, 80, 25))
		self.pauseButton.setObjectName("pauseButton")
		self.frameSlider = QtWidgets.QSlider(self.groupBox)
		self.frameSlider.setGeometry(QtCore.QRect(20, 30, 691, 20))
		self.frameSlider.setOrientation(QtCore.Qt.Horizontal)
		self.frameSlider.setObjectName("frameSlider")
		self.frameTextBox = QtWidgets.QSpinBox(self.groupBox)
		self.frameTextBox.setGeometry(QtCore.QRect(200, 60, 60, 26))
		self.frameTextBox.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
		self.frameTextBox.setObjectName("frameTextBox")
		Motion_Viewer.setCentralWidget(self.centralwidget)
		self.timer = QtCore.QTimer()

		self.retranslateUi(Motion_Viewer)
		QtCore.QMetaObject.connectSlotsByName(Motion_Viewer)

		self.playButton.clicked.connect(self.playButtonClicked)
		self.pauseButton.clicked.connect(self.pauseButtonClicked)
		self.setSlider()
		self.setTextbox()
		self.setTimer()

	def retranslateUi(self, Motion_Viewer):
		_translate = QtCore.QCoreApplication.translate
		Motion_Viewer.setWindowTitle(_translate("Motion_Viewer", "Motion Viewer"))
		self.playButton.setText(_translate("Motion_Viewer", "Play"))
		self.pauseButton.setText(_translate("Motion_Viewer", "Pause"))

	#Setting Widget
	def setSlider(self):
		slider = self.frameSlider
		slider.setRange(0, self.openGLWidget.maxframe-1)
		slider.setSingleStep(1)
		slider.valueChanged.connect(self.changeSlider)

	def setTextbox(self):
		textbox = self.frameTextBox
		textbox.setRange(0, self.openGLWidget.maxframe-1)
		textbox.setSingleStep(1)
		textbox.valueChanged.connect(self.changeTextbox)

	def setTimer(self):
		self.timer.timeout.connect(self.timeout)
		self.timer.setInterval(1000/self.openGLWidget.fps)

	#Widget handler
	def changeSlider(self):
		self.openGLWidget.curframe = self.frameSlider.value()
		self.frameTextBox.setValue(self.frameSlider.value())
		self.openGLWidget.run = True
		self.openGLWidget.repaint()

	def changeTextbox(self):
		self.openGLWidget.curframe = self.frameTextBox.value()
		self.frameSlider.setValue(self.frameTextBox.value())

	def timeout(self):
		self.openGLWidget.curframe += 1
		self.frameSlider.setValue(self.openGLWidget.curframe)

	def playButtonClicked(self) :
		self.timer.start()

	def pauseButtonClicked(self) :
		self.timer.stop()

if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	Motion_Viewer = QtWidgets.QMainWindow()
	ui = Ui_Motion_Viewer(Motion_Viewer)
	Motion_Viewer.show()
	sys.exit(app.exec_())

