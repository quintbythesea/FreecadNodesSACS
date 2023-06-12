import os
import pandas as pd

"""

GENERATE SACS SECTIONS FROM TXT FILE

"""



#--------------------------------------------INPUTS
#Txt input file name for sections
#inputFile='X52_Seamless_Sections'
inputFile='X65_Welded_Sections'
#inputFile='Valves'
customLines=[
    ['FA1','Bla','Bla']
]
#--------------------------------------------INPUTS

txtPath = os.getcwd()+os.sep+inputFile+'.txt'
with open(txtPath, "r") as file1:
    sectionList = [line.split('x') for line in file1]


df = pd.DataFrame(data=sectionList,columns=("Diam","Th"))
print(df.to_markdown(index=False,tablefmt='simple_grid' ))

sectionName = [( str(int( float(x[0]) )) +'X'+ str(int(float(x[1]))) ) for x in sectionList ]

print (sectionName)

df.insert(0,'Section Name',sectionName,True)
print(df.to_markdown(index=False,tablefmt='simple_grid' ))


def inputGeneratorSec(df):
    for i in range(0, df.shape[0]):

        line = ''

        node = df.loc[i, 'Section Name']
        loadFormat = [['SECT'], [1], [node,7,True], [3],['TUB'],[31],['Diam', 6], ['Th', 5]]

        for j in loadFormat:
            if len(j) == 1:
                if type(j[0]) == int:
                    line = line + ' ' * j[0]
                else:
                    line = line + j[0]
            elif len(j)==2:
                word = j[0]
                word = df.iloc[i, df.columns.get_loc(word)]
                word = round(float(word)*0.1, 3)
                if word - int(word) == 0:
                    word = format(word, str(j[1] - 1) + 'g') + "."
                else:
                    word = format(word, str(j[1]) + 'g')
                line = line + word
            else:
                word = j[0]
                space = " "*(j[1]-len(j[0]))
                line = line + word + space

        print(line)

inputGeneratorSec(df)