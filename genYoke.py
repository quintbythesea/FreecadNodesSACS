import os
import pandas as pd
import genSACSin
import members
from dictree import object_tree
import numpy as np

# import members

inputdir = os.getcwd() + os.sep + 'Input'
mydir = os.getcwd() + os.sep + 'YOKE'


def yokepointonly():
    filter = []
    for file in os.listdir(inputdir):
        if file.startswith('sacinp'):
            txtPath = mydir + os.sep + file
            with open(txtPath, "r") as file1:
                for line in file1:
                    # print (line[:5])
                    if line[:7] == 'JOINT Y':
                        filter.append(line)
            # print (filter)
            # print(file)
            name = file.split('_')[1]

            with open(mydir + os.sep + 'Export' + os.sep + name + '.txt', 'w') as f:
                for line in filter:
                    f.write(line)
            filter = []


def noyokepointonly():
    filter = []
    for file in os.listdir(inputdir):
        if file.startswith('sacinp'):
            txtPath = inputdir + os.sep + file
            with open(txtPath, "r") as file1:
                for line in file1:
                    # print (line[:5])
                    if line[:7] != 'JOINT Y':
                        filter.append(line)
            # print (filter)
            # print(file)
            name = file.split('_')[1]

            with open(mydir + os.sep + 'Export' + os.sep + name + 'NOYOKE.txt', 'w') as f:
                for line in filter:
                    f.write(line)
            filter = []


# object_tree(members.reg)
# rotation of YOKE from PLET X line
#rotations = [36.5,40,43, 45, 90 - 20, 90 - 15, 90, 120]
rotations = [48, 90 - 20, 90 - 15, 90, 120]
#rotations = [90]
# rotation node
rot_point = members.get_obj('0125', 'Point')
print ('origin pos',rot_point.pos)

# print(rn.pos)
yoke_points = []
point_array = []
for point in members.reg['Point']:
    if point.name.startswith('Y'):
        print(point.pos)
        yoke_points.append(point.name)
        point_array.append(point.pos)

point_array = np.array(point_array)
centroid = np.mean(point_array, axis=0)
axis_to_centroid = centroid - np.array(rot_point.pos)
orig_rotation_angle = np.arctan2(axis_to_centroid[2], axis_to_centroid[0])
orig_rotation_angle = np.degrees(orig_rotation_angle)
print(f'Current yoke rotation = {round(orig_rotation_angle)}{chr(176)}')


def angle_in_xz_plane(point1, point2):
    # Calculate the vector between the two points
    vector = point2 - point1

    # Project the vector onto the XZ plane by setting the Y component to 0
    projected_vector = np.array([vector[0], 0, vector[2]])

    # Calculate the angle between the projected vector and the positive X-axis
    angle = np.arctan2(projected_vector[2], projected_vector[0])

    # Convert the angle to degrees
    angle_degrees = np.degrees(angle)

    return angle_degrees


#orig_rotation_angle = round(angle_in_xz_plane(rot_point.pos, point_array[0]))
print('Original Rotation ', orig_rotation_angle)


def rotate_y_axis(points, origin, phi):
    # deg to radians
    phi = np.radians(phi)

    # Translate the points so that the rotation axis passes through the point (x, y, z)
    points_translated = points - np.array(origin.pos)

    # Calculate the rotation matrix around the y-axis
    rotation_matrix = np.array([[np.cos(phi), 0, np.sin(phi)],
                                [0, 1, 0],
                                [-np.sin(phi), 0, np.cos(phi)]])

    # Apply the rotation matrix to the translated points
    points_rotated = np.dot(points_translated, rotation_matrix.T)

    # Translate the points back to the original position
    points_final = points_rotated + np.array(origin.pos)

    return points_final


def sacs_nodes(points, new_coord):
    df = pd.DataFrame(data=new_coord, columns=("X", "Y", "Z"))
    # df = df*0.001
    # df = df.round(3)
    # df.fillna(0,inplace=True)
    # df.sort_values(['Z','X'],inplace=True)
    # df.drop_duplicates(inplace=True)
    # df.reset_index(drop=True,inplace=True)
    # print (nodeList)
    df = pd.concat([pd.Series(points, name='Node'), df], axis=1)

    # print(df.to_string(index=False))
    print(df.to_markdown(index=False, tablefmt='simple_grid', floatfmt=".3f"))
    # print(df.to_markdown(index=False,tablefmt='simple_grid'))

    # print(df.to_markdown())

    #auxi = [[round(x, 3) for x in line] for line in new_coord]
    auxi = [[x for x in line] for line in new_coord]
    SACSint = [[int(item) for item in line] for line in auxi]
    #SACSfrac = [[round((x - y) * 100, 3) for x, y in zip(line1, line2)] for line1, line2 in zip(auxi, SACSint)]
    SACSfrac = [[((x - y) * 100) for x, y in zip(line1, line2)] for line1, line2 in zip(auxi, SACSint)]

    SACSdata = [x + y for x, y in zip(SACSint, SACSfrac)]

    dfSACS = pd.DataFrame(data=SACSdata, columns=("Xint", "Yint", "Zint", "Xfrc", "Yfrc", "Zfrc"))

    # dfSACS.sort_values(['Zint','Zfrc'],inplace=True)
    # dfSACS.reset_index(drop=True,inplace=True)
    dfSACS = pd.concat([pd.Series(points, name='Node'), dfSACS], axis=1)

    # print(dfSACS.to_string(index=False))

    def inputGeneratorNodes(df):
        texto = []
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
                    word = round(word, 3)
                    if word - int(word) == 0:
                        word = format(word, str(j[1] - 1) + 'g') + "."
                    else:
                        word = format(word, str(j[1]) + 'g')
                    line = line + word
            print(line)
            texto.append(line)

        return texto

    return inputGeneratorNodes(dfSACS)


for angle in rotations:
    # input de 0 passa a 90
    print('ROTACAO - ',angle,'\n')
    if angle != round(orig_rotation_angle):
        rot = orig_rotation_angle - angle
        print(rot)
        rotated_points = rotate_y_axis(point_array, rot_point, rot)
        texto = sacs_nodes(yoke_points, rotated_points)

        filename = f'JOINTYOKE{angle}.txt'

        with open(mydir + os.sep + 'Export' + os.sep + filename, 'w') as f:
            for line in texto:
                f.write(line + '\n')

noyokepointonly()
