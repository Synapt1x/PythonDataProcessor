"""
Data Processor
============================
Created by: Chris Cadonic
For: Dr. Debbie Kelly lab
----------------------------
This program was developed to automatically
format input excel data for statistical
analysis in the statistical analysis
software.

IN:

OUT:

"""
#import Tkinter as tk# import tk for gui
from PIL import Image, ImageTk
from Tkinter import *
from ttk import Frame, Style

import glob
import time

from os import chdir, path

import pandas as pd  # import pandas data structures (DataFrame) and read_excel

# Import module with class/functions
from pigeon import Pigeon

# Import for directory dialog
import tkFileDialog
import tkFont

root = Tk()  # create GUI root
root.wm_title("Data Processor") # create title label
root.geometry("480x520+300+300") # set the size of the window

# Initialize variables
pigeonName = ""
allPigeons = {}
allData = {}
groupsForOutput = []

# locate the current directory and file location
dirname, mainFile = path.split(path.abspath("__file__"))

# define the output spreadsheet
outputFilename = path.join(dirname,"output.xls")

# Ask user to identify the data directory
"""while True:
    try:
        dataDirname = tkFileDialog.askdirectory(parent=root,
            initialdir="/",title="Please select the data directory.")
        if not dataDirname:
            raise ValueError("empty string")
        break
    except ValueError:
        print "Please select a valid directory..."
        """

dataDirname = "C:/Users/chris/Documents/Projects/DrKellyProject/Data/"

# cd to data directory
chdir(dataDirname)

# list all files of type .xls
allFiles = glob.glob("*Test.xls")

# create excelwriter object for outputting all data to excel
allWriter = pd.ExcelWriter(outputFilename)

# First read-in the data
for file in allFiles:
    datafile = pd.ExcelFile(file)
    index = allFiles.index(file)

    # now read excel file data into a DataFrame
    pigeonData = pd.read_excel(datafile)

    # extract pigeon name
    pigeonNametemp = pigeonData["Trial Information"][0].split('_')[0]  # take first
    # term from trial information in first entry

    # convert unicode to utf8
    pigeonName = pigeonNametemp.encode('utf8')

    # create pigeon
    allPigeons[pigeonName] = Pigeon(pigeonData)

# loop through all of the pigeons loaded into the dictionary allPigeons
for pigeonName, pigeon in allPigeons.iteritems():
    # find the indices of the goal locations in (x,y)
    pigeon.calcDist()

    # use the excel writer to save this pigeon to a data sheet in output.xls
    pigeon.dataframe.to_excel(allWriter,sheet_name = pigeonName)

    # also save each pigeon data to a dictionary for GUI processing
    allData[pigeonName]=pigeon.dataframe

