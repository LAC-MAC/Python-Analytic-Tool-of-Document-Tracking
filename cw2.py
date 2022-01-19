#!/usr/bin/python
import argparse
import sys
import getopt
import tkinter
from functools import partial
from tkinter import *
from tkinter import simpledialog
from tkinter import filedialog
from tkinter import messagebox
import time
import pandas as pd
from data import Data
import matplotlib as mpl
import matplotlib.pyplot as plt
from processing import Processing
from task2 import Task2
from task3 import Task3
from task4 import Task4
from task5 import Task5


# Create new tkinter window 

# Function called when quit button is pressed
def quit():
    sys.exit()

# Funciton for loading in a json file, opens a file picker window which allows the user to select a file
# it then sets the global data variable as the new file

def load_json():
    filename = filedialog.askopenfilename()
    global data
    data = ""
    data = Data(filename)
    data = data.makeDataFrame()

# Function for task2a and task2b. Takes a in documentID as input and returns the graph for the countries and continents for the 
# specified documents
def task2_gui(task_id):
    # ask user for docid. Validate a id was entered
    doc_id = simpledialog.askstring("Input", "Please enter in a document id", parent=window)
    if doc_id is None:
        print("Please enter in a valid document id")
    else:
        # if task2a, call countries function and plot graph for the results 
        if task_id == "a":
            try:
                t2_gui = Task2(data)
                result = t2_gui.countriesForDoc(doc_id)
                t2_gui.plotOccur(result, "Countries", doc_id ,"./Task2a -")
            # catch any exceptions
            except Exception as e:
                print("ERROR - ", e)
        # if task2b, call continents function and plot graph for the results 
        else:
            try:
                t2_gui = Task2(data)
                result = t2_gui.continentsForDoc(doc_id)
                t2_gui.plotOccur(result, "Continents", doc_id, "./Task2b -")
            # catch any exceptions
            except Exception as e:
                print("ERROR - ", e)

# Function for task 3a and 3b. Returns all browser data for task3a and general browser data in 3b both in graph formats
def task3_gui(task_id):
    # ask user for docid. docid is optional. Validate a id was entered
    doc_id = simpledialog.askstring("Input", "(Optional) Please enter in a document id", parent=window)
    try:
        t3_gui = Task3(data)
        # call all browser data if task a selected
        if task_id == "a":
            # if optional docid is provided, retrieve browser data for specified document
            if doc_id is None:
                result = t3_gui.browserData()
            else:
                result = t3_gui.browserData(doc_id)
            # plot graph for all browser data
            result = t3_gui.plotOccur(result, "Browser", "All Browser Data", "./Task3a -")
        # retrieve general browser data if task3b is selected
        else:
            if doc_id is None:
                result = t3_gui.GeneralBrowserData()
            else:
                result = t3_gui.GeneralBrowserData(doc_id)
            # plot graph for all browser data
            result = t3_gui.plotOccur(result, "Browser", "General Browser Data", "./Task3b -")

    except Exception as e:
        print("ERROR -", e)

# Function for task 4. This produces a graph that lists the top 10 most avid readers.
def task4_gui():
    try:
        # Create an instance of task 4 and call the biggest readers function
        t4_gui = Task4(data)
        biggestReaders = t4_gui.biggestReaders()
        result = t4_gui.plotOccur(biggestReaders, "readers", "biggestReaders" , "./Task4 -", "ReadTime")
    except Exception as e:
        print("ERROR - ", e)

