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
op_code_list=["add","sub","mov","mov","ld","st","mul","div","rs","ls","xor","or","and","not","cmp","jmp","jlt","jgt","je","hlt"]
instruction_counter=0
var_counter=0
instruction_pointer=0
line_counter=1
var_name_list=[]
assembly_code=[]
machine_code=[]
label_name_list=[]
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

def is_label(line):
    words = line.strip().split()
    if words[0][-1] == ":":
        if len(words)==1:
            if words[0][:-1] in var_name_list:
                print("ERROR,at line no.",line_counter,"same label name declared multiple times")
                sys.exit()
            label_name_list.append(words[0][:-1])
            return True
        else:
            print("ERROR,at line no.",line_counter,"in label,  next instruction hsould be from next line")
            sys.exit()
            
def is_hlt_last(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
        last_line = lines[-1].strip()
        if last_line != "hlt":
            print("ERROR:  at line no. ",line_counter, "hlt instruction missing from last of program")
            sys.exit()
        for line in lines[:-1]:
            if line[0]=="hlt":
                print("ERROR:  at line no. ",line_counter, " hlt instruction present in a line other than the last one")
                sys.exit()
        return True


#code for error checking
def check_instruction_error(line, op_code_list):
    words = line.strip().split()
    if len(words) > 0 and words[0] in op_code_list:  # type_A error checking
        op_code = words[0]
        if op_code in ["add", "sub", "mul", "xor", "or", "and"]:
            if len(words) == 4:
                for word in words[1:]:
                    if word not in ["reg0", "reg1", "reg2", "reg3", "reg4", "reg5", "reg6","FLAGS"]:
                        print("Syntax ERROR:  at line no. ",line_counter, ""  + word+"is not a valid register name")
                        sys.exit()
                    if word=="FLAGS":
                        print("ERROR:at line no.",line_counter,",  illegal use of FLAGS  register")
                        sys.exit()
                return True
            else:
                print("Syntax ERROR: at line no.",line_counter, +   op_code + "' supports three operands, " + str(len(words)-1) + " were given")
                sys.exit()
                
                
                
        elif op_code in ["mov","rs","ls","div","not","cmp"]: #type_B and type_C error checking
            if words[2]  not in  ["reg0", "reg1", "reg2", "reg3", "reg4", "reg5", "reg6"]: #type_B
                if len(words) == 3:
                    for word in words[1:2]:
                        if word not in ["reg0", "reg1", "reg2", "reg3", "reg4", "reg5", "reg6","FLAGS"]:
                            print("Syntax ERROR:  at line no. ",line_counter, ""  + word+"is not a valid register name")
                            sys.exit()
                        if word=="FLAGS":
                            print("ERROR:at line no.",line_counter,",  illegal use of FLAGS  register")
                            sys.exit()
                    for word in words[2:3]:
                        if word[0]=="$":
                            if not is_valid_number(word[1:]):
                                print("ERROR :  at line no. ",line_counter, ""  + word+"must be integer between 0 and 127")
                                sys.exit() 
                        else:
                            print("Syntax ERROR:  at line no. ",line_counter, " Second operand must be $imm integer between 0 and 127 , wrong syntax or \"$\" is missing  ")
                    return True
                else:
                    print("Syntax ERROR:  at line no. ",line_counter, "'" + op_code + "' supports 2 operands, " + str(len(words)-1) + " were given")
                    sys.exit()
                    
            else: #type_C
                if len(words) == 3:
                    if words[0]=="mov":
                        for word in words[1:2]:
                            if word not in ["reg0", "reg1", "reg2", "reg3", "reg4", "reg5", "reg6","FLAGS"]:
                                print("Syntax ERROR:  at line no. ",line_counter, ""  + word+"is not a valid register name")
                                sys.exit()
                            if word=="FLAGS":
                                print("ERROR:at line no.",line_counter,",  illegal use of FLAGS  register")
                                sys.exit()
                        for word in words[2:]:
                            if word not in ["reg0", "reg1", "reg2", "reg3", "reg4", "reg5", "reg6","FLAGS"]:
                                print("Syntax ERROR:  at line no. ",line_counter, ""  + word+"is not a valid register name")
                                sys.exit()
                    else:
                        for word in words[1:]:
                            if word not in ["reg0", "reg1", "reg2", "reg3", "reg4", "reg5", "reg6","FLAGS"]:
                                print("Syntax ERROR:  at line no. ",line_counter, ""  + word+"is not a valid register name")
                                sys.exit()
                            if word=="FLAGS":
                                print("ERROR:at line no.",line_counter,",  illegal use of FLAGS  register")
                                sys.exit()
                        return True
                else:
                    print("Syntax ERROR:  at line no. ",line_counter, "'" + op_code + "' supports 2 operands, " + str(len(words)-1) + " were given")
                    sys.exit()
            
        elif op_code in ["ld","st"]: #type_D error checking
            if len(words) == 3:
                for word in words[1:2]:
                    if word not in ["reg0", "reg1", "reg2", "reg3", "reg4", "reg5", "reg6","FLAGS"]:
                        print("Syntax ERROR at line no. ",line_counter, ": "  + word+"is not a valid register name")
                        sys.exit()
                    if word=="FLAGS":
                        print("ERROR:at line no.",line_counter,",  illegal use of FLAGS  register")
                        sys.exit()
                for word in words[2:3]:
                    if  word in var_name_list:
                         pass
                    else:
                        print("Name ERROR: at line no.",line_counter, ""  + word+" is not a defined variable ")
                        sys.exit()        
                              
                return True
            else:
                print("Syntax ERROR:  at line no. ",line_counter, "'" + op_code + "' supports 2 operands, " + str(len(words)-1) + " were given")
                sys.exit()
                
        elif op_code in ["jmp","jlt","jgt","je"]: #type_E error checking
            if len(words) == 2:
                for word in words[1:2]:
                    if  word in label_name_list:
                         pass
                    else:
                        print("Name ERROR: at line no.",line_counter, ""  + word+" is not a defined label")
                        sys.exit()  
                
                return True
            else:
                print("Syntax ERROR:  at line no. ",line_counter, " '" + op_code + "' supports 2 operands, " + str(len(words)-1) + " were given")
                sys.exit() 
    else:
        print("Syntax ERROR:  at line no. ",line_counter, "Invalid instruction! ",words[0],"is not an instruction")
        sys.exit()
        
        
   
         
def is_valid_variable_name(line, var_name_list):
    words = line.strip().split()
    if words[0] == "var":
        if len(words) == 2:
            if instruction_pointer==0:
                var_name = words[1]
                if keyword.iskeyword(var_name):
                    print("Error,  at line no. ",line_counter, "Python keyword can not be used as var name")
                    sys.exit()
                if not var_name.isidentifier():
                    print("ERROR  at line no. ",line_counter, "", words[1], "can not be a valid variable name")
                    sys.exit()
                if var_name in var_name_list:
                    print("ERROR,at line no."+line_counter+" same variable name declared multiple times")
                    sys.exit()
                var_name_list.append(var_name)
                return True
            else:
                print("ERROR, at line no. ",line_counter, " variable names should be declared in the  starting of the program")
                sys.exit()
        else:
            print("syntax ERROR at line no. ",line_counter, " 'var' takes only one operand as name of the var but ", str(len(words) - 1), " was given")
            sys.exit()
            
with open('input_assembly.txt', 'r') as file:
    for line in file:
        if comment_or_emptyline(line):
                continue
        if is_label(line):
            line_counter+=1
        else:
            line_counter+=1
          

        
line_counter=1
with open('input_assembly.txt', 'r') as file:
    for line in file:
        if is_hlt_last("input_assembly.txt"):
            if comment_or_emptyline(line):
                continue
            elif is_label(line):
                pass
            else:
                if is_valid_variable_name(line,var_name_list):
                    pass
                elif check_instruction_error(line, op_code_list):
                    instruction_pointer+=1
        line_counter+=1
        assembly_code.append(line.strip().split()) 

instruction_counter=0      
for i in assembly_code:
    if i[0] =="var":
        continue
    elif  i[0][:-1] in label_name_list:
        j=decimal_to_binary_7(instruction_counter+1)
        temp_list=[j,i[0],"0000000"]
        memory_address[i[0][:-1]]=temp_list
    else:
        instruction_counter+=1    
          
# here wwe are alloting memory to variables     
for i in assembly_code:
    if i[0]=="var":
        j=decimal_to_binary_7(instruction_counter)
        temp_list=[j,i[1],"0000000"]
        memory_address[i[1]]=temp_list
        instruction_counter+=1   

memory_address_pointer=0
k=0     
while k<len(assembly_code):
    i=assembly_code[k]
    ########## type A
    if i[0]=="add":
        machine_code.append(opcode[i[0]]+"_00"+"_"+registers[i[1]][0]+"_"+registers[i[2]][0]+"_"+registers[i[3]][0])
        if binary_to_decimal(registers[i[2]][1])+binary_to_decimal(registers[i[3]][1])>65535:
            registers["FLAGS"][1]="0000000000001000"
            registers[i[1]][1]="0000000000000000"
        else:
            registers[i[1]][1]=decimal_to_binary_16(    binary_to_decimal(registers[i[2]][1])  +   binary_to_decimal(registers[i[3]][1])   )   
        j=decimal_to_binary_7(memory_address_pointer)
        memory_address[j].append(opcode[i[0]]+"_00"+"_"+registers[i[1]][0]+"_"+registers[i[2]][0]+"_"+registers[i[3]][0])
        k+=1
        
    elif i[0]=="mul":
        machine_code.append(opcode[i[0]]+"_00"+"_"+registers[i[1]][0]+"_"+registers[i[2]][0]+"_"+registers[i[3]][0])
        if binary_to_decimal(registers[i[2]][1])*binary_to_decimal(registers[i[3]][1])>65535:
            registers["FLAGS"][1]="0000000000001000"
            registers[i[1]][1]="0000000000000000"
        else:
            registers[i[1]][1]=decimal_to_binary_16(    binary_to_decimal(registers[i[2]][1])  *   binary_to_decimal(registers[i[3]][1])   )   
        j=decimal_to_binary_7(memory_address_pointer)
        memory_address[j].append(opcode[i[0]]+"_00"+"_"+registers[i[1]][0]+"_"+registers[i[2]][0]+"_"+registers[i[3]][0])
        k+=1
        
    elif i[0]=="sub":
        machine_code.append(opcode[i[0]]+"_00"+"_"+registers[i[1]][0]+"_"+registers[i[2]][0]+"_"+registers[i[3]][0])
        if binary_to_decimal(registers[i[2]][1])<binary_to_decimal(registers[i[3]][1]):
            registers["FLAGS"][1]="0000000000001000"
            registers[i[1]][1]="0000000000000000"
        else:
            registers[i[1]][1]=decimal_to_binary_16(    binary_to_decimal(registers[i[2]][1])  -   binary_to_decimal(registers[i[3]][1])   )
        j=decimal_to_binary_7(memory_address_pointer)
        memory_address[j].append(opcode[i[0]]+"_00"+"_"+registers[i[1]][0]+"_"+registers[i[2]][0]+"_"+registers[i[3]][0])
        k+=1
        
    elif i[0]=="xor":
        machine_code.append(opcode[i[0]]+"_00"+"_"+registers[i[1]][0]+"_"+registers[i[2]][0]+"_"+registers[i[3]][0])
        registers[i[1]][1]=(bin(int(registers[i[2]][1], 2) ^ int(registers[i[3]][1], 2))[2:].zfill(16))
        j=decimal_to_binary_7(memory_address_pointer)
        memory_address[j].append(opcode[i[0]]+"_00"+"_"+registers[i[1]][0]+"_"+registers[i[2]][0]+"_"+registers[i[3]][0])
        k+=1
        
    elif i[0]=="or":
        machine_code.append(opcode[i[0]]+"_00"+"_"+registers[i[1]][0]+"_"+registers[i[2]][0]+"_"+registers[i[3]][0])
        registers[i[1]][1]=(bin(int(registers[i[2]][1], 2) | int(registers[i[3]][1], 2))[2:].zfill(16))
        j=decimal_to_binary_7(memory_address_pointer)
        memory_address[j].append(opcode[i[0]]+"_00"+"_"+registers[i[1]][0]+"_"+registers[i[2]][0]+"_"+registers[i[3]][0])
        k+=1
        
    elif i[0]=="and":
        machine_code.append(opcode[i[0]]+"_00"+"_"+registers[i[1]][0]+"_"+registers[i[2]][0]+"_"+registers[i[3]][0])
        registers[i[1]][1]=bin(int(registers[i[2]][1], 2)  &   int(registers[i[3]][1], 2)  )[2:].zfill(16) 
        j=decimal_to_binary_7(memory_address_pointer)
        memory_address[j].append(opcode[i[0]]+"_00"+"_"+registers[i[1]][0]+"_"+registers[i[2]][0]+"_"+registers[i[3]][0])
        k+=1
        
        
    
 #### type B  & type C
    elif i[0]=="mov":
        if i[2] not in ["reg0", "reg1", "reg2", "reg3", "reg4", "reg5", "reg6"]: #type B
            machine_code.append("00010"+"_0"+"_"+registers[i[1]][0]+"_"+decimal_to_binary_7((i[2][1:])))
            registers[i[1]][1]="000000000_"+decimal_to_binary_7(i[2][1:])
            j=decimal_to_binary_7(memory_address_pointer)
            memory_address[j].append(opcode[i[0]]+"_0"+"_"+registers[i[1]][0]+"_"+decimal_to_binary_7((i[2][1:])))
        else:
            machine_code.append("00011"+"_00000"+"_"+registers[i[1]][0]+"_"+registers[i[2][0]]) # type C
            registers[i[1]][1]=registers[i[2][1]][:-1]+"1"
            registers[i[2][1]]="0000000000000000"
            j=decimal_to_binary_7(memory_address_pointer)
            memory_address[j].append(opcode[i[0]]+"_00000"+"_"+registers[i[1]][0]+"_"+registers[i[2][0]])
        k+=1
            
            
    ########## type B    
    elif i[0]=="rs":
        machine_code.append(opcode[i[0]]+"_0"+"_"+registers[i[1]][0]+"_"+decimal_to_binary_7((i[2][1:])))
        shifted=((int(registers[i[1]][1],2))>>(int(i[2][1:]))) & 0xFFFF
        registers[i[1]][1]=(bin(shifted)[2:].zfill(16))
        j=decimal_to_binary_7(memory_address_pointer)
        memory_address[j].append(opcode[i[0]]+"_0"+"_"+registers[i[1]][0]+"_"+decimal_to_binary_7((i[2][1:])))
        k+=1
        
    elif i[0]=="ls":
        machine_code.append(opcode[i[0]]+"_0"+"_"+registers[i[1]][0]+"_"+decimal_to_binary_7((i[2][1:])))
        shifted=((int(registers[i[1]][1],2))<<(int(i[2][1:]))) & 0xFFFF
        registers[i[1]][1]=(bin(shifted)[2:].zfill(16))
        j=decimal_to_binary_7(memory_address_pointer)
        memory_address[j].append(opcode[i[0]]+"_0"+"_"+registers[i[1]][0]+"_"+decimal_to_binary_7((i[2][1:])))
        k+=1

############# type C            
    elif i[0]=="div":
        machine_code.append(opcode[i[0]]+"_00000"+"_"+registers[i[1]][0]+"_"+registers[i[2]][0])
        if binary_to_decimal(binary_to_decimal(registers[i[2]][1]))==0:
            registers["FLAGS"][1]=registers["FLAGS"][1]
            registers["reg0"]="0000000000000000"
            registers["reg1"]="0000000000000000"
        else:
            registers["reg0"]=decimal_to_binary_16(    binary_to_decimal(registers[i[2]][1])  //   binary_to_decimal(registers[i[3]][1])   )
            registers["reg1"]=decimal_to_binary_16(    binary_to_decimal(registers[i[2]][1])  %   binary_to_decimal(registers[i[3]][1])   )
        j=decimal_to_binary_7(memory_address_pointer)
        memory_address[j].append(opcode[i[0]]+"_00000"+"_"+registers[i[1]][0]+"_"+registers[i[2]][0])
        k+=1
    
    elif i[0]=="not":
        machine_code.append(opcode[i[0]]+"_00000"+"_"+registers[i[1]][0]+"_"+registers[i[2]][0])
        registers[i[1]][1]=bin(~(binary_to_decimal(registers[i[2]][1])))[3:].zfill(16)
        j=decimal_to_binary_7(memory_address_pointer)
        memory_address[j].append(opcode[i[0]]+"_00000"+"_"+registers[i[1]][0]+"_"+registers[i[2]][0])
        k+=1
    
    elif i[0]=="cmp":
        machine_code.append(opcode[i[0]]+"_00000"+"_"+registers[i[1]][0]+"_"+registers[i[2]][0])
        if binary_to_decimal(registers[i[1]][1])>binary_to_decimal(registers[i[2]][1]):
            registers["FLAGS"][1]="0000000000000010"
        elif binary_to_decimal(registers[i[1]][1])<binary_to_decimal(registers[i[2]][1]):
            registers["FLAGS"][1]="0000000000000100"
        elif binary_to_decimal(registers[i[1]][1])==binary_to_decimal(registers[i[2]][1]):
            registers[i[1]][1]="0000000000000001"
        j=decimal_to_binary_7(memory_address_pointer)
        memory_address[j].append(opcode[i[0]]+"_00000"+"_"+registers[i[1]][0]+"_"+registers[i[2]][0])
        k+=1
        
        
###### type D
    elif i[0]=="ld":
        machine_code.append(opcode[i[0]]+"_0"+"_"+registers[i[1]][0]+"_"+memory_address[i[2]][0])
        registers[i[1]][0]=memory_address[i[2]][2]
        j=decimal_to_binary_7(memory_address_pointer)
        memory_address[j].append(opcode[i[0]]+"_0"+"_"+registers[i[1]][0]+"_"+memory_address[i[2]][0])
        k+=1
    
    elif i[0]=="st":
        machine_code.append(opcode[i[0]]+"_0"+"_"+registers[i[1]][0]+"_"+memory_address[i[2]][0])
        memory_address[i[2]][2]=registers[i[1]][0]
        j=decimal_to_binary_7(memory_address_pointer)
        memory_address[j].append(opcode[i[0]]+"_0"+"_"+registers[i[1]][0]+"_"+memory_address[i[2]][0])
        k+=1
        
        
#### handling labels
    elif is_label(i[0]):
        temp=i[0][:-1]
        j=decimal_to_binary_7(memory_address_pointer)
        memory_address[temp]=[j,temp]
        memory_address_pointer=memory_address_pointer-1
        k+=1
    
    
    ####### type E
    elif i[0]=="jmp":
        machine_code.append(opcode[i[0]]+"_0000"+"_"+memory_address[i[1]][0])
        j=decimal_to_binary_7(memory_address_pointer)
        memory_address[j].append(opcode[i[0]]+"_0000"+"_"+memory_address[i[1]][0])
        k=assembly_code.index([i[1]+":"])
        k+=1
     
    elif i[0]=="jlt":
        machine_code.append(opcode[i[0]]+"_0000"+"_"+memory_address[i[1]][0])
        j=decimal_to_binary_7(memory_address_pointer)
        memory_address[j].append(opcode[i[0]]+"_0000"+"_"+memory_address[i[1]][0])
        if registers["FLAGS"][1][-3]=="1":
            k=assembly_code.index([i[1]+":"])
            k+=1
        else:
            k+=1
    
    elif i[0]=="jgt":
        machine_code.append(opcode[i[0]]+"_0000"+"_"+memory_address[i[1]][0])
        j=decimal_to_binary_7(memory_address_pointer)
        memory_address[j].append(opcode[i[0]]+"_0000"+"_"+memory_address[i[1]][0])
        if registers["FLAGS"][1][-2]=="1":
            k=assembly_code.index([i[1]+":"])
            k+=1
        else:
            k+=1
   
    elif i[0]=="je":
        machine_code.append(opcode[i[0]]+"_0000"+"_"+memory_address[i[1]][0])
        j=decimal_to_binary_7(memory_address_pointer)
        memory_address[j].append(opcode[i[0]]+"_0000"+"_"+memory_address[i[1]][0])
        if registers["FLAGS"][1][-1]=="1":
            k=assembly_code.index([i[1]+":"])
            k+=1
        else:
            k+=1
     
    ########## type F   
    elif i[0]=="hlt":
        machine_code.append(opcode[i[0]]+"_00000000000")
        j=decimal_to_binary_7(memory_address_pointer)
        memory_address[j].append(opcode[i[0]]+"_00000000000")
        break
    
    else:
        k+=1
    
    memory_address_pointer+=1  

    
        
for i in machine_code:
    print(i)
print(memory_address)
                                  
                                  
