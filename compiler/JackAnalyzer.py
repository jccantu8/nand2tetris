from compiler.JackTokenizer import JackTokenizer
from compiler.CompilationEngine import CompilationEngine
import re
import os.path

files = []
isDirectory = False

def main(source):
	singleFileOrDirectory(source)
	
	for file in files:
		token = JackTokenizer(file, isDirectory, source)
		CompilationEngine(token.tokens, file, isDirectory, source)

def singleFileOrDirectory(source):
	if re.search('\.jack', source):
		files.append(source)
	else:
		global isDirectory
		isDirectory = True
		
		for file in os.listdir(f'./{source}'):
			if re.search('\.jack', file):
				files.append(file)
			
if __name__ == "__main__":
	main('Square')