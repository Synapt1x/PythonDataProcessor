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
import sys
import numpy as np # required for pandas
import pandas as pd # import pandas data structures (dataFrame) and read_excel

# Initialize variables
xCoords = {}
yCoords = {}
peckNum = {}
trial = {}

# First read-in the data
file = open('data/test.xls')

# now read excel file data
pigeonData = pd.read_excel(file)

# parse the data and separate columns into series'

