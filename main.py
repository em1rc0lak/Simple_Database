#310201091
import os 
            
def print_fetched(fetched_attribute,fetched_info):
    
    width = max(len(element) for info_list in fetched_info for element in info_list) 
    max_width = max(width, max(len(attribute) for attribute in fetched_attribute)) + 2

    print("-" * (max_width * len(fetched_info[0])+5))
    print("|", end = " ")
    for attribute in fetched_attribute:
        print(attribute.ljust(max_width) , end="| ")
    print()
    print("-" * (max_width * len(fetched_info[0])+5))
    for list in fetched_info:
        print("|", end = " ")
        for element in list:
            print(element.ljust(max_width) , end="| ")
        print()
    print("-" * (max_width * len(fetched_info[0])+5))


while True:

    querry = input("What is your querry?\n")
    if querry == "x":
        break
    
    querry_list = querry.split(" ")

    ### DISPLAY FILES ###
    # display files
    if querry == "display files":
        print("Number of files: ", len(os.listdir())-1)
        count = 1
        for file in os.listdir():
            with open(file, 'r') as f: attributes = f.readline()
            if file.endswith(".txt"):
                print(f"{count}) {file[:file.find(".")]}: {attributes[:-1]}")
                count += 1
        print()
        continue

    ### DELETE FILE ###
    # delete file FILE
    if querry.startswith("delete file") and len(querry_list) == 3:
        file = querry[12:] + ".txt"  
        if file in os.listdir():
            os.remove(file)
            print("Corresponding file was successfully deleted.\n")
        else:
            print("There is no such file.\n")
        continue
        
    ### CREATE FILE ###  
    # create file FILE with ATTRIBUTES 
    if querry.startswith("create file") and len(querry_list) == 5 and querry_list[3] == "with":
        file = querry_list[2] + ".txt"
        attributes = querry_list[-1]
        
        if "id" in attributes:
            print("You cannot create a file with attribute 'id'.\n")
            continue
        else:
            attributes = "id," + attributes + "\n"
        
        overwritten = file in os.listdir()
        
        with open(file, 'w') as f: f.write(attributes)
        
        if overwritten:
            print("There was already such a file. It is removed and then created again.\n")
        else:
            print("Corresponding file was successfully created.\n")

        continue

    ### ADD LINE ###
    # add ATTRIBUTE into FILE
    if querry.startswith("add") and len(querry_list) == 4 and querry_list[-2] == "into":
        file_name = querry_list[-1] + ".txt"
        
        if file_name not in os.listdir():
            print("There is no such file.\n")
            continue
        else:
            with open (file_name, 'r+') as f:
                id_list = []
                line_list = []

                for line in f:
                    if line_list == []: 
                        line_list = line.split(',')
                    if line.split(',')[0].isdigit():
                        id_list.append(line.split(',')[0])
                
                id = "1"
                while id in id_list:
                    id = str(int(id)+1)

                if len(querry_list[1].split(","))+1 == len(line_list):
                    f.write(id + ",")
                    f.write(querry_list[1] + "\n")
                    print("New line was successfully added to "+ querry_list[-1] + " with id = "+id+".\n")
                    continue
                else:
                    print("Number of attributes do not match.\n")
                    continue
    
    ### DELETE LINE ###
    # remove lines from FILE where ATTRIBUTE ==|!= VALUE
    if querry.startswith("remove lines from") and len(querry_list) == 8 and querry_list[-4] == "where" and(querry_list[-2] == "==" or querry_list[-2] == "!="):
        file_name = querry_list[-5] + ".txt"
        attribute = querry_list[-3]
        checked_value = querry_list[-1]
        operator = querry_list[-2]

        if file_name not in os.listdir():
            print("There is no such file.\n")
            continue            

        with open(file_name, 'r') as f: 
            lines = f.readlines()
            
            if attribute not in lines[0]:
                print("Your querry contains an unknown attribute.\n")
                continue

            attribute_list = lines[0].split(",")
            attribute_list[-1] = attribute_list[-1].strip("\n")
            
            checked_index = attribute_list.index(attribute)
            
            removed_lines = []
            
            count = 0
            for i in range(len(lines)):
                line_list = lines[i].split(",")
                line_list[-1] = line_list[-1].strip("\n")

                if operator == "==" and i != 0 and line_list[checked_index] == checked_value:
                    lines[i] = "x"
                    count += 1
                elif operator == "!=" and i != 0 and line_list[checked_index] != checked_value:
                    lines[i] = "x"
                    count += 1
            print(f"{count} lines were successfully removed.\n")
            with open(file_name, 'w') as f:
                for line in lines:
                    if line != "x":
                        f.write(line)
            continue
        
    ### MODIFY LINE ###
    # modify ATTRIBUTE in FILE as NEW_VALUE where ATTRIBUTE == VALUE
    if querry.startswith("modify") and len(querry_list) == 10 and querry_list[2] == "in" and querry_list[4] == "as" and querry_list[6] == "where" and (querry_list[-2] == "==" or querry_list[-2] == "!="):
        file_name = querry_list[3] + ".txt"
        modified_attribute = querry_list[1]
        new_value = querry_list[5]
        checked_attribute = querry_list[7]
        checked_value = querry_list[9]
        operator = querry_list[-2]

        if file_name not in os.listdir():
            print("There is no such file.\n")
            continue
        
        if modified_attribute == "id":
            print("Id values cannot be changed.\n")
            continue

        with open(file_name, 'r') as f:
            lines = f.readlines()
            attribute_list = lines[0].split(",")
            attribute_list[-1] = attribute_list[-1].strip("\n")
            

            if modified_attribute not in lines[0] or checked_attribute not in lines[0]:
                print("Your querry contains an unknown attribute.\n")
                continue

            checked_index = attribute_list.index(checked_attribute)
            modified_index = attribute_list.index(modified_attribute)

            count = 0
            for i in range(len(lines)):
                line_list = lines[i].split(",")
                line_list[-1] = line_list[-1].strip("\n")

                if operator == "==" and i != 0 and line_list[checked_index] == checked_value:
                    line_list[modified_index] = new_value
                    lines[i] = ",".join(line_list) + "\n"
                    count += 1
                elif operator == "!=" and i != 0 and line_list[checked_index] != checked_value:
                    line_list[modified_index] = new_value
                    lines[i] = ",".join(line_list) + "\n"
                    count += 1
            print(f"{count} lines were successfully modified.\n")
        
            with open(file_name, 'w') as f:
                for line in lines:
                    f.write(line)
        continue    

    ### FETCH LINES ###   
    # fetch ATTRIBUTES from FILE where ATTRIBUTE ==|!= VALUE
    if querry.startswith("fetch") and len(querry_list) == 8 and querry_list[2] == "from" and querry_list[4] == "where" and (querry_list[-2] == "==" or querry_list[-2] == "!="):
        fetched_attributes = querry_list[1].split(",")
        file_name = querry_list[3] + ".txt"
        checked_attribute = querry_list[5]
        checked_value = querry_list[-1]
        operator = querry_list[-2]

        if file_name not in os.listdir():
            print("There is no such file.\n")
            continue
        
        with open(file_name, 'r') as f:
            lines = f.readlines()

            attribute_list = lines[0].split(",")
            attribute_list[-1] = attribute_list[-1].strip("\n")
            
            if checked_attribute not in lines[0]:             
                print("Your querry contains an unknown attribute.\n")
                continue

            for attribute in fetched_attributes:
                if attribute not in lines[0]:
                    print("Your querry contains an unknown attribute.\n")
                    continue           

            fetched_indexes = []
            for attribute in fetched_attributes:
                attribute = attribute.strip("\n")
                fetched_indexes.append(attribute_list.index(attribute))

            checked_index = attribute_list.index(checked_attribute)

            info = []
            for i in range(len(lines)):
                line_list = lines[i].split(",")
                line_list[-1] = line_list[-1].strip("\n")

                fetched_line = []
                if operator == "==" and i != 0 and line_list[checked_index] == checked_value:
                    for j in fetched_indexes:
                        fetched_line.append(line_list[j])
                elif operator == "!=" and i != 0 and line_list[checked_index] != checked_value:
                    for j in fetched_indexes:
                        fetched_line.append(line_list[j])

                if fetched_line != []:
                    info.append(list(fetched_line))
            print_fetched(fetched_attributes,info)
        continue
      
    print("Invalid querry.\n")    
    



