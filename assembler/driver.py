from assembler.parser import Parser
from assembler.symboltable import SymbolTable

def main(filename):
    # Instantiate file
    file = Parser(filename)
    
    # First pass of the program where labels are added to the symbol table
    while file.hasMoreCommands():
            file.advance()
            if file.commandType() == 'L_COMMAND':
                file.symbol()
            
    file.resetPosition()
    
    # Create binary code file to hold translated instructions
    with open("solution.txt", 'w') as f:        
        while file.hasMoreCommands():
            file.advance()
            # Translate a-instructions
            if file.commandType() == 'A_COMMAND':
                f.write(file.symbol())
                f.write("\n")
            else:
                # Translate c-instructions
                f.write("111" + file.comp() + file.dest() + file.jump())
                f.write("\n")
            

if __name__ == "__main__":
    main('Pong.asm')