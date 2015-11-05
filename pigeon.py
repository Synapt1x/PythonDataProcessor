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
        self.xCoords = self.allData['X']
        self.yCoords = self.allData['Y']
        self.allPecks = self.allData['Peck']
        self.allTrials = self.allData['Trial Information']

    def findGoals(self): # method for finding the indices corresponding to goals
        indices = np.where(self.allPecks=='goal')[0] # find indices where allPecks has the word goal

        # extract the x and y co-ordinates of each goal
        xGoals = self.xCoords[indices]
        yGoals = self.yCoords[indices]


        return (indices,xGoals,yGoals)