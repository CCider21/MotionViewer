from Skeleton import Skeleton
import ViewerMath as math
import numpy as np
import copy

class Posture:

	def __init__(self, skeleton = Skeleton(), framedata=[]):
		self.skeleton = skeleton
		self.framedata = framedata
		self.rotationMatrix = {}
		self.transMatrix = {}
		self.rootPosition = np.identity(4)

		if (len(framedata) != 0) & (skeleton.root != None):
			self.setRootPosition()
			self.saveTransAndRotationMatrix()

	def getRotationMatirx(self, joint):
		return self.rotationMatrix[joint.name]

	def getTransMatrix(self, joint):
		return self.transMatrix[joint.name]

	def saveTransAndRotationMatrix(self):
		index = 3

		for joint in self.skeleton.joints:
			angChannel = []
			angData = []
			if '_end' not in joint.name:
				if joint == self.skeleton.root:
					angChannel = joint.channels[3:]
				else:
					angChannel = joint.channels
				angData = self.framedata[index:index+3]

				R = self.makeRotationMatrix(angData, angChannel)
				T = self.makeTransMatrix(joint.offset)
				self.rotationMatrix[joint.name] = R
				self.transMatrix[joint.name] = T

				#if joint == self.skeleton.root:
				#	self.transMatrix[joint.name] = T + self.rootPosition
				#else:
				#	self.transMatrix[joint.name] = T

				index += 3

	def makeTransMatrix(self, offset):
		M = np.identity(4)
		M[:3,3] = offset[:3]
		return M

	def makeRotationMatrix(self, angData, angChannel):
		R = [0, 0, 0]
		M = np.identity(4)

		Rx = math.getRx(angData[angChannel.index('Xrotation')])
		Ry = math.getRy(angData[angChannel.index('Yrotation')])
		Rz = math.getRz(angData[angChannel.index('Zrotation')])

		R[angChannel.index('Xrotation')] = Rx
		R[angChannel.index('Yrotation')] = Ry
		R[angChannel.index('Zrotation')] = Rz

		M[:3,:3] = R[0] @ R[1] @ R[2]
		return M

	def setRootPosition(self):
		xyzPosition = np.zeros(3)
		posData = self.framedata[:3]
		posChannel = self.skeleton.root.channels[:3]

		xyzPosition[0] = posData[posChannel.index('Xposition')]
		xyzPosition[1] = posData[posChannel.index('Yposition')]
		xyzPosition[2] = posData[posChannel.index('Zposition')]

		self.rootPosition[:3,3] = xyzPosition

	def interpolation(self, p1, alpha):
		p0 = self
		posture = Posture(p0.skeleton)
		posture.transMatrix = p0.transMatrix

		for joint in p0.rotationMatrix.keys():
			R0 = p0.rotationMatrix[joint]
			R1 = p1.rotationMatrix[joint]
			R = math.Slerp(R0, R1, alpha)

			posture.rotationMatrix[joint] = R

		rootPos = math.interpolateTrans(p0.rootPosition, p1.rootPosition, alpha)
		posture.rootPosition = rootPos

		return posture

#pos1 + pos2
def postureAdd(pos1, pos2):
	posture = copy.deepcopy(pos1)
	posture.framedata = []
	posture.rotationMatrix = {}
	#posture = Posture(pos1.skeleton)
	#posture.transMatrix = pos1.transMatrix

	for joint in pos1.rotationMatrix.keys():
		Ro = pos1.rotationMatrix[joint]
		Rd = pos2.rotationMatrix[joint]

		posture.rotationMatrix[joint] = Ro@Rd

	posture.rootPosition = pos1.rootPosition + pos2.rootPosition
	return posture

#pos2 - pos1 = diff
def postureDiff(pos1, pos2):
	posture = copy.deepcopy(pos1)
	posture.framedata = []
	posture.rotationMatrix = {}

	for joint in pos1.rotationMatrix.keys():
		Ro1 = pos1.rotationMatrix[joint]
		Ro2 = pos2.rotationMatrix[joint]

		posture.rotationMatrix[joint] = Ro1.T @ Ro2

	posture.rootPosition = pos2.rootPosition - pos1.rootPosition
	return posture

# c * pos
def postureScale(pos, c):
	posture = copy.deepcopy(pos)
	posture.framedata = []
	posture.rotationMatrix = {}

	for joint in pos.rotationMatrix.keys():
		R = pos.rotationMatrix[joint]
		posture.rotationMatrix[joint] = math.Slerp(np.identity(4), R, c)

	posture.rootPosition = c * pos.rootPosition
	return posture
