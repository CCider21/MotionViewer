import numpy as np
from pyquaternion import Quaternion

def getRx(xAng=0):
	xAng = xAng*(np.pi/180)
	Rx =np.array([[1,0,0],
				[0,np.cos(xAng),-np.sin(xAng)],
				[0,np.sin(xAng),np.cos(xAng)]])
	return Rx

def getRy(yAng=0):
	yAng = yAng*(np.pi/180)
	Ry =np.array([[np.cos(yAng),0,np.sin(yAng)],
				[0,1,0],
				[-np.sin(yAng),0,np.cos(yAng)]])
	return Ry

def getRz(zAng=0):
	zAng = zAng*(np.pi/180)
	Rz =np.array([[np.cos(zAng),-np.sin(zAng),0],
				[np.sin(zAng),np.cos(zAng),0],
				[0,0,1]])
	return Rz

def Slerp(R1, R2, t):
	R = np.identity(4)
	q1 = Quaternion(matrix=R1)
	q2 = Quaternion(matrix=R2)

	q = Quaternion.slerp(q1, q2, t)
	R[:3,:3] = q.rotation_matrix
	return R

def interpolateTrans(T0, T1, t):
	M = np.identity(4)
	M[:3,3] = T0[:3,3]*t + T1[:3,3]*(1-t)
	return M

def matrix2vector(R):
	vector = np.zeros(3)
	theta = np.arccos((R[0,0]+R[1,1]+R[2,2]-1)/2)
	vector[0] = (R[2,1]-R[1,2])/(2*np.sin(theta))
	vector[1] = (R[0,2]-R[2,0])/(2*np.sin(theta))
	vector[2] = (R[1,0]-R[0,1])/(2*np.sin(theta))
	return vector, theta


def newRootOrientation(R):
	v, theta = matrix2vector(R)
	v[0] = 0.
	v[2] = 0.
	q = Quaternion(axis=v, radians=theta)

	M = np.identity(4)
	M[:3,:3] = q.rotation_matrix
	return M

def vectorMagnitude(v1, v2=np.zeros(3)):
	dv = np.array(v1) - np.array(v2)

	return np.sqrt(np.sum(dv**2))

def vectorNorm(v):
	mag = vectorMagnitude(v)
	norm = np.array(v)/mag

	return norm


