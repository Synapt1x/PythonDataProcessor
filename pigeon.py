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
# define the class for pigeon objects
class Pigeon:
    def __init__(self,data): # define the constructor
        self.allData = data
        self.xCoords = list(self.allData['X'])
        self.yCoords = list(self.allData['Y'])
        self.allPecks = list(self.allData['Peck'])
        self.allTrials = list(self.allData['Trial Information'])