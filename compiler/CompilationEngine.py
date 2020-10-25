import re
import os.path

class CompilationEngine(object):
	
	def __init__(self, tokenizedInput = None, inputFilename = None, isDirectory = False, source = None):
		self._isDirectory = isDirectory
		self.tokenizedInput = tokenizedInput
		
		self.inputFilename = self._removeJackExtension(inputFilename)
		
		self.position = 0
		
		self.OPS = ['+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '=']
		
		self.UNARYOPS = ['-', '~']
		
		self.KEYWORDS = ['true', 'false', 'null', 'this']
		
		self.compileFile(source, inputFilename)
		
	def compileFile(self, source, inputFilename):
		if self._isDirectory:
			with open(f'./{source}/{self.inputFilename}.xml', 'w') as f:
				self.compileClass(f)
					
		else: # Source is a single .jack file then
			with open(f'{self.inputFilename}.xml', 'w') as f:
				self.compileClass(f)
	
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
			
			self._writeKeyword(f) #Should be 'static or field'
			self.advancePosition()
			
			if self.getToken() in ['int', 'char', 'boolean']: #Handle Type
				self._writeKeyword(f) #Should be 'int', 'char', 'boolean'
				self.advancePosition()
			else:
				self._writeIdentifier(f) #Should be className
				self.advancePosition()
				
			if self.getTokenType() == 'identifier': #Should be varName
				self._writeIdentifier(f)
				self.advancePosition()
				
			while self.getToken() != ';': #Handle more varNames
				if self.getToken() == ',': #Should be ',
					self._writeSymbol(f)
					self.advancePosition()
				
				if self.getTokenType() == 'identifier': #Should be varName
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
		if self.getToken() in ['constructor', 'function', 'method']:
			f.write(f'<subroutineDec>\n')
			
			self._writeKeyword(f) #Should be 'constructor', 'function', 'method'
			self.advancePosition()
			
			if self.getToken() == 'void':
				self._writeKeyword(f) #Should be 'void'
				self.advancePosition()
			else: # Should be type
				if self.getToken() in ['int', 'char', 'boolean']: #Handle Type
					self._writeKeyword(f) #Should be 'int', 'char', 'boolean'
					self.advancePosition()
				else:
					self._writeIdentifier(f) #Should be className
					self.advancePosition()
				
			if self.getTokenType() == 'identifier': #Should be subroutineName
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
				
				self.compileStatements(f)
				
				if self.getToken() == '}':
					self._writeSymbol(f) #Should be '}'
					self.advancePosition()
					
				f.write(f'</subroutineBody>\n')
					
			f.write(f'</subroutineDec>\n')
			
			if self.getToken() in ['constructor', 'function', 'method']:
				self.compileSubroutine(f)
			else:
				return
	
	def compileParameterList(self, f):
		### Can be empty in xml

		if self.getToken() != ')':
			f.write(f'<parameterList>\n')
			
			if self.getToken() in ['int', 'char', 'boolean']: #Handle Type
				self._writeKeyword(f) #Should be 'int', 'char', 'boolean'
				self.advancePosition()
				temp = True
			else:
				self._writeIdentifier(f) #Should be className
				self.advancePosition()
				temp = False
			
			if self.getTokenType() == 'identifier': #Should be varName
				self._writeIdentifier(f)
				self.advancePosition()
					
				while self.getToken() != ')': #Handle more types and varNames
					if self.getToken() == ',': #Should be ',
						self._writeSymbol(f)
						self.advancePosition()
							
					if self.getToken() in ['int', 'char', 'boolean']: #Handle Type
						self._writeKeyword(f) #Should be 'int', 'char', 'boolean'
						self.advancePosition()
					else:
						self._writeIdentifier(f) #Should be className
						self.advancePosition()
							
					if self.getTokenType() == 'identifier': #Should be varName
						self._writeIdentifier(f)
						self.advancePosition()
		
		
			f.write(f'</parameterList>\n')
			
		else:
			f.write(f'<parameterList>\n')	
			f.write(f'</parameterList>\n')	
	
	def compileVarDec(self, f):
		if self.getToken() == 'var':
			f.write(f'<varDec>\n')
			
			self._writeKeyword(f) #Should be 'var'
			self.advancePosition()
			
			if self.getToken() in ['int', 'char', 'boolean']: #Handle Type
				self._writeKeyword(f) #Should be 'int', 'char', 'boolean'
				self.advancePosition()
			else:
				self._writeIdentifier(f) #Should be className
				self.advancePosition()
				
			if self.getTokenType() == 'identifier': #Should be varName
				self._writeIdentifier(f)
				self.advancePosition()
				
			while self.getToken() != ';': #Handle more varNames
				if self.getToken() == ',': #Should be ',
					self._writeSymbol(f)
					self.advancePosition()
				
				if self.getTokenType() == 'identifier': #Should be varName
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
		
		self._writeKeyword(f) #Should be 'do'
		self.advancePosition()
		
		#SubroutineCall
		if self.getTokenType() == 'identifier': #Should be subroutineName
			self._writeIdentifier(f)
			self.advancePosition()
		
			if self.getToken() == '(': #start of ( expressionList )
				self._writeSymbol(f) #Should be '('
				self.advancePosition()
					
				self.compileExpressionList(f)
				
				if self.getToken() == ')':
					self._writeSymbol(f) #Could be ')'
					self.advancePosition()
			else: #Then should be className or varName
				#if self.getTokenType() == 'identifier': #Should be varName or className
				#	self._writeIdentifier(f)
				#	self.advancePosition()
					
				if self.getToken() == '.':
					self._writeSymbol(f) #Should be '.'
					self.advancePosition()
				
				if self.getTokenType() == 'identifier': #Should be subroutineName
					self._writeIdentifier(f)
					self.advancePosition()
			
				if self.getToken() == '(':
					self._writeSymbol(f) #Should be '('
					self.advancePosition()
					
				self.compileExpressionList(f)
					
				if self.getToken() == ')':
					self._writeSymbol(f) #Should be ')'
					self.advancePosition()
				
			if self.getToken() == ';':
				self._writeSymbol(f) #Should be ';'
				self.advancePosition()
		
		f.write(f'</doStatement>\n')
	
	def compileLet(self, f):
		f.write(f'<letStatement>\n')
		
		self._writeKeyword(f) #Should be 'let'
		self.advancePosition()
		
		if self.getTokenType() == 'identifier': #Should be varName
			self._writeIdentifier(f)
			self.advancePosition()
			
			if self.getToken() == '[': #Check if start of expression in brackets
				self._writeSymbol(f) #Should be '['
				self.advancePosition()
				
				self.compileExpression(f)
				
				if self.getToken() == ']':
					self._writeSymbol(f) #Should be ']'
					self.advancePosition()
			
			if self.getToken() == '=':
				self._writeSymbol(f) #Should be '='
				self.advancePosition()
				
			self.compileExpression(f)
			
			if self.getToken() == ';':
				self._writeSymbol(f) #Should be ';'
				self.advancePosition()
		
		f.write(f'</letStatement>\n')
	
	def compileWhile(self, f):
		f.write(f'<whileStatement>\n')
		
		self._writeKeyword(f) #Should be 'while'
		self.advancePosition()
		
		if self.getToken() == '(':
			self._writeSymbol(f) #Should be '('
			self.advancePosition()
					
			self.compileExpression(f)
				
			if self.getToken() == ')':
				self._writeSymbol(f) #Should be ')'
				self.advancePosition()
				
			if self.getToken() == '{':
				self._writeSymbol(f) #Should be '{'
				self.advancePosition()
					
			self.compileStatements(f)
				
			if self.getToken() == '}':
				self._writeSymbol(f) #Should be '}'
				self.advancePosition()
			
		f.write(f'</whileStatement>\n')
	
	def compileReturn(self, f):
		f.write(f'<returnStatement>\n')
		
		self._writeKeyword(f) #Should be 'return'
		self.advancePosition()
		
		if self.getToken() == ';':
			self._writeSymbol(f) #Should be ';'
			self.advancePosition()
		else:
			self.compileExpression(f)
			
			self._writeSymbol(f) #Should be ';'
			self.advancePosition()
			
		f.write(f'</returnStatement>\n')
	
	def compileIf(self, f):
		f.write(f'<ifStatement>\n')
		
		self._writeKeyword(f) #Should be 'if'
		self.advancePosition()
		
		if self.getToken() == '(':
			self._writeSymbol(f) #Should be '('
			self.advancePosition()
					
			self.compileExpression(f)
				
			if self.getToken() == ')':
				self._writeSymbol(f) #Should be ')'
				self.advancePosition()
				
			if self.getToken() == '{':
				self._writeSymbol(f) #Should be '{'
				self.advancePosition()
					
			self.compileStatements(f)
				
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
			
		f.write(f'</ifStatement>\n')
	
	def compileExpression(self, f):
		f.write(f'<expression>\n')
		
		self.compileTerm(f)
		
		while self.getToken() in self.OPS:
			self._writeSymbol(f) #Should be an op
			self.advancePosition()
			
			self.compileTerm(f)
			
		f.write(f'</expression>\n')
	
	def compileTerm(self, f):
		f.write(f'<term>\n')

		currentTokenType = self.getTokenType()
		currentToken = self.getToken()
		
		if currentTokenType == 'identifier':
			nextToken = self.tokenizedInput[self.position + 1][1]
			
			if nextToken == '[':
				self._writeIdentifier(f)
				self.advancePosition()
					
				self._writeSymbol(f)
				self.advancePosition()
				
				self.compileExpression(f)
				
				if self.getToken() == ']':
					self._writeSymbol(f)
					self.advancePosition()
					
			elif nextToken in ['(', '.']:
				#SubroutineCall
				if self.getTokenType() == 'identifier': #Should be subroutineName
					self._writeIdentifier(f)
					self.advancePosition()
				
					if self.getToken() == '(': #start of ( expressionList )
						self._writeSymbol(f) #Should be '('
						self.advancePosition()
							
						self.compileExpressionList(f)
						
						if self.getToken() == ')':
							self._writeSymbol(f) #Could be ')'
							self.advancePosition()
					else: #Then should be className or varName
						#if self.getTokenType() == 'identifier': #Should be varName or className
						#	self._writeIdentifier(f)
						#	self.advancePosition()
							
						if self.getToken() == '.':
							self._writeSymbol(f) #Should be '.'
							self.advancePosition()
						
						if self.getTokenType() == 'identifier': #Should be subroutineName
							self._writeIdentifier(f)
							self.advancePosition()
					
						if self.getToken() == '(':
							self._writeSymbol(f) #Should be '('
							self.advancePosition()
							
						self.compileExpressionList(f)
							
						if self.getToken() == ')':
							self._writeSymbol(f) #Should be ')'
							self.advancePosition()
			else:
				self._writeIdentifier(f)
				self.advancePosition()
		elif currentTokenType == 'keyword':
			self._writeKeyword(f)
			self.advancePosition()
		elif currentTokenType == 'integer':
			self._writeInteger(f)
			self.advancePosition()
		elif currentTokenType == 'string':
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
			
			self.compileTerm(f)
		
		f.write(f'</term>\n')
		
	def compileExpressionList(self, f):
		### Can be empty in xml

		if self.getToken() != ')':
			f.write(f'<expressionList>\n')
			
			self.compileExpression(f)
			
			while self.getToken() != ')': #Handle  more expressions, if present
				self._writeSymbol(f) #Should be a ','
				self.advancePosition()
				
				self.compileExpression(f)
				
			f.write(f'</expressionList>\n')	
		
		else: #Should be a ')'
			f.write(f'<expressionList>\n')
			f.write(f'</expressionList>\n')
	
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
