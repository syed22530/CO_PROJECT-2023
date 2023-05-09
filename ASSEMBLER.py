# opcode_={"instruction name":["binary of opcode instruction","type of instruction"]}
opcode={
    "add": ["10000","A"],
    "sub": ["10001","A"],
    "mov": ["10010","B"], #MoveImmediate
    "mov": ["10011","C"], #MoveRegister
    "ld" : ["10100","D"],
    "st" : ["10101","D"],
    "mul": ["10110","A"],
    "div": ["10111","C"],
    "rs" : ["11001","B"],
    "ls" : ["11001","B"],
    "xor": ["11010","A"],
    "or" : ["11011","A"],
    "and": ["11100","A"],
    "not": ["11101","C"],
    "cmp": ["11110","C"],
    "jmp": ["11111","E"],
    "jlt": ["01100","E"],
    "jgt": ["01101","E"],
    "je" : ["01111","E"],
    "hlt": ["01010","F"],}
registers={"reg1":"000",
           "reg2":"001",
           "reg3":"010",
           "reg4":"011",
           "reg5":"100",
           "reg6":"101",
           "reg7":"110",
           "FLAGS":"111"}
reg1=""
reg2=""
reg3=""
reg4=""
reg5=""
reg6=""
reg7=""
FLAGS=""
op_code_list=["add","sub","mov","mov","ld","st","mul","div","rs","ls","xor","or","and","not","cmp","jmp","jlt","jgt","je","hlt"]
location_counter=0
instruction_counter=0
var_counter=0
def comment(line):
    if (line != "\n" and line.strip()[0] == "#"):
        return True
    return False
def is_empty(line):
    if not line.strip():
        return True
    return False
def is_label(line):
    if line.strip()[-1] == ':':
        return True
    return False
def decimal_to_binary(decimal):
    return bin(decimal)[2:].zfill(7)
def binary_to_decimal(binary):
    return int(binary, 2)
def check_op_code(line, op_code_list):
    words = line.strip().split()
    if len(words) > 0 and words[0] in op_code_list:
        return True
    else:
        return False

with open('input_assembly.txt', 'r') as file:
    for line in file:
        print(line)
        if comment(line):
            continue
        elif is_empty(line):
            continue
        else:
            if check_op_code(line, op_code_list):
                pass
            else:
                words = line.strip().split()
                print("syntax error,",words[0],"is not defined")
                
            
 
