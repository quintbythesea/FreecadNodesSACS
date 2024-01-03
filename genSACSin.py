# from core import *
import datetime
import members
import core
# from database import *
import pandas as pd
import os
import database
from pprint import pprint
import sys

assert database  # imported because of database vars

""" 
MAIN IMPORT MODULE - READS SACS FILES AND GENERATES REGISTER
OPTION TO EXPORT WEIGHT FROM GROUPS WITH TUBES
"""

print('\nRunning genSACSin...')

# For macOS
# os.chdir(app_dir = os.path.dirname(os.path.abspath(sys.argv[0])))
SACSdir = os.getcwd() + os.sep + 'input'


# print(os.getcwd(),'aqui')

def subItem(mainList, indexList, entry):
    aux = [x for x in indexList if x[0].startswith(entry)]
    if len(aux) > 1:
        primeiro = aux[0][1]
        outroInd = indexList.index((aux[len(aux) - 1])) + 1
        ultimo = indexList[outroInd][1]
        return mainList[primeiro:ultimo]
    else:
        return False


def nowName():
    date = datetime.datetime.now()
    day = ("%02d" % (date.day,))
    month = (date.strftime("%b")).upper()
    hour = ("%02d" % date.hour)
    minute = ("%02d" % date.minute)
    return month + day + ' - ' + hour + '.' + minute


# PARSERS

def memberparser(member: list, prt=False):
    df = list()
    i = 1
    for line in member:
        if line[7:14] != 'OFFSETS' and len(line.split()) > 2:
            # print (line)
            if prt:
                print('B' + str(i).zfill(3) + ': J1:' + line[7:11] + ', J2:' + line[11:15] + ', Sect:' + line[16:19])
            df.append(['B' + str(i).zfill(3), line[7:11].strip(), line[11:15].strip(), line[16:19].strip()])
            i += 1
    return df


def jointparser(joint: list, prt=False):
    i = 1

    def xE(number: str):
        # number.strip() or 0
        if '-' not in number.strip()[1:]:
            #print (number,number[1:6])
            return number.strip() or 0
        else:
            #return '0.'
            return 0

    df = list()

    for line in joint:
        if prt:
            print (line)
        if len(line.split()) > 4 and line[0] != '*':
            if prt:
                print('node:', line[6:10], ', X', line[11:18], ', Y', line[18:25], ', Z', line[25:32], sep=' ')
                print('node:', line[6:10], ', Xf', xE(line[32:39]), ', Yf', xE(line[39:46]), ', Zf', xE(line[46:53]),
                      sep=' ')

            node = line[6:10].strip()
            x = float(line[11:18]) + float(xE(line[32:39])) * 0.01
            y = float(line[18:25]) + float(xE(line[39:46])) * 0.01
            z = float(line[25:32]) + float(xE(line[46:53])) * 0.01

            #df.append([node, round(x, 2), round(y, 2), round(z, 2)])
            #df.append([node, round(x, 6), round(y, 6), round(z, 6)])
            df.append([node, round(x, 4), round(y, 4), round(z, 4)])

            i += 1

    return df


def sectparser(sect: list, prt=False):
    df = list()
    for line in sect:
        if len(line.split()) > 2 and line[0] != '*':
            # print (line)
            name = line[5:12].strip()
            sectype = line[15:18]
            # print(sectype)

            # TUBES
            if sectype == 'TUB':
                D0 = float(line[49:55])
                th = float(line[55:60])
                if prt:
                    print('Section', name, 'Type:', sectype, sep=' ')
                    print('D0', D0, 'Th:', th, sep=' ')
                members.Tube(name, D0, th)

            # RHS
            elif sectype == 'BOX':
                height = float(line[49:55])
                width = float(line[60:66])
                th = float(line[55:60])
                if prt:
                    print('Section', name, 'Type:', sectype, sep=' ')
                    print('Height', height, 'Width:', width, 'th:', th, sep=' ')
                members.RecSection(name, height,width,th)
                # df.append([name, sectype, D0, th])

            # IBeams
            elif sectype in ['Ibeams', 'WFC', 'PLG']:
                height = float(line[49:55])
                th_f = float(line[55:60])
                width = float(line[60:66])
                th_w = float(line[66:72])
                if prt:
                    print('Section', name, 'Type:', sectype, sep=' ')
                    print('height', height, 'width:', width, 'th_f:', th_f, 'th_w:', th_w, sep=' ')
                members.Isection(name, height, width, th_f, th_w)

            # Channels
            elif sectype in 'Channel':
                height = float(line[49:55])
                th_f = float(line[55:60])
                width = float(line[60:66])
                th_w = float(line[66:72])
                if prt:
                    print('Section', name, 'Type:', sectype, sep=' ')
                    print('height', height, 'width:', width, 'th_f:', th_f, 'th_w:', th_w, sep=' ')
                members.ChanelSection(name, height, width, th_f, th_w)

            # Flatbars
            elif sectype == 'PRI':
                height = float(line[49:55])
                # print(line)
                th = float(line[60:66])
                # print(th)
                if prt:
                    print('Section:', name, 'Type:', sectype, sep=' ')
                    print('height:', height, 'th:', th, sep=' ')
                members.FlatBar(name, height, th)

            elif sectype == 'CON':
                D1 = float(line[49:55])
                D2 = float(line[60:66])
                th = float(line[55:60])
                if prt:
                    print('Section', name, 'Type:', sectype, sep=' ')
                    print('D1', D1, 'D2', D2, 'Th:', th, sep=' ')
                members.Conical(name, D1, D2, th)

    return df