# Function for task 5 and 6. Asks for a docid and userid. Calls the also likes function. Returns a graph if taskid 6 is passed. Returns 
# a list of documents based on the number of readers of the same document 
def task5and6_gui(task_id):
    doc_id = simpledialog.askstring("Input", "Please enter in a document id", parent=window)
    user_id = simpledialog.askstring("Input", "(Optional) Please enter in a user id", parent=window)
    if doc_id is None:
        print("Please enter in a valid document id")
    else:
        try:
            t5_gui = Task5(data)
            if user_id is None:
                result = t5_gui.alsoLikes(task_id, doc_id, sorter=t5_gui.sorter) 
            else:
                result = t5_gui.alsoLikes(task_id, doc_id, user_id, sorter=t5_gui.sorter) 
            # display messagebox with output for task 5d
            if task_id == "5d":
                messagebox.showinfo("Task 5d", result)         
        except Exception as e:
            print("ERROR: ", e)

def gui():
    # Tkinter window with buttons for each task
    global window
    window = tkinter.Tk()
    window.title("Data Analysis of a Document Tracker")
    tkinter.Button(window, text="Choose a JSON File", fg="grey", width=25, height=5, command=load_json).pack()
    tkinter.Button(window, text="Task 2a", fg="red", width=25, height=5, command=partial(task2_gui, "a")).pack()
    tkinter.Button(window, text="Task 2b", fg="black", width=25, height=5, command=partial(task2_gui, "b")).pack()
    tkinter.Button(window, text="Task 3a", fg="navy", width=25, height=5, command=partial(task3_gui, "a")).pack()
    tkinter.Button(window, text="Task 3b", fg="blue", width=25, height=5,command=partial(task3_gui, "b")).pack()
    tkinter.Button(window, text="Task 4", fg="purple", width=25, height=5, command=task4_gui).pack()
    tkinter.Button(window, text="Task 5d", fg="brown", width=25, height=5,command=partial(task5and6_gui,"5d")).pack()
    tkinter.Button(window, text="Task 6", fg="green",  width=25, height=5, command=partial(task5and6_gui,"6")).pack()
    tkinter.Button(window, text="Exit", fg="red",  width=25, height=5, command=quit).pack()

    window.mainloop()

# Display the relevant output for task 2a and 2b in the command line 
def task2(doc_id, task_id):
    try:
        t2 = Task2(data)
        if task_id == "2a":                 
            result = t2.countriesForDoc(doc_id)
            t2.plotOccur(result, "Countries", doc_id ,"./Task2a -")
            print("A histogram has been produced at ./Task2a -", doc_id, ".png")
        else: 
            result = t2.continentsForDoc(doc_id)
            t2.plotOccur(result, "Continents", doc_id, "./Task2b -")
            print("A histogram has been produced at ./Task2a -", doc_id, ".png")
    except Exception as e:
        print("ERROR -" , e)


# Display the relevant output for task 3a and 3b in the command line 
def task3(task_id, doc_id=None):
    try:
        t3 = Task3(data)
        if task_id == "3a":     
            if doc_id != "":
                result = t3.browserData(doc_id)
                print("The browser data of all browser identifiers of a specific document is as follows:\n", result)
                result = t3.plotOccur(result, "Browser", "All Browser Data", "./Task3a -")
                print("A histogram has been produced at ./Task3a -All Browser Data.png")
            else:
                result = t3.browserData()
                print("The browser data of all browser identifiers of the viewers is as follows:\n", result)
                result = t3.plotOccur(result, "Browser", "All Browser Data", "./Task3a -")
                print("A histogram has been produced at ./Task3a -All Browser Data.png")
        else:
            if doc_id != "":
                result = t3.GeneralBrowserData(doc_id)
                print("The general browser data for the specified document is as follows:\n", result)
                result = t3.plotOccur(result, "Browser", "General Browser Data", "./Task3b -")
                print("A histogram has been produced at ./Task3b -General Browser Data.png")
            else:
                result = t3.GeneralBrowserData()
                print("The general browser data is as follows:\n", result)
                result = t3.plotOccur(result, "Browser", "General Browser Data", "./Task3b -")
                print("A histogram has been produced at ./Task3b -General Browser Data.png")
    except Exception as e:
        print("ERROR -", e)

