# import genSec
# import genNode
# import genValve
# import valve
# import FilterJoints
import core
import members
# Generate SACS Nodes
# genNode.inputGeneratorNodes(genNode.dfSACS)

# Generate SACS Sections
# genSec.inputGeneratorSec(genSec.df)

# Generate Valves
# genValve.inputGenerator(genValve.df)

# import genYoke
from members import reg

import genSACSin

import freecad

#members.jointpopulate()
#Adicionar Nos de 2 vigas que nao sao detectados automaticamente
members.jointadd(['0134'])


# for joint in reg['Joint']:
#    print(joint.point.name)
# for group in members.reg['Group']:
#    print(group.name,group.elem[0].section.name)


txtfile = ['import Draft', 'import Arch', 'import Part']
txtfile += freecad.pointCloud(reg)

#txtfile += freecad.beamGen(reg, sections=True)
#txtfile += freecad.beamGen(reg, sections=[20])
#txtfile += freecad.beamgroup(reg,sections=True,colour=False)

#ENABLE FOR COLOURED SECTION VIEW
#txtfile += freecad.beamgroup(reg,sections=True,colour_opt=True,mix=True,export=True,groups=True)

#GREY SECTIONS
txtfile += freecad.beamgroup(reg,sections=True)

#GREY SECTIONS ALL GROUPS
#txtfile += freecad.beamgroup(reg,sections=True,groups=False)

#CENTRELINES
#txtfile += freecad.beamgroup(reg,sections=False)

# pprint(freecad.jointSpheres(reg))
# txtfile += freecad.jointSpheres(reg)

# JOINTS
#txtfile += freecad.jointLabels(reg, sections=True)

#txtfile += freecad.jointGen(reg, ['0158'])
#txtfile += freecad.jointGen(reg, stub_len=1)
#txtfile += ['FreeCAD.ActiveDocument.recompute()']

core.writeTxt('commands', txtfile)
