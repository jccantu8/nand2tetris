class FileParser(Object):

	def __init__(self, filename):
		self._COMMANDSLIST = {
			"push": "C_PUSH",
			"pop": "C_POP",
			"add": "C_ARITHMETIC",
			"sub": "C_ARITHMETIC",
			"neg": "C_ARITHMETIC",
			"eq": "C_ARITHMETIC",
			"gt": "C_ARITHMETIC",
			"lt": "C_ARITHMETIC",
			"and": "C_ARITHMETIC",
			"or": "C_ARITHMETIC",
			"not": "C_ARITHMETIC",
			"label": "C_LABEL",
			"goto": "C_GOTO",
			"if-goto": "C_IF",
			"function": "C_FUNCTION",
			"return": "C_RETURN",
			"call": "C_CALL",
		}

		# Open the provided vm file and add all lines to an instance variable 
		# list that will serve as the program instructions to be read from. 
		# All whitespace and comments are removed.
        with open(filename, 'r') as data:
            self._data = []
            
            for line in data:
                line = line.strip()
                line = re.sub("\/\/.*", "", line)
                if line:
                    self._data.append(line)

        # Initialize a 'cursor' pointer to keep track of which instruction
        # command is being executed in the program. Starts at -1 because 
        # the first call to advance will place the cursor at the start of the list.
        self._currentPosition = -1

	def hasMoreCommands(self):
		# Checks if there are more instructions in the program by ensuring currentPosition cursor
        # is not outside the programs instruction's list range
        if (self._currentPosition + 1) < len(self._data):
            return True
        else:
            return False

	def advance(self):
		self._currentPosition += 1

	# Could be a private method
	def currentCommand(self):
		# Split the current command into an array containing its respective components
		# e.g. "push local 1" becomes ["push", "local", "1"]
		# Could memoize this
		return self._data[self._currentPosition].split()

	def commandType(self):
		# Returns type of current command
		return self._COMMANDSLIST[self.currentCommand()[0]]

	def arg1(self):
		# If current command is an arithmetic command, return that specific command.
		# If current command is the return command, return None.
		# Else returns first argument of current command, if it exists
		commandType = self.commandType()
		if commandType in ["C_ARITHMETIC", "C_RETURN"]:
			if commandType == "C_ARITHMETIC":
				return self.currentCommand()[0]
			else:
				return None
		else:
			return self.currentCommand()[1] or None

	def arg2(self):
		# If current command is push, pop, function, or call return the second argument
		# in the current command. Else return None.
		commandType = self.commandType()
		if commandType in ["C_PUSH", "C_POP", "C_FUNCTION", "C_CALL"]:
			self.currentCommand()[2]
		else:
			return None