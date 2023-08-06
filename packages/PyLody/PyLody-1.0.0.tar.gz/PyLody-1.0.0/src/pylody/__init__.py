import os
from . import parser


class MelodyBuilder:
	def __init__(self, notes=None):
		if notes != None:
			if os.path.exists(notes):
				with open(notes, "r") as f:
					notes = f.read()
			
			self.elements = list(parser.parse(notes))
		else:
			self.elements = []
	
	def add(self, element):
		self.elements.append(element)
	
	def __iter__(self):
		return iter(self.elements)
	
	def __str__(self):
		return "\n".join(map(str, self.elements))
	def __repr__(self):
		return "MelodyBuilder: [" + ", ".join(map(repr, self.elements)) + "]"
	
	def play(self):
		for element in self:
			element.play()
