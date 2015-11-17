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

    def processFrame(self,dataframe): # method for formatting the dataframe

        # convert x and y coordinates by calibration coefficients
        self.dataframe['X'] = self.dataframe['Calibration Coefficient']*self.dataframe['X']/10
        self.dataframe['Y'] = self.dataframe['Calibration Coefficient']*self.dataframe['Y']/10

        # separate Trial Information into separate columns
        colnames = ['Pigeon Name','Experiment Phase','Session','Trial','Trial Type'] #name the columns
        tempDf=pd.DataFrame(dataframe['Trial Information'].str.split('_').tolist(),columns=colnames)

        # remove calibration coeffient and trial information columns
        self.dataframe = self.dataframe.drop(['Calibration Coefficient','Trial Information'],axis=1)

        # add the columns extracted from trial information
        self.dataframe = self.dataframe.join(tempDf)

        return self.dataframe

    def __init__(self,data): # define the constructor for when pigeons are made
        self.dataframe = data

        self.dataframe = self.processFrame(self.dataframe)

        print self.dataframe

    def findGoals(self): # method for finding the indices corresponding to goals
        # find indices where allPecks has the word goal
        self.indices = np.where(self.dataframe['Peck']=='goal')[0]

        # extract the x and y co-ordinates of each goal
        self.xGoals = self.dataframe['X'][self.indices]
        self.yGoals = self.dataframe['Y'][self.indices]

        return (self.xGoals,self.yGoals)

    def parseTrialInfo(self): # method for parsing the trial information series
        # find each trial based on when a new goal is defined
        return 'parse'

    def calcDist(self): # method for calculating euclidean distance from goals
        return 'calc'

    def formatOuput(self): # method for summarizing and formatting output data
        return 'format'
