from tkinter import *
from tkinter import ttk, messagebox
import csv

# from models import search

# open the file in read mode
locationsFile = open('locations.csv', 'r')
classMarkFile = open('class_marks.csv', 'r')


# creating dictreader object
locations = csv.DictReader(locationsFile, fieldnames=('Locations', 'Classmarks'))
classMarks = csv.DictReader(classMarkFile)

subject_references = {}
classmark_locations = {}
for row in classMarks:
    subject_references[f"{row['Subjects'].strip()}"] = f"{row['References']}"
    
for value in locations:
    classmark_locations[f"{value['Locations']}"] = f"{value['Classmarks']}"


root = Tk()
root.minsize(height= 100, width=500)    # This sets the frame of the dialouge box

def class_finder():
    def choice():
        info_label.destroy()          #Removes the previous paragraph text
        dropdown.destroy()              #Removes the dropdown
        search_param.destroy()              #removes the button
        
        def return_to_base():
            if clicked.get() == "Location":
                info_label_2.destroy()
                info_label_3.destroy()
                info_label_4.destroy()
            else: 
                new_info_label.destroy()        #Removing the new paragrapgh text
            parameter_value.destroy()    #Removing the input box
            search.destroy()                 #Removing the search button
            return_button.destroy()             #Removing the return button
            class_finder()                         #Initializing the Class finder model again
        
        def quick_check():
            if clicked.get() == "Subject name or Part-name":
                subject_name = parameter_value.get()
                try:
                    if subject_name in subject_references.keys():
                        reference = (subject_references[f'{subject_name}'])
                        for loc, clmrk in classmark_locations.items():
                            [begin, end] = clmrk.split('-')
                            if reference[0] >= begin and reference[0] <= end:
                                location = loc  
                                result = f"Found {subject_name} with the Classmark(s) '{reference}' on the {location}"             
                                break
                        
                    return messagebox.showinfo("Message", f"{result}")           #All logic falls under these conditions, return the.
                 
                except: 
                    return messagebox.showinfo("Error","\n\nOops... couldn't find that Subject name/Part-name in this Library.\n\nCheck that it's typed correctly")
                
                
            elif clicked.get() == "Classmark":
                classmark = parameter_value.get()
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
                                            result = f"Found the subjects {subjects} with the Classmark '{reference}', on the {location}"
                                        else:
                                            result = f"Found {subject_name} with the Classmark '{reference}', on the {location}"  
                                            
                    return messagebox.showinfo("Message", f"{result}")
                
                except:
                    return messagebox.showinfo("Error","\n\nOops... couldn't find that Classmark in this Library.\n\nCheck that it's typed correctly")
                
                
            else:
                location = parameter_value.get()
                try:
                    clsmrk_range = classmark_locations[f'{location}']
                    [begin, end] = clsmrk_range.split('-')
                    result = []
                    for subject, reference in subject_references.items():
                        reference = reference.split(',')
                        for item in reference:
                            if item >= begin and item <= end:
                                result.append([f"Found {subject} with the Classmark '{item}', on the {location}"])
                    
                    return messagebox.showinfo("Message", f'{[x for x in result]}')
                
                except:
                    return messagebox.showinfo("Error", "\n\nOops... couldn't find that Location in this Library.\n\nCheck that it's typed correctly")
            
        if clicked.get() == "Location":
            info_label_2 = Label(root, text="Available locations for search include:")
            info_label_2.pack()
            info_label_3 = Label(root, text="Top Floor Back Left, Top Floor Front Left, Top Floor Back Right, Top Floor Front Right, Middle Floor, Ground Floor")
            info_label_3.pack()
            info_label_4 = Label(root, text="Type in the Location")
            info_label_4.pack()
        
        else:
            new_info_label = Label(root, text= f"Type in the {clicked.get()}.")     #A new message
            new_info_label.pack()               #Displays a new message
        
        global parameter_value
        parameter_value = Entry(root, bd=5)   #Setting an input box
        parameter_value.pack()                  #Displays the input box
        
        
        search = Button(root, text="Search", command=quick_check)   #Setting the Search button linking it to the quick_search function
        search.pack()                                                  #Displaying the Search button

        return_button = Button(root, text="Return", command=return_to_base)
        return_button.pack()

    info_label = Label(root, text="Select your search parameter from the dropdown menu below and click enter")  #Sets a paragraph of text
    info_label.pack()                                                                                           #This dispalys the text containing instructions to the client
    
    selection = [                               #List of the dropdown options
        "Subject name or Part-name",
        "Classmark",
        "Location",
        ]

    clicked = StringVar()
    clicked.set(selection[0])                   #Sets the first value of the list as the default selection 

    dropdown = OptionMenu(root, clicked, *selection)     #Renders the dropdown
    dropdown.pack()                                      #Displays the dropdown   
    
    search_param = Button(root, text="Enter", command=choice)   #Setting the Enter button that links to the choice functions
    search_param.pack()                                         #Displays the Enter button

class_finder()  #Initiates the class finder model

root.mainloop()