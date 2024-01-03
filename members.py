from math import pi, sqrt

# Class lingo
# type(x).__name__ >> returns name of instance x class
# super().__init__(name) >> inherits super class

# Vars

reg = {}


# Classes

class GlobalOps:
    def __init__(self, name):
        self.name = name

        # add class group to reg dict

        classname = self.__class__.__name__
        if classname in reg.keys():
            reg[classname].append(self)
        else:
            reg[classname] = [self]


# add boundary conditions
class Point(GlobalOps):
    def __init__(self, name, x, y, z):
        super().__init__(name)
        self.x = x
        self.y = y
        self.z = z
        self.pos = (x, y, z)

    def __sub__(self, other):  # TODO replace by len
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2) ** 0.5

    def __mul__(self, other):  # TODO replace by len
        return tuple([self.x * other, self.y * other, self.z * other])


class Node:
    # nodes are not in register and are only for contruction purposes
    def __init__(self, pos):
        if isinstance(pos, Point):
            self.x = pos.x
            self.y = pos.y
            self.z = pos.z
            self.pos = pos.pos

        else:  # List
            self.x = pos[0]
            self.y = pos[1]
            self.z = pos[2]
            self.pos = pos

    def __sub__(self, other):
        return [self.x - other.x, self.y - other.y, self.z - other.z]

    def __mul__(self, vector):
        return [self.x * vector.x, self.y * vector.y, self.z * vector.z]

    def __len__(self, other):
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2


class Vector:
    def __init__(self, pointA, pointB):
        self.dim = [pointB.x - pointA.x, pointB.y - pointA.y, pointB.z - pointA.z]
        self.nodeA = Node(pointA.pos)
        self.nodeB = Node(pointA.pos)
        self.x = self.dim[0]
        self.y = self.dim[1]
        self.z = self.dim[2]
        self.len = sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        self.unit = [xyz / self.len for xyz in self.dim]

    def __mul__(self, other):
        return [xyz * other for xyz in self.unit]

    def node_along(self, point='A', dist=1):
        if point == 'A':
            point = self.nodeA
        if point == 'B':
            point = self.nodeB
        return Node([k1 + k2 for k1, k2 in zip(point.pos, self * dist)])

    def scale(self, factor):  # TODO
        print('scale')


class Material(GlobalOps):
    def __init__(self, name, ystress, emod, poisson, density, straincurve=None):
        super().__init__(name)
        self.ystress = ystress
        self.emod = emod
        self.poisson = poisson
        self.density = density
        # wtf
        self.straincurve = straincurve


# S355_DNV_TrueSS = [[255, 0], [256, 0.2], [260, 0.5]]

class Tube(GlobalOps):
    def __init__(self, name, diam, thick):
        super().__init__(name)
        self.diam = diam
        self.thick = thick
        # self.material = material
        self.area = pi * ((diam / 2) ** 2 - ((diam - 2 * thick) / 2) ** 2) * 0.01


class Isection(GlobalOps):
    def __init__(self, name, height, width, tf, tw):
        super().__init__(name)
        self.height = height
        self.width = width
        self.tf = tf
        self.tw = tw
        # self.material = material
        self.area = (width * tf * 2 + (height - tf) * tw) * 0.01


class RecSection(GlobalOps):

    def __init__(self, name, height, width,th):
        super().__init__(name)
        self.height = height
        self.width = width
        self.th = th
        self.area = (height-th+width-th)*2*th * 0.01
        # self.material = material


class ChanelSection(GlobalOps):
    def __init__(self, name, height, width, tf, tw):
        super().__init__(name)
        self.height = height
        self.width = width
        self.tf = tf
        self.tw = tw
        self.area = (width * tf * 2 + (height - tf) * tw) * 0.01
        # self.material = material


class FlatBar(GlobalOps):
    def __init__(self, name, height, th):
        super().__init__(name)
        self.height = height
        self.th = th
        self.area = (height * th) * 0.01
        # self.material = material


class Conical(GlobalOps):
    def __init__(self, name, diam1, diam2, thick):
        super().__init__(name)
        self.diam1 = diam1
        self.diam2 = diam2
        self.th = thick

        # Equivalent area
        diam_eq = (diam1 + diam2) / 2
        self.area = pi * ((diam_eq / 2) ** 2 - ((diam_eq - 2 * thick) / 2) ** 2) * 0.01
        # Section area
        self.area1 = pi * ((diam1 / 2) ** 2 - ((diam1 - 2 * thick) / 2) ** 2) * 0.01
        self.area2 = pi * ((diam2 / 2) ** 2 - ((diam2 - 2 * thick) / 2) ** 2) * 0.01

    def vol(self, lth: float):
        # len in m
        r1 = self.diam1 * 0.5
        r2 = self.diam2 * 0.5
        v_outer = (1 / 3) * pi * lth * (r2 ** 2 + r2 * r1 + r1 ** 2)
        r1 = r1 - self.th
        r2 = r2 - self.th
        v_inner = (1 / 3) * pi * lth * (r2 ** 2 + r2 * r1 + r1 ** 2)

        return v_outer - v_inner


class Beam(GlobalOps):

    def __init__(self, name, start, end, section, material):
        super().__init__(name)
        self.name = name
        self.start = start
        self.end = end
        self.section = section
        self.material = material

    def length(self):
        return self.end - self.start

    def weight(self):
        if isinstance(self.section, Conical):
            return self.section.vol(self.length()) * self.material.density * 0.0001
        else:
            return self.length() * self.section.area * self.material.density * 0.01


class Group(GlobalOps):
    def __init__(self, name: str, material, section, elem: list):
        super().__init__(name)
        self.material = material
        self.section = section
        self.elem = elem


class Joint(GlobalOps):
    def __init__(self, name: str, point: Point, beams: list):
        super().__init__(name)
        self.point = point
        self.beams = beams


def jointpopulate():
    print('USED ------------------------------------------------------------')

    count = 0
    for point in reg['Point']:
        aux = list()
        for beam in reg['Beam']:
            if beam.end == point or beam.start == point:
                if isinstance(beam.section, Tube):
                    aux.append(beam)
        # change to 1 for all 2 beam insterections
        # if len(aux) > 1:
        if len(aux) > 2:
            count += 1
            Joint('J' + str(count), point, aux)


def jointadd(nodelist:list):
    count = len(reg.get('Joint', {}))
    for joints in nodelist:
        for point in reg['Point']:
            aux = list()
            for beam in reg['Beam']:
                if beam.end == point or beam.start == point:
                    if isinstance(beam.section, Tube):
                        aux.append(beam)
            # change to 1 for all 2 beam insterections
            # if len(aux) > 1:
            count += 1
            Joint('J' + str(count), point, aux)

def get_obj(name: str, group='Beam'):
    if group != 'Section':
        aux = next((x for x in reg[group] if x.name == name), None)
        return aux
    else:
        # print('trying to find', name)
        for section in ['Conical', 'Isection', 'Tube', 'RecSection', 'ChanelSection', 'FlatBar']:
            if section in reg.keys():
                # print ('section found')
                aux = next((x for x in reg[section] if x.name == name), None)
                if aux is not None:
                    return aux
        print('Section not found')


def addNewMaterials(fy, emod, dens):
    fy = float(fy) * 10
    emod = float(emod) * 10
    dens = float(dens) * 1000
    for material in reg['Material']:
        if material.ystress == fy:
            if material.emod == emod:
                if material.density == dens:
                    return material.name
    name = 'M' + str(len(reg['Material'])).zfill(2)
    Material(name, fy, emod, 0.3, dens)
    return name
