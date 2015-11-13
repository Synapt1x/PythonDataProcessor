'''
Pigeon class
============================
Created by: Chris Cadonic
For: Dr. Debbie Kelly lab
----------------------------
This module holds the class definition, and function
definitions for use in the data processor in
Dr. Debbie Kelly's lab.

IN:

OUT:

'''

import numpy as np
import pandas as pd

# define the class for pigeon objects
class Pigeon:
    def __init__(self,data): # define the constructor for when pigeons are made
        self.allData = data
        self.allPecks = self.allData['Peck']
        self.allTrials = self.allData['Trial Information']
        self.allCalibs = self.allData['Calibration Coefficient']
        self.sessions = {}
        self.trials = {}

        # import x and y coordinates with conversion
        self.xCoords = self.allCalibs*self.allData['X']/10
        self.yCoords = self.allCalibs*self.allData['Y']/10

    def findGoals(self): # method for finding the indices corresponding to goals
        self.indices = np.where(self.allPecks=='goal')[0] # find indices where allPecks has the word goal

        # extract the x and y co-ordinates of each goal
        self.xGoals = self.xCoords[self.indices]
        self.yGoals = self.yCoords[self.indices]

        return (self.xGoals,self.yGoals)

    def parseTrialInfo(self): # method for parsing the trial information series
        eachTrial = self.allTrials[self.indices]

        return eachTrial