'''
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

'''
# Import relevant packages
from os import chdir, path

import pandas as pd  # import pandas data structures (DataFrame) and read_excel
from Tkinter import * # import Tkinter for gui
import glob

# Import GUI developed for the program
from finalGUI import App

# Import module with class/functions
from pigeon import Pigeon

# create the gui and display it using the gui.py program
root = Tk()  # create GUI root
root.wm_title('Data Processor') # create title label
root.geometry('480x360+300+300') # set the size of the window

app = App(root) # place all components
root.mainloop()

# Initialize variables
pigeonName = ''
allPigeons = {}

# locate the current directory and file location
dirname, mainFile = path.split(path.abspath('__file__'))

# define the output spreadsheet
outputFilename = path.join(dirname,'output.xls')

# locate the data directory and store all files in a list
#Left out for convenience during testing
#dataDirname = app.dataDirname

dataDirname = '/home/synapt1x/Projects/DrKellyProject/data'

# cd to data directory
chdir(dataDirname)

# list all files of type .xls
allFiles = glob.glob('*Test.xls')

# create excelwriter object for outputting to excel
writer = pd.ExcelWriter(outputFilename)

# First read-in the data
for file in allFiles:
    datafile = open(file)
    index = allFiles.index(file)

    # now read excel file data into a DataFrame
    pigeonData = pd.read_excel(datafile)

    # extract pigeon name
    pigeonName = pigeonData['Trial Information'][0].split('_')[0]  # take first
    # term from trial information in first entry

    # create pigeon
    allPigeons[pigeonName] = Pigeon(pigeonData)

# loop through all of the pigeons loaded into the dictionary allPigeons
for pigeonName, pigeon in allPigeons.iteritems():
    # find the indices of the goal locations in (x,y)
    pigeon.calcDist()

    # separate data into session, trial and trial type
    trialInfo = pigeon.parseTrialInfo()

    # use the excel writer to save this pigeon to a data sheet in output.xlsx
    pigeon.dataframe.to_excel(writer,sheet_name = pigeonName)

    print 'Saving output of pigeon', pigeonName, 'to Output.xls...'
    writer.save()
