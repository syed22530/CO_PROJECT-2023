import sys
import keyword
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
registers={"reg0":"000",
           "reg1":"001",
           "reg2":"010",
           "reg3":"011",
           "reg4":"100",
           "reg5":"101",
           "reg6":"110",
           "FLAGS":"111"}
reg0=""
reg1=""
reg2=""
reg3=""
reg4=""
reg5=""
reg6=""
FLAGS=""
op_code_list=["add","sub","mov","mov","ld","st","mul","div","rs","ls","xor","or","and","not","cmp","jmp","jlt","jgt","je","hlt"]
location_counter=0
instruction_counter=0
var_counter=0
instruction_pointer=0
var_name_dict={}
def comment_or_emptyline(line):
    if line.strip() == "" or line.strip()[0] == "#":
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
def is_label(line):
    words = line.strip().split()
    if words[0][-1] == ":":
        if len(words)==1:
            return True
        else:
            return False
    else:
        return False
def is_hlt_last(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
        last_line = lines[-1].strip()
        if last_line != "hlt":
            print("ERROR: hlt instruction missing from last of program")
            sys.exit()
        for line in lines[:-1]:
            if "hlt" in line:
                print("ERROR: hlt instruction present in a line other than the last one")
                sys.exit()
        return True



def check_instruction_type_A(line, op_code_list):
    words = line.strip().split()
    if words[0]=="var" or words[0][-1]==":":
        pass
    else:
        if len(words) > 0 and words[0] in op_code_list:
            op_code = words[0]
            if op_code in ["add", "sub", "mul", "xor", "or", "and"]:
                if len(words) == 4:
                    for word in words[1:]:
                        if word not in ["reg0", "reg1", "reg2", "reg3", "reg4", "reg5", "reg6"]:
                            print("Syntax ERROR:"  + word+"is not a valid register name")
                            sys.exit()
                    return True
                else:
                    print("Syntax ERROR: '" + op_code + "' supports three operands, " + str(len(words)-1) + " were given")
                    sys.exit()
            else:
                return True
        else:
            print("Syntax ERROR: Invalid instruction! ",words[0],"is not an instruction")
            sys.exit()
def check_instruction_type_D(line, op_code_list):
    words = line.strip().split()
    if words[0]=="var":
        pass
    else:
        if len(words) > 0 and words[0] in op_code_list:
            op_code = words[0]
            if op_code in ["ld","st"]:
                if len(words) == 4:
                    for word in words[1:]:
                        if word not in ["reg0", "reg1", "reg2", "reg3", "reg4", "reg5", "reg6"]:
                            print("Syntax ERROR:"  + word+"is not a valid register name")
                            sys.exit()
                    return True
                else:
                    print("Syntax ERROR: '" + op_code + "' supports three operands, " + str(len(words)-1) + " were given")
                    sys.exit()
            else:
                return True
        else:
            print("Syntax ERROR: Invalid instruction! ",words[0],"is not an instruction")
            sys.exit()
            
def is_valid_variable_name(line, var_name_dic):
    words = line.strip().split()
    if words[0] == "var":
        if len(words) == 2:
            if instruction_pointer==0:
                var_name = words[1]
                if keyword.iskeyword(var_name):
                    print("Error, Python keyword can not be used as var name")
                    sys.exit()
                if not var_name.isidentifier():
                    print("ERROR ", words[1], "can not be a valid variable name")
                    sys.exit()
                var_name_dict[var_name]=[]
                return True
            else:
                print("ERROR, variable names should be declared in the  starting of the program")
                sys.exit()
        else:
            print("syntax ERROR 'var' takes only one operand as name of the var but ", str(len(words) - 1), " was given")
            sys.exit()
        
        
        
            
with open('input_assembly.txt', 'r') as file:
    for line in file:
        if is_hlt_last("input_assembly.txt"):
            if comment_or_emptyline(line):
                continue
            elif is_label(line):
                pass
            else:
                if is_valid_variable_name(line,var_name_dict):
                    pass
                if check_instruction_type_A(line, op_code_list):
                    instruction_pointer+=1
        
                
            
            
            
                
            
 
