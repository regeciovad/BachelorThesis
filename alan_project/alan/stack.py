class Stack(object):

	def __init__(self):
		self._stack = []

	def is_empty(self):
		return self._stack == []

	def push(self, item):
		self._stack.append(item)

	def pop(self):
		return self._stack.pop()

	def get_stack(self):
		return self._stack