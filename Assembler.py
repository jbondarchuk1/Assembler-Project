import os
import re
from AssemInstruc import comp, jump, dest, label

class assembler:
    def __init__ (self, file):
        self.file = file

    def prepareFile (self, preParse):
        # we need to do a passthrough of the entire code to translate it properly. 
        # for any personal label (string), remove the (string) from the program and change its corresponding @string to be-
        # -@ line number of instruction immediately after (string)
        # for any @string/char type, variable, that has no (parentheses): increment for each variable starting at memory location 16

        personalLabel = {} # save the whole variable name along with line number, ex: {"(variable)":5}
        currentLineNumber = 0
        numberOfVariables = 0
        for line in preParse:
            line = line[:len(line)-1]
            
            if '//' in line:
                commentOut = re.split(r'[/]', line)
                line = commentOut[0]
            line = line.strip()
            if line != '':
                currentLineNumber += 1
                # print(f'line={line}, line number= {currentLineNumber}')
                if line[0] == '(':
                    myLabel = line
                    # myLabel = line[:len(line)-1]
                    personalLabel[myLabel] = currentLineNumber-numberOfVariables-1
                    numberOfVariables += 1

        # print(personalLabel)
        variableCounter = 0
        preParse1 = []
        namedSymbols = {}
        for line in preParse: # removing comments
            line = line[:len(line)-1]
            if '//' in line:
                commentOut = re.split(r'[/]', line)
                line = commentOut[0]
            line = line.strip()

            if line != '': # don't include whitespace
                if line[0] != '(': # don't include lines with (variable)
                    if line[0] == '@':
                        try: # handling of @memory variables
                            int(line[1:])
                        except:
                            personalLabelCheck = '('+line[1:]+')'
                            if line[1:] in label.keys(): # handling of preset symbols
                                line = '@' + label[line[1:]]

                            elif personalLabelCheck in personalLabel.keys(): # handling of named symbols that reference an area in the code
                                line = '@' + f'{str(personalLabel[personalLabelCheck])}'
                                numberOfVariables -=1

                            else: # handling of arbitrarily named symbols
                                print(line)
                                if line in namedSymbols.keys():
                                    line = '@' + f'{namedSymbols[line] + 16}'
                                elif line not in namedSymbols.keys():
                                    namedSymbols[line] = variableCounter
                                    line = '@' + f'{str(16 + variableCounter)}'
                                    variableCounter += 1
                    preParse1.append(line)
        print(f'named symbols: {namedSymbols.keys()}')
        # print(preParse1)
        return preParse1

# requirements: takes a file with: no variables, arbitrary labels, or (variable) reference lines and turns it from .asm to .hack
    def parser (self):
        # opening file
        asmFile= open(self.file, "r") # open asm file
        preParse = asmFile.readlines()

        hackLocation = self.file
        hackLocation = hackLocation[:len(hackLocation)-3]
        hackLocation+='hack'

        hackFile = open(f"{hackLocation}", "w+") # open hack file in same folder as asm file
        preParse1 = self.prepareFile(preParse)

        hackFileContents = []
        for line in preParse1: # make sure to change this to the array made from the first for loop
            if line != '':
                if line[0] == '@': # handling of A instructions
                    # print(line)
                    memLocation = int(line[1:]) # handles normal integer memLocation
                    binaryMemLocation = bin(memLocation)
                    binaryMemLocation = str(binaryMemLocation[2:])
                    for _ in range(16-len(binaryMemLocation)):
                        binaryMemLocation= "0" + binaryMemLocation
                    hackFileContents.append(binaryMemLocation + "\n")

                else: # handling of C instructions
                    line = re.split(r'[;=]', line)
                    # print(line)
                    runningCBinary = '111'
                    onlyCompAndJump = False
            # computation handling
                    if line[1] in comp.keys():
                        runningCBinary += comp[line[1]]
                    else:
                        runningCBinary += comp[line[0]]
                        if line[1] in jump.keys():
                            onlyCompAndJump = True

            # destination handling
                    if line[0] in dest.keys() and onlyCompAndJump == False:
                        runningCBinary += dest[line[0]]
                    else:
                        runningCBinary += "000"

            # jump handling
                    if onlyCompAndJump == True:
                        runningCBinary += jump[line[1]]
                    else:
                        runningCBinary += '000'

                    if len(line) >= 3:
                        if line[2] in jump.keys():
                            runningCBinary += jump[line[3]]
                        else:
                            runningCBinary += "000"


                    hackFileContents.append(runningCBinary + '\n')

        hackFile.writelines(hackFileContents)
        asmFile.close()
        hackFile.close()

        # print(hackFileContents)

add = assembler("projects/06/add/Add.asm")
Max = assembler("projects/06/max/Max.asm")
pong = assembler("projects/06/pong/Pong.asm")
rect = assembler("projects/06/rect/Rect.asm")
MaxL = assembler("projects/06/max/MaxL.asm")

add.parser()
Max.parser()
pong.parser()
rect.parser()