# Display the relevant output for task 4 in the command line 
def task4():
    t4 = Task4(data)
    try:
        result = t4.biggestReaders()
        result = t4.plotOccur(result, "readers", "biggestReaders" , "./Task4 -")
        print("A graph was produced at ./Task4 -biggestReaders")
    except Exception as e:
        print("ERROR -", e)

# Display the relevant output for task 5d and 6 in the command line 
def task5and6(doc_id,user_id,task_id):
    
    try:
        
        if doc_id != "":
            t5 = Task5(data)
            if user_id !="":
                
                result = t5.alsoLikes(task_id, doc_id, visitorUUID=user_id, sorter=t5.sorter)
                
            else:
                result = t5.alsoLikes(task_id, doc_id, sorter=t5.sorter)
                
        else:
            print("ERROR - Error loading in docid or userid")
    except Exception as e:
        print("ERROR -" , e)

# main function that reads in inputs and calls functions
def main(argv):
    # Initialise variables
    user_id = ''
    doc_id = ''
    filename = ''
    task_id = 0

    try:
        # using getopt, read in userid, docid and taskid
        options, arguments = getopt.getopt(argv, "hu:d:t:f:", ["user_id=", "doc_id=", "task_id=", "filename="])
    except getopt.GetoptError as e:
        print(
            "The correct format to run the code is as follows: './cw2 -u <user_uuid> -d <doc_uuid> -t <task_id> -f <filename>'")
    # -h allows for help feature
    for opt, arg in options:
        if opt == '-h':
            print("The format to run the program is: './cw2 -u <user_uuid> -d <doc_uuid> -t <task_id> -f <filename>'\n")
            print("The following tasks are available to run:\n")
            print("--> Task 2a: Histogram of countries of viewers\n")
            print("--> Task 2b: Histogram of continents of viewers\n")
            print("--> Task 3a: Histogram of all browser identifiers of the viewers\n")
            print("--> Task 3b: Histogram of only main browsers\n")
            print("--> Task 4: Top 10 readers of a chosen document\n")
            print("--> Task 5d: List of top 10 document UUID\n")
            print("--> Task 6: Display a graph that displays the input document and all documents that have been found as “also like” documents\n")
            print("--> Task 7: Launch GUI to interact with the program\n")
            sys.exit()
        # assign variables to input values
        elif opt in ("-u", "--user_id"):
            user_id = arg
        elif opt in ("-d", "--doc_id"):
            doc_id = arg
        elif opt in ("-t", "--task_id"):
            task_id = arg
        elif opt in ("-f", "--filename"):
            filename = arg
     
    if filename != "":
        global data
        data = ""
        data = Data(filename)
        data = data.makeDataFrame()
        if data is None:
            print("ERROR - Couldn't Load File, Check Path")
            quit()
    else:
        if task_id == "7":
            data = Data("./sample_100k_lines.json")
            data = data.makeDataFrame()
        else:
            print("ERROR - Please enter in a valid JSON files")
            quit()

    if task_id == "2a" or task_id == "2b":
        # print task 2, Views by country/continent
        print("-> executing task", task_id, "...")
        task2(doc_id,task_id)
    elif task_id == "3a" or task_id == "3b":
        # print task 3, views by browser
        print("-> executing task", task_id, "...")
        task3(task_id, doc_id)
    elif task_id == "4":
        # print task 4, reader profiles, most avid readers
        print("-> executing task 4...")
        task4()
    elif task_id == "5d":
        # print task5d, produce an “also like” list of documents 
        print("-> executing task 5d...")
        task5and6(doc_id, user_id, task_id)
    elif task_id == "6":
        # Print task 6, this is the also likes graph
        print("-> executing task 6...")
        task5and6(doc_id,user_id, task_id)
    elif task_id == "7":
        # Launch the GUI
        print("-> executing task 7... Launching GUI")
        gui()

if __name__ == "__main__":
    #Initialise default data file to use the 100k lines .json file
    
    main(sys.argv[1:])
    
