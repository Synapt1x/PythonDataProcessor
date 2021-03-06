"""
Pigeon class
============================
Created by: Chris Cadonic
For: Dr. Debbie Kelly lab
----------------------------
This module holds the class definition, and function
definitions for use in the data processor in
Dr. Debbie Kelly"s lab.

IN:

OUT:

"""

# import necessary packages
import numpy as np
import pandas as pd
from math import sqrt

#=============================================================================#

# define the class for pigeon objects
class Pigeon:

    def processFrame(self, dataframe): # method for formatting the dataframe

        # convert x and y coordinates by calibration coefficients
        self.dataframe["X"] = self.dataframe["Calibration Coefficient"]*self.dataframe["X"]/10
        self.dataframe["Y"] = self.dataframe["Calibration Coefficient"]*self.dataframe["Y"]/10

        # separate Trial Information into separate columns
        colnames = ["Pigeon Name", "Experiment Phase", "Session", "Trial", "Trial Type"]  #name the columns
        tempDf=pd.DataFrame(dataframe["Trial Information"].str.split('_').tolist(),columns=colnames) # make a table with these columns to be added to self.dataframe

        # remove calibration coeffient and trial information columns
        self.dataframe = self.dataframe.drop(["Calibration Coefficient", "Trial Information"], axis=1)

        # add the columns extracted from trial information
        self.dataframe = self.dataframe.join(tempDf)

        return self.dataframe

    def findGoals(self, goalType):  # method for finding the indices
        # corresponding to goals
        # find indices where allPecks has the word goal
        goalIndices = np.where(self.dataframe["Peck"] == goalType)[0]

        # extract the x and y co-ordinates of each goal
        xGoals = self.dataframe["X"][goalIndices]
        yGoals = self.dataframe["Y"][goalIndices]

        return (xGoals, yGoals, goalIndices)

    def thresholdCalc(self, xDists, yDists, threshold): # method for thresholding distances
        totalDist = xDists*xDists + yDists*yDists
        sqrtDist = totalDist.apply(sqrt)

        # Set values above threshold as NaN, ignore those below
        finalDists = sqrtDist.apply(lambda x: np.nan if x > threshold else x)

        # Count number of NaNs representing number of outliers
        numsAboveThreshold = finalDists.isnull().sum()

        # Calculate the average distance after removing outliers
        avgDist = finalDists.mean()

        # Set all the finalDists to 0 instead of NaN
        finalDists = finalDists.fillna("Out")

        return (finalDists,numsAboveThreshold,avgDist)

    def calcDist(self, threshold):  # method for calculating euclidean distance from goals
        # call findGoals to determine the (x,y,indices) of the goals
        (self.goalsX, self.goalsY, self.goalIndices) = self.findGoals("goal")
        (self.OppsX, self.OppsY, self.OppsIndices) = self.findGoals("Opp goal")
        (self.AFsX, self.AFsY, self.AFIndices) = self.findGoals("AF goal")

        # create enumerator object to go over all goals and index them
        peckIterator = enumerate(self.goalIndices)

        # initialize placeholder series to dynamically append calc for each goal
        allDists = pd.Series([])
        allOppDists = pd.Series([])
        allAFDists = pd.Series([])
        removedPecks = pd.Series([])
        avgPeckDist = pd.Series([])
        oppPeckDist = pd.Series([])
        AFPeckDist = pd.Series([])

        # iterate over all goals with an index for loop number (i.e. trial num)
        for goalNum, peckIndex in peckIterator:
            # define first peck index for this particular goal
            firstPeck = peckIndex + 1
            # use try-except to define last index for goal, except catches the end of the series and sets the final lastPeck to the last poss. ind
            try:
                lastPeck = self.goalIndices[goalNum+1]
            except IndexError:
                lastPeck = len(self.dataframe)

            # Create range for the indices of pecks for this goal
            peckRange = range(firstPeck, lastPeck)

            # Check if Opp goal and/or AF goal are defined, if so then remove them from peckRange as they are currently included at the start
            if (peckIndex+1 in self.OppsIndices):
                del peckRange[0]
            if (peckIndex+2 in self.AFIndices):
                del peckRange[0]

            # Acquire all the peck locations for this trial
            xPecks = self.dataframe["X"][peckRange]
            yPecks = self.dataframe["Y"][peckRange]

            # Find each direct x and y distance from goal
            xDists = xPecks.apply(lambda x: x - self.goalsX[peckIndex])
            yDists = yPecks.apply(lambda y: y - self.goalsY[peckIndex])

            # Calculate the Euclidean distance for each peck from goal
            # Also filter out distances above distance threshold
            (finalDists,numRemoved,avgDist) = self.thresholdCalc(xDists,yDists, threshold)

            # store all distances in Series to be added to data frame
            allDists = pd.concat([allDists,finalDists], axis=0)

            # store the number of removed pecks and avg distances
            removedPecks[peckIndex] = numRemoved

            # repeat the above process now for opp and AF goals
            if (peckIndex+1 in self.OppsIndices):
                xOppDists = xPecks.apply(lambda x: x - self.OppsX[peckIndex+1])
                yOppDists = yPecks.apply(lambda y: y - self.OppsY[peckIndex+1])
                (finalOppDists,OppnumRemoved,OppavgDist) = self.thresholdCalc(xOppDists,yOppDists, threshold)
                allOppDists = pd.concat([allOppDists,finalOppDists], axis=0)
                removedPecks[peckIndex+1] = OppnumRemoved
                oppPeckDist[peckIndex+1] = "No Pecks" if (OppnumRemoved==10) else OppavgDist
            if (peckIndex+2 in self.AFIndices):
                xAFDists = xPecks.apply(lambda x: x - self.AFsX[peckIndex+2])
                yAFDists = yPecks.apply(lambda y: y - self.AFsY[peckIndex+2])
                (finalAFDists,AFnumRemoved,AFavgDist) = self.thresholdCalc(xAFDists,yAFDists, threshold)
                allAFDists = pd.concat([allAFDists,finalAFDists], axis=0)
                removedPecks[peckIndex+2] = AFnumRemoved
                AFPeckDist[peckIndex+2] = "No Pecks" if (AFnumRemoved==10) else AFavgDist

            # store average peck distances, unless all pecks were removed
            avgPeckDist[peckIndex] = "No Pecks" if (numRemoved==10) else avgDist

        # Add all peck distances to main data frame
        self.dataframe["Dist To Main Goal"] = allDists
        self.dataframe["Dist to Opp Goal"] = allOppDists
        self.dataframe["Dist to AF Goal"] = allAFDists

        # Set all NaN"s to "goal"
        self.dataframe = self.dataframe.fillna("goal")

        # Add num of removed pecks and average peck distances
        self.dataframe["Removed Pecks"] = removedPecks
        self.dataframe["Average Dist"] = avgPeckDist
        self.dataframe["Average Opp Dist"] = oppPeckDist
        self.dataframe["Average AF Dist"] = AFPeckDist

    def __init__(self, data):  # define the constructor for when pigeons are
        # made
        self.dataframe = data

        self.dataframe = self.processFrame(self.dataframe)
