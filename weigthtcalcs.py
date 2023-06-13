from math import pi


def volTube(diam, thick, lth):
    # self.material = material

    area = pi * ((diam / 2) ** 2 - ((diam - 2 * thick) / 2) ** 2) * 0.01
    print('Area', area)
    return area * lth


def volCone(d1, d2, th, lth, met=1):
    diam_eq = (d1 / 2 + d2 / 2) / 2
    area_eq = pi * ((diam_eq / 2) ** 2 - ((diam_eq - 2 * th) / 2) ** 2) * 0.01

    if met == 1:
        # return pi * lth * ((d1 + d2) / 4) * th*0.01
        r1 = d1 / 2
        r2 = d2 / 2
        print('Vol', (1 / 3) * pi * lth * (
                    (r2 ** 2 + r2 * r1 + r1 ** 2) - ((r2 - th) ** 2 + (r2 - th) * (r1 - th) + (r1 - th) ** 2)) * 0.01)
        v_outer = (1 / 3) * pi * lth * (r2 ** 2 + r2 * r1 + r1 ** 2)
        r1 = r1 - th
        r2 = r2 - th
        v_inner = (1 / 3) * pi * lth * (r2 ** 2 + r2 * r1 + r1 ** 2)

        print('Vol', (v_outer - v_inner) * 0.01)

        return (v_outer - v_inner) * 0.01

    if met == 2:
        print('Area eq', area_eq)
        return area_eq * lth


ds = 7890 * 0.01

# FA1
d_FA1 = 44.56
th_FA1 = 2.45
l_FA1 = 0.57
weight_FA1 = volTube(d_FA1, th_FA1, l_FA1) * ds
print('FA1', round(weight_FA1), 'kg')

# FA3
d_FA3 = 71.12
th_FA3 = 3.18
l_FA3 = 0.19
weight_FA3 = volTube(d_FA3, th_FA3, l_FA3) * ds
print('FA3', round(weight_FA3), 'kg')

# FA2
d_FA2_1 = d_FA3
d_FA2_2 = d_FA1
th_FA2 = 7
l_FA2 = 0.33
weight_FA2 = volCone(d_FA2_1, d_FA2_2, th_FA2, l_FA2, 1) * ds
print('FA2', round(weight_FA2), 'kg')


# print('FA2',round(volCone(d_FA2_1,d_FA2_2,th_FA2,l_FA2,2)*ds),'kg')


def FEvol(d1, d2, th, lth, it):
    parciais = 0
    length = 0
    slope = (d1 - d2) * 0.5 / lth
    inc = lth / it
    for i in range(1, it):
        # print (i,'D',d2+(i*inc*slope*2))
        parciais += volTube(d2 + (i * inc * slope * 2), th, inc)
        length += inc
    print('vol:', parciais, 'W', parciais * ds)
    print('len:', length)


FEvol(d_FA2_1, d_FA2_2, th_FA2, l_FA2, 500)

print(volTube((d_FA2_1 + d_FA2_2) / 2, 7, 0.33) * ds)