def gruparser(grup: list, prt=False):
    df = list()
    for line in grup:
        if len(line.split()) > 6 and line[0] != '*':
            group = line[5:8]
            section = line[9:17]
            emod = line[30:35]
            fy = line[40:45]
            dens = line[70:76]
            if '+' in emod:
                emod = emod.replace('+', 'e+')
            elif '-' in emod:
                emod = emod.replace('-', 'e-')
            if '+' in dens:
                dens = dens.replace('+', 'e+')
            elif '-' in dens:
                dens = dens.replace('-', 'e-')
            if prt:
                print(group, section, emod, fy, dens, sep=' ')
            df.append([group, section, emod, fy, dens])
    return df


# FILE SELECTOR #TODO make this a function you can call from elsewhere
for file in os.listdir(SACSdir):
    if file.startswith('sacinp') and not file.endswith('bak'):
        sacsin = SACSdir + os.sep + file
        print(f"\nDIR> {sacsin}\n\n")


# print (SACSdir)
# print(fileSelector)
# print('Select List File: ')
# sel = input()

# Make function - text reader


def process_sacsin(sacsin_file: str):
    SACS = [line.rstrip('\n') for line in open(sacsin_file)] + ['TERMINUS']
    indexL = []
    notable = ('OPTIONS', 'LCSEL', 'SECT', 'GRUP', 'MEMBER', 'JOINT', 'LOADCNDEAD', 'LOADCNDM',
               'LOADCNVR', 'LCOMB', 'END', 'TERMINUS', 'WGTMEMANC', 'LOAD', 'PLATE', 'PGRUP')

    for x in range(0, len(SACS)):
        if any(SACS[x].startswith(z) for z in notable):
            indexL.append((SACS[x], x))

    # print (indexL)

    # options = subItem(SACS, indexL, 'OPTIONS')
    # lcsel = subItem(SACS, indexL, 'LCSEL')
    sect = subItem(SACS, indexL, 'SECT')
    # core.writeTxt('sect', sect)
    grup = subItem(SACS, indexL, 'GRUP')
    # core.writeTxt('grup', grup)
    member = subItem(SACS, indexL, 'MEMBER')
    # core.writeTxt('member', member)
    joint = subItem(SACS, indexL, 'JOINT')
    # core.writeTxt('joint', joint)
    weight = subItem(SACS, indexL, 'WGTMEMANC')
    # loadDead = subItem(SACS, indexL, 'LOADCNDEAD')
    # loadVR = subItem(SACS, indexL, 'LOADCNVR')
    # loadDummy = subItem(SACS,indexL,'LOADCNDM')
    # lcomb = subItem(SACS, indexL, 'LCOMB')
    # end = subItem(SACS, indexL, 'END')

    sectparser(sect, prt=False)
    # for line in sectparser(sect):
    # print(line)
    # print(len(line))
    # print (line)
    # members.Tube(line[0].strip(), round(line[2] * 10, 2), round(line[3] * 10, 2))

    # Populate Class Points
    # 1print (joint)
    for line in jointparser(joint,True):
        members.Point(line[0], line[1], line[2], line[3])

    # Populate Groups Dictionary
    # pp(SACSin.gruparser(SACSin.grup))
    groups = dict()
    for line in gruparser(grup):
        # print (line)
        groups[line[0].strip()] = {'Section': line[1].strip(),
                                   'Material': members.addNewMaterials(line[3], line[2], line[4]),
                                   'Members': []}

    # Populate Beams Class
    # pp(SACSin.memberparser(SACSin.member))
    for line in memberparser(member):
        if '' in (groups[line[3]]['Section']):
            # print (line[3])
            # print(members.get_obj(line[3], 'Section'))
            members.Beam(line[0],
                         members.get_obj(line[1].strip(), 'Point'),
                         members.get_obj(line[2].strip(), 'Point'),
                         members.get_obj(groups[line[3]]['Section'], 'Section'),
                         members.get_obj(groups[line[3]]['Material'], 'Material'))

            groups[line[3]]['Members'].append(line[0])

    # Populate GROUPS Class
    for group, elem in zip(groups, groups.values()):
        if len(elem['Members']) > 0:
            print(group, elem['Section'], elem['Members'])
            beams = []
            for beam_name in elem['Members']:
                beams.append(members.get_obj(beam_name, 'Beam'))
            #print(beams)
            # Populate by getting data from 1st beam
            members.Group(group, beams[0].material, beams[0].section, beams)

    return groups


