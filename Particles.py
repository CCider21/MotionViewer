from Solver import *
import copy


class Particle:
	def __init__(self):
		self.pos = [0, 0, 0]
		self.v = [0, 0, 0]
		self.f = 0
		self.m = 0
		self.adj = []


class ParticleSystem:
	def __init__(self):
		self.particles = []
		self.time = 0
		self.linked = []
		self.rootPos = []

	def getPos(self):
		pos = []
		for p in self.particles:
			pos.append(p.pos)
		return pos


	def getState(self):
		state = []
		for p in self.particles:
			state.extend(p.pos)
			state.extend(p.v)

		return state

	def setState(self, data):
		i = 0
		for p in self.particles:
			p.pos = data[i:i+3]
			p.v = data[i+3:i+6]
			i += 6

	def setAdjParticles(self):
		for i in range(len(self.particles)):
			p = self.particles[i]
			adj = self.linked[i]

			for index in adj:
				p.adj.append(self.particles[index])


def cube():
	p1 = Particle()
	p2 = Particle()
	p3 = Particle()
	p4 = Particle()
	p5 = Particle()
	p6 = Particle()
	p7 = Particle()
	p8 = Particle()

	offset = np.array([0, 60, 0])

	p1.pos = [5., 2., 0.] + offset
	p2.pos = [5., 9., 7.] + offset
	p3.pos = [-5., 7., 7.] + offset
	p4.pos = [-5., 0., 0.] + offset
	p5.pos = [5., 9., -7.] + offset
	p6.pos = [5., 16., 0.] + offset
	p7.pos = [-5., 14., 0.] + offset
	p8.pos = [-5., 7., -7.] + offset

	p1.m = 5
	p2.m = 5
	p3.m = 5
	p4.m = 5
	p5.m = 5
	p6.m = 5
	p7.m = 5
	p8.m = 5

	p1.f = [100, 0, 0]
	p2.f = [100, 0, 0]
	p3.f = [100, 0, 0]
	p4.f = [100, 0, 0]

	sys = ParticleSystem()
	sys.particles.append(p1)
	sys.particles.append(p2)
	sys.particles.append(p3)
	sys.particles.append(p4)
	sys.particles.append(p5)
	sys.particles.append(p6)
	sys.particles.append(p7)
	sys.particles.append(p8)

	sys.linked = [[1,2,3,4,5,7],
				  [0,2,3,4,5,6],
				  [0,1,3,5,6,7],
				  [0,1,2,4,6,7],
				  [0,1,3,5,6,7],
				  [0,1,2,4,6,7],
				  [1,2,3,4,5,7],
				  [0,2,3,4,5,6]]

	sys.setAdjParticles()
	sys.rootPos = sys.getPos()

	return sys
