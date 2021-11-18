from Skeleton import Skeleton
from Motion import Motion
from BvhJoint import BvhJoint
import numpy as np
import re


class BvhParser:
	def __init__(self, file):
		if file == '':
			print('Please set bvh file path and name')
			return 0
		self.joints = []
		self.root = None
		self.keyframes = None
		self.frames = 0
		self.fps = 0
		self.parse_file(file)

	# parse hierarchy
	def parse_hierarchy(self, text):
		lines = re.split('\\s*\\n+\\s*', text)

		joint_stack = []

		for line in lines:
			words = re.split('\\s+', line)
			instruction = words[0]

			if instruction == "JOINT" or instruction == "ROOT":
				parent = joint_stack[-1] if instruction == "JOINT" else None
				joint = BvhJoint(words[1], parent)
				if parent:
					parent.add_child(joint)
				joint_stack.append(joint)
				if instruction == "ROOT":
					self.root = joint_stack[-1]
			elif instruction == "CHANNELS":
				for i in range(2, len(words)):
					joint_stack[-1].channels.append(words[i])
			elif instruction == "OFFSET":
				for i in range(1, len(words)):
					joint_stack[-1].offset[i - 1] = float(words[i])
			elif instruction == "End":
				joint = BvhJoint(joint_stack[-1].name + "_end", joint_stack[-1])
				joint_stack[-1].add_child(joint)
				joint_stack.append(joint)
			elif instruction == '}':
				self.joints.append(joint_stack[-1])
				joint_stack.pop()

	def parse_motion(self, text):
		lines = re.split('\\s*\\n+\\s*', text)

		frame = 0
		for line in lines:
			if line == '':
				continue
			words = re.split('\\s+', line)

			if line.startswith("Frame Time:"):
				self.fps = round(1 / float(words[2]))
				continue
			if line.startswith("Frames:"):
				self.frames = int(words[1])
				continue

			if self.keyframes is None:
				self.keyframes = np.empty((self.frames, len(words)), dtype=np.float32)

			for angle_index in range(len(words)):
				self.keyframes[frame, angle_index] = float(words[angle_index])

			frame += 1

	def parse_string(self, text):
		hierarchy, motion = text.split("MOTION")
		self.parse_hierarchy(hierarchy)
		self.parse_motion(motion)

	def parse_file(self, path):
		with open(path, 'r') as f:
			self.parse_string(f.read())


	def getMotion(self, end=0, start=0):
		motion = Motion()

		if end == 0:
			end = self.frames

		motion.setSkeleton(self.root)
		motion.fps = self.fps
		for frame in range(start, end):
			motion.addPosture(frame, self.keyframes[frame])

		return motion