# Total Weight
# pp(reg)

# weight = 0
# for beam in reg['Beam']:
#     print (beam.name,beam.start,beam.end)
#     print(beam.name, beam.section.name, beam.section.diam, beam.section.thick, beam.start.pos, beam.end.pos,
#           ' ------- ', str(round(beam.length(), 2)) + 'm',
#           str(round(beam.weight(), 2)) + 'kg')
#     weight += beam.weight()
# print(round(weight, 2), 'kg')

# from pprint import pprint as pp

# pp(groups)


def weightTubes(dict_groups: dict, groupsel=False, export=False):
    df = []

    if not groupsel:
        groupsel = []
        for group in groups:
            if len(groups[group]['Members']) > 0:
                groupsel.append(group)

    for group in groupsel:

        totalWeightGrp = 0
        totalLengthGrp = 0
        members.get_obj(groups[group]['Members'][0])
        beamOne = members.get_obj(groups[group]['Members'][0])

        sectype = type(beamOne.section).__name__

        if sectype == 'Tube':

            beamSection = beamOne.section.name
            beamD0 = beamOne.section.diam
            beamth = beamOne.section.thick
            beamWeight = beamOne.section.area * beamOne.material.density * 0.0001

            for beam in groups[group]['Members']:
                beam = members.get_obj(beam)
                totalWeightGrp += beam.weight()
                totalLengthGrp += beam.length()
            df.append([group, beamSection, beamD0, beamth,
                       round(totalLengthGrp, 2),
                       round(beamWeight, 2),
                       round(totalWeightGrp, 2)])
    df = pd.DataFrame(columns=['Group', 'Section', 'D0', 'Th', 'Length', 'Weight/m', 'TotalWeight'],
                      data=df)
    if export:
        filename = os.getcwd() + os.sep + 'WEIGHT TUBES' + nowName() + '.xlsx'
        core.makedir(filename)
        writer = pd.ExcelWriter(filename, engine='openpyxl')
        df.to_excel(writer, sheet_name='Group Summary', index=False)
        writer.close()

    return df


def weightreport(dict_groups: dict, groupsel=False, export=False):
    df = []

    if not groupsel:
        groupsel = []
        for group in groups:
            if len(groups[group]['Members']) > 0:
                groupsel.append(group)

    # print (groupsel)

    for group in groupsel:

        totalWeightGrp = 0
        totalLengthGrp = 0
        # members.get_obj(groups[group]['Members'][0])
        beamOne = members.get_obj(groups[group]['Members'][0])
        # print (group,beamOne.name)
        # print (beamOne.section)

        sectype = type(beamOne.section).__name__

        beamSection = beamOne.section.name
        # beamD0 = beamOne.section.diam
        # beamth = beamOne.section.thick
        beamWeight = beamOne.section.area * beamOne.material.density * 0.01

        # print (group)

        for beam in groups[group]['Members']:
            beam = members.get_obj(beam)
            totalWeightGrp += beam.weight()
            totalLengthGrp += beam.length()

        attributes = ', '.join([f"{att}={round(val, 2) if isinstance(val, (int, float)) else val}"
                                for att, val in beamOne.section.__dict__.items() if att != 'name'])

        df.append([group, beamSection, sectype,
                   round(totalLengthGrp, 2),
                   round(beamWeight, 2),
                   round(totalWeightGrp, 2),
                   attributes])
    df = pd.DataFrame(columns=['Group', 'Section', 'Type', 'Length', 'Weight/m', 'TotalWeight', 'Att'],
                      data=df)
    if export:
        filename = os.getcwd() + os.sep + 'WEIGHT REPORT ' + nowName() + '.xlsx'
        core.makedir(filename)
        writer = pd.ExcelWriter(filename, engine='openpyxl')
        df.to_excel(writer, sheet_name='Group Summary', index=False)
        writer.close()

    return df


groups = process_sacsin(sacsin)

#weightgroup(groups,groupsel=[BR1 HSP JLT LG1 LTR P10 PAD POU SLE TEE VP YK1 YK2],export=True)
weightreport(groups, export=True)
# weightTubes(groups, export=True)
# print (members.reg)
