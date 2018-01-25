# -*- coding: utf-8 -*-


External_Volume_Result = True

# Import the necessary
import salome
salome.salome_init()
import GEOM
from salome.geom import geomBuilder
geompy = geomBuilder.New(salome.myStudy)

# Number selected objects
selCount = salome.sg.SelectedCount()

# Solid
selected = salome.sg.getSelected(0) # First selection
selobj = salome.myStudy.FindObjectID(selected).GetObject() # Reference object

# Internal Face
selected2 = salome.sg.getSelected(1) # Second selection
selobj2 = salome.myStudy.FindObjectID(selected2).GetObject() # Objetive object


RemoveIntWires_1 = geompy.SuppressInternalWires(selobj, [])
SuppressHoles_1 = geompy.SuppressHoles(RemoveIntWires_1, [])
list_shell = geompy.ExtractShapes(SuppressHoles_1, geompy.ShapeType["SHELL"], True)
n_shells = len(list_shell)

if selCount == 2:
  for i in range(0,n_shells):
    isOk, res1, res2 = geompy.FastIntersect(list_shell[i], selobj2, 0)
    if isOk > 0:
      common1 = geompy.MakeCommon(selobj2, list_shell[i])
      props = geompy.BasicProperties(common1)
      area_com = props[1]
      if area_com > 0:
	if External_Volume_Result == True:
	  volume = geompy.MakeCompound([list_shell[i]])
	  geompy.addToStudy( volume, 'InternalVolume' )
	  gg = salome.ImportComponentGUI("GEOM")
          volume.SetColor(SALOMEDS.Color(1,0,0))
	else:
	  Group_ob = geompy.CreateGroup(selobj, geompy.ShapeType["FACE"])
	  list_faces = geompy.ExtractShapes(list_shell[i], geompy.ShapeType["FACE"], True)
	  nlist = len(list_faces)
	  for i in range(0,nlist):
	    try:
	      ID = geompy.GetSubShapeID(selobj, list_faces[i])
	      geompy.AddObject(Group_ob, ID)
            except:
	      pass
	  resGroup = geompy.addToStudyInFather(selobj, Group_ob, 'InternalSurface')
          gg = salome.ImportComponentGUI("GEOM")
          gg.setColor(resGroup,255,0,0)
          gg.createAndDisplayGO(resGroup)

if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(True)
  


  
  


