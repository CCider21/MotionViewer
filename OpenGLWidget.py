
from BvhParser import BvhParser
from Motion import *
from PyQt5.QtWidgets import QApplication, QOpenGLWidget
from Draw import *
from Particles import *

gCamAng = 0.
gCamHeight = 1.0
gZoom = 1.0

file1 = './bvhfile/Walking001.bvh'
file2 = './bvhfile/HopOverObstacle001.bvh'
file3 = './bvhfile/Catwalk001.bvh'
file4 = './bvhfile/RunningOnBench001.bvh'

class OpenGLWidget(QOpenGLWidget):

	def  __init__(self, parent = None):
		super(OpenGLWidget,self).__init__(parent)

		#mouse XY
		self.curX = 0.
		self.curY = 0.
		self.jointname = "LeftForeArm"

		self.cube = None

		self.run = False
		self.motion1, self.motion2, self.motion3 = None,None,None

		self.motion = BvhParser(file1).getMotion()
		#self.timeWarpingSim()
		#self.motionStitchingSim()
		self.curframe = 0
		self.maxframe = self.motion.frames
		self.fps = self.motion.fps
		
		self.cubeSim()

	#########                      For simulation                      ##############
	def timeWarpingSim(self):
		self.motion1 = BvhParser(file2).getMotion()
		self.motion = timeWarping(self.motion1, linearFunc,2)
		self.maxframe = max(self.motion.frames, self.motion1.frames)
		self.fps = self.motion.fps

	def motionStitchingSim(self):
		walkMotion = BvhParser(file1).getMotion()
		hopMotion = BvhParser(file2).getMotion(300)
		self.motion = motionStitching(hopMotion, walkMotion, 150)
		self.maxframe = self.motion.frames
		self.fps = self.motion.fps

	def motionWarpingSim(self):
		walkMotion = BvhParser(file1).getMotion()
		hopMotion = BvhParser(file2).getMotion()
		self.hopPos = hopMotion.postures[600]
		self.motion1 = walkMotion
		self.motion = motionWarping(walkMotion, self.hopPos, 1200, 1150, 1250)
		self.maxframe = max(self.motion.frames, self.motion1.frames)
		self.fps = self.motion.fps

	def motionBlendingSim(self):
		self.motion = BvhParser(file4).getMotion(60,35)
		self.motion1 = BvhParser(file3).getMotion(466,435)

		self.motion2 = motionBlending(self.motion1, self.motion)	#Uniform
		#self.motion2 = motionBlending(self.motion1, self.motion, HermiteFunc)	#NonUniform
		self.maxframe = max(self.motion.frames, self.motion1.frames, self.motion2.frames)
		self.fps = self.motion.fps

	def cubeSim(self):
		self.cube = cube()
		self.maxframe = 1000
		self.curframe = 0
		self.fps = 60
	##################################################################################

	def initializeGL(self):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(90,1,1,1000)
		glEnable(GL_DEPTH_TEST)


	#Drawing Function
	def paintGL(self):
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		#at = self.motion.postures[self.curframe].rootPosition[:3,3]
		at = [0, 20, 80]
		eye = [10.0*np.sin(gCamAng)*gZoom, gCamHeight*gZoom, 10.0*np.cos(gCamAng)*gZoom]

		gluLookAt(at[0]+eye[0],at[1]+eye[1],at[2]+eye[2],at[0],at[1],at[2],0,1,0)
		drawGrid()

		glColor3ub(0, 255, 0)
		drawParticles(self.cube, self.fps, self.run)
		#drawMotion(self.motion, self.curframe)

		if (self.motion1 != None):
			glColor3ub(255, 0, 0)
			drawMotion(self.motion1, self.curframe)
		
		if (self.motion2 != None):
			glColor3ub(0, 0, 255)
			drawMotion(self.motion2, self.curframe)

		#self.drawPosture(self.hopPos)
		#self.drawLinearVelocity(self.motion)

	def drawLinearVelocity(self, motion):
		glColor3ub(0,255 ,0)
		if self.curframe != 0:
			curPosition = motion.getJointPosition(self.jointname, self.curframe)[:3, 3]
			prePosition = motion.getJointPosition(self.jointname, self.curframe - 1)[:3, 3]
			mag = (curPosition - prePosition) * motion.fps
			drawPoint(curPosition)
			drawLine(curPosition, curPosition + mag)

	#Mouse Event
	def mouseMoveEvent(self, event):
		global gCamHeight, gCamAng
		self.run = False

		if abs(event.x() - self.curX) > 10:
			if event.x() > self.curX:
				gCamAng += np.radians(5)
			else:
				gCamAng -= np.radians(5)
			self.curX = event.x()
			self.repaint()

		if abs(event.y() - self.curY) > 10:
			if event.y() > self.curY:
				gCamHeight += 1
			if event.y() < self.curY:
				gCamHeight -= 1
			self.curY = event.y()
			self.repaint()

	def wheelEvent(self, event):
		global gZoom
		self.run = False
		if event.angleDelta().y() > 0:
			gZoom -= 0.1
		else:
			gZoom += 0.1
		self.repaint()

	def mousePressEvent(self, event):
		self.curX = event.x()
		self.curY = event.y()


if	__name__ == "__main__" :
	app = QApplication(sys.argv)
	myWindow = OpenGLWidget()
	myWindow.show()
	app.exec_()


