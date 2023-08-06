import abc, winsound, time

class MelodyElement(abc.ABC):
	def __init__(self, **kwargs):
		for key, value in kwargs.items():
			setattr(self, key, value)
	
	@abc.abstractmethod
	def play(self): pass

class Block(MelodyElement):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.elements = []
	
	def __iter__(self):
		return iter(list(self.elements))
	
	def __str__(self):
		return str(self.repeattimes) + " {\n" + " " * 4 + (",\n" + " " * 4).join(map(repr, self.elements)) + "\n}"
	def __repr__(self):
		return "Block: " + str(self.repeattimes) + " { " + ", ".join(map(repr, self.elements)) + " }"
	
	def add(self, element):
		self.elements.append(element)
	
	def play(self):
		i = 0
		while i < self.repeattimes if self.repeattimes != "*" else True:
			for element in self:
				element.play()
			i += 1

class Pause(MelodyElement):
	def __str__(self):
		return "- " + str(self.duration)
	def __repr__(self):
		return "Pause: " + str(self.duration) + "ms"
	
	def play(self):
		time.sleep(self.duration / 1000)

class Note(MelodyElement):
	def __str__(self):
		return self.note[:1] + str(self.octave) + self.note[1:] + " " + str(self.duration)
	def __repr__(self):
		return "Note (note=" + self.note + ", octave=" + str(self.octave) + "): " + str(self.duration) + "ms"
	
	def play(self):
		winsound.Beep(round({
			"A"  : 27.50,
			"A#" : 29.13,
			"B"  : 30.87,
			"C"  : 32.70,
			"C#" : 34.65,
			"D"  : 36.95,
			"D#" : 38.88,
			"E"  : 41.21,
			"F"  : 43.65,
			"F#" : 46.25,
			"G"  : 49.00,
			"G#" : 51.90,
		}[self.note] * (2 ** self.octave)), self.duration)
