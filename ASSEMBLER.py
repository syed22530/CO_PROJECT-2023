
import sys
import keyword
# opcode_={"instruction name":["binary of opcode instruction","type of instruction"]}
opcode={
    "add": "00000",
    "sub": "00001",
    "mov": "00010",     
    "mov": "00011",     
    "ld" : "00100",
    "st" : "00101",
    "mul": "00110",
    "div": "00111",
    "rs" : "01000",
    "ls" : "01001",
    "xor": "01010",
    "or" : "01011",
    "and": "01100",
    "not": "01101",
    "cmp": "01110",
    "jmp": "01111",
    "jlt": "11100",
    "jgt": "11101",
    "je" : "11111",
    "hlt": "11010",}
registers={"reg0":["000","0000000000000000"],
           "reg1":["001","0000000000000000"],
           "reg2":["010","0000000000000000"],
           "reg3":["011","0000000000000000"],
           "reg4":["100","0000000000000000"],
           "reg5":["101","0000000000000000"],
           "reg6":["110","0000000000000000"],
           "FLAGS":["111","0000000000000000"]}
memory_address = {}
for i in range(128):
    bin_str = format(i, '07b')  
    memory_address[bin_str] = []

def is_valid_number(num):
    if num.isdigit():  
        num = int(num)
        if 0 <= num <= 127: 
            return True
    return False
def is_binary(value):
    value_str = str(value)
    for char in value_str:
        if char != "0" and char != "1":
            return False
    return True

def comment_or_emptyline(line):
    if line.strip() == "" or line.strip()[0] == "#":
        return True
    return False
def is_empty(line):
    if not line.strip():
        return True
    return False

def decimal_to_binary_7(decimal):
    decimal=int(decimal)
    return bin(decimal)[2:].zfill(7)

def decimal_to_binary_16(decimal):
    decimal=int(decimal)
    return bin(decimal)[2:].zfill(16) 

def binary_to_decimal(binary):
    return int(binary, 2)

def comment_or_emptyline(line):
    if line.strip() == "" or line.strip()[0] == "#":
        return True
    return False
            
def is_hlt_last(input):
    lenth=len(input)-1
    if input[lenth][-1]=="hlt":
        pass
    else:
        print("ERROR:  at line no. ",lenth+1, "hlt instruction missing from last of program")

def is_hlt_only_in_last(input):
    for i in range(len(input)-1):
        if input[i][0]=="hlt":
            print("ERROR:  at line no. ",i+1, " hlt instruction present in a line other than the last one")
            sys.exit()
    else:
        return True  
    
def is_valid_word(input):
    for i in range(len(input)):
        if input[i][0] in opcode.keys():
            continue
        elif input[i][0]=="var":
            continue
        elif input[i][0][-1]==":":
            continue
        else:
            print("Syntax ERROR,at",i+1,"not a valid opcode/literal/label")
            sys.exit()
    return True

var_name_list=[]
def is_var(input):
    for i in range(len(input)):
        if input[i][0]=="var":
            if len(input[i]) == 2:
                var_name = input[i][1]
                if keyword.iskeyword(var_name):
                    print("Error,  at line no. ",i+1, "Python keyword can not be used as var name")
                    sys.exit()
                if not var_name.isidentifier():
                    print("ERROR  at line no. ",i+1, "", words[1], "can not be a valid variable name")
                    sys.exit()
            else:
                print("syntax ERROR at line no. ",i+1, " 'var' takes only one operand as name of the var but ", str(len(input[i])-1), " was given")
                sys.exit()
        var_name_list.append(input[i][1])
    return True 
    
label_name_list=[]
def is_label(input):
    for i in range(len(input)):
        if input[i][0][-1]==":":
            label_name_list.append(input[i][0])
    return True   
             
def is_var_above(input):   
    for i in range(len(input)):
        if input[i][0]!="var":
            break    
    for j in range(i,len(input)):
        if input[j][0]=="var": 
            print("ERROR, at line no. ",j+1, " variable names should be declared in the  starting of the program")
            sys.exit()        
    return True

