from compiler.SymbolTable import SymbolTable
from compiler.VMWriter import VMWriter
import re
import os.path


## Handle string assignments -> String.appendChar(c)

class CompilationEngine(object):
	
	def __init__(self, tokenizedInput = None, inputFilename = None, isDirectory = False, source = None):
		self._isDirectory = isDirectory
		self.tokenizedInput = tokenizedInput
		
		self.whileCounter = 0
		self.ifCounter = 0
		
		self.inputFilename = self._removeJackExtension(inputFilename)
		
		self.classSymbolTable = SymbolTable()
		self.subroutineSymbolTable = SymbolTable()
		
		self.position = 0
		
		self.OPS = ['+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '=']
		
		self.UNARYOPS = ['-', '~']
		
		self.KEYWORDS = ['true', 'false', 'null', 'this']
		
		self.className = None
		
		self.compileFile(source, self.inputFilename)
		
	def compileFile(self, source, inputFilename):
		if self._isDirectory:
			with open(f'./{source}/{self.inputFilename}.xml', 'w') as f:
				self.VMWriter = VMWriter(source, inputFilename)
				self.compileClass(f)
				self.VMWriter.close()
					
		else: # Source is a single .jack file then
			with open(f'{self.inputFilename}.xml', 'w') as f:
				self.VMWriter = VMWriter(None, inputFilename)
				self.compileClass(f)
				self.VMWriter.close()
	
	def advancePosition(self):
		self.position += 1
		
	def getTokenType(self):
		return self.tokenizedInput[self.position][0]
	
	def getToken(self):
		return self.tokenizedInput[self.position][1]
	
	def compileClass(self, f):
		if self.getToken() == 'class':
			f.write(f'<class>\n')
			
			self._writeKeyword(f) #Should be 'class'
			self.advancePosition()
			
			if self.getTokenType() == 'identifier': #Next token is className which is an identifier
				self.className = self.getToken()
				self._writeIdentifier(f)
				self.advancePosition()
				
				if self.getToken() == '{': #Next token is '{'
					self._writeSymbol(f)
					self.advancePosition()
					
					self.compileClassVarDec(f)
					
					self.compileSubroutine(f)
					
					if self.getToken() == '}': #Next token is '}'
						self._writeSymbol(f)
						self.advancePosition()
			
			f.write(f'</class>')
	
	def compileClassVarDec(self, f):
		if self.getToken() in ['static', 'field']:
			f.write(f'<classVarDec>\n')
			
			kind = self.getToken().upper()
			
			self._writeKeyword(f) #Should be 'static or field'
			self.advancePosition()
			
			type = ''
			
			if self.getToken() in ['int', 'char', 'boolean']: #Handle Type
				
				type += self.getToken()
				
				self._writeKeyword(f) #Should be 'int', 'char', 'boolean'
				self.advancePosition()
			else:
				
				type += self.getToken()
				
				self._writeIdentifier(f) #Should be className
				self.advancePosition()
				
			name = ''
				
			if self.getTokenType() == 'identifier': #Should be varName
				
				name += self.getToken()
				
				self._writeIdentifier(f)
				self.advancePosition()
				
			self.classSymbolTable.define(name, type, kind)
				
			while self.getToken() != ';': #Handle more varNames
				
				if self.getToken() == ',': #Should be ',
					self._writeSymbol(f)
					self.advancePosition()
				
				if self.getTokenType() == 'identifier': #Should be varName
					
					name = self.getToken()
					self.classSymbolTable.define(name, type, kind)
					
					self._writeIdentifier(f)
					self.advancePosition()
			
			self._writeSymbol(f) #Should be ';'
			self.advancePosition()
			
			f.write(f'</classVarDec>\n')
			
			if self.getToken() in ['static', 'field']: #Handle if there are more classVarDecs
				self.compileClassVarDec(f)
			else:
				return
	
	def compileSubroutine(self, f):
		self.subroutineSymbolTable.startSubroutine()
		
		voidFlag = False
		constructorFlag = False
		methodFlag = False
		
		if self.getToken() in ['constructor', 'function', 'method']:
			f.write(f'<subroutineDec>\n')
			
			if self.getToken() == 'method':
				self.subroutineSymbolTable.define('this', self.className, 'ARG')
				methodFlag = True
			elif self.getToken() == 'constructor':
				constructorFlag = True
				 
			self._writeKeyword(f) #Should be 'constructor', 'function', 'method'
			self.advancePosition()
			
			if self.getToken() == 'void':
				voidFlag = True
				
				self._writeKeyword(f) #Should be 'void'
				self.advancePosition()
			else: # Should be type
				if self.getToken() in ['int', 'char', 'boolean']: #Handle Type
					self._writeKeyword(f) #Should be 'int', 'char', 'boolean'
					self.advancePosition()
				else:
					self._writeIdentifier(f) #Should be className
					self.advancePosition()
				
			subroutineName = ''
			if self.getTokenType() == 'identifier': #Should be subroutineName
				subroutineName = self.getToken()
				self._writeIdentifier(f)
				self.advancePosition()
				
			if self.getToken() == '(':
				self._writeSymbol(f) #Should be '('
				self.advancePosition()
				
			self.compileParameterList(f)
			
			if self.getToken() == ')':
				self._writeSymbol(f) #Should be ')'
				self.advancePosition()
			
			### Subroutine body ###
			if self.getToken() == '{':
				f.write(f'<subroutineBody>\n')
				
				self._writeSymbol(f) #Should be '{'
				self.advancePosition()
				
				self.compileVarDec(f)
				
				self.VMWriter.writeFunction(f'{self.className}.{subroutineName}', self.subroutineSymbolTable.varCount('VAR'))
				
				if constructorFlag:
					numOfClassVars = self.classSymbolTable.varCount('FIELD') + self.classSymbolTable.varCount('STATIC')
					
					self.VMWriter.writePush('constant', numOfClassVars)
					self.VMWriter.writeCall('Memory.alloc', 1)
					self.VMWriter.writePop('pointer', 0)
				elif methodFlag:
					self.VMWriter.writePush('ARG', 0)
					self.VMWriter.writePop('pointer', 0)
				
				self.compileStatements(f)
				
				if self.getToken() == '}':
					self._writeSymbol(f) #Should be '}'
					self.advancePosition()
					
				f.write(f'</subroutineBody>\n')
				
			#self.VMWriter.writePush('pointer', 0) #**** Should only do this for constructor? If so, jack language already takes care of this so maybe not necessary?
			
			#If voidflag is on, must get rid of top of stack (pop temp 0)
					
			f.write(f'</subroutineDec>\n')
			
			if self.getToken() in ['constructor', 'function', 'method']:
				self.compileSubroutine(f)
			else:
				return
	
	def compileParameterList(self, f):
		### Can be empty in xml

		if self.getToken() != ')':
			f.write(f'<parameterList>\n')
			
			kind = 'ARG'
			type = ''
			
			if self.getToken() in ['int', 'char', 'boolean']: #Handle Type
				
				type = self.getToken()
				
				self._writeKeyword(f) #Should be 'int', 'char', 'boolean'
				self.advancePosition()
				temp = True
			else:
				
				type = self.getToken()
				
				self._writeIdentifier(f) #Should be className
				self.advancePosition()
				temp = False
				
			name = ''
			
			if self.getTokenType() == 'identifier': #Should be varName
				
				name = self.getToken()
				self.subroutineSymbolTable.define(name, type, kind)
				f.write(f'*******{name}: {type}, {kind}*****************')
				
				self._writeIdentifier(f)
				self.advancePosition()
					
				while self.getToken() != ')': #Handle more types and varNames					
					if self.getToken() == ',': #Should be ',
						self._writeSymbol(f)
						self.advancePosition()
						
					type = ''
							
					if self.getToken() in ['int', 'char', 'boolean']: #Handle Type
						
						type = self.getToken()
						
						self._writeKeyword(f) #Should be 'int', 'char', 'boolean'
						self.advancePosition()
					else:
						
						type = self.getToken()
						
						self._writeIdentifier(f) #Should be className
						self.advancePosition()
						
					name = ''
							
					if self.getTokenType() == 'identifier': #Should be varName
						
						name = self.getToken()
						self.subroutineSymbolTable.define(name, type, kind)
						f.write(f'*******{name}: {type}, {kind}*****************')
						
						self._writeIdentifier(f)
						self.advancePosition()
		
		
			f.write(f'</parameterList>\n')
			
		else:
			f.write(f'<parameterList>\n')	
			f.write(f'</parameterList>\n')	
	
	def compileVarDec(self, f):
		if self.getToken() == 'var':
			f.write(f'<varDec>\n')
			
			kind = 'VAR'
			
			self._writeKeyword(f) #Should be 'var'
			self.advancePosition()
			
			type = ''
			
			if self.getToken() in ['int', 'char', 'boolean']: #Handle Type
				
				type += self.getToken()
				
				self._writeKeyword(f) #Should be 'int', 'char', 'boolean'
				self.advancePosition()
			else:
				
				type += self.getToken()
				
				self._writeIdentifier(f) #Should be className
				self.advancePosition()
				
			name = ''	
			
			if self.getTokenType() == 'identifier': #Should be varName
				
				name += self.getToken()
				
				self._writeIdentifier(f)
				self.advancePosition()
				
			self.subroutineSymbolTable.define(name, type, kind)
			f.write(f'*******{name}: {type}, {kind}*****************')
				
			while self.getToken() != ';': #Handle more varNames				
				if self.getToken() == ',': #Should be ',
					self._writeSymbol(f)
					self.advancePosition()
				
				if self.getTokenType() == 'identifier': #Should be varName
					
					name = self.getToken()
					self.subroutineSymbolTable.define(name, type, kind)
					f.write(f'*******{name}: {type}, {kind}*****************')
					
					self._writeIdentifier(f)
					self.advancePosition()
			
			self._writeSymbol(f) #Should be ';'
			self.advancePosition()
			
			f.write(f'</varDec>\n')
			
			if self.getToken() == 'var': #Handle if there are more varDecs
				self.compileVarDec(f)
			else:
				return
	
	def compileStatements(self, f):
		if self.getToken() in ['let', 'if', 'while', 'do', 'return']:
			f.write(f'<statements>\n')
			
			while self.getToken() != '}': #Should mark the end of statements				
				if self.getToken() == 'let':
					self.compileLet(f)
				elif self.getToken() == 'if':
					self.compileIf(f)
				elif self.getToken() == 'while':
					self.compileWhile(f)
				elif self.getToken() == 'do':
					self.compileDo(f)
				elif self.getToken() == 'return':
					self.compileReturn(f)
				
			f.write(f'</statements>\n')
	
	def compileDo(self, f):
		f.write(f'<doStatement>\n')
		
		# methods in context of do should not disregard the returned value (pop temp 0)
		
		self._writeKeyword(f) #Should be 'do'
		self.advancePosition()
		
		#SubroutineCall  so args need to be pushed onto stack  - treat method specially first if its a method
		if self.getTokenType() == 'identifier': #Should be subroutineName OR (className or varName)
			nextToken = self.tokenizedInput[self.position + 1][1]
			
			if nextToken == '(': #start of ( expressionList )
				#Should not be necessary to do a symbolLookup here because this should be a subroutineName
				subroutineName = f'{self.className}.{self.getToken()}'
							
				self._writeIdentifier(f) #Should be subroutineName
				self.advancePosition()
						
				self._writeSymbol(f) #Should be '('
				self.advancePosition()
				
				self.VMWriter.writePush('pointer', 0)
							
				nArgs =  self.compileExpressionList(f)
				
				nArgs += 1 #Methods have at least one implicit argument
						
				self.VMWriter.writeCall(subroutineName, nArgs) #className is in local subroutineName variable
				
				self.VMWriter.writePop('temp', 0)
						
				if self.getToken() == ')':
					self._writeSymbol(f) #Could be ')'
					self.advancePosition()
			else:
				className = ''
				
				methodFlag = False
						
				if self.inSymbolTable(f'{self.getToken()}'): #If in the symbolTable, its a varName object, so it has to get pushed onto stack
					[kind, type, index] = self.symbolTableLookup(f'{self.getToken()}')
					
					methodFlag = True
					
					className = type
							
					self.VMWriter.writePush(kind, index)
				else:
					className = self.getToken()
						
				self._writeIdentifier(f) #Should be (className or varName)
				self.advancePosition()
						
				if self.getToken() == '.':
					self._writeSymbol(f) #Should be '.'
					self.advancePosition()
						
				subroutineName = ''
						
				if self.getTokenType() == 'identifier': #Should be subroutineName therefore it should not be necessary to do a symbolLookup here
					subroutineName = self.getToken()
					self._writeIdentifier(f)
					self.advancePosition()
					
				if self.getToken() == '(':
					self._writeSymbol(f) #Should be '('
					self.advancePosition()
					
				nArgs = self.compileExpressionList(f)
				
				if methodFlag:
					nArgs += 1
							
				if self.getToken() == ')':
					self._writeSymbol(f) #Should be ')'
					self.advancePosition()
							
				self.VMWriter.writeCall(f'{className}.{subroutineName}', nArgs)
				
				self.VMWriter.writePop('temp', 0)
				
			if self.getToken() == ';':
				self._writeSymbol(f) #Should be ';'
				self.advancePosition()
		
		f.write(f'</doStatement>\n')
	
	def compileLet(self, f):
		f.write(f'<letStatement>\n')
		
		self._writeKeyword(f) #Should be 'let'
		self.advancePosition()
		
		arrayFlag = False
		
		if self.getTokenType() == 'identifier': #Should be varName
			[kind, type, index] = [None, None, None]
			
			if self.inSymbolTable(f'{self.getToken()}'): #should be in here
				[kind, type, index] = self.symbolTableLookup(f'{self.getToken()}')
			
			self._writeIdentifier(f)
			self.advancePosition()
			
			if self.getToken() == '[': #Check if start of expression in brackets
				
				arrayFlag = True
				
				self.VMWriter.writePush(kind, index)
					
				self._writeSymbol(f) #Should be '['
				self.advancePosition()
				
				self.compileExpression(f)
				
				self.VMWriter.writeArithmetic('+')
				
				if self.getToken() == ']':
					self._writeSymbol(f) #Should be ']'
					self.advancePosition()
			
			if self.getToken() == '=':
				self._writeSymbol(f) #Should be '='
				self.advancePosition()
				
			self.compileExpression(f)
			
			if arrayFlag:
				self.VMWriter.writePop('temp', 0)
				self.VMWriter.writePop('pointer', 1)
				self.VMWriter.writePush('temp', 0)
				self.VMWriter.writePop('that', 0)
			else:
				self.VMWriter.writePop(kind, index)
			
			if self.getToken() == ';':
				self._writeSymbol(f) #Should be ';'
				self.advancePosition()
		
		f.write(f'</letStatement>\n')
	
	def compileWhile(self, f):
		f.write(f'<whileStatement>\n')
		
		index = self.whileCounter
		self.whileIncrementer()
		
		self._writeKeyword(f) #Should be 'while'
		self.advancePosition()
		
		if self.getToken() == '(':
			self._writeSymbol(f) #Should be '('
			self.advancePosition()
			
			self.VMWriter.writeLabel(f'WHILE_EXP{index}')
					
			self.compileExpression(f)
				
			if self.getToken() == ')':
				self._writeSymbol(f) #Should be ')'
				self.advancePosition()
				
			if self.getToken() == '{':
				self._writeSymbol(f) #Should be '{'
				self.advancePosition()
				
			self.VMWriter.writeArithmetic('not')
				
			self.VMWriter.writeIf(f'WHILE_END{index}')
					
			self.compileStatements(f)
			
			self.VMWriter.writeGoto(f'WHILE_EXP{index}')
			
			self.VMWriter.writeLabel(f'WHILE_END{index}')
				
			if self.getToken() == '}':
				self._writeSymbol(f) #Should be '}'
				self.advancePosition()
			
		f.write(f'</whileStatement>\n')
	
	def compileReturn(self, f):
		f.write(f'<returnStatement>\n')
		
		self._writeKeyword(f) #Should be 'return'
		self.advancePosition()
		
		if self.getToken() == ';':
			#if in here, must be a void method or void function so push constant 0, return
			self.VMWriter.writePush('constant', 0)
			self.VMWriter.writeReturn()
			
			self._writeSymbol(f) #Should be ';'
			self.advancePosition()
		else:
			self.compileExpression(f)
			
			self.VMWriter.writeReturn()
			
			self._writeSymbol(f) #Should be ';'
			self.advancePosition()
			
		f.write(f'</returnStatement>\n')
	
	def compileIf(self, f):
		f.write(f'<ifStatement>\n')
		
		index = self.ifCounter
		self.ifIncrementer()
		
		self._writeKeyword(f) #Should be 'if'
		self.advancePosition()
		
		if self.getToken() == '(':
			self._writeSymbol(f) #Should be '('
			self.advancePosition()
					
			self.compileExpression(f)
			
			self.VMWriter.writeArithmetic('not')
				
			if self.getToken() == ')':
				self._writeSymbol(f) #Should be ')'
				self.advancePosition()
				
			if self.getToken() == '{':
				self._writeSymbol(f) #Should be '{'
				self.advancePosition()
					
			self.VMWriter.writeIf(f'IF_TRUE{index}')
					
			self.compileStatements(f)
			
			self.VMWriter.writeGoto(f'IF_FALSE{index}')
			
			self.VMWriter.writeLabel(f'IF_TRUE{index}')
				
			if self.getToken() == '}':
				self._writeSymbol(f) #Should be '}'
				self.advancePosition()
				
			if self.getToken() == 'else': #check if there is an else statement
				self._writeKeyword(f) #Should be 'else'
				self.advancePosition()
				
				if self.getToken() == '{':
					self._writeSymbol(f) #Should be '{'
					self.advancePosition()
						
				self.compileStatements(f)
					
				if self.getToken() == '}':
					self._writeSymbol(f) #Should be '}'
					self.advancePosition()
					
			self.VMWriter.writeLabel(f'IF_FALSE{index}')
			
		f.write(f'</ifStatement>\n')
	
	def compileExpression(self, f):
		f.write(f'<expression>\n')
		
		self.compileTerm(f)
		
		while self.getToken() in self.OPS:
			sym = self.getToken()
			self._writeSymbol(f) #Should be an op
			self.advancePosition()
			
			self.compileTerm(f)
			
			self.VMWriter.writeArithmetic(sym)
			
		f.write(f'</expression>\n')
	
	def compileTerm(self, f):
		f.write(f'<term>\n')

		currentTokenType = self.getTokenType()
		currentToken = self.getToken()
		
		if currentTokenType == 'identifier':
			nextToken = self.tokenizedInput[self.position + 1][1]
			
			if nextToken == '[': #Array
				[kind, type, index] = [None, None, None]
			
				if self.inSymbolTable(f'{self.getToken()}'):
					[kind, type, index] = self.symbolTableLookup(f'{self.getToken()}')
				
				self._writeIdentifier(f)
				self.advancePosition()
					
				self._writeSymbol(f)
				self.advancePosition()
				
				self.VMWriter.writePush(kind, index)
				
				self.compileExpression(f)
				
				self.VMWriter.writeArithmetic('+')
				
				self.VMWriter.writePop('pointer', 1)
				
				self.VMWriter.writePush('that', 0)
				
				if self.getToken() == ']':
					self._writeSymbol(f)
					self.advancePosition()

			elif nextToken in ['(', '.']:
				#SubroutineCall  so args need to be pushed onto stack  - treat method specially first if its a method
				if self.getTokenType() == 'identifier': #Should be subroutineName OR (className or varName)
					if nextToken == '(': #start of ( expressionList )
						#Should not be necessary to do a symbolLookup here because this should be a subroutineName
						subroutineName = f'{self.className}.{self.getToken()}'
							
						self._writeIdentifier(f) #Should be subroutineName
						self.advancePosition()
						
						self._writeSymbol(f) #Should be '('
						self.advancePosition()
							
						nArgs = self.compileExpressionList(f)
						
						nArgs += 1 #Methods have at least one implicit argument
						
						self.VMWriter.writeCall(subroutineName, nArgs) #className is in local subroutineName variable
						
						if self.getToken() == ')':
							self._writeSymbol(f) #Could be ')'
							self.advancePosition()
					else:
						className = ''
						
						methodFlag = False
						
						if self.inSymbolTable(f'{self.getToken()}'): #If in the symbolTable, its a varName object, so it has to get pushed onto stack
							[kind, type, index] = self.symbolTableLookup(f'{self.getToken()}')
							
							methodFlag = True
							
							className = type
							
							self.VMWriter.writePush(kind, index)
						else:
							className = self.getToken()
						
						self._writeIdentifier(f) #Should be (className or varName)
						self.advancePosition()
						
						if self.getToken() == '.':
							self._writeSymbol(f) #Should be '.'
							self.advancePosition()
						
						subroutineName = ''
						
						if self.getTokenType() == 'identifier': #Should be subroutineName therefore it should not be necessary to do a symbolLookup here
							subroutineName = self.getToken()
							self._writeIdentifier(f)
							self.advancePosition()
					
						if self.getToken() == '(':
							self._writeSymbol(f) #Should be '('
							self.advancePosition()
							
						nArgs = self.compileExpressionList(f)
						
						if methodFlag:
							nArgs += 1
							
						if self.getToken() == ')':
							self._writeSymbol(f) #Should be ')'
							self.advancePosition()
							
						self.VMWriter.writeCall(f'{className}.{subroutineName}', nArgs)
			else:
				if self.inSymbolTable(f'{self.getToken()}'):
					[kind, type, index] = self.symbolTableLookup(f'{self.getToken()}')
					
					self.VMWriter.writePush(kind, index)
					
				self._writeIdentifier(f)
				self.advancePosition()
		elif currentTokenType == 'keyword':
			# I think constants should be handled here?
			
			if self.getToken() == 'true':
				self.VMWriter.writePush('constant', 1)
				self.VMWriter.writeArithmetic('neg')
			elif self.getToken() in ['false', 'null']:
				self.VMWriter.writePush('constant', 0)
			else:
				# this?
				self.VMWriter.writePush('pointer', 0)
			self._writeKeyword(f)
			self.advancePosition()
		elif currentTokenType == 'integer':
			self.VMWriter.writePush('constant', self.getToken())
			self._writeInteger(f)
			self.advancePosition()
		elif currentTokenType == 'string':
			string = self.getToken()
			
			self.VMWriter.writePush('constant', len(string))
			self.VMWriter.writeCall('String.new', 1)
			
			for letter in string:
				self.VMWriter.writePush('constant', ord(letter))
				self.VMWriter.writeCall('String.appendChar', 2)
				
			self._writeString(f)
			self.advancePosition()
		elif currentToken == '(':
			self._writeSymbol(f) #should be a '('
			self.advancePosition()
			
			self.compileExpression(f)
			
			if self.getToken() == ')':
				self._writeSymbol(f) #should be a ')'
				self.advancePosition()
				
		elif currentToken in self.UNARYOPS:
			self._writeSymbol(f)
			self.advancePosition()
			
			if currentToken == '-':
				self.compileTerm(f)
				self.VMWriter.writeArithmetic('neg')
			else:
				self.compileTerm(f)
				self.VMWriter.writeArithmetic('not')
		
		f.write(f'</term>\n')
		
	def compileExpressionList(self, f):
		### Can be empty in xml
		
		nArgs = None

		if self.getToken() != ')':
			f.write(f'<expressionList>\n')
			
			nArgs = 1
			
			self.compileExpression(f)
			
			while self.getToken() != ')': #Handle  more expressions, if present				
				nArgs += 1
				
				self._writeSymbol(f) #Should be a ','
				self.advancePosition()
				
				self.compileExpression(f)
				
			f.write(f'</expressionList>\n')	
		
		else: #Should be a ')'
			nArgs = 0
			f.write(f'<expressionList>\n')
			f.write(f'</expressionList>\n')
			
		return nArgs
	
	def _writeString(self, f):
		f.write(f'<stringConstant> {self.getToken()} </stringConstant>\n')
	
	def _writeInteger(self, f):
		f.write(f'<integerConstant> {self.getToken()} </integerConstant>\n')

	def _writeIdentifier(self, f):
		f.write(f'<identifier> {self.getToken()} </identifier>\n')
	
	def _writeKeyword(self, f):
		f.write(f'<keyword> {self.getToken()} </keyword>\n')
	
	def _writeSymbol(self, f):			
		f.write(f'<symbol> {self.getToken()} </symbol>\n')
		
	def _removeJackExtension(self, filename):
		return re.sub(".jack", "", filename)
	
	def inSymbolTable(self, name):
		if name in self.subroutineSymbolTable.table:
			return True
		elif name in self.classSymbolTable.table:
			return True
		else:
			return None
		
	def symbolTableLookup(self, name):
		if name in self.subroutineSymbolTable.table:
			return [self.subroutineSymbolTable.kindOf(name),
					self.subroutineSymbolTable.typeOf(name),
					self.subroutineSymbolTable.indexOf(name)]
		elif name in self.classSymbolTable.table:
			return [self.classSymbolTable.kindOf(name),
					self.classSymbolTable.typeOf(name),
					self.classSymbolTable.indexOf(name)]
	
	def whileIncrementer(self):
		self.whileCounter += 1
		
	def ifIncrementer(self):
		self.ifCounter += 1	
