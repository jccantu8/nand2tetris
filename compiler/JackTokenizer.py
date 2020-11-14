import re
import os.path

class JackTokenizer(object):
	
	def __init__(self, inputFilename = None, isDirectory = False, source = None):
		self._isDirectory = isDirectory
		
		self.tokens = []
		
		self.KEYWORDS = [
			'class',
			'constructor',
			'function',
			'method',
			'field',
			'static',
			'var',
			'int',
			'char',
			'boolean',
			'void',
			'true',
			'false',
			'null',
			'this',
			'let',
			'do',
			'if',
			'else',
			'while',
			'return',
		]
		
		self.SYMBOLS = [
			'{',
			'}',
			'(',
			')',
			'[',
			']',
			'.',
			',',
			';',
			'+',
			'-',
			'*',
			'/',
			'&',
			'|',
			'<',
			'>',
			'=',
			'~',
		]
		
		self._SPECIALSYMBOLS = {
			'<' : '&lt;',
			'>' : '&gt;',
			'"' : '&quot;',
			'&' : '&amp;',
		}
		
		self._stripFile(inputFilename, source)
		self._tokenizeFile(inputFilename, source)
		
	# Private methods
	
	def _writeString(self, f, token):
		token = re.sub("[\n\"]", "", token)
		f.write(f'<stringConstant> {token} </stringConstant>\n')
		
		self.tokens.append(['string', token])
	
	def _writeInteger(self, f, token):
		f.write(f'<integerConstant> {token} </integerConstant>\n')
		
		self.tokens.append(['integer', token])
	
	def _writeIdentifier(self, f, token):
		f.write(f'<identifier> {token} </identifier>\n')
		
		self.tokens.append(['identifier', token])
	
	def _writeKeyword(self, f, token):
		f.write(f'<keyword> {token} </keyword>\n')
		
		self.tokens.append(['keyword', token])
	
	def _writeSymbol(self, f, token):
		if token in self._SPECIALSYMBOLS.keys():
			token = self._SPECIALSYMBOLS[token]
			
		f.write(f'<symbol> {token} </symbol>\n')
		
		self.tokens.append(['symbol', token])
		
	def _tokenizeFile(self, inputFilename, source):
		if self._isDirectory:
			with open(os.path.abspath(f'./{source}/stripped_{inputFilename}'), 'r') as data:
				with open(f'./{source}/tokenized_{inputFilename}', 'w') as f:
					self._writeTokens(data, f)
					
		else: # Source is a single .jack file then
			with open(os.path.abspath(f'./stripped_{inputFilename}'), 'r') as data:
				with open(f'tokenized_{inputFilename}', 'w') as f:
					self._writeTokens(data, f)
						
	def _writeTokens(self, data, f):
		f.write("<tokens>\n")
					
		for line in data:
			token = ''
						
			stringFlag = False
			intFlag = False
			identifierFlag = False
			newTokenFlag = True
						
			for ch in line:
							
				if ch == ' ' and not stringFlag:
					if identifierFlag:
						identifierFlag = False
						self._writeIdentifier(f, token)
					elif intFlag:
						intFlag = False
						self._writeInteger(f, token)
								
					token = ''
					newTokenFlag = True
					continue
							
				if newTokenFlag and ch.isdigit():
					intFlag = True
					newTokenFlag  = False
					token += ch
					continue
								
				if ch in self.SYMBOLS and not stringFlag:
					if identifierFlag:
						identifierFlag = False
						self._writeIdentifier(f, token)
					elif intFlag:
						intFlag = False
						self._writeInteger(f, token)
									
					self._writeSymbol(f, ch)
					token = ''
					newTokenFlag = True
					continue
								
				if intFlag:
					token += ch
					newTokenFlag = False
					continue
							
				if ch == '"':
					if stringFlag:
						token += ch
						stringFlag = False
						self._writeString(f, token)
						identifierFlag = False
						token = ''
						newTokenFlag = True
					else:
						stringFlag = True
						newTokenFlag = False
						token += ch
									
					continue
							
				token += ch
							
				if token in self.KEYWORDS:
					self._writeKeyword(f, token)
					token = ''
					newTokenFlag = True
					identifierFlag = False
				else:
					identifierFlag = True
					newTokenFlag = False
					
		f.write("</tokens>")
		
	def _stripFile(self, inputFilename, source):
		if self._isDirectory:
			with open(os.path.abspath(f'./{source}/{inputFilename}'), 'r') as data:
				f = open(f'./{source}/stripped_{inputFilename}', 'w')
				
				self._removeComments(data, f)

				f.close()
		else: # Source is a single .jack file then
			with open(os.path.abspath(f'./{inputFilename}'), 'r') as data:
		
				f = open(f'stripped_{inputFilename}', 'w')
				
				self._removeComments(data, f)

				f.close()
		
		return f
	
	def _removeComments(self, data, f):
		isMultilineComment = False
				
		for line in data:
			#Remove single line comments i.e., "//........."
			line = re.sub("\/\/.*", "", line)
						
			if isMultilineComment:
				# Check if line contains the end of a multiline comment i.e., */
				if re.search('\*\/', line):
					isMultilineComment = False
							
					line = re.sub(".*\*\/", "", line)
				else:
					#Skip to next line
					continue
						
			# Check if line is a one line comment of the form '/* ..... */'
			elif re.search('\/\*.*\*\/', line):
				line = re.sub("\/\*.*\*\/", "", line)					
					
			# Check if line contains the start of a multiline comment i.e., /*
			elif re.search('\/\*', line):
				isMultilineComment = True
				line = re.sub("\/\*.*", "", line)
	
			if line and not line.isspace():
				line = line.strip()
				f.write(line + '\n')	