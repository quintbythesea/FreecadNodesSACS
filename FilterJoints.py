import os
import pandas as pd

filter = 'Y'

mydir = os.getcwd()+os.sep+'JOINTS'


filter=[]

for file in os.listdir(mydir):
    if file != 'Export':
        txtPath = mydir + os.sep + file
        with open(txtPath, "r") as file1:
            for line in file1:
                #print (line[:5])
                if line[:7]=='JOINT Y':
                    filter.append(line)
        #print (filter)
        print(file)
        name = file.split('_')[1]

        with open(mydir+os.sep+'Export'+os.sep+name+'.txt', 'w') as f:
            for line in filter:
                f.write(line)
        filter=[]




    #print (txtPath)
    #print (file)

#txtPath = os.getcwd()+os.sep+inputFile+'.txt'
#with open(txtPath, "r") as file1:
#    sectionList = [line.split('x') for line in file1]