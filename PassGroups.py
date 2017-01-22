###### Pass groups from objects ###

# Import the necessary
import salome
salome.salome_init()
import GEOM
from salome.geom import geomBuilder
geompy = geomBuilder.New(salome.myStudy)

# Number selected objects
selCount = salome.sg.SelectedCount()

# Reference object and its groups
selected = salome.sg.getSelected(0) # First selection
selobj = salome.myStudy.FindObjectID(selected).GetObject() # Reference object
SubObjsAll = geompy.GetGroups(selobj) # Groups of Reference
n_groups = len(SubObjsAll) # Number of groups

# Objetive object
selec_obj = salome.sg.getSelected(1) # Second selection
Objetive = salome.myStudy.FindObjectID(selec_obj).GetObject() # Objetive object

# Proceed if are two objects selected
if selCount == 2:
    for i in range(0,n_groups):
        group_p = SubObjsAll[i]
        name_g = group_p.GetName()
        type_g = str(group_p.GetShapeType())
        props = geompy.BasicProperties(group_p)
        if type_g == "COMPOUND":
            if props[2]==0:
                type_g = "FACE"
            if props[1]==0:
                type_g = "EDGE"
            if props[2]>0:
                type_g = "SOLID"
        elements = geompy.ExtractShapes(group_p, geompy.ShapeType[type_g], True)
        Group_ob = geompy.CreateGroup(Objetive, geompy.ShapeType[type_g])
        try:
            if len(elements) > 1:
                for elem in elements:
                    group_pass = geompy.GetSame(Objetive, elem)
                    Element_ID = geompy.GetSubShapeID(Objetive, group_pass)
                    geompy.AddObject(Group_ob, Element_ID)
                geompy.addToStudyInFather(Objetive, Group_ob, name_g)
            else:
                group_pass = geompy.GetSame(Objetive, group_p)
                Element_ID = geompy.GetSubShapeID(Objetive, group_pass)
                geompy.AddObject(Group_ob, Element_ID)
                geompy.addToStudyInFather( Objetive, Group_ob, name_g )
        except:
            print "error con" + name_g
else:
    print "Only select two objects"


if salome.sg.hasDesktop():
    salome.sg.updateObjBrowser(1)

