

class Skeleton:
	def __init__(self, root=None):
		self.root = root
		if root != None:
			self.joints = self.saveJointList(root)

	def getJoint(self, name):
		for joint in self.joints:
			if joint.name == name:
				return joint


	def saveJointList(self, root):
		stack = []
		visited = []

		stack.append(root)
		while stack:
			joint =stack.pop()
			if joint not in visited:
				visited.append(joint)
				for child in reversed(joint.children):
					stack.append(child)
		return visited

