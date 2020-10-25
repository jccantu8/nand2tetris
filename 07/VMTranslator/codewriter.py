class CodeWriter(Object):

	def __init__(self, filename):
		pass

	#def setFileName(self, filename):
		#pass

	def writeArithmetic(self, command):
		if command == 'add':
			result = ''
			result += f''
		elif command == 'sub':
			pass
		elif command == 'neg':
			pass
		elif command == 'eq':
			pass
		elif command == 'gt':
			pass
		elif command == 'lt':
			pass
		elif command == 'and':
			pass
		elif command == 'or':
			pass	
		else:
			# Not
			pass

	def writePushPop(self, command, segment, index):
		if command == 'C_PUSH':
			result = ''
			result += f'@{index}\n'
			result += f'D=A\n'
			result += f'@SP\n'
			result += f'A=M\n'
			result += f'M=D\n'
			result += f'@SP\n'
			result += f'M=M+1\n'

			return result
		else:
			# C_POP
			pass

	#def close(self):
		#pass