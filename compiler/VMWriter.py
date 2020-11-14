class VMWriter(object):
	
	def __init__(self, source, inputFilename):
		self.COMMANDS = {
			'+': 'add',
			'-': 'sub',
			'&amp;': 'and',
			'&lt;': 'lt',
			'&gt;': 'gt',
			'=': 'eq',
			'|': 'or',
		}
		
		if source:
			self.f = open(f'./{source}/{inputFilename}.vm', 'w')
		else: 
			self.f = open(f'{inputFilename}.vm', 'w')
	
	def writePush(self, segment, index):
		if segment == 'VAR':
			segment = 'local'
		elif segment == 'ARG':
			segment = 'argument'
		elif segment == 'FIELD':
			segment = 'this'
		elif segment == 'STATIC':
			segment = 'static'
			
		self.f.write(f'push {segment} {index}\n')
	
	def writePop(self, segment, index):
		if segment == 'VAR':
			segment = 'local'
		elif segment == 'ARG':
			segment = 'argument'
		elif segment == 'FIELD':
			segment = 'this'
		elif segment == 'STATIC':
			segment = 'static'
			
		self.f.write(f'pop {segment} {index}\n')
	
	def writeArithmetic(self, command):
		if command in ['neg', 'not']:
			if command == 'neg':
				self.f.write('neg\n')
			else:
				self.f.write('not\n')
		elif command in ['*', '/']:
			if command == '*':
				self.writeCall("Math.multiply", 2)
			else:
				self.writeCall("Math.divide", 2)
		else:
			self.f.write(f'{self.COMMANDS[command]}\n')
	
	def writeLabel(self, label):
		self.f.write(f'label {label}\n')
	
	def writeGoto(self, label):
		self.f.write(f'goto {label}\n')
	
	def writeIf(self, label):
		self.f.write(f'if-goto {label}\n')
	
	def writeCall(self, name, nArgs):
		self.f.write(f'call {name} {nArgs}\n')
	
	def writeFunction(self, name, nLocals):
		self.f.write(f'function {name} {nLocals}\n')
	
	def writeReturn(self):
		self.f.write(f'return\n')
	
	def close(self):
		self.f.close()