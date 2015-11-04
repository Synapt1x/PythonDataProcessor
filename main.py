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
import pandas as pd  # import pandas data structures (DataFrame) and read_excel

# Initialize variables
xCoords, yCoords, peckNum, trial = {}, {}, {}, {}
pigeon, condition, session, trial, group = 0, '', '', 0, ''

# First read-in the data
file = open('data/test.xls')

# now read excel file data into a DataFrame
pigeonData = pd.read_excel(file)

# define the class for pigeon objects
class Pigeon:
    def __init__(self,data):
        self.allData = data

# separate columns into pandas series'
#xCoords = list(pigeonData['X'])
#yCoords = list(pigeonData['Y'])
#allPecks = list(pigeonData['Peck'])
#allTrials = list(pigeonData['TrialInfo'])

# loop over allTrials series to extract trial properties
#for trial in allTrials:
#    [pigeon, condition, session, trial, group] = trial.split("_")



# loop over peckNum series to extract indices where goal
#for peckNum in allPecks:
#    if peckNum == 'goal':
#        continue