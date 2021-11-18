import numpy as np

class BvhJoint:
	def __init__(self, name, parent):
		self.name = name
		self.parent = parent
		self.offset = np.zeros(3)
		self.channels = []
		self.children = []

	def add_child(self, child):
		self.children.append(child)
