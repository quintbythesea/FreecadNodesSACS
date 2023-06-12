
import pandas as pd

#--------------------------------------------INPUTS
#Txt input file name from FreeCAD
inputFile='Auxi'
#Initial numbering for nodes
initialNode = 0
#Node First letters
fl = 'AX'
#--------------------------------------------INPUTS

txtPath = 'C:\\Users\\SAFCO108791\\Desktop\\'+inputFile+'.txt'

with open(txtPath, "r") as file1:
    pointList = [list(map(int,line.rstrip().split())) for line in file1]
#
df = pd.DataFrame(data=pointList,columns=("X","Y","Z"))
df = df*0.001
#df = df.round(3)
df.fillna(0,inplace=True)
df.sort_values(['Z','X'],inplace=True)
df.drop_duplicates(inplace=True)
df.reset_index(drop=True,inplace=True)
pointList = df.values.tolist()



nodeList = [("%04d" % (x+initialNode)) for x in range(df.shape[0])]
#node first letter
nodeList = [ fl+x[len(fl):] for x in nodeList]
#print (nodeList)
df = pd.concat([pd.Series(nodeList, name='Node'),df],axis=1)

#print(df.to_string(index=False))
print(df.to_markdown(index=False,tablefmt='simple_grid',floatfmt=".3f" ))
#print(df.to_markdown(index=False,tablefmt='simple_grid'))

#print(df.to_markdown())

auxi = [[round(x,3) for x in line] for line in pointList]
SACSint = [[int(item) for item in line] for line in auxi]
SACSfrac = [[round((x-y)*100,3) for x,y in zip(line1,line2)] for line1,line2 in zip(auxi,SACSint)]

SACSdata = [x+y for x,y in zip(SACSint,SACSfrac)]

dfSACS = pd.DataFrame(data=SACSdata,columns=("Xint","Yint","Zint","Xfrc","Yfrc","Zfrc"))

#dfSACS.sort_values(['Zint','Zfrc'],inplace=True)
#dfSACS.reset_index(drop=True,inplace=True)
dfSACS = pd.concat([pd.Series(nodeList, name='Node'),dfSACS],axis=1)

#print(dfSACS.to_string(index=False))

def inputGeneratorNodes(df):
    for i in range(0, df.shape[0]):

        line = ''

        node = df.loc[i, 'Node']
        loadFormat = [['JOINT'], [1], [node], [1], ['Xint', 7], ['Yint', 7], ['Zint', 7], ['Xfrc', 7]
            , ['Yfrc', 7], ['Zfrc', 7]]

        for j in loadFormat:
            if len(j) == 1:
                if type(j[0]) == int:
                    line = line + ' ' * j[0]
                else:
                    line = line + j[0]
            else:
                word = j[0]
                word = df.iloc[i, df.columns.get_loc(word)]
                word = round(word, 2)
                if word - int(word) == 0:
                    word = format(word, str(j[1] - 1) + 'g') + "."
                else:
                    word = format(word, str(j[1]) + 'g')
                line = line + word
        print(line)

inputGeneratorNodes(dfSACS)

