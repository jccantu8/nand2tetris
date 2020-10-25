class CodeWriter(object):

	def __init__(self):
		self._equal_label_counter = 0
		self._less_than_label_counter = 0
		self._greater_than_label_counter = 0
		self._pop_temp_counter = 0
		self._push_temp_counter = 0
		self._return_counter = 0
		self._return_frame_counter = 0
		self._return_ret_counter = 0
		
		self._POINTERSLIST = {
			"local": "LCL",
			"argument": "ARG",
			"this": "THIS",
			"that": "THAT",
			}

	def setFileName(self, filename):
		self._filename = filename

	def writeArithmetic(self, command):
		if command == 'add':
			result = ''
			result += f'@SP //add\n'
			result += f'M=M-1\n'
			result += f'A=M\n'
			result += f'D=M\n'
			result += f'A=A-1\n'
			result += f'M=D+M\n'
			
			return result
		elif command == 'sub':
			result = ''
			result += f'@SP //sub\n'
			result += f'M=M-1\n'
			result += f'A=M\n'
			result += f'D=M\n'
			result += f'A=A-1\n'
			result += f'M=M-D\n'
			
			return result
		elif command == 'neg':
			result = ''
			result += f'@SP //neg\n'
			result += f'A=M\n'
			result += f'A=A-1\n'
			result += f'M=-M\n'
			
			return result
		elif command == 'eq':
			self._equal_label_counter += 1
			
			result = ''
			
			# Make @SP address correctly
			result += f'@SP //eq\n'
			result += f'M=M-1\n'
			result += f'A=M\n'
			result += f'D=M\n'
			result += f'A=A-1\n'
			result += f'D=D-M\n'
			result += f'@EQUAL_LABEL_{self._equal_label_counter}\n'
			result += f'D;JEQ\n'
			result += f'@SP\n'
			result += f'A=M-1\n'
			result += f'M=0\n'
			result += f'@EQUAL_LABEL_{self._equal_label_counter}_END\n'
			result += f'0;JMP\n'
			result += f'(EQUAL_LABEL_{self._equal_label_counter})\n'
			result += f'@SP\n'
			result += f'A=M-1\n'
			result += f'M=-1\n'
			result += f'(EQUAL_LABEL_{self._equal_label_counter}_END)\n'
			
			return result
		elif command == 'gt':
			self._greater_than_label_counter += 1
			
			result = ''
			result += f'@SP //gt\n'
			result += f'M=M-1\n'
			result += f'A=M\n'
			result += f'D=M\n'
			result += f'A=A-1\n'
			result += f'D=M-D\n'
			result += f'@GREATER_THAN_LABEL_{self._greater_than_label_counter}\n'
			result += f'D;JGT\n'
			result += f'@SP\n'
			result += f'A=M-1\n'
			result += f'M=0\n'
			result += f'@GREATER_THAN_LABEL_{self._greater_than_label_counter}_END\n'
			result += f'0;JMP\n'
			result += f'(GREATER_THAN_LABEL_{self._greater_than_label_counter})\n'
			result += f'@SP\n'
			result += f'A=M-1\n'
			result += f'M=-1\n'
			result += f'(GREATER_THAN_LABEL_{self._greater_than_label_counter}_END)\n'
			
			return result
		elif command == 'lt':
			self._less_than_label_counter += 1
			
			result = ''
			result += f'@SP //lt\n'
			result += f'M=M-1\n'
			result += f'A=M\n'
			result += f'D=M\n'
			result += f'A=A-1\n'
			result += f'D=M-D\n'
			result += f'@LESS_THAN_LABEL_{self._less_than_label_counter}\n'
			result += f'D;JLT\n'
			result += f'@SP\n'
			result += f'A=M-1\n'
			result += f'M=0\n'
			result += f'@LESS_THAN_LABEL_{self._less_than_label_counter}_END\n'
			result += f'0;JMP\n'
			result += f'(LESS_THAN_LABEL_{self._less_than_label_counter})\n'
			result += f'@SP\n'
			result += f'A=M-1\n'
			result += f'M=-1\n'
			result += f'(LESS_THAN_LABEL_{self._less_than_label_counter}_END)\n'
			
			return result
		elif command == 'and':
			result = ''
			result += f'@SP //and\n'
			result += f'M=M-1\n'
			result += f'A=M\n'
			result += f'D=M\n'
			result += f'A=A-1\n'
			result += f'M=M&D\n'
			
			return result
		elif command == 'or':
			result = ''
			result += f'@SP //or\n'
			result += f'M=M-1\n'
			result += f'A=M\n'
			result += f'D=M\n'
			result += f'A=A-1\n'
			result += f'M=D|M\n'
			
			return result	
		else:
			# Not
			result = ''
			result += f'@SP //not\n'
			result += f'A=M\n'
			result += f'A=A-1\n'
			result += f'M=!M\n'
			
			return result
		
	def writeCall(self, function_name, num_of_args):
		# go back and set arg to num_of_args
		# save caller's frame (return-address, lcl, arg, this, that)
		# jump to function execution
		self._return_counter += 1
		
		result = ''
		result += f'@{self._filename}$ret.{self._return_counter} //call\n'
		result += f'D=A\n'
		result += f'@SP\n'
		result += f'A=M\n'
		result += f'M=D\n'
		result += f'@SP\n'
		result += f'M=M+1\n'
		
		result += f'@LCL\n'
		result += f'D=M\n'
		result += f'@SP\n'
		result += f'A=M\n'
		result += f'M=D\n'
		result += f'@SP\n'
		result += f'M=M+1\n'
		
		result += f'@ARG\n'
		result += f'D=M\n'
		result += f'@SP\n'
		result += f'A=M\n'
		result += f'M=D\n'
		result += f'@SP\n'
		result += f'M=M+1\n'
		
		result += f'@THIS\n'
		result += f'D=M\n'
		result += f'@SP\n'
		result += f'A=M\n'
		result += f'M=D\n'
		result += f'@SP\n'
		result += f'M=M+1\n'
		
		result += f'@THAT\n'
		result += f'D=M\n'
		result += f'@SP\n'
		result += f'A=M\n'
		result += f'M=D\n'
		result += f'@SP\n'
		result += f'M=M+1\n'
		
		result += f'@{int(num_of_args)}\n'
		result += f'D=A\n'
		result += f'@5\n'
		result += f'D=D+A\n'
		result += f'@SP\n'
		result += f'D=M-D\n'
		result += f'@ARG\n'
		result += f'M=D\n'
		
		result += f'@SP\n'
		result += f'D=M\n'
		result += f'@LCL\n'
		result += f'M=D\n'
		
		result += f'@{function_name}\n'
		result += f'0;JMP\n'
		
		result += f'({self._filename}$ret.{self._return_counter})\n'
		
		return result
		
	def writeFunction(self, label, num_of_locals):
		# push num_of_locals 
		# push return value onto stack ? or do this in return? if void function push 0?
		result = ''
		result += f'({label}) //function\n'
		
		for i in range(int(num_of_locals)):
			result += f'@SP\n'
			result += f'A=M\n'
			result += f'M=0\n'
			result += f'@SP\n'
			result += f'M=M+1\n'	
		
		return result
		
	def writeIf(self, label):
		result = ''
		result += f'@SP //if\n'
		result += f'M=M-1\n'
		result += f'A=M\n'
		result += f'D=M\n'
		result += f'@{label}\n'
		result += f'D;JNE\n'

		return result
	
	def writeInit(self):
		result = f''
		result += f'@256 //init\n'
		result += f'D=A\n'
		result += f'@SP\n'
		result += f'M=D\n'
		
		result += f'@{self._filename}$ret.{self._return_counter}\n'
		result += f'D=A\n'
		result += f'@SP\n'
		result += f'A=M\n'
		result += f'M=D\n'
		result += f'@SP\n'
		result += f'M=M+1\n'
		
		result += f'@LCL\n'
		result += f'D=M\n'
		result += f'@SP\n'
		result += f'A=M\n'
		result += f'M=D\n'
		result += f'@SP\n'
		result += f'M=M+1\n'
		
		result += f'@ARG\n'
		result += f'D=M\n'
		result += f'@SP\n'
		result += f'A=M\n'
		result += f'M=D\n'
		result += f'@SP\n'
		result += f'M=M+1\n'
		
		result += f'@THIS\n'
		result += f'D=M\n'
		result += f'@SP\n'
		result += f'A=M\n'
		result += f'M=D\n'
		result += f'@SP\n'
		result += f'M=M+1\n'
		
		result += f'@THAT\n'
		result += f'D=M\n'
		result += f'@SP\n'
		result += f'A=M\n'
		result += f'M=D\n'
		result += f'@SP\n'
		result += f'M=M+1\n'
		
		result += f'@0\n'
		result += f'D=A\n'
		result += f'@5\n'
		result += f'D=D+A\n'
		result += f'@SP\n'
		result += f'D=M-D\n'
		result += f'@ARG\n'
		result += f'M=D\n'
		
		result += f'@SP\n'
		result += f'D=M\n'
		result += f'@LCL\n'
		result += f'M=D\n'
		
		result += f'@Sys.init\n'
		result += f'0;JMP\n'
		
		result += f'({self._filename}$ret.{self._return_counter})\n'
		
		return result
		
	def writeGoto(self, label):
		result = ''
		result += f'@{label} //goto\n'
		result += f'0;JMP\n'

		return result	
	
	def writeLabel(self, label):
		result = ''
		result += f'({label}) //label\n'

		return result
		
	def writePushPop(self, command, segment, index):
		result = ''
		
		if command == 'C_PUSH':
			if segment == 'constant':
				result += f'@{index} //push constant\n'
				result += f'D=A\n'
				result += f'@SP\n'
				result += f'A=M\n'
				result += f'M=D\n'
				result += f'@SP\n'
				result += f'M=M+1\n'
			elif segment == 'static':
				result += f'@{self._filename}.{index} //push static\n'
				result += f'D=M\n'
				result += f'@SP\n'
				result += f'A=M\n'
				result += f'M=D\n'
				result += f'@SP\n'
				result += f'M=M+1\n'
			elif segment == 'pointer':
				this_or_that = 'THAT' if int(index) else 'THIS'
				
				result += f'@{this_or_that} //push point\n'
				result += f'D=M\n'
				result += f'@SP\n'
				result += f'A=M\n'
				result += f'M=D\n'
				result += f'@SP\n'
				result += f'M=M+1\n'
			elif segment == 'temp':
				result += f'@{index} //push temp\n'
				result += f'D=A\n'
				result += f'@5\n'
				result += f'A=A+D\n'
				result += f'D=M\n'
				result += f'@SP\n'
				result += f'A=M\n'
				result += f'M=D\n'
				result += f'@SP\n'
				result += f'M=M+1\n'
			elif segment in ['local', 'argument', 'this', 'that']:
				self._push_temp_counter += 1
				
				result += f'@{index} //push {segment}\n'
				result += f'D=A\n'
				result += f'@{self._POINTERSLIST[segment]}\n'
				result += f'A=M+D\n'
				result += f'D=M\n'
				result += f'@SP\n'
				result += f'A=M\n'
				result += f'M=D\n'
				result += f'@SP\n'
				result += f'M=M+1\n'
			else:
				pass
			
		else:
			# C_POP
			if segment == 'static':
				result += f'@SP //pop static\n'
				result += f'M=M-1\n'
				result += f'@SP\n'
				result += f'A=M\n'
				result += f'D=M\n'
				result += f'({self._filename}.{index})\n'
				result += f'@{self._filename}.{index}\n'
				result += f'M=D\n'
			elif segment == 'pointer':
				this_or_that = 'THAT' if int(index) else 'THIS'
				
				result += f'@SP //pop pointer\n'
				result += f'M=M-1\n'
				result += f'@SP\n'
				result += f'A=M\n'
				result += f'D=M\n'
				result += f'@{this_or_that}\n'
				result += f'M=D\n'
			elif segment == 'temp':
				result += f'@{index} //pop temp\n'
				result += f'D=A\n'
				result += f'@5\n'
				result += f'D=A+D\n'
				result += f'@R13\n'
				result += f'M=D\n'
				result += f'@SP\n'
				result += f'M=M-1\n'
				result += f'@SP\n'
				result += f'A=M\n'
				result += f'D=M\n'
				result += f'@R13\n'
				result += f'A=M\n'
				result += f'M=D\n'
			elif segment in ['local', 'argument', 'this', 'that']:
				self._pop_temp_counter += 1
				
				result += f'@{index} //pop {segment}\n'
				result += f'D=A\n'
				result += f'@{self._POINTERSLIST[segment]}\n'
				result += f'D=M+D\n'
				result += f'@R13\n'
				result += f'M=D\n'
				result += f'@SP\n'
				result += f'M=M-1\n'
				result += f'@SP\n'
				result += f'A=M\n'
				result += f'D=M\n'
				result += f'@R13\n'
				result += f'A=M\n'
				result += f'M=D\n'
			else:
				pass
			
		return result
	
	def writeReturn(self):
		self._return_frame_counter
		self._return_ret_counter
		
		# copies return value to first arg (arg 0)
		# restores segment pointers of caller
		# clears stack
		# sets sp for caller
		# jump to return address
		result = ''	
		result += f'@LCL //return\n'
		result += f'D=M\n'
		result += f'@R13\n'
		result += f'M=D\n'
		
		result += f'@5\n'
		result += f'D=A\n'
		result += f'@R13\n'
		result += f'D=M-D\n'
		result += f'A=D\n'
		result += f'D=M\n'
		result += f'@R14\n'
		result += f'M=D\n'
		
		result += f'@SP\n'
		result += f'M=M-1\n'
		result += f'A=M\n'
		result += f'D=M\n'
		result += f'@ARG\n'
		result += f'A=M\n'
		result += f'M=D\n'
		
		result += f'@ARG\n'
		result += f'D=M\n'
		result += f'@SP\n'
		result += f'M=D+1\n'
		
		result += f'@1\n'
		result += f'D=A\n'
		result += f'@R13\n'
		result += f'D=M-D\n'
		result += f'A=D\n'
		result += f'D=M\n'
		result += f'@THAT\n'
		result += f'M=D\n'
		
		result += f'@2\n'
		result += f'D=A\n'
		result += f'@R13\n'
		result += f'D=M-D\n'
		result += f'A=D\n'
		result += f'D=M\n'
		result += f'@THIS\n'
		result += f'M=D\n'
		
		result += f'@3\n'
		result += f'D=A\n'
		result += f'@R13\n'
		result += f'D=M-D\n'
		result += f'A=D\n'
		result += f'D=M\n'
		result += f'@ARG\n'
		result += f'M=D\n'
		
		result += f'@4\n'
		result += f'D=A\n'
		result += f'@R13\n'
		result += f'D=M-D\n'
		result += f'A=D\n'
		result += f'D=M\n'
		result += f'@LCL\n'
		result += f'M=D\n'
		
		result += f'@R14\n'
		result += f'A=M\n'
		result += f'0;JMP\n'
		
		return result

	#def close(self):
		#pass