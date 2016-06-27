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
from Tkinter import *
from ttk import Frame, Style
from os import chdir, path

import pandas as pd  # import pandas data structures (DataFrame) and read_excel

# Import module with class/functions
from pigeon import Pigeon

# Import tool tip function developed by Michael Lange at
# http://tkinter.unpythonic.net/wiki/ToolTip, Licensed under
# GNU General Public License, Ver 2
from ToolTip import ToolTip

# Import for directory dialog
import tkFileDialog, tkMessageBox, tkFont, glob, time

#=============================================================================#

root = Tk()  # create GUI root
root.wm_title("Data Processor") # create title label
root.geometry("840x520+300+300") # set the size of the window

# Initialize variables
toolTipDelay = 700 #ms
defaultThreshold = 50
outputFilename = ""
pigeonName = ""
allPigeons = {}
allData = {}
groupsForOutput = []
trialButtons = []
trialButtonTooltips = []
animalButtons = []

# locate the current directory and file location
dirname, mainFile = path.split(path.abspath("__file__"))

# Ask user to identify the data directory
"""while True:
    try:
        dataDirname = tkFileDialog.askdirectory(parent=root,
            initialdir="/",title="Please select the data directory.")
        if not dataDirname:
            raise ValueError("empty string")
        break
    except ValueError:
        tkMessageBox.showinfo("Invalid directory","Please select a valid directory...")
        """

dataDirname = "C:/Users/chris/Documents/Projects/DrKellyProject/Data/"

# cd to data directory
chdir(dataDirname)

# list all files of type .xls
allFiles = glob.glob("*Test.xls")
numFiles = len(allFiles)

# create excelwriter object for outputting all data to excel
#allWriter = pd.ExcelWriter(outputFilename)

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

def analyzePigeons(calcForThreshold, path):
    print "\nProcessing %1.0f data files with a threshold of %0.0f units, \
please wait..." % (numFiles, calcForThreshold)

    startTime = time.time() # start timer
    progressTime = startTime
    # define the output spreadsheet
    outputFilename = path.join(dirname,"output-threshold-%0.0f.xls" % calcForThreshold)

    allWriter = pd.ExcelWriter(outputFilename)
    currFile = 0
    progressTime = 0
    # loop through all of the pigeons loaded into the dictionary allPigeons
    for pigeonName, pigeon in allPigeons.iteritems():
        currFile += 1
        if ((time.time() - progressTime) > 5): # display progress
            progressTime = time.time() # update progress time

        # find the indices of the goal locations in (x,y)
        pigeon.calcDist(calcForThreshold)

        # use the excel writer to save this pigeon to a data sheet in output.xls
        pigeon.dataframe.to_excel(allWriter,sheet_name = pigeonName)
        print "Progress: %0.0f/%0.0f..." % (currFile,numFiles)

        # also save each pigeon data to a dictionary for GUI processing
        allData[pigeonName]=pigeon.dataframe

    # also calculate how long formatting takes
    processingTime = time.time() - startTime

    return (outputFilename, processingTime)

def printInfo(processingTime,outputFilename):
    print "Processing the selected data files took %1.2f seconds." % processingTime
    print "\nFormatted output of all selected data files located in " + outputFilename + '.'