class App(Frame):

    # Constructor
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.pack(fill=BOTH, expand=True)
        self.createComponents()

    # Callback for select all and de-select all buttons
    def allButtons(self,buttonGroup, event):
        for buttonNum in range(len(buttonGroup)):
            if event == "Select":
                buttonGroup[buttonNum].set(1)
            else:
                buttonGroup[buttonNum].set(0)

    # Output the desired analyses
    def run(self):
        groupsForOutput = self.getGroups(self.grpVals)
        outputFrame = self.analyzeGroups(groupsForOutput)

        # get the output name for saving the excel file
        todaysDate = time.strftime("%Y-%m-%d")
        initialFileName = todaysDate + "-Groups.xls"
        chosenName = tkFileDialog.asksaveasfilename(initialdir=dirname, initialfile=initialFileName)

        try:
            # create excelwriter object for outputting to excel
            writer = pd.ExcelWriter(chosenName)

            # create the excel writer object
            outputFrame.to_excel(writer,sheet_name = "Main Processing")

            print "Saving output of chosen groups and pigeons to ", chosenName
            writer.save()
        except runtimeError:
            print "Saving was cancelled..."


    # Create all of the buttons and components of the GUI
    def createComponents(self):
        # Create text fonts for components
        self.titleFont = tkFont.Font(family="Arial",size=18)
        self.componentFont = tkFont.Font(family="Helvetica",size=16)

        # Create a frame for the title section
        #======================================================================
        titleFrame = Frame(self)
        titleFrame.pack(fill=X)

        # Create the title label
        title_label = Label(titleFrame, text="Data Processor For Pigeon Experiment",
                            font=self.titleFont)
        title_label.pack(fill=X, expand=True)

        # Create a canvas for drawing a separation line
        canv = Canvas(titleFrame, width=480, height=10)
        canv.create_line(0, 10, 480, 10)
        canv.pack(fill=X, anchor=CENTER, expand=True)


        # Create a frame for the bottom section
        #======================================================================
        footerFrame = Frame(self)
        footerFrame.pack(anchor=S, expand=True, side=BOTTOM)

        # Create a run button
        runButton = Button(footerFrame, width=200,text="Run Processing", command=self.run)
        runButton.pack(fill=Y)


        # Create a frame for the group buttons
        #======================================================================
        grpFrame = Frame(self)
        grpFrame.pack(expand=True, anchor=W, side=LEFT)
        # Create a checkbox for each test group
        self.grpLabels = ["Control Group","Non-reinforced","Binocular",
                       "Cap-Left","Cap-Right"]
        self.grpKeys = ["CTRL","NR","BIN","CL","CR"]
        self.grpVals = []
        grpButtons = []
        # Create all of the group buttons
        for grpName in range(len(self.grpLabels)):
            self.grpVals.append(IntVar())
            grpButtons.append(Checkbutton(grpFrame, text=self.grpLabels[grpName],
                                   variable=self.grpVals[grpName],
                                   font=self.componentFont))
            grpButtons[-1].pack(pady=8)
        grpCanv = Canvas(grpFrame, width=220, height=10)
        grpCanv.create_line(20,10,220,10, dash=(2,4))
        grpCanv.pack(fill=X)

        # Add some select / de-select all buttons
        selectAllGrps = Button(grpFrame, text="Select All",
                         command=lambda:
                         self.allButtons(self.grpVals,"Select")).pack()
        deselectAllGrps = Button(grpFrame, text="De-Select All",
                           command=lambda:
                           self.allButtons(self.grpVals,"De-Select")).pack()


        # Create a frame for handling all of the birds
        #======================================================================
        animalsFrame = Frame(self)
        animalsFrame.pack(expand=True, anchor=CENTER, side=LEFT)
        animals = ["Bird1","Bird2","Bird3",
                       "Bird4","Bird5", "Bird6","Bird7","Bird8"]
        animalVals = []
        animalButtons = []
        # Create a button for each bird in the data directory
        for bird in range(len(animals)):
            animalVals.append(IntVar())
            animalButtons.append(Checkbutton(animalsFrame, text=animals[bird],
                                   variable=animalVals[bird],
                                   font=self.componentFont))
            animalButtons[-1].pack(pady=8)
        animalsCanv = Canvas(animalsFrame, width=220, height=10)
        animalsCanv.create_line(20,10,220,10, dash=(2,4))
        animalsCanv.pack(fill=X)

        # Add some select / de-select all buttons
        selectAllAnimals = Button(animalsFrame, text="Select All",
                         command=lambda:
                         self.allButtons(animalVals,"Select")).pack()
        deselectAllAnimals = Button(animalsFrame, text="De-Select All",
                           command=lambda:
                           self.allButtons(animalVals,"De-Select")).pack()


        # Create a frame for handling all of the additional buttons
        #======================================================================
        buttonsFrame = Frame(self)
        buttonsFrame.pack(fill=X, expand=True)

        # Create a quit button
        quitButton = Button(buttonsFrame, text="Quit", command=self.quit)
        quitButton.pack()

    def create_window(self):
        self.counter += 1
        t = tk.Toplevel(self)
        t.wm_title("Window #%s" % self.counter)
        l = tk.Label(t, text="This is window #%s" % self.counter)
        l.pack(side="top", fill="both", expand=True, padx=100, pady=100)


    # function for determining which groups will be analyzed
    def getGroups(self, buttons):
        groupsForOutput = []

        # check which buttons are selected
        for buttonNum in buttons:
            if buttonNum.get():
                indexOfButton = buttons.index(buttonNum)
                groupsForOutput.append(self.grpKeys[indexOfButton])
        return groupsForOutput

    # function for parsing dataframe based on groups
    def analyzeGroups(self, groups):
        outputFrame = pd.DataFrame({})

        for pigeon in allData:
            for group in groups:
                pigeonFrame = allData[pigeon]
                tempFrame = pigeonFrame.loc[pigeonFrame["Trial Type"]==group][["Pigeon Name","Trial Type","Average Dist"]]

                # remove NaNs and "No Pecks"
                tempFrame = tempFrame.dropna()
                tempFrame[tempFrame["Average Dist"].str.contains("No Peck")==False]

                outputFrame = outputFrame.append(tempFrame)
        return outputFrame

# run the GUI
app = App(root)

root.resizable(width=FALSE, height=FALSE)
root.mainloop()
