import salome
salome.salome_init()
import GEOM
from salome.geom import geomBuilder
geompy = geomBuilder.New(salome.myStudy)
gg = salome.ImportComponentGUI("GEOM")
import math
salome.salome_init()
theStudy = salome.myStudy
import salome_notebook
notebook = salome_notebook.NoteBook(theStudy)

selCount = salome.sg.SelectedCount()

#def_coef = 0.0001

gap = 0

Common = True

#selCount

for i in range(0, selCount):
  for j in range(0, selCount):
    if i != j and i < j:
      sel_i=salome.sg.getSelected(i)
      selobj_i=salome.myStudy.FindObjectID(sel_i).GetObject()
      sel_j=salome.sg.getSelected(j)
      selobj_j=salome.myStudy.FindObjectID(sel_j).GetObject()
      isOk, res1, res2 = geompy.FastIntersect(selobj_i, selobj_j, gap)
      if isOk > 0:
	N_C = len(res1)
	N_C2 = len(res2)
	CONT  = geompy.SubShapes(selobj_i, res1)
	CONT2 = geompy.SubShapes(selobj_j, res2)
	cont_sf_i = list()
	cont_sf_j = list()
	for h in range(0, N_C):
            for k in range(0, N_C2):
              common1 = geompy.MakeCommon(CONT[h], CONT2[k])
	      props = geompy.BasicProperties(common1)
	      area_com = props[1]
	      if Common == False:
                  if area_com > 0.0:
                      name_group_i = 'CZ_' + str(i) + str(j) + '_' + str(k)
                      geompy.addToStudyInFather( selobj_i, CONT[h], name_group_i )
                      name_group_j = 'CZ_' + str(j) + str(i) + '_' + str(h)
                      geompy.addToStudyInFather( selobj_j, CONT2[k], name_group_j )
	      if Common == True:
                  if area_com > 0.0:
                      cont_sf_i.append(CONT[h])
                      cont_sf_j.append(CONT2[k])
                      comp_sf_i = geompy.MakeCompound(cont_sf_i)
                      name_group_i = 'CZ_' + str(i) + str(j)
                      geompy.addToStudyInFather( selobj_i, comp_sf_i, name_group_i )
                      comp_sf_j = geompy.MakeCompound(cont_sf_j)
                      name_group_j = 'CZ_' + str(j) + str(i)
                      geompy.addToStudyInFather( selobj_j, comp_sf_j, name_group_j )
	    


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(1)




#for i in range(0, selCount):
  #for j in range(0, selCount):
    #if i != j:
      #sel_i=salome.sg.getSelected(i)
      #selobj_i=salome.myStudy.FindObjectID(sel_i).GetObject()
      #sel_j=salome.sg.getSelected(j)
      #selobj_j=salome.myStudy.FindObjectID(sel_j).GetObject()
      #isOk, res1, res2 = geompy.FastIntersect(selobj_i, selobj_j, gap)
      #if isOk > 0:
	#N_C = len(res1)
	#N_C2 = len(res2)
	#CONT  = geompy.SubShapes(selobj_i, res1)
	#CONT2 = geompy.SubShapes(selobj_j, res2)
	#cont_sf_i = list()
	#for h in range(0, N_C):
            #for k in range(0, N_C2):
              #common1 = geompy.MakeCommon(CONT[h], CONT2[k])
	      #props = geompy.BasicProperties(common1)
	      #area_com = props[1]
	      #if Common == False:
                  #if area_com > 0:
                      #name_group_i = 'CZ_' + str(i) + str(j) + '_' + str(k)
                      #geompy.addToStudyInFather( selobj_i, CONT[h], name_group_i )
	      #if Common == True:
                  #if area_com > 0:
                      #cont_sf_i.append(CONT[h])
        #if Common == True:
            #comp_sf_i = geompy.MakeCompound(cont_sf_i)
            #name_group_i = 'CZ_' + str(i) + str(j)
            #geompy.addToStudyInFather( selobj_i, comp_sf_i, name_group_i )
	    


#if salome.sg.hasDesktop():
  #salome.sg.updateObjBrowser(1)


