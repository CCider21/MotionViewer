from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
from Particles import *
import time

def drawGrid():
	halflength = 500.0
	distance = 20.0

	#테두리 그리기
	glBegin(GL_QUADS)
	glColor3f(0.5, 0.5, 0.5)
	glVertex3f(halflength, -0.01, halflength)
	glVertex3f(halflength, -0.01, -halflength)
	glVertex3f(-halflength, -0.01, -halflength)
	glVertex3f(-halflength, -0.01, halflength)
	glEnd()

	#격자 그리기
	glBegin(GL_LINES)
	glColor3f(0.8,0.8,0.8)
	for i in np.arange(-halflength, halflength+distance, distance):
		glVertex3f(i, 0, -halflength)
		glVertex3f(i, 0, halflength)

		glVertex3f(-halflength, 0, i)
		glVertex3f(halflength, 0, i)
	glEnd()

def drawMotion(motion, curframe):
	if curframe < motion.frames:
		glPushMatrix()
		curPosture = motion.postures[curframe]
		glMultMatrixf(curPosture.rootPosition.T)
		drawBone(curPosture.skeleton.root, curPosture)
		glPopMatrix()

def drawPosture(posture):
	glPushMatrix()
	glMultMatrixf(posture.rootPosition.T)
	drawBone(posture.skeleton.root, posture)
	glPopMatrix()

def drawBone(joint, posture):
	if '_end' not in joint.name:
		glPushMatrix()

		glMultMatrixf(posture.getTransMatrix(joint).T)
		glMultMatrixf(posture.getRotationMatirx(joint).T)

		for child in joint.children:
			drawLine([0,0,0],child.offset)

		for child in joint.children:
			drawBone(child, posture)
		glPopMatrix()


def drawLine(start, end):
	glBegin(GL_LINES)
	glVertex3f(start[0],start[1],start[2])
	glVertex3f(end[0], end[1], end[2])
	glEnd()

def drawPoint(point):
	glColor3ub(255,0,0)
	length = 2.0

	glBegin(GL_LINES)
	glVertex3f(point[0]+length, point[1]+length, point[2])
	glVertex3f(point[0]-length, point[1]-length, point[2])

	glVertex3f(point[0]-length, point[1]+length, point[2])
	glVertex3f(point[0]+length, point[1]-length, point[2])
	glEnd()



def LimbIK(self):
	#inverse kinematics
	self.motion.inverseKinematics()
	glMultMatrixf(self.motion.A.T)
	axis = self.motion.Axis0
	glRotatef(self.motion.A_diff*180/np.pi,axis[0],axis[1],axis[2])

	glColor3ub(0,255,0)
	self.drawBone(self.motion.Ajoint)


def drawParticles(sys, fps, run):
	h = 0.002
	step = int(1/(fps*h))
	if run == True:
		for i in range(step):
			start = time.time()
			eulerStep(sys, h)
			#print(time.time() - start)

	for p in sys.particles:
		for adj in p.adj:
			drawLine(p.pos, adj.pos)


#render skel file

def drawCube(size):
	glScaled(size[0], size[1], size[2])

	n = np.array( [[-1.0, 0.0, 0.0],
					[0.0, 1.0, 0.0],
					[1.0, 0.0, 0.0],
					[0.0, -1.0, 0.0],
					[0.0, 0.0, 1.0],
					[0.0, 0.0, -1.0]],
					dtype=GLfloat)

	faces = np.array([[0, 1, 2, 3],
					[3, 2, 6, 7],
					[7, 6, 5, 4],
					[4, 5, 1, 0],
					[5, 6, 2, 1],
					[7, 4, 0, 3]],
					dtype=GLint)

	v = np.array([[-.5, -.5, -.5],
				[-.5, -.5, .5],
				[-.5, .5, .5],
				[-.5, .5, -.5],
				[.5, -.5, -.5],
				[.5, -.5, .5],
				[.5, .5, .5],
				[.5, .5, -.5]],
				dtype=GLfloat)

	for i in range(0,6):
		glBegin(GL_QUADS)
		glNormal3fv(n[i])
		glVertex3fv(v[faces[i][0]])
		glVertex3fv(v[faces[i][1]])
		glVertex3fv(v[faces[i][2]])
		glVertex3fv(v[faces[i][3]])
		glEnd()
