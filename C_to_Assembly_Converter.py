print("PLease enter name of your C file:")
c_file = input()
document = open(c_file, "r")
assembly_code = open("Assembly.txt", "w")
row_document = document.readlines()
function_names = []
assignments = []
registers = []
numbers = [0]
numbers[0] = 10

def functions_detector(row):
    """""
    It finds the functions in the given c-code. It writes the function name and necessary assembly code parts.
    """
    if row.find("int") != -1 and row.find("main") != -1:
        assembly_code.write("main:\n\tSUB.W   #6 R1")
    elif row.find("int") != -1 and row.find("main") == -1 and row.find("(") != -1:
        row = row.replace("int", "")
        row = row.replace(" ", "")
        new_list = list(row)
        index = new_list.index("(")
        del new_list[index:]
        function_name = ("".join(new_list))
        assembly_code.write(function_name)
        assembly_code.write(":\n\t")
        assembly_code.write("SUB.W   #4, R1\n\tMOV.W   R12, 2(R1)\n\tMOV.W   R13, @R1\n")
        function_names.append(function_name)

def assignments_detector(row):
    """""
     This Function find the assignments which are given in the C-code and it assigns a register to each variable. Also it
     writes the necessary assembly code parts  to creating file.Also it records the variable names and registers which
     are belong to these variables. .For example;\n
     Assignment = ['a','b','c','d'...] (Variables)\n
     Registers = ['&R1','2(R1)','(4R1)','6(R1)'...]  (Registers belongs to these registers)
     """
    row = row.replace("int", "").replace(" ", "").replace("\n", "").replace("\t", "").replace(";", "")
    if row.find("=") != -1 and row.find("(") == -1 and row.find("+") == -1 and row.find("-") == -1 and row.find(
            "*") == -1 and row.find("&") == -1 and row.find("^") == -1 and row.find("||") == -1:
        new_list = list(row)
        index = new_list.index("=")
        variable = ("".join(new_list[0:index]))
        value = ("".join(new_list[index + 1:]))
        if variable in assignments:
            c = assignments.index(variable)
        else:
            assignments.append(variable)
            c = assignments.index(variable)
            if c == 0:
                a = "@R1"
            else:
                a = str(2 * c) + "(R1)"
            registers.append(a)
        assembly_code.write("\n\tMOV.W   #")
        assembly_code.write(value)
        assembly_code.write(", ")
        assembly_code.write(registers[c])

def function_calling_detector(row):
    """""
    This function determines the function calls at the main. Also it determines the which variables are sending and
    their registers. This works only when two variables are sending to function. Also it writes the necessary assembly code
    parts to creating file.
    """
    row = row.replace(" ", "")
    row = row.replace("\n", "")
    if row.find("(") != -1 and row.find(")") != -1 and row.find("for") == -1 and row.find("else") == -1 and row.find(
            "if") == -1 and row.find("main") == -1 and row.find("int") == -1:
        row = row.replace(")", "").replace(";", "")
        new_list = list(row)
        index = new_list.index("(")
        index1 = new_list.index(",")
        function_name = ("".join(new_list[0:index]))
        variable1 = ("".join(new_list[index + 1:index1]))
        variable2 = ("".join(new_list[index1 + 1:]))
        index2 = assignments.index(variable1)
        index3 = assignments.index(variable2)
        assembly_code.write("\n\tMOV.W   ")
        assembly_code.write(registers[index2])
        assembly_code.write(", R13\n\t")
        assembly_code.write("MOV.W   ")
        assembly_code.write(registers[index3])
        assembly_code.write(", R12\n\tCALL #")
        assembly_code.write(function_name)

