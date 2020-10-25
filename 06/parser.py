import re
from assembler.code import Code
from assembler.symboltable import SymbolTable

class Parser(object):
    
    def __init__(self, filename):
        # Instantiate instances of Code class and SymbolTable class to be used
        self._myCode = Code()
        self._myTable = SymbolTable()
        
        # Open the provided assembly file and add all lines to an instance variable list
        # that will serve as the program instructions to be read from. All whitespace and
        # comments are removed.
        with open(filename, 'r') as data:
            self._data = []
            
            for line in data:
                line = line.strip()
                line = re.sub("\s", "", line)
                line = re.sub("\/\/.*", "", line)
                if line:
                    self._data.append(line)
                    
        # Initialize two 'cursors' to keep track of locations in the program. currentPosition
        # starts at -1 because the first call to advance will place the cursor at the start of the list.
        # variablePosition starts at 16 because that is the starting point in RAM given
        # in the specifications.
        self._currentPosition = -1
        self._variablePosition = 16
                
    
    def hasMoreCommands(self):
        # Checks if there are more instructions in the program by ensuring currentPosition cursor
        # is not outside the programs instruction's list range
        if (self._currentPosition + 1) < len(self._data):
            return True
        else:
            return False
    
    def advance(self):
        self._currentPosition += 1
        
    def resetPosition(self):
        self._currentPosition = -1
        
    def commandType(self):
        # Returns the command type as a string by analyzing first character
        firstChar = self._data[self._currentPosition][0]
        if firstChar == '@':
            return 'A_COMMAND'
        elif firstChar == '(':
            return 'L_COMMAND'
        else:
            return 'C_COMMAND'
    
    def symbol(self):
        currentInstruction = self._data[self._currentPosition]
        
        if self.commandType() == 'A_COMMAND':
            # Delete the '@' symbol from the instruction
            currentInstruction = re.sub("@", "", currentInstruction)
            
            # If the instruction contains any non-digit, it must be a symbol
            if re.search("\D+", currentInstruction):
                if self._myTable.contains(currentInstruction):
                    currentInstruction = self._myTable.getAddress(currentInstruction)
                else:
                    self._myTable.addEntry(currentInstruction, str(self._variablePosition))
                    self._variablePosition += 1
                    currentInstruction = self._myTable.getAddress(currentInstruction)
                    
            # Translate current Instruction into 16-bit binary code
            translatedInstruction = bin(int(re.search("\d+", currentInstruction).group()))[2:].zfill(16)
        
            return translatedInstruction
        
        else: # Must be an 'L_COMMAND' then
            # Delete parentheses from instruction
            currentInstruction = re.sub("\(", "", currentInstruction)
            currentInstruction = re.sub("\)", "", currentInstruction)
            self._myTable.addEntry(currentInstruction, str(self._currentPosition))
            # After adding symbol and its memory location to the symbol table, delete its
            # entry in the program instructions list and move the currentPosition cursor back one
            del self._data[self._currentPosition]
            self._currentPosition -= 1
    
    def dest(self):
        currentInstruction = self._data[self._currentPosition]
        
        # Check if dest code is not '000' by scanning instruction for an '='
        if re.search("=", currentInstruction):
            # Take part of instruction before '='
            destinationMnemonic = re.search(".+=", currentInstruction).group()
            destinationMnemonic = re.sub("=", "", destinationMnemonic)
        else:
            destinationMnemonic = None
        
        # Translate instruction in binary
        return self._myCode.dest(destinationMnemonic)
    
    def comp(self):
        currentInstruction = self._data[self._currentPosition]
        
        # Check if instruction contains a dest command
        if re.search("=", currentInstruction):
            # Check if instruction contains a jump command
            if re.search(";", currentInstruction):
                # Take part of instruction after '=' and before ';'
                computeMnemonic = re.search("=.+;", currentInstruction).group()
                computeMnemonic = re.sub("=", "", computeMnemonic)
                computeMnemonic = re.sub(";", "", computeMnemonic)
            else:
                # Take part of instruction after '='
                computeMnemonic = re.search("=.+", currentInstruction).group()
                computeMnemonic = re.sub("=", "", computeMnemonic)
        elif re.search(";", currentInstruction):
            # Take part of instruction before ';'
            computeMnemonic = re.search(".+;", currentInstruction).group()
            computeMnemonic = re.sub(";", "", computeMnemonic)
        else:
            computeMnemonic = currentInstruction
        
        # Translate instruction in binary
        return self._myCode.comp(computeMnemonic)
    
    def jump(self):
        currentInstruction = self._data[self._currentPosition]
        
        # Check if instruction contains a jump command
        if re.search(";", currentInstruction):
            # Take part of instruction after ';'
            jumpMnemonic = re.search(";.+", currentInstruction).group()
            jumpMnemonic = re.sub(";", "", jumpMnemonic)
        else:
            jumpMnemonic = None
        
        # Translate instruction in binary
        return self._myCode.jump(jumpMnemonic)