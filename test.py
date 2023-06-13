import core
import os
# import pandas as pd
from pprint import pprint as pp

# aux = list()
# for i in [1,2,3,4,3,4,5]:
#    if i not in aux:
#        aux.append(i)
#        print (aux)

# OBTER OUPUT DE CODEX PARA PARSING
string = [0] * 4
string[
    0] = 'FA1 FA01-FA02 7002  12.09 110.3   4594.3 2588.0 2340.0   .3E+03 .8E+05 .3E+03 .3E+03   TN+BN    0.33   0.33 ' \
         '  0.85   0.85'
string[1] = 'SECT 22X22     TUB                               55.8802.223'
string[2] = 'SECT LPD       PRI                               100.00     10.000'
string[3] = 'SECT 28X23     TUB                               71.1202.382'


def posCount(string):
    aux = []
    aux2 = []
    for pos, letter in enumerate(string):
        aux.append(pos)
        aux2.append(letter)
    print([aux, aux2])

    # pp(aux2)


# posCount(string[3])

def stringCount(string, sep=False):
    aux = []
    words = string.split()
    for word in words:
        if sep is False or word.count('.') < 2:
            start = string.find(word)
            end = start + len(word)
            aux = aux + [[start, end]]
        else:
            print('este')
            start = string.find(word)
            end = start + len(word)
            aux = aux + [[start, end]]
    print(words)
    # print(core.Color.OKGREEN,aux,core.Color.ENDC)
    core.Color.prtOKRANDOM(aux)
    return aux


# Section generator
file = os.getcwd() + os.sep + 'sect.txt'


def textCount(filePath):
    text = [line for line in open(filePath) if len(line.split()) > 3]
    media = []
    maxid = []
    for line in text:
        media.append(stringCount(line))

    minwords = min(len(line) for line in media)


# textCount(file)

# Section generator
# file = core.SACSdir + os.sep + 'Sections.txt'
# text = [line.rstrip('\n').split() for line in open(file)]
# pp(text)
# for line in text:
#     diam = round(float(line[1])/10,2)
#     thick = round(float(line[2])/10,2)
#     print ('SECT ',' '*(7-len(line[0])),line[0],'   TUB',' '*31,
#            ' '*(5-len(str(diam))),diam,' '*(5-len(str(thick))),thick,sep='')

rgb = []
hexlist = ['#440154FF', '#481567FF', '#482677FF', '#453781FF', '#404788FF',
           '#39568CFF', '#33638DFF', '#2D708EFF', '#287D8EFF', '#238A8DFF',
           '#1F968BFF', '#20A387FF', '#29AF7FFF', '#3CBB75FF', '#55C667FF',
           '#73D055FF', '#95D840FF', '#B8DE29FF', '#DCE319FF', '#FDE725FF']
for hexc in hexlist:
    h = hexc.lstrip('#')
    val = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    print('RGB =', val)
    rgb.append(val)

print(rgb)