def summation_detector(row):
    """
    This function detects the summation operations. It finds the all variables in the summation operation
    and it finds the result of summation for two constant variable. It writes the necessary assembly code
    parts to creating file. Also it determines the kind of variables like constant or assigned. For example;\n
    a = b+c (summation of two assigned variable)\n
    a = 2+b (summation of assigned and constant variable)\n
    a = 2+3 (summation of two constant variables)
    """
    row = row.replace("int", "").replace(" ", "").replace("\n", "").replace("\t", "").replace(";", "")
    if row.find("+") != -1 and row.find("return") != -1 and row.find("(") == -1:
        assembly_code.write("\tMOV.W   2(R1), R12\n\tADD.W   @R1, R12\n\tADD.W   #4, R1\n\tRET\n")
    elif row.find("+") != -1 and row.find("=") != -1 and row.find("return") == -1 and row.find(
            "(") == -1:  # We eliminate the if,else,else if,fo
        new_list = list(row)
        index = new_list.index("=")
        index2 = new_list.index("+")
        variable = ("".join(new_list[0:index]))
        variable1 = ("".join(new_list[index + 1:index2]))  # First value of the summuation
        variable2 = ("".join(new_list[index2 + 1:]))  # second value of the summuation
        if variable1 in assignments:
            c = assignments.index(variable1)
            if variable2 in assignments:
                k = assignments.index(variable2)
                assembly_code.write("\n\tMOV.W   ")
                assembly_code.write(registers[c])
                assembly_code.write(", (R12)")
                assembly_code.write("\n\tADD.W   ")
                assembly_code.write(registers[k])
                assembly_code.write(", (R12)")
                assembly_code.write("\n\tMOV.W   (R12),")
                assembly_code.write(registers[assignments.index(variable)])
            else:
                assembly_code.write("\n\tMOV.W   ")
                assembly_code.write(registers[c])
                assembly_code.write(", (R12)")
                assembly_code.write("\n\tADD.W   #")
                assembly_code.write(variable2)
                assembly_code.write(", (R12)")
                assembly_code.write("\n\tMOV.W   (R12),")
                assembly_code.write(registers[assignments.index(variable)])
        else:
            if variable2 in assignments:
                k = assignments.index(variable2)
                assembly_code.write("\n\tMOV.W   #")
                assembly_code.write(variable1)
                assembly_code.write(", (R12)")
                assembly_code.write("\n\tADD.W   #")
                assembly_code.write(registers[k])
                assembly_code.write(", (R12)")
                assembly_code.write("\n\tMOV.W   (R12),")
                assembly_code.write(registers[assignments.index(variable)])
            else:
                assembly_code.write("\n\tMOV.W   #")
                sum = int(variable1) + int(variable2)
                assembly_code.write("\n\tMOV.W   #")
                assembly_code.write(str(sum))
                assembly_code.write(", ")
                assembly_code.write(registers[assignments.index(variable)])

