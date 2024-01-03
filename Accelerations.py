import math
import os
import numpy as np
from math import pi
from tabulate import tabulate
from itertools import product
from core import writeTxt
import xlsOps
import pandas as pd
from pprint import pprint as pp

gvt = 9.810
factor = 1.12
#factor = 1
""" INPUT DATA """

# Given data
roll_angle = 5  # Roll angle in degrees
pitch_angle = 5  # Pitch angle in degrees
heave_acceleration = 0.1  # Heave acceleration in m/s^2 [g]
period = 10  # Period in s

# COG (Center of Gravity) and COM (Center of Motion) positions
cog = np.array([85.75, -10, 1])  # [X, Y, Z] coordinates of COG
com = np.array([45.75, 0, -4.467])  # [X, Y, Z] coordinates of COM

""" --------- """

# Convert angles to radians
roll_accel = np.deg2rad(roll_angle) * 4 * (pi / period) ** 2
pitch_accel = np.deg2rad(pitch_angle) * 4 * (pi / period) ** 2

lever = cog - com

prints = [['Roll Angle',roll_angle],
          ['Pitch Angle',pitch_angle],
          ['Heave Acceleration',heave_acceleration],
          ['Period',period],
          ['COG Object',cog],
          ['COM Barge',com],
          ['Roll Accel',round(roll_accel,3)],
          ['Pitch Accel',round(pitch_accel,3)]]

for item in prints:
    print(item[0],item[1])


# Calculate accelerations
angular_acceleration = np.array([0.0, 0.0, 0.0])  # Initialize angular acceleration
linear_acceleration = np.array([0.0, 0.0, heave_acceleration])  # Linear acceleration in heave [g]

# Calculate angular acceleration due to roll and pitch
angular_acceleration[0] = roll_accel / gvt  # Roll acceleration [g]
angular_acceleration[1] = pitch_accel / gvt  # Pitch acceleration [g]


# ROTATION MATRIX GENERATION ON 3 AXIS
def rotmat(alfa, beta, teta, sequence: list):  # input angles in degrees, sequence rotation axis - X=1 Y=2 Z=3

    alfa = np.deg2rad(alfa)
    beta = np.deg2rad(beta)
    teta = np.deg2rad(teta)

    rotx = np.array([[1, 0, 0], [0, np.cos(alfa), -np.sin(alfa)], [0, np.sin(alfa), np.cos(alfa)]])
    roty = np.array([[np.cos(beta), 0, np.sin(beta)], [0, 1, 0], [-np.sin(beta), 0, np.cos(beta)]])
    rotz = np.array([[np.cos(teta), -np.sin(teta), 0], [np.sin(teta), np.cos(teta), 0], [0, 0, 1]])
    rotmats = [rotx, roty, rotz]

    axis = ['x', 'y', 'z']

    rotmatrix = np.identity(3)

    aux = ''

    for op in sequence:
        op = op - 1
        aux += axis[op]
        rotmatrix = np.dot(rotmats[op], rotmatrix)
        # print ('\n>Rotation',aux,'\n')
        # print (rotmatrix.round(3))

    return rotmatrix


# COMB GENERATION
fullvar_values = [1, 0, -1]
partial_values = [0.8, 0.6, -0.6, -0.8]
heave_values = [1, -1]

names = ['Roll', 'Pitch', 'Heave']
basic = ['ACCX', 'ACCY', 'ACCZ']
start = 6001

comb_1 = list(product(fullvar_values, fullvar_values, heave_values))
comb_2 = list(product(partial_values, partial_values, heave_values))

def accelcomb_gen(comb: list, start: int, prt=False):
    linelist = []
    table = []
    for combo in comb:
        # print('combo',combo)
        if not ((combo[0] == 0 and combo[1] == 0) or (
                abs(combo[0]) == 1 and abs(combo[1]) == 1)):  # exclude combs that have both 0 component

            alfa, beta = 0, 0
            angular_acc_it = [0,0,0]
            linear_acc_it = [0,0,0]

            seq = []
            if combo[0] != 0:  # if roll>0 add roll seq to rotmat
                seq += [1]
                alfa = math.copysign(roll_angle, combo[0] * -1)
            if combo[1] != 0:  # if pitch>0 add pitch seq to rotmat
                seq += [2]
                beta = math.copysign(pitch_angle, combo[1] * -1)

            angular_acc_it[0] = angular_acceleration[0] * combo[0]
            angular_acc_it[1] = angular_acceleration[1] * combo[1]

            linear_acc_it[2] = linear_acceleration[2] * combo[2] - 1

            acc_coef = np.dot(rotmat(alfa, beta, 0, seq), linear_acc_it) + np.cross(angular_acc_it, lever)

            # print ('linear acc',np.dot(rotmat(alfa,beta,0,seq),linear_acceleration))
            # print ('angular acc',np.cross (angular_acceleration,lever))

            num = str(start).zfill(4)
            title = f'*** COMB {num} - Transport {num} - '
            line = 'LCOMB ' + num + ' '

            if prt:
                print('////COMB',num)
                print ('++Dot prod: Rot Mat.Lin Acc\n',np.round(rotmat(alfa, beta, 0, seq),4),'dot',np.transpose(linear_acc_it),'=',np.dot(rotmat(alfa, beta, 0, seq), linear_acc_it))
                print ('++Cross prod: Ang Acc x Arm\n',np.round(angular_acc_it,4),'x',lever,'=',np.cross(angular_acc_it, lever))


            start += 1
            # aux = ''

            coefs = []
            for coef, name, bc, acc in zip(combo, names, basic, acc_coef):
                #print (coef)
                coefs+=[coef]
                # if coef != 0:
                title += f'({coef}){name} '
                #print(title)

                if acc != 0:
                    # print (coef,acc)
                    line += f'{bc}{"{:<07}".format(round(float(acc*factor), 3))[:6]}'  # format number to 7 characters

            print(title)
            linelist += [title]
            print(line)
            linelist += [line]
            print('*')
            linelist += ['*']
            acc_coef = [round(x*factor, 3) for x in acc_coef]
            table += [[title.split(' -')[0].split()[2], *coefs, *acc_coef]]
            # cases = [roll,pitch,heave]
    #print (table)
    return [table, linelist]


output = [accelcomb_gen(comb_1, 6001,prt=True), accelcomb_gen(comb_2, 6101,prt=True)]

# Txt Export
writeTxt('LCOMB_Transportation', ['LCOMB'] + output[0][1] + output[1][1])  # LCOMB.txt

# XlsOps Export
formatcdx = [[[4, 5, 6], {'num_format': '0.000'}]]  # XlsOps format cdx
data = output[0][0] + output[1][0]
columns = ['COMB', 'Roll','Pitch','Heave', 'Acc X', 'Acc Y', 'Acc Z']
workbook = xlsOps.workbookGen(name='Accelerations', dirPath=os.getcwd(), stamp=False)
xlsOps.xlsFormat(pd.DataFrame(data=data, columns=columns), sheetName='Accelerations', workbook=workbook,
                 formatcdx=formatcdx, colWidthList=[[1, 8],[2,8],[3,8]])
workbook.close()

print (tabulate(data,columns,tablefmt='github'))