
from compiler import compiler

input_memory_min = 16636
ram_memory_min = 32768
screen_memory_min = 16892
screen_memory_max = 18892
screen_width = 80
screen_height = 25


def add(n):
    return hex(ram_memory_min + n)

def screen(x, y):
    return hex(screen_memory_min + (y * screen_width) + x)

def ascii(char):
    return hex(ord(char))

def input(n):
    return hex(input_memory_min + n)

def val(n):
    opVal = [120, 119, 76, 43, 22, 17,  2]
    return hex(opVal[n])


data = [
    ["SET", "A", screen(1, 1)], # Screen Index

    ["JMP", "X", hex(7)], # 1
    ["ADD", "A", hex(1)],
    ["EQ", "D", ascii('q')],
    ["JMC", "Z", hex(6)],
    ["JMP", "Z", hex(1)],

    ["HLT", "Z", "Z"], # 6


    # Function Load Letter (Return Register D)
    ["SET", "D", ascii("a")], # 7 - ? | Current letter
    ["SET", "E", "Y"],
    ["MV", "G", "E"], # MOV E in G
    ["LD", "F", input(0)],
    ["EZ", "F", "Z"],
    ["JMC", "Z", "E"], # 12 - 3

    ["ADD", "G", hex(10)],
    ["EQ", "F", ascii('n')],
    ["JMC", "Z", "G"], # 15 - ?

    ["ADD", "G", hex(3)],
    ["EQ", "F", ascii('p')],
    ["JMC", "Z", "G"],

    ["ADD", "G", hex(4)], # 19 - 10
    ["ADD", "D", hex(1)],
    ["JMP", "Z", "G"],

    ["SUB", "D", hex(1)],

    ["ST", "D", "A"], # 23 - 15

    ["LT", "F", ascii('s')], # si D < s
    ["JMC", "Z", "E"],
    ["SUB", "D", hex(1)],
    ["HFT", "Z", "Z"]

]


cmp = compiler()

prog = ""
for d in data:
    print(str(d[0]) + " " + d[1] + " " + d[2])
    prog += cmp.instructionToBinary(d[0], d[1], d[2])

file = open("bintest","w")
file.write(prog)
file.close()
