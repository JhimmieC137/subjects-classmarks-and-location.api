import csv


'''
1. Using CSV, get columns as list
2. Loop through class mark list and create new table with subject, classmark, location
'''

# open the file in read mode
locationsFile = open('locations.csv', 'r')
classMarkFile = open('class_marks.csv', 'r')
subjectReferenceFile = open('subjectRefLocation.csv', 'w')

subjectLocationList = []

# creating dictreader object
locations = csv.DictReader(locationsFile, fieldnames=('Locations', 'Classmarks'))
classMarks = csv.DictReader(classMarkFile)  


#Creating proper dictionaries for data from the csv files
subject_references = {}
classmark_locations = {}
for row in classMarks:
    subject_references[f"{row['Subjects'].strip()}"] = f"{row['References']}"
    
for value in locations:
    classmark_locations[f"{value['Locations']}"] = f"{value['Classmarks']}"



## Create a file that has subjects, reference and location
corresponding_location = []

#Uncomment the 11 lines below if you want to conduct a self test to see how the script works
'''classmark_locations = {}
classmark_references = []
for row in classMarks:
    classmark_references.append(row['References'].split(','))
for value in locations:
    classmark_locations[f"{value['Locations']}"] = f"{value['Classmarks']}"
for ref in classmark_references:
    for loc, clmrk in classmark_locations.items():
        [begin, end] = clmrk.split('-')
        if ref[0] >= begin and ref[0] <= end:
            corresponding_location.append(loc)'''
            
options = { 
        "A":"Subject name/part name",
        "B":"Classmark",
        "C":"Location"
          }
            
            
def self_test():              #To test how the script works without interaction
    for i in corresponding_location:
        print(i, "\n")


def search_library(param_1, param_2):      #Searches the csv files with the given parameters
    if options[param_1] == "Subject name/part name":    #Subject name/part name case search
        subject_name = param_2
        try:
            if subject_name in subject_references.keys():
                reference = (subject_references[f'{subject_name}'])
                for loc, clmrk in classmark_locations.items():
                    [begin, end] = clmrk.split('-')
                    if reference[0] >= begin and reference[0] <= end:
                        location = loc
                        result = f"Found {subject_name} with classmark '{reference}', on the{location}"             
                        break
                
            return f"{result}"                                                        #Returning results
        except: 
            return("\n\nOops... couldn't find that Subject name/Part-name in this Library.\n\nCheck that it's typed correctly")
    
    elif options[param_1] == "Classmark":               #Classmark case search
        classmark = param_2
        count = 0
        subjects = []
        try:
            for subject, reference in subject_references.items():
                reference = reference.split(',')
                for item in reference:
                    item = item.strip()
                    if classmark == item:
                        subject_name = subject
                        reference = item
                        count+=1
                        subjects.append(subject)
                        for loc, clmrk in classmark_locations.items():
                            [begin, end] = clmrk.split('-')
                            if reference >= begin and reference <= end:
                                if reference >= "JX" and reference <= "KZ":
                                    location = "Ground Floor"
                                else:
                                    location = loc
                                if count > 1:
                                    result = f"Found the Subjects {subjects} with Classmark '{reference}' on the {location}"
                                else:
                                    result = f"Found {subject_name} with Classmark '{reference}' on the {location}"   
                                       
            return f"{result}"                                                             #Returning results
        except:
            return ("\n\nOops... couldn't find that Classmark in this Library.\n\nCheck that it's typed correctly")
    
    else:                                               #Location case search
        location = param_2
        try:
            clsmrk_range = classmark_locations[f'{location}']
            [begin, end] = clsmrk_range.split('-')
            result = []
            for subject, reference in subject_references.items():
                reference = reference.split(',')
                for item in reference:
                    if item >= begin and item <= end:
                        result.append([f"Found {subject} with Classmark '{item}', on the {location}"])
            
            return f'{[x for x in result]}'                                                #Returning results 
        except:
            return ("\n\nOops... couldn't find that Location in this Library.\n\nCheck that it's typed correctly")
        

    
def home():                                             #The initiating function, it runs in a look till you dicide to quit
    exit = False
    while exit is not True: 
        print("Welcome, Select a search parameter")
        
        for a, b in options.items():
            print(f" Type {a} for {b}")
            
        print("  and hit Enter,\n Type 'Q' if you wish to quit ")
        
        first_choice = input("\n: ").upper()
        if first_choice == "Q":
            break
        
        print(f"\n**************************\nYou have selected to search by {options[first_choice]}")
        
        if first_choice == "C":
            print("\nAvailable locations for search include: \nTop Floor Back Left, \nTop Floor Front Left, \nTop Floor Back Right, \nTop Floor Front Right, \nMiddle Floor, \nGround Floor\n")
        
            print(f"\nPlease enter the {options[first_choice]} you want to find in the same way as seen above, \nType 'Q' if you wish to quit\n " )
        else:
            print(f"\nPlease enter the {options[first_choice]} you want to find, Note: {options[first_choice]} is case sensitive \nType 'Q' if you wish to quit\n " )
        
        second_choice = input(": ")
        if second_choice == "Q" or second_choice == "q" :
            break
        
        results = search_library(first_choice, second_choice)
        print(results)
        print("Hit 'C' to continue or 'Q' to quit and hit 'Enter'")
        third_choice = input("\n: ").upper()
        if third_choice == "Q":
            break
        print("\n \n")
    print("Bye")

    
    
    
## Write data back to file
with open('subjectRefLocation.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=('Subjects','References','Location'))
    
##    # Write the header
    writer.writeheader()
    
    for row in subjectLocationList:
        writer.writerow(row)
        
home()