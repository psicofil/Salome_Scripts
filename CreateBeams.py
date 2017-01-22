# -*- coding: utf-8 -*-

# Beams

import salome
salome.salome_init()
import GEOM
from salome.geom import geomBuilder
geompy = geomBuilder.New(salome.myStudy)
gg = salome.ImportComponentGUI("GEOM")
import math
#from PyQt4 import QtGui,QtCore
import SALOMEDS

## Options

Solid = False
Vertex = False


###### PROCEED ######

# selected Objects
selected=salome.sg.getSelected(0)
selobjID=salome.myStudy.FindObjectID(selected)
selobj=selobjID.GetObject()
selected1=salome.sg.getSelected(1)
selobjID1=salome.myStudy.FindObjectID(selected1)
selobj1=selobjID1.GetObject()

Face_1 = geompy.MakeFaceWires(selobj, 1)

Face_2 = geompy.MakeFaceWires(selobj1, 1)

faces1 = geompy.ExtractShapes(Face_1, geompy.ShapeType["FACE"], True)
group1=list()

faces2 = geompy.ExtractShapes(Face_2, geompy.ShapeType["FACE"], True)
group2=list()

for i in faces1:
    Vertex_1 = geompy.MakeVertexOnSurface(i, 0.5, 0.5)
    #V1 = geompy.addToStudy( Vertex_1, 'V1' )
    group1.append(Vertex_1)

for i in faces2:
    Vertex_2 = geompy.MakeVertexOnSurface(i, 0.5, 0.5)
    #V2 = geompy.addToStudy( Vertex_2, 'V2' )
    group2.append(Vertex_2)

groupL=list()
groupS=list()
prop_c = geompy.BasicProperties(faces1[0])
import math
r = prop_c[0]/(2.0*math.pi)


if len(group1)==len(group2):
    for i in range(0,len(group1)):
        Line = geompy.MakeLineTwoPnt(group1[i], group2[i])
        prop = geompy.BasicProperties(Line)
        Cylinder = geompy.MakeCylinder(group1[i], Line, r, prop[0])
        groupL.append(Line)
        groupS.append(Cylinder)
    compound = geompy.MakeCompound(groupL)
    compoundS = geompy.MakeCompound(groupS)
    if Solid == False:
        beams = geompy.addToStudy( compound, 'Beams' )
        gg.createAndDisplayGO(beams)
    else:
        beamsS = geompy.addToStudy( compoundS, 'BeamsS' )
        gg.createAndDisplayGO(beamsS)
else:
    print "The groups no same number of elements"


#Cylinder_1 = geompy.MakeCylinder(O, OZ, 100, 300)

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(1)
  salome.sg.UpdateView()





