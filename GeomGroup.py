import sys
import salome

salome.salome_init()
theStudy = salome.myStudy
import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS
import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder
smesh = smeshBuilder.New(theStudy)

# Number selected objects
selCount = salome.sg.SelectedCount()
# Mesh selection
selected = salome.sg.getSelected(0)
Mesh_1 = salome.myStudy.FindObjectID(selected).GetObject()

# Proceed if are two objects selected
for i in range(1,selCount):
  try:
    selected_i = salome.sg.getSelected(i)
    selobj_i = salome.myStudy.FindObjectID(selected_i).GetObject()
    name_geom_group = selobj_i.GetName()
    elem = str(selobj_i.GetMaxShapeType())
    if elem == "FACE":
      type_g = SMESH.FACE
    if elem == "EDGE":
      type_g = SMESH.EDGE
    if elem == "SOLID":
      type_g = SMESH.VOLUME
    # Criterios
    aCriteria = []
    aCriterion1 = smesh.GetCriterion(type_g,SMESH.FT_BelongToGeom,SMESH.FT_Undefined,name_geom_group)
    aCriteria.append(aCriterion1)
    aFilter_1 = smesh.GetFilterFromCriteria(aCriteria)
    aFilter_1.SetMesh(Mesh_1.GetMesh())
    Group_1 = Mesh_1.CreateGroupFromFilter( type_g, name_geom_group, aFilter_1 )
    smesh.SetName(Group_1, name_geom_group)
  except:
    print "Error"
    print "Error con el grupo" + name_geom_group


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(1)
  