#=============================================================================#
#==========main function for handling processing and GUI functions============#
#=============================================================================#
class App(Frame):

    # Constructor
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.pack(fill=BOTH, expand=True)
        # run the initial formatting on the data folder
        (outputFilename,processingTime) = analyzePigeons(defaultThreshold, path)

        printInfo(processingTime,outputFilename)

        print "\nTips for using the GUI of this program can be found in the supplied \
README file. Tooltips are also available upon hovering over any \
element within the GUI."

        self.createComponents()

    # function for creating the select all and de-select button frames
    def createButtons(self, frame, vals, text):
        # create canvas for select all and deselect all buttons
        canv = Canvas(frame, width=220, height=10)
        canv.create_line(20,10,220,10, dash=(2,4))
        canv.pack(fill=X)

        # create each button separately
        selectAll = Button(frame, text="Select All",
                        command=lambda:
                        self.allButtons(vals,"Select"))
        selectAll.pack()
        selectTrialToolTip = ToolTip(selectAll, delay=toolTipDelay,
                    text="Select all " + text + " for analysis.")
        deselectAll = Button(frame, text="De-Select All",
                       command=lambda:
                       self.allButtons(vals,"De-Select"))
        deselectAll.pack()
        deselectTrialToolTip = ToolTip(deselectAll, delay=toolTipDelay,
                    text="Deselect all " + text + " marked for analysis.")

        return (selectAll, deselectAll)


    # Callback for select all and de-select all buttons
    def allButtons(self,buttonGroup, event):
        for buttonNum in range(len(buttonGroup)):
            if event == "Select":
                buttonGroup[buttonNum].set(1)
            else:
                buttonGroup[buttonNum].set(0)

    # Output the desired analyses
    def run(self):
        trialsForOutput = self.getGroups(self.trialVals, "trials")
        animalsForOutput = self.getGroups(self.animalVals, "animals")
        if ((trialsForOutput!=[]) and (animalsForOutput!=[])):
            outputFrames = self.analyzeGroups(trialsForOutput, animalsForOutput)

            # get the output name for saving the excel file
            todaysDate = time.strftime("%Y-%m-%d")
            initialFileName = todaysDate + '-' + '-'.join(trialsForOutput) + ".xls"
            chosenName = tkFileDialog.asksaveasfilename(initialdir=dirname,
                            initialfile=initialFileName)

            try:
                # create excelwriter object for outputting to excel
                writer = pd.ExcelWriter(chosenName)

                # create the excel writer object
                for frameIndex in outputFrames:
                    outputFrames[frameIndex].to_excel(writer,sheet_name = frameIndex)

                print "Saving output of chosen groups and pigeons to ", chosenName
                writer.save()
            except:
                tkMessageBox.showinfo("Saving cancelled", "Saving operation was cancelled")
        elif (trialsForOutput==[] and animalsForOutput==[]):
            tkMessageBox.showinfo("Nothing selected",
                            "Please select something to analyze")
        elif (trialsForOutput==[]):
            tkMessageBox.showinfo("No groups selected",
                            "Please select at least one grouping to analyze")
        elif (animalsForOutput==[]):
            tkMessageBox.showinfo("No birds selected",
                            "Please select at least one bird to analyze")

    def checkReformat(self, value, reset): # re-run if threshold has been changed
        if (value,reset)==(defaultThreshold,False):
            print "Threshold has not changed from default."
        elif (value,reset)==(defaultThreshold,True):
            (outputFilename, processingTime) = analyzePigeons(defaultThreshold,path)
            printInfo(processingTime, outputFilename)
        else:
            (outputFilename, processingTime) = analyzePigeons(value,path)
            printInfo(processingTime, outputFilename)

    def resetFormat(self, thresholdBox): # reset back to default
        thresholdBox.delete(0,END)
        thresholdBox.insert(0,defaultThreshold)
        self.checkReformat(defaultThreshold, reset=True)


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
        title_labelTooltip = ToolTip(title_label, delay=toolTipDelay+500,
                    text="This program was created by Chris Cadonic for use \
                    by the laboratory of Dr. Debbie Kelly.")

        # Create a canvas for drawing a separation line
        canv = Canvas(titleFrame, width=840, height=10)
        canv.create_line(0, 10, 840, 10)
        canv.pack(fill=X, anchor=CENTER, expand=True)


        # Create a frame for the bottom section
        #======================================================================
        footerFrame = Frame(self)
        footerFrame.pack(anchor=S, expand=True, side=BOTTOM)

        # Create a run button
        runButton = Button(footerFrame, width=200,text="Run Processing", command=self.run)
        runButton.pack(fill=Y)
        runToolTip = ToolTip(runButton,delay=toolTipDelay,
                    text = "Run analysis based on the groups and animals\
                    selected above.")


        # Create and populate group and trial button frames
        #======================================================================
        trialFrame = Frame(self)
        trialFrame.pack(expand=True, anchor=W, side=LEFT)

        # Create a checkbox for each test group
        self.trialLabels = ["Non-reinforced training","Control 1", "Control 2",
                        "Feature Only","Geometry Only","Affine"]
        self.trialKeys = ["Nrtr","C1","C2","FO","GO","AF"]
        self.trialTooltips = ["Non-reinforced training group.", "Control group 1",
                        "Control group 2", "Group where an extra wall and a \
feature wall are placed in the environment to create an enclosed square.",
"Group where the feature wall is removed, but the geometry of the environment \
remains the same.", "Group where the feature wall is moved to the end of the \
long wall."]
        self.trialVals = []

        # create all of the group buttons
        for num in range(len(self.trialLabels)):
            self.trialVals.append(IntVar())
            trialButtons.append(Checkbutton(trialFrame, text=self.trialLabels[num],
                        variable=self.trialVals[num], font=self.componentFont))
            trialButtons[-1].pack(pady=8)
            trialButtonTooltips.append(ToolTip(trialButtons[-1],
                        delay=toolTipDelay, text=self.trialTooltips[num]))

        # create select/deselect all buttons
        self.createButtons(trialFrame,self.trialVals, "experimental phases")

        # Create a frame for handling all of the birds
        #======================================================================
        animalsFrame = Frame(self)
        animalsFrame.pack(expand=True, anchor=CENTER, side=RIGHT)
        self.animals = list(allData.keys())

        self.animalVals = []

        # Create a button for each bird in the data directory
        for bird in range(len(self.animals)):
            self.animalVals.append(IntVar())
            animalButtons.append(Checkbutton(animalsFrame, text=self.animals[bird],
                                   variable=self.animalVals[bird],
                                   font=self.componentFont))
            self.animalVals[-1].set(1)
            animalButtons[-1].pack(pady=8)
        # create select/deselect all buttons
        self.createButtons(animalsFrame,self.animalVals, "animals")

        # Create a frame for handling all of the additional buttons
        #======================================================================
        buttonsFrame = Frame(self)
        buttonsFrame.pack(fill=X, expand=True)

        # Threshold label
        thresholdLabel = Label(buttonsFrame, text="Change threshold: ")

        # Threshold entry box
        thresholdBox = Entry(buttonsFrame, width=10)
        thresholdBox.pack()
        thresholdBox.insert(0, defaultThreshold)
        thresholdBoxTooltip = ToolTip(thresholdBox, delay=toolTipDelay,
                    text="Change this value to set a new threshold value \
for calculating the max distance away from a goal to be kept for data analysis.")

        # Re-analyze with new thresholdBox
        reformatButton = Button(buttonsFrame, text="Apply new threshold",
                    command=lambda: self.checkReformat(float(thresholdBox.get()), False))
        reformatButton.pack()
        reformatTooltip = ToolTip(reformatButton, delay=toolTipDelay,
                    text="Click to apply any changes to threshold box above.")

        # Reset threshold to defaultThreshold
        resetButton = Button(buttonsFrame, text="Reset threshold and run",
                    command=lambda: self.resetFormat(thresholdBox))
        resetButton.pack()
        resetButtonTooltip = ToolTip(resetButton, delay=toolTipDelay,
                    text="Click to reset threshold to default value.")

        # Create a sort button
        self.sortOutput = IntVar()
        sortButton = Checkbutton(buttonsFrame, text="Sort",
                    variable=self.sortOutput,font=self.componentFont)
        sortButton.pack()
        sortTooltip = ToolTip(sortButton, delay=toolTipDelay,
                    text="Select to auto-sort the output excel spreadsheets by \
trial type.")

        # Create a quit button
        quitButton = Button(buttonsFrame, text="Quit", command=self.quit)
        quitButton.pack()
        quitToolTip = ToolTip(quitButton, delay=toolTipDelay,
                    text="Quit the program and close the GUI.")


    def create_window(self):
        self.counter += 1
        t = tk.Toplevel(self)
        t.wm_title("Window #%s" % self.counter)
        l = tk.Label(t, text="This is window #%s" % self.counter)
        l.pack(side="top", fill="both", expand=True, padx=100, pady=100)

    # function for determining which groups/animals will be analyzed
    def getGroups(self, buttons, groupType):
        groupsForOutput = []
        if (groupType=="animals"):
            keys = self.animals
        else:
            keys = self.trialKeys

        # check which buttons are selected
        for buttonNum in buttons:
            if buttonNum.get():
                indexOfButton = buttons.index(buttonNum)
                groupsForOutput.append(keys[indexOfButton])
        return groupsForOutput

    # sort by group and store in list of dataframes
    def sortByTrialType(self, trial, gotrialFrame, AFtrialFrame, trialFrame, outputFrames):
        if (trial=="GO"):
            outputFrames["GO-Opp Distance"] = gotrialFrame.sort_values(["Trial Type",
            "Pigeon Name"])
        elif (trial=="AF"):
            outputFrames["AF-Opp Distance"] = gotrialFrame.sort_values(["Trial Type",
            "Pigeon Name"])
            outputFrames["AF-AF Distance"] = AFtrialFrame.sort_values(["Trial Type",
            "Pigeon Name"])
        outputFrames[trial] = trialFrame.sort_values(["Trial Type","Pigeon Name"])

        return outputFrames


    # function for parsing dataframe based on groups
    def analyzeGroups(self, trials, animals):
        outputFrames = {}
        columns = ["Pigeon Name","Trial Type", "Average Dist"]
        goColumns = list(columns)
        goColumns[-1] = "Average Opp Dist"
        AFColumns = list(goColumns)
        AFColumns.extend(["Average AF Dist"])
        '''if X and Y coordinates option selected
            columns = columns.append(["X Dist", "Y Dist"])'''

        for trial in trials:
            trialFrame = pd.DataFrame({}) # storage frame for each trial
            gotrialFrame = pd.DataFrame({})
            AFtrialFrame = pd.DataFrame({})
            # loop over each pigeon and acquire data matching requested trials
            for pigeon in animals:
                tempFrame = pd.DataFrame({})
                pigeonFrame = allData[pigeon]

                if (trial=="GO"):
                    goFrame = self.getFrame(pigeonFrame,goColumns, trial)
                    gotrialFrame = gotrialFrame.append(goFrame)
                elif (trial=="AF"):
                    goFrame = self.getFrame(pigeonFrame,goColumns, trial)
                    gotrialFrame = gotrialFrame.append(goFrame)
                    AFFrame = self.getFrame(pigeonFrame,AFColumns, trial)
                    AFtrialFrame = AFtrialFrame.append(AFFrame)

                tempFrame = self.getFrame(pigeonFrame, columns, trial)
                trialFrame = trialFrame.append(tempFrame) # add this pigeon to trial frame

            if (self.sortOutput.get()): # sort if the sort checkbutton is selected
                outputFrames[trial] = self.sortByTrialType(trial, gotrialFrame,
                            AFtrialFrame, trialFrame, outputFrames)

        return outputFrames


    # function to also create a processed dataframe for each pigeon/trial
    def getFrame(self, pigeonFrame, columns, trial):
        tempFrame = pigeonFrame.loc[pigeonFrame["Experiment Phase"]==trial][columns]
        tempFrame = tempFrame.dropna()

        #tempFrame = tempFrame[~tempFrame[columns[-1]].isin(["No Pecks"])==True]
        return tempFrame

# run the GUI
app = App(root)

root.resizable(width=FALSE, height=FALSE)
root.mainloop()
