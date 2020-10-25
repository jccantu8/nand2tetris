from vmtranslator.fileparser import FileParser
from vmtranslator.codewriter import CodeWriter
import os.path

def main(directory):
	# Instantiate codewriter
	cw = CodeWriter()

	with open(os.path.abspath(f'./{directory}/{directory}.asm'), 'w') as f:
		for file in os.listdir(f'./{directory}'):
			filename = file
			cw.setFileName(filename)
		
			file = FileParser(directory, filename)
			
			initialization_flag = True
			
			while file.hasMoreCommands():
				file.advance()
				
				if initialization_flag: f.write(cw.writeInit())
				
				initialization_flag = False
	
				commandType = file.commandType()
				if commandType == "C_ARITHMETIC":
					f.write(cw.writeArithmetic(file.arg1()))
				elif commandType in ["C_PUSH", "C_POP"]:
					f.write(cw.writePushPop(commandType, file.arg1(), file.arg2()))
				elif commandType == "C_LABEL":
					f.write(cw.writeLabel(file.arg1()))
				elif commandType == "C_IF":
					f.write(cw.writeIf(file.arg1()))
				elif commandType == "C_GOTO":
					f.write(cw.writeGoto(file.arg1()))
				elif commandType == "C_FUNCTION":
					f.write(cw.writeFunction(file.arg1(), file.arg2()))
				elif commandType == "C_RETURN":
					f.write(cw.writeReturn())
				elif commandType == "C_CALL":
					f.write(cw.writeCall(file.arg1(), file.arg2()))
				else:
					pass				f.write("\n")

if __name__ == "__main__":
	main('StaticsTest')