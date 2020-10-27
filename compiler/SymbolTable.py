class SymbolTable(object):
	
	def __init__(self):
		self.table = {}
		
		self.varCounts = {
			'FIELD': 0,
			'STATIC': 0,
			'ARG': 0,
			'VAR': 0 #local vars
		}
	
	#***** classVarDec is where static and field is defined. varDec is where var (local) is defined, and parameterList is where argument is defined .... i think
	#***** expression is where identifiers are being used
	
	def startSubroutine(self):
		self.table = {}
	
	def define(self, name, type, kind):
		#kind should be passed as STATIC, FIELD, ARG, or VAR
		
		self.table[name]= {'type': type, 'kind': kind, 'index': self.varCount(kind)}
		
		self._indexIncrementer(kind)
	
	def varCount(self, kind):
		# Should return an int
		return self.varCounts[kind]
	
	def kindOf(self, name):
		# Should return STATIC, FIELD, ARG, VAR, or NONE
		
		# TODO: handle none
		return self.table[name]['kind']
	
	def typeOf(self, name):
		# Should return a string
		return self.table[name]['type']
	
	def indexOf(self, name):
		# Should return an int
		return self.table[name]['index']
	
	#Private
	
	def _indexIncrementer(self, kind):
		self.varCounts[kind] += 1