def subtraction_detector(row):
    """
   This function detects the subtraction operations. It finds the all variables in the subtraction operation
   and it finds the result of subtraction for two constant variable. It writes the necessary assembly code parts
   to creating file. Also it determines the kind of variables like constant or assigned. For example;\n
    a = b-c (subtraction of two assigned variable)\n
    a = b-2 (subtraction of assigned and constant variables)\n
    a = 3-2 (subtraction of two constant variables)
    """
    row = row.replace("int", "").replace(" ", "").replace("\n", "").replace("\t", "").replace(";", "")
    if row.find("-") != -1 and row.find("return") != -1 and row.find("(") == -1:
        assembly_code.write("\tMOV.W   2(R1), R12\n\tADD.W   @R1, R12\n\tADD.W   #4, R1\n\tRET\n")
    elif row.find("-") != -1 and row.find("=") != -1 and row.find("return") == -1 and row.find(
            "(") == -1:  # We eliminate the if,else,else if,fo
        new_list = list(row)
        index = new_list.index("=")
        index2 = new_list.index("-")
        variable = ("".join(new_list[0:index]))
        variable1 = ("".join(new_list[index + 1:index2]))  # First value of the summuation
        variable2 = ("".join(new_list[index2 + 1:]))  # second value of the summuation
        if variable1 in assignments:
            c = assignments.index(variable1)
            if variable2 in assignments:
                k = assignments.index(variable2)
                assembly_code.write("\n\tMOV.W   ")
                assembly_code.write(registers[c])
                assembly_code.write(", (R12)")
                assembly_code.write("\n\tSUB.W   ")
                assembly_code.write(registers[k])
                assembly_code.write(", (R12)")
                assembly_code.write("\n\tMOV.W   (R12),")
                assembly_code.write(registers[assignments.index(variable)])
            else:
                assembly_code.write("\n\tMOV.W   ")
                assembly_code.write(registers[c])
                assembly_code.write(", (R12)")
                assembly_code.write("\n\tADD.W   #-")
                assembly_code.write(variable2)
                assembly_code.write(", (R12)")
                assembly_code.write("\n\tMOV.W   (R12),")
                assembly_code.write(registers[assignments.index(variable)])
        else:
            if variable2 in assignments:
                k = assignments.index(variable2)
                assembly_code.write("\n\tMOV.B   #")
                assembly_code.write(variable1)
                assembly_code.write(", (R12)")
                assembly_code.write("\n\tSUB.W   #")
                assembly_code.write(registers[k])
                assembly_code.write(", (R12)")
                assembly_code.write("\n\tMOV.W   (R12),")
                assembly_code.write(registers[assignments.index(variable)])
            else:
                assembly_code.write("\n\tMOV.W   #")
                sum = int(variable1) - int(variable2)
                assembly_code.write("\n\tMOV.W   #")
                assembly_code.write(str(sum))
                assembly_code.write(", ")
                assembly_code.write(registers[assignments.index(variable)])

def multiplication_detector(row):
    """""
    This function detects the multiplication operations. It finds the all variables at the multiplication operation
    and it calculates the result of multiplication for two constant variables. It writes the necessary assembly code part
    to creating file. It does it for two constant term. For example;\n
    a = 2*3
    """
    row = row.replace("int", "").replace(" ", "").replace("\n", "").replace("\t", "").replace(";", "")
    if row.find("*") != -1 and row.find("return") != -1:
        assembly_code.write(
            "\tMOV.W   @R1, R13\n\tMOV.W   2(R1), R12\n\tCALL    #__mspabi_mpyi\n\tADD.W   #4, R1\n\tRET\n")
    elif row.find("*") != -1 and row.find("=") != -1 and row.find("return") == -1 and row.find(
            "(") == -1:  # We eliminate the if,else,else if,fo
        new_list = list(row)
        index = new_list.index("=")
        index2 = new_list.index("*")
        variable = ("".join(new_list[0:index]))
        value1 = ("".join(new_list[index + 1:index2]))  # First value of the summuation
        value2 = ("".join(new_list[index2 + 1:]))  # second value of the summuation
        sum = int(value1) * int(value2)
        if variable in assignments:
            c = assignments.index(variable)
        assembly_code.write("\n\tMOV.W   #")
        assembly_code.write(str(sum))
        assembly_code.write(", ")
        assembly_code.write(registers[c])

def and_detector(row):
    """""
    This function finds the and operation in the given c-code. It works only all operation elements are assigned values.
    For example;\n
    d = a && b (All variables a, b and d are assigned)\n
    It finds the registers of given variables from the recorded list. It writes the necessary assembly code to creating file.
    """
    if row.find("&&") != -1:
        temp_value = max(numbers)
        row = row.replace("int", "").replace(" ", "").replace("\n", "").replace("\t", "").replace(";", "").replace(
            "for", "").replace("if", "").replace("else if", "")
        new_list = list(row)
        index = new_list.index("=")
        index1 = new_list.index("&")
        variable = ("".join(new_list[0:index]))
        variable1 = ("".join(new_list[index + 1:index1]))
        variable2 = ("".join(new_list[index1 + 2:]))
        location = assignments.index(variable)
        location1 = assignments.index(variable1)
        location2 = assignments.index(variable2)
        assembly_code.write("\n\tCMP.W   #0,  " + registers[location1] + "  { JEQ        .L" + str(temp_value))
        assembly_code.write("\n\tCMP.W   #0,  " + registers[location2] + "  { JEQ       .L" + str(temp_value))
        assembly_code.write("\n\tMOV.B   #1, R12" + "\n\tBR   #.L" + str(temp_value + 1))
        assembly_code.write("\n.L" + str(temp_value) + ":\n\t")
        assembly_code.write("MOV.B   #0, R12")
        assembly_code.write("\n.L" + str(temp_value + 1) + ":")
        assembly_code.write("\n\tR12, " + registers[location])
        numbers.append(temp_value + 2)

