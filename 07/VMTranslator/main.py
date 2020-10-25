from VMTranslator.fileparser import FileParser
from VMTranslator.codewriter import CodeWriter

def main(filename):
	# Instantiate file and codewriter
    file = Parser(filename)
    cw = CodeWriter()

    with open(f'{filename}.asm', 'w') as f:
	    while file.hasMoreCommands():
	    	file.advance()

	    	commandType = file.commandType()
	    	if commandType == "C_ARITHMETIC":
	    		f.write(cw.writeArithmetic(file.arg1()))
	    	elif commandType in ["C_PUSH", "C_POP"]:
	    		f.write(cw.writePushPop(commandType, file.arg1(), file.arg2()))
	    	else:
	    		pass
	    	f.write("\n")



if __name__ == "__main__":
	main('filename')