class Stack(object):

	def __init__(self):
		self._stack = []

	def is_empty(self):
		return self._stack == []

	def push(self, item):
		self._stack.append(item)

	def pop(self):
		if not self.is_empty():
			return self._stack.pop()

	def get_stack(self):
		return str(self._stack)

	def get_topmost(self):
		if self.is_empty():
			return None
		else:
			return self._stack[-1]