

class compiler:

    opVal = {
    "NOP" : 0x00,
    "JMP" : 0x01,
    "JMZ" : 0x02,
    "JMO" : 0x03,
    "JMC" : 0x04,
    "SET" : 0x05,
    "LD" : 0x06,
    "ST" : 0x07,
    "MV" : 0x08,
    "ADD" : 0x09,
    "SUB" : 0x0A,
    "MUL" : 0x0B,
    "DIV" : 0x0C,
    "OR" : 0x00D,
    "AND" : 0x0E,
    "XOR" : 0x0F,
    "NOT" : 0x10,
    "HLT" : 0x11,
    "HFT" : 0x12, # Quitter la fonction
    "LT" : 0x13,
    "GT" : 0x14,
    "LE" : 0x15,
    "GE" : 0x16,
    "EQ" : 0x17,
    "EZ" : 0x18,
    "NZ" : 0x19,
    }

    registers = {
    "A" : 0x01,
    "B" : 0x02,
    "C" : 0x03,
    "D" : 0x04,
    "E" : 0x05,
    "F" : 0x06,
    "G" : 0x07,
    "H" : 0x08,
    "I" : 0x09,
    "X" : 0x18, # is current heap address
    "Y" : 0x19, # is current PC
    "Z" : 0x00  # is null value
    }

    def parseFile(self, filename, exportfilename = "bin"):
        """
        Convert file with instrcution to a binary file ('bin')
        """
        result = ""
        (success, content) = self.getContentOfFileWithName(filename)
        if (not success):
            print("Impossible to open : " + filename)
            return False
        for line in content:
            split = line.split(' ')
            if (len(split) > 2 and split[0][0] != "#"):
                op = split[0]
                register = split[1]
                value = split[2]
                currentRes = self.instructionToBinary(op, register, value)
                if (currentRes == False):
                    print("Compilation Error. Impossible to parse : " + str(line))
                    return False
                result += currentRes
        if (not self.exportInFile(exportfilename, result)):
            print("Impossible to export binary : " + exportfilename)
            return False
        return True

    def instructionToBinary(self, opCode, reg, val):
        """
        Convert instruction to binary string
        """
        if not opCode in self.opVal or not reg in self.registers:
            print("ERROR : op or register doesn't exist")
            return False
        (value, op) = self.getValueOfEntry(val)
        if (value == None):
            print("Load Value ERROR")
            return False
        op += self.opVal[opCode]
        bits = value
        bits += op * 0x1000000
        bits += self.registers[reg] * 0x10000
        return bin(bits)[2:].zfill(32)

    def getValueOfEntry(self, entry):
        if (not entry):
            return (0, 0)
        if (entry[0] == "#"):
            return 0
        if (entry[-1:] == '\n'):
            entry = entry[:-1]
        if (len(entry) == 0):
            return (0, 0)

        op = 0
        tmp = None
        if entry in self.registers:
            tmp = self.registers[entry]
        else:
            op += 128
            tmp = self.getNumber(entry, 10)
            if tmp == None:
                tmp = self.getNumber(entry, 16)
            if tmp == None:
                tmp = self.getNumber(entry, 2)
            if tmp == None:
                tmp = self.getAscii(entry)

        if tmp == None:
            print("Impossible to parse value : " + str(entry))
            return (None, None)
        return (tmp, op)

    def getAscii(self, value):
        if (len(value) == 8 and value[:6] == "ASCII("):
            return ord(value[6])
        return None

    def getNumber(self, value, base):
        """
        Try to convert value to int with base
        """
        try:
            return int(value, base)
        except ValueError:
            return None

    def exportInFile(self, filename, content):
        """
        Export binary prog in a file
        """
        try:
            file = open(filename,"w")
            file.write(content)
            file.close()
            return True
        except:
            return False

    def getContentOfFileWithName(self, filename):
        """
        Load file with instrcutions
        """
        try:
            file = open(filename, 'r')
            content = file.readlines()
            file.close()
            return (True, content)
        except:
            return (False, None)
