import numpy as np
from ViewerMath import *

def computeForce(sys):
	G = -9.8
	kd = 0.1
	for i in range(len(sys.particles)):
		p = sys.particles[i]
		force = np.zeros(3)

		force[1] += p.m * G

		force -= kd * np.array(p.v)

		#Dumped Spring Force
		for j in sys.linked[i]:
			adj = sys.particles[j]
			rest = vectorMagnitude(sys.rootPos[i], sys.rootPos[j])
			force -= springforce(p, adj, rest)
		p.f = force

def springforce(p1, p2, rest):
	ks = 1000
	kd = 100

	dx = np.array(p1.pos) - np.array(p2.pos)
	mag_dx = vectorMagnitude(dx)
	dv = np.array(p1.v) - np.array(p2.v)

	f = (ks*(mag_dx - rest) + kd*(np.dot(dv, dx.T)/mag_dx))*vectorNorm(dx)
	return f


def particleDerivative(sys):
	deri = []
	computeForce(sys)

	for p in sys.particles:
		deri.extend(p.v)
		tmp = np.array(p.f)/p.m
		deri.extend(list(tmp))
	return deri



def eulerStep(sys, h):
	deri = np.array(particleDerivative(sys))
	curState = np.array(sys.getState())
	sys.setState(curState + deri*h)
	detect = []
	while collisionDetection(sys, detect):
		h /= 2
		sys.setState(curState + deri*h)

	if len(detect) != 0:
		collisionResponse(sys, detect)

	sys.time = sys.time + h


def collisionDetection(sys, detect):
	P = np.array([0,0,0])
	N = np.array([0,1,0])

	w = 0.1
	flag = False
	for i in range(len(sys.particles)):
		p = sys.particles[i]
		xdotn = np.dot(p.pos-P, N.T)
		ndotv = np.dot(N, p.v.T)
		if (xdotn < w) and (ndotv < 0):
			detect.append(i)
			flag = True
	return flag

def collisionResponse(sys, detect):
	P = np.array([0,0,0])
	N = np.array([0,1,0])

	kr = 0.1
	for i in detect:
		p = sys.particles[i]
		Vn = np.array([0,p.v[1], 0])
		Vt = np.array([p.v[0], 0, p.v[2]])
		p.v = Vt - kr*Vn
