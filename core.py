import os
import random

# SACSdir = '/Users/gq/Onedrive/Python Snippets/SACS/IFA'
# SACSdir = os.getcwd()+os.sep+'Input Files'


def getInput(path, key, displaytxt=False):
    fileSelector = [[os.path.join(r, file), file] for r, d, f in os.getcwd()
                    for file in f if ((fileExt(file) == '.PLET_Installation') and ('sacinp' in file))]
    for count, file in enumerate(fileSelector):
        print('[' + str(count) + ']' + file[0])
    if len(fileSelector) == 1:
        sel = 0
    else:
        sel = input()
    return fileSelector[int[sel]]


def fileExt(file):
    filename, file_ext = os.path.splitext(file)
    return file_ext


class Color():
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def prtOKGREEN(line):
        print(Color.OKGREEN, line, Color.ENDC)

    def prtOKBLUE(line):
        print(Color.OKBLUE, line, Color.ENDC)

    def prtOKRANDOM(line):
        print(random.choice(['\033[95m', '\033[94m', '\033[93m', '\033[92m', '\033[91m']), line, Color.ENDC)


def DictAttQuery(obj_type, dict_type):
    for prop in dict_type[obj_type]:
        print(Color.HEADER + '>> ' + obj_type + Color.ENDC)
        for item in prop.__dict__:
            if isinstance(prop.__dict__[item], str):
                print(item.capitalize() + ': ' + prop.__dict__[item])
            elif prop.__dict__[item] is None:
                print(item.capitalize() + ': None')
            elif isinstance(prop.__dict__[item], (int, float, tuple, list)):
                print(item.capitalize() + ': ' + str(prop.__dict__[item]))
            else:
                print(item.capitalize() + ': ' + prop.__dict__[item].name)


class Directory:

    def __init__(self, path):
        self.dirList = path.split(os.sep)
        self.path = path
        self.dirpath = os.path.dirname(path)
        self.dir = self.dirList[len(self.dirList) - 1]

    def tree(self, ext: str = None, dirs: list = None):
        for path, dirs, files in os.walk(self.path):
            print(path)
            for f in files:
                if ext is None:
                    print('- ' + f)
                else:
                    if ext in f:
                        print(' -' + f)


def makedir(filename):
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))


def writeTxt(ouput, input: list, clean=False):
    # clean: removal string
    with open(ouput + '.txt', 'w') as writer:
        for item in input:
            if type(item) == list:
                item = item[0]
            if not clean:
                writer.write("%s\n" % item)
            else:
                if item.split()[0] not in clean:
                    writer.write("%s\n" % item)