def or_detector(row):
    """""
    This function finds the or operation in the given c-code. It works only all operation elements are assigned values.
    For example;\n
    d = a || b  (All variables a, b and d are assigned)\n
    It finds the registers of given variables from the recorded list. It writes the necessary assembly code to creating file.
    """
    if row.find("||") != -1:
        temp_value = max(numbers)
        row = row.replace("int", "").replace(" ", "").replace("\n", "").replace("\t", "").replace(";", "").replace(
            "for", "").replace("if", "").replace("else if", "")
        new_list = list(row)
        index = new_list.index("=")
        index1 = new_list.index("|")
        variable = ("".join(new_list[0:index]))
        variable1 = ("".join(new_list[index + 1:index1]))
        variable2 = ("".join(new_list[index1 + 2:]))
        location = assignments.index(variable)
        location1 = assignments.index(variable1)
        location2 = assignments.index(variable2)
        assembly_code.write("\n\tCMP.W   #0,  " + registers[location1] + "  { JEQ        .L" + str(temp_value))
        assembly_code.write(
            "\n\tCMP.W   #0,  " + registers[location2] + "  { JEQ       .L" + str(temp_value + 1) + "\n.L" + str(
                temp_value) + ":")
        assembly_code.write("\n\tMOV.B   #1, R12" + "\n\tBR   #.L" + str(temp_value + 2))
        assembly_code.write("\n.L" + str(temp_value + 1) + ":\n\t")
        assembly_code.write("MOV.B   #0, R12")
        assembly_code.write("\n.L" + str(temp_value + 2) + ":")
        assembly_code.write("\n\tMOV.W   R12, " + registers[location] + "\n\tMOV.B   #0, R12")
        numbers.append(temp_value + 2)

def xor_detector(row):
    """""
    This function finds the and operation in the given c-code. It works only all operation elements are assigned values. For example;\n
    d = a ^ b (All variables a, b and d are assigned)\n
    It finds the registers of given variables from the recorded list. It writes the necessary assembly code to creating file.
    """
    if row.find("^") != -1:
        temp_value = 12
        row = row.replace("int", "").replace(" ", "").replace("\n", "").replace("\t", "").replace(";", "").replace(
            "for", "").replace("if", "").replace("else if", "")
        new_list = list(row)
        index = new_list.index("=")
        index1 = new_list.index("^")
        variable = ("".join(new_list[0:index]))
        variable1 = ("".join(new_list[index + 1:index1]))
        variable2 = ("".join(new_list[index1 + 1:]))
        location = assignments.index(variable)
        location1 = assignments.index(variable1)
        location2 = assignments.index(variable2)
        assembly_code.write("\n\tMOV.W   " + registers[location1] + ", R12")
        assembly_code.write("\n\tMOV.W   " + registers[location2] + ", R12")
        assembly_code.write("\n\tMOV.W    R12," + registers[location])
        assembly_code.write("\n\tMOV.B    #0, R12")

def main():
    """""
    We control the code from here. We send the codes to functions line by line and functions make their jobs.
    """

    for row in row_document:
        functions_detector(row)
        assignments_detector(row)
        function_calling_detector(row)
        summation_detector(row)
        subtraction_detector(row)
        multiplication_detector(row)
        and_detector(row)
        or_detector(row)
        xor_detector(row)
main()
document.close()
assembly_code.write("\n\tADD.W    #8,  (R1)\n\tRET")
assembly_code.close()
