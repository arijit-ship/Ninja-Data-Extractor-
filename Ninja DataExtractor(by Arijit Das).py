#Written by Arijit Das
#July, 2021


#Data extractor
#Take a string in the form of a list[(tuple)] as string
#Parse data from it
#Do math--avg
#Write a spreadsheet
#Export as xls
#I misspelled tuple in many places... "touple"  (lol)

import os
import time
from datetime import datetime
from datetime import date
import numpy as np
import xlsxwriter
from colorama import init 
from termcolor import colored 
from colorama import Fore, Back, Style 

init(convert=True)

path = os.path.normpath(os.path.expanduser("~/Desktop"))

def inputStringHandeler(input_string):
     return input_string[1:len(input_string)-1]

def countdown(t):
    
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print("Application is auto-closing in ", timer,"sec...", end="\r")
        time.sleep(1)
        t -= 1

#Welcome Screen

welcome = """
  _   _ _       _         _____        _          ______      _                  _                        
 | \ | (_)     (_)       |  __ \      | |        |  ____|    | |                | |                       
 |  \| |_ _ __  _  __ _  | |  | | __ _| |_ __ _  | |__  __  _| |_ _ __ __ _  ___| |_ ___  _ __            
 | . ` | | '_ \| |/ _` | | |  | |/ _` | __/ _` | |  __| \ \/ / __| '__/ _` |/ __| __/ _ \| '__|           
 | |\  | | | | | | (_| | | |__| | (_| | || (_| | | |____ >  <| |_| | | (_| | (__| || (_) | |              
 |_|_\_|_|_| |_| |\__,_| |_____/ \__,_|\__\__,_| |______/_/\_/\__|_|  \__,_|\___|\__\___/|_|              
  / _|        _/ | |  | |         | |      | | |  / ____(_)               | |     | | (_)                 
 | |_ ___  _ |__/| |__| | __ _ ___| | _____| | | | (___  _ _ __ ___  _   _| | __ _| |_ _  ___  _ __  ___  
 |  _/ _ \| '__| |  __  |/ _` / __| |/ / _ \ | |  \___ \| | '_ ` _ \| | | | |/ _` | __| |/ _ \| '_ \/ __| 
 | || (_) | |    | |  | | (_| \__ \   <  __/ | |  ____) | | | | | | | |_| | | (_| | |_| | (_) | | | \__ \ 
 |_| \___/|_|    |_|  |_|\__,_|___/_|\_\___|_|_| |_____/|_|_| |_| |_|\__,_|_|\__,_|\__|_|\___/|_| |_|___/ 
                                                                                                          
"""
print(Fore.BLUE + welcome)

info1 = """Use this data extractor to get the Bosons, Fermions experiments done!! Just follow the simple instructions and it will generate a spreadsheet containing energy values and number of particles, average particle-number (in .xlxs file) and a data file (.dat file, open with Notepad/Notepad++) to plot the graph."""

print("\n\n")
print("Created by Arijit Das, July, 2021. Version: 2.0, Feedback: dasarijit1st@gmail.com\n")
print(Style.RESET_ALL)
print("Repository: https://github.com/arijit-ship/Ninja-DataExtractor\n")
print(info1)
print("\n\n")
print("Hit 'Ctrl+C' to terminate the operation. ")
print("------------------------------------------------")
print("\n\n")

print("Enter (copy values to avoid any mistake) all the given energies in the form of a LIST: " + Fore.MAGENTA + "[E1, E2,E3...]   \n\n")
print(Style.RESET_ALL)
energyListStr = input()
print("--------------------------------------------------")
print("\n\nEnter all the data of particle-distribution sets in the form of ([triad, triad, triad...], temperature) where triad is a tuple of (energy, no. of particles, index).      \n")

energyList = eval (energyListStr)
noOfList = len(energyList) 
dataLst = []
dataString = ""
i= 0 
counter = 0

try:

    while True:
        print("\n\nEnter(copy whole tuple to avoid any mistake) distribution set " + str(i+1) + ":" + Fore.MAGENTA+"  ([triad, triad, triad...], temperature) \n" +  Fore.CYAN + "(Type 'done' when you're finished): \n")
        print(Style.RESET_ALL)
        disSet = input()
        
        if disSet.lower() == "done":
            break
        else:
            disSet = str(eval(disSet)[0])
            disSet = inputStringHandeler(disSet)
            dataString = dataString + disSet + ","
            counter += 1
            
        i = i+1
    print("\n\n")
    print("Parsing your input data...\n")
    
    dataTouple = eval(dataString[:len(dataString)-1])   

    #Storing total particle number for all  distribution
    particleNo = []
    for i in range (0, len(dataTouple)):
        particleNo.append(int(dataTouple[i][1]))


    #Time & Date for file name
    today = date.today()
    now = datetime.now().time() # time object

    print("Creating .xlsx file...\n")

    #Spreadsheet name and location managing
    xl_name = "Spreadsheet "+str(now).replace(":","-")[:8] + "--" + str(today) + ".xlsx"


    #Data plugging in spreadsheet

    workbook = xlsxwriter.Workbook(path+"\\"+xl_name)
    worksheet = workbook.add_worksheet()
    
    row = 0
    column = 0    
    for e in energyList :
        # write operation perform
        worksheet.write(row, column, e)
        # incrementing the value of row by one
        # with each iteratons.
        row += 1

    row = 0
    column = 1    
    for e in energyList :
        # write operation perform
        worksheet.write(row, column, "--->")
        # incrementing the value of row by one
        # with each iteratons.
        row += 1

    row = 0
    column = 2
    i = 0
    j = len(energyList)
    for n in particleNo:
            worksheet.write(row, column, n)
            row += 1
            if row > len(energyList)-1:
                column +=1 
                row = 0
            else:
                pass

    arr = np.mat(particleNo).reshape((len(energyList),counter), order = "f")
    avgParticleNo = []
    for i in range(0, len(energyList)):
        temp = float(np.sum(arr[i]))
        avgParticleNo.append(temp/counter)

    row = 0 #Don not set column = 0 again.
    for avg in  avgParticleNo:
        worksheet.write(row, column, "avg--->")    #alternatively column --> counter + 1 + 1  
        worksheet.write(row, column+1, avg)       # alternatively  column+1 -->counter + 1 + 1+ 1 
        row += 1
    workbook.close()

    print("Spreadsheet completed!\n")
    print("Creating .dat file...\n")

    ep = list(zip(energyList, avgParticleNo))
    # Specify the file name by time and date
    f_name = "Data Points "+str(now).replace(":","-")[:8] + "--" + str(today) + ".dat"


    with open(os.path.join(path, f_name), 'w') as fp:
        for i in ep:
            data = str(i)
            data = data.replace("(", "")
            data = data.replace(")", "")
            data = data.replace(",", "")
            fp.write(data)
            fp.write("\n")

    print("Datafile completed!\n\n")
    print("Your spreadsheet and datafile are saved to " + Fore.YELLOW + "Desktop.\n")
    print(Style.RESET_ALL)
    print(Fore.GREEN + "Note: You can modify/stylize the spreadsheet as needed. Use datafile(.dat open with Notepad/Notepad++) file to plot the graph.")
    print(Style.RESET_ALL)
    print("\nThanks for using this application.\n\n")
    countdown(59)
    time.sleep(1)
except Exception as e:
    print(e)
    print("-----------------------------\n\n")
    print(Fore.RED + "ERROR OCCURRED. You may want to restart the application (Hit 'Ctrl+C' to terminate and close the app)!")
    countdown(59)
    time.sleep(1)
        
