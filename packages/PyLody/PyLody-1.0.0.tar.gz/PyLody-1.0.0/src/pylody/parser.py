import re, collections, enum
from . import elements

class TokenType(enum.Enum):
	PAUSE       = 0
	NOTE        = 1
	BLOCK_START = 2
	BLOCK_END   = 3

Token = collections.namedtuple("Token", "type value")

def parse(notes):
	blocks = []
	for token in tokenize(re.sub(r"\\.+\\", "", notes, re.MULTILINE)):
		if token.type == TokenType.PAUSE:
			element = elements.Pause(duration=token.value["duration"])
		elif token.type == TokenType.NOTE:
			element = elements.Note(note=token.value["note"],
									octave=token.value["octave"],
									duration=token.value["duration"])
		elif token.type == TokenType.BLOCK_START:
			blocks.append(elements.Block(repeattimes=token.value["repeattimes"]))
			continue
		elif token.type == TokenType.BLOCK_END:
			element = blocks.pop()
		if len(blocks) > 0:
			blocks[-1].add(element)
		else:
			yield element

def tokenize(notes):
	for match in re.findall(r"((\w)(\d)(#?)|\-)\s(\d+)|(\d|\*).*({)|(})", notes, re.MULTILINE):
		tknval = {}
		if match[0] == "-":
			tkntype = TokenType.PAUSE
			tknval["duration"] = int(match[4])
		elif match[0] != "":
			tkntype = TokenType.NOTE
			tknval["note"] = match[1] + match[3]
			tknval["octave"] = int(match[2])
			tknval["duration"] = int(match[4])
		elif match[6] == "{":
			tkntype = TokenType.BLOCK_START
			tknval["repeattimes"] = int(match[5]) if match[5] != "*" else match[5]
		elif match[7] == "}":
			tkntype = TokenType.BLOCK_END
		yield Token(tkntype, tknval)
