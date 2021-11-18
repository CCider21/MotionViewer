from Posture import *
from Skeleton import Skeleton

class Motion:
	def __init__(self):
		self.skeleton = None
		self.postures = []
		self.curframe = 0
		self.frames = 0
		self.fps = 0

	def addPosture(self, frame, framedata):
		posture = Posture(self.skeleton, framedata)
		self.postures.insert(frame, posture)
		self.frames = self.frames + 1

	def updataPosture(self, frame, framedata):
		posture = Posture(self.skeleton, framedata)
		self.postures[frame] = posture

	def setSkeleton(self, root):
		self.skeleton = Skeleton(root)

	def getCurPosture(self):
		return self.postures[self.curframe]

	def getJointPosition(self, jointname, frame):
		jointPos = np.identity(4)
		if frame < 0 | frame > (self.frames-1):
			return jointPos

		posture = self.postures[frame]
		joint = self.skeleton.getJoint(jointname)
		while joint != None:
			jointPos = posture.getRotationMatirx(joint) @ jointPos
			jointPos = posture.getTransMatrix(joint) @ jointPos
			joint = joint.parent

		jointPos = posture.rootPosition @ jointPos
		return jointPos

	def appendPosture(self, posture):
		self.postures.append(posture)

def linearFunc(frames, k):
	return np.arange(0, frames-1, k)

def HermiteFunc(frames):
	x_axis = np.arange(0, 1, 1/frames)
	y_axis = list()

	for t in x_axis:
		H1 = -2*np.power(t,3) + 3*np.power(t,2)
		H2 = np.power(t,3) - 2*np.power(t,2) + t
		H3 = np.power(t,3) - np.power(t,2)

		f1 = 1
		f2 = 2

		y_axis.append(H1 + f1*H2 + f2*H3)

	time = np.array(y_axis) * frames

	return time

def timeWarping(motion, func, k=1):
	newMotion = Motion()
	newMotion.skeleton = motion.skeleton
	newMotion.fps = motion.fps

	#Time Scaling
	if func == linearFunc:
		time = func(motion.frames, k)
	elif func == HermiteFunc:
		time = func(motion.frames)

	#Interpolate postures
	for t in time:
		frame = int(t)
		alpha = t - int(t)
		p0 = motion.postures[frame]
		if frame == (motion.frames-1):
			p1 = motion.postures[frame]
		else:
			p1 = motion.postures[frame+1]

		newPosture = p0.interpolation(p1, alpha)

		newMotion.appendPosture(newPosture)
		newMotion.frames += 1

	return newMotion

def motionWarping(motion, posture, frame, start, end):
	newMotion = Motion()
	newMotion = copy.deepcopy(motion)

	diffPos = postureDiff(motion.postures[frame], posture)

	if frame == start:
		offset = list(np.arange(1,0,-1/(end-frame)))
	elif frame == end:
		offset = list(np.arange(0,1,1/(frame-start)))
	else:
		offset = list(np.arange(0,1,1/(frame-start))) + list(np.arange(1,0,-1/(end-frame)))
	
	for i in range(len(offset)):
		newPos = postureAdd(motion.postures[start+i], postureScale(diffPos,offset[i]))
		newMotion.postures[start+i] = newPos

	return newMotion

def motionStitching(motion1, motion2, frameNum):
	newMotion = copy.deepcopy(motion1)

	diffPos = postureDiff(motion2.postures[0], motion1.postures[motion1.frames-1])
	rootname = diffPos.skeleton.root.name
	diffOri = math.newRootOrientation(diffPos.rotationMatrix[rootname])
	offset = np.arange(1,0,-1/frameNum)

	for i in range(len(offset)):
		newPos = postureAdd(motion2.postures[i], postureScale(diffPos,offset[i]))
		newMotion.postures.append(newPos)
		newMotion.frames += 1

	for i in range(len(offset), motion2.frames):
		pos_i = copy.deepcopy(motion2.postures[i])
		newMotion.postures.append(pos_i)
		newMotion.frames += 1

	#root align
	for i in range(motion2.frames):
		root_i = motion2.postures[i].rootPosition
		root_0 = motion2.postures[0].rootPosition
		m1_endRoot = motion1.postures[motion1.frames-1].rootPosition
		pos = newMotion.postures[i+motion1.frames]

		pos.transMatrix = copy.copy(motion1.postures[0].transMatrix)

		tmp = (diffOri@(root_i-root_0) + m1_endRoot)[:3,3]
		tmp[1] = pos.rootPosition[1,3]
		pos.rootPosition[:3,3] = tmp
		pos.rotationMatrix[rootname] = diffOri @ motion2.postures[i].rotationMatrix[rootname]

	return newMotion


def motionBlending(motion1, motion2, func=linearFunc):
	newMotion = Motion()
	newMotion.frames = int((motion1.frames + motion2.frames)/2)
	newMotion.fps = motion1.fps

	m1 = timeWarping(motion1, linearFunc, (motion1.frames-1)/newMotion.frames)
	m2 = timeWarping(motion2, linearFunc, (motion2.frames-1)/newMotion.frames)

	diffPos = postureDiff(m2.postures[0], m1.postures[0])
	for i in range(m2.frames):
		m2.postures[i].rootPosition += diffPos.rootPosition


	for i in range(newMotion.frames):
		s = 0.5*np.cos(np.pi/(newMotion.frames)*i)+0.5
		m1_pos = m1.postures[i]
		m2_pos = m2.postures[i]
		newPos = m2_pos.interpolation(m1_pos, s)

		newMotion.postures.append(newPos)

	del m1
	del m2
	blendMotion = timeWarping(newMotion, func)

	return blendMotion

def motionAdd(motion1, motion2):
	newMotion = copy.deepcopy(motion1)

	for pos in motion2.postures:
		newPos = copy.deepcopy(pos)
		newMotion.postures.append(newPos)
		newMotion.frames +=1

	return newMotion