def is_valid_syntax(input):
    for i in range(len(input)):
        if input[i][0][-1]==":":
            input[i]=input[i][1:]
        words=input[i]
        op_code= words[0]
        if op_code in ["add", "sub", "mul", "xor", "or", "and"]:
            if len(words) == 4:
                for word in words[1:]:
                    if word not in ["reg0", "reg1", "reg2", "reg3", "reg4", "reg5", "reg6","FLAGS"]:
                        print("Syntax ERROR:  at line no. ",i+1, ""  + word+"is not a valid register name")
                        sys.exit()
                    if word=="FLAGS":
                        print("ERROR:at line no.",i+1,",  illegal use of FLAGS  register")
                        sys.exit()
                return True
            else:
                print("Syntax ERROR: at line no.",i+1, +   op_code + "' supports three operands, " + str(len(words)-1) + " were given")
                sys.exit()
                
                
                
        elif op_code in ["mov","rs","ls","div","not","cmp"]: #type_B and type_C error checking
            if words[2]  not in  ["reg0", "reg1", "reg2", "reg3", "reg4", "reg5", "reg6"]: #type_B
                if len(words) == 3:
                    for word in words[1:2]:
                        if word not in ["reg0", "reg1", "reg2", "reg3", "reg4", "reg5", "reg6","FLAGS"]:
                            print("Syntax ERROR:  at line no. ",i+1, ""  + word+"is not a valid register name")
                            sys.exit()
                        if word=="FLAGS":
                            print("ERROR:at line no.",i+1,",  illegal use of FLAGS  register")
                            sys.exit()
                    for word in words[2:3]:
                        if word[0]=="$":
                            if not is_valid_number(word[1:]):
                                print("ERROR :  at line no. ",i+1, ""  + word+"must be integer between 0 and 127")
                                sys.exit() 
                        else:
                            print("Syntax ERROR:  at line no. ",i+1, " Second operand must be $imm integer between 0 and 127 , out of range value or \"$\" is missing  ")
                    return True
                else:
                    print("Syntax ERROR:  at line no. ",i+1, "'" + op_code + "' supports 2 operands, " + str(len(words)-1) + " were given")
                    sys.exit()
                    
            else: #type_C
                if len(words) == 3:
                    if words[0]=="mov":
                        for word in words[1:2]:
                            if word not in ["reg0", "reg1", "reg2", "reg3", "reg4", "reg5", "reg6","FLAGS"]:
                                print("Syntax ERROR:  at line no. ",i+1, ""  + word+"is not a valid register name")
                                sys.exit()
                            if word=="FLAGS":
                                print("ERROR:at line no.",i+1,",  illegal use of FLAGS  register")
                                sys.exit()
                        for word in words[2:]:
                            if word not in ["reg0", "reg1", "reg2", "reg3", "reg4", "reg5", "reg6","FLAGS"]:
                                print("Syntax ERROR:  at line no. ",i+1, ""  + word+"is not a valid register name")
                                sys.exit()
                    else:
                        for word in words[1:]:
                            if word not in ["reg0", "reg1", "reg2", "reg3", "reg4", "reg5", "reg6","FLAGS"]:
                                print("Syntax ERROR:  at line no. ",i+1, ""  + word+"is not a valid register name")
                                sys.exit()
                            if word=="FLAGS":
                                print("ERROR:at line no.",i+1,",  illegal use of FLAGS  register")
                                sys.exit()
                        return True
                else:
                    print("Syntax ERROR:  at line no. ",i+1, "'" + op_code + "' supports 2 operands, " + str(len(words)-1) + " were given")
                    sys.exit()
            
        elif op_code in ["ld","st"]: #type_D error checking
            if len(words) == 3:
                for word in words[1:2]:
                    if word not in ["reg0", "reg1", "reg2", "reg3", "reg4", "reg5", "reg6","FLAGS"]:
                        print("Syntax ERROR at line no. ",i+1, ": "  + word+"is not a valid register name")
                        sys.exit()
                    if word=="FLAGS":
                        print("ERROR:at line no.",i+1,",  illegal use of FLAGS  register")
                        sys.exit()
                for word in words[2:3]:
                    if  word in var_name_list:
                         pass
                    else:
                        print("Name ERROR: at line no.",i+1, ""  + word+" is not a defined variable ")
                        sys.exit()        
                              
                return True
            else:
                print("Syntax ERROR:  at line no. ",i+1, "'" + op_code + "' supports 2 operands, " + str(len(words)-1) + " were given")
                sys.exit()
                
        elif op_code in ["jmp","jlt","jgt","je"]: #type_E error checking
            if len(words) == 2:
                for word in words[1:2]:
                    if  word in label_name_list:
                         pass
                    else:
                        print("Name ERROR: at line no.",i+1, ""  + word+" is not a defined label")
                        sys.exit()  
                
                return True

            else:
                print("Syntax ERROR:  at line no. ",i+1, " '" + op_code + "' supports 2 operands, " + str(len(words)-1) + " were given")
                sys.exit() 
                
        elif op_code=="hlt" :
            return True            
        
        elif op_code=="var":
            pass
            
        elif op_code[-1]==":":
            pass
        
        else:
            print("Syntax ERROR:  at line no. ",i+1, "Invalid instruction! ",words[0],"is not an instruction")
            sys.exit()
                
        
     
input = []
with open('input_assembly.txt', 'r') as file:
    for line in file:
        line = line.rstrip() 
        if comment_or_emptyline(line):
            continue
        else:
            words = line.split()  
            input.append(words)

if is_hlt_last(input):
    pass
if is_hlt_only_in_last(input):
    pass
if is_var_above(input):
    pass
if is_valid_word(input):
    pass
if is_label(input):
    pass
if is_var(input):
    pass
if is_valid_syntax(input):
    pass

total_instruction=0
for i in input:
    if i[0]=="var":
        continue
    else:
        total_instruction+=1

for i in input:
    if i[0]=="var":
        j=decimal_to_binary_7(total_instruction)
        memory_address[j]=[i[1]]
        temp_list=[j,i[1],"0000000"]
        memory_address[i[1]]=temp_list
        total_instruction+=1
        
total_lines=0
for i in input:
    if i[0]=="var":
        pass
    elif 
    
print(memory_address)


