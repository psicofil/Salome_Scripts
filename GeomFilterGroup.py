# Create groups form filters

import salome
salome.salome_init()
import GEOM
from salome.geom import geomBuilder
geompy = geomBuilder.New(salome.myStudy)
import math
from PyQt4 import QtGui,QtCore
import SALOMEDS


###### PROCEED ######

# Selected Object
def selectGroupRef():
    try:
        # selected Object
        selected=salome.sg.getSelected(0)
        selobjID=salome.myStudy.FindObjectID(selected)
        selobj=selobjID.GetObject()
        type_o = str(selobj.GetShapeType())
        # Set object Name
        le_ref_g.setText(selobj.GetName())
        # Set normal availble
        if type_o=='FACE':
            cb_norm.setEnabled(True)
        else:
            cb_norm.setEnabled(False)
    except:
        selobj = None
    return selobj


# Run proceed
def proceed():
    try:
        # selected Object
        selobj=selectGroupRef()
        # Is a group?
        isgroup = geompy.ShapeIdToType(selobj.GetType()) == 'GROUP'
        # The father of group
        father = geompy.GetMainShape(selobj)
        # Type of element
        elem = str(selobj.GetShapeType())
        # Size
        props = geompy.BasicProperties(selobj)
        if elem=="EDGE":
            Sref = props[0]
        if elem=="FACE":
            Sref = props[1]
        if elem=="SOLID":
            Sref = props[2]
        # Location
        cm_ref = geompy.MakeCDG(selobj)
        coords_ref = geompy.PointCoordinates(cm_ref)
        # Normal (Element==Face)
        if elem=="FACE":
            vnorm_ref = geompy.GetNormal(selobj)
        else:
            vnorm_ref = None
        # Create container group
        group=list()
        # All Object elements of type elem
        elements = geompy.ExtractShapes(father, geompy.ShapeType[elem], True)
        # Create group
        Group_f = geompy.CreateGroup(father, geompy.ShapeType[elem])
        # Options
        name_g = str(le_nam_g.text())
        pr = eval(str(sb_tol.text()))
    except:
        QtGui.QMessageBox.critical(None,'Error',"error 1",QtGui.QMessageBox.Abort)
    try:
        # Selected elements for the group whit the desired conditios
        for i in elements:
            props = geompy.BasicProperties(i)
            cm = geompy.MakeCDG(i)
            coords = geompy.PointCoordinates(cm)
            # Element i coordinates
            x = coords[0]
            y = coords[1]
            z = coords[2]
            # Element i size
            if elem=="EDGE":
                S = props[0]
            if elem=="FACE":
                S = props[1]
            if elem=="SOLID":
                S = props[2]
            # Element==Face i Normal
            if vnorm_ref==None:
                vnorm=None
            else:
                vnorm = geompy.GetNormal(i)
                angle = geompy.GetAngle(vnorm_ref, vnorm)
            # Comparations
            cond = list()
            if cb_size.isChecked():
                cond.append(S<Sref*(1+pr) and S>Sref*(1-pr))
            else:
                cond.append(True)
            if cb_locx.isChecked():
                if coords_ref[0]>=0:
                    cond.append(x<coords_ref[0]*(1+pr) and x>coords_ref[0]*(1-pr))
                else:
                    cond.append(x>coords_ref[0]*(1+pr) and x<coords_ref[0]*(1-pr))
            else:
                cond.append(True)
            if cb_locy.isChecked():
                if coords_ref[1]>=0:
                    cond.append(y<coords_ref[1]*(1+pr) and y>coords_ref[1]*(1-pr))
                else:
                    cond.append(y>coords_ref[1]*(1+pr) and y<coords_ref[1]*(1-pr))
            else:
                cond.append(True)
            if cb_locz.isChecked():
                if coords_ref[2]>=0:
                    cond.append(z<coords_ref[2]*(1+pr) and z>coords_ref[2]*(1-pr))
                else:
                    cond.append(z>coords_ref[2]*(1+pr) and z<coords_ref[2]*(1-pr))
            else:
                cond.append(True)
            if  cb_norm.isChecked() and vnorm != None:
                cond.append(angle<0.0+0.001 and angle>0.0-0.001)
            else:
                cond.append(True)
            if cond[0] and cond[1] and cond[2] and cond[3] and cond[4]:
                ID = geompy.GetSubShapeID(father,i)
                group.append(ID)
                cond.append(cond)
    except:
        QtGui.QMessageBox.critical(None,'Error',"error 2",QtGui.QMessageBox.Abort)
    # Add elements desired to Group
    try:
        geompy.UnionIDs(Group_f, group)
        # Set color of the group
        Group_f.SetColor(SALOMEDS.Color(1,0,0))
        # Add group in hte gui
        resGroup = geompy.addToStudyInFather(father, Group_f, name_g)
        # View group
        gg = salome.ImportComponentGUI("GEOM")
        gg.createAndDisplayGO(resGroup)
        # Update Object Browser
        if salome.sg.hasDesktop():
            salome.sg.updateObjBrowser(1)
    except:
        QtGui.QMessageBox.critical(None,'Error',"error 3",QtGui.QMessageBox.Abort)
    return 0.0


def hide():
    dialog.hide()


### GUI APLIACTION ###
dialog = QtGui.QDialog()
dialog.resize(400,300)
dialog.setWindowTitle("Create Group for same criteriums")
dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
# Options
l_ref_g  = QtGui.QLabel("Reference Group:")
pb_ref_g = QtGui.QPushButton()
pb_ref_g.setText("Select")
le_ref_g = QtGui.QLineEdit()
l_nam_g  = QtGui.QLabel("Name result Group:")
le_nam_g = QtGui.QLineEdit()
le_nam_g.setText("Group_R")
l_crit   = QtGui.QLabel("Criteriums")
cb_size  = QtGui.QCheckBox("Size")
cb_size.setChecked(QtCore.Qt.Checked)
cb_locx  = QtGui.QCheckBox("Location X")
cb_locy  = QtGui.QCheckBox("Location Y")
cb_locz  = QtGui.QCheckBox("Location Z")
cb_norm  = QtGui.QCheckBox("Normal")
cb_norm.setEnabled(False)
l_tol    = QtGui.QLabel("% Tolerance:")
sb_tol   = QtGui.QDoubleSpinBox()
sb_tol.setValue(0.01)
sb_tol.setMaximum(1.00)
sb_tol.setMinimum(0.01)
okbox = QtGui.QDialogButtonBox(dialog)
okbox.setOrientation(QtCore.Qt.Horizontal)
okbox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
# Call selectGroupRef function
selectGroupRef()
# Layout
layout = QtGui.QGridLayout(dialog)
layout.addWidget(l_ref_g,1,0)
layout.addWidget(pb_ref_g,2,0)
layout.addWidget(le_ref_g,2,1)
layout.addWidget(l_nam_g,3,0)
layout.addWidget(le_nam_g,3,1)
layout.addWidget(l_crit,4,0)
layout.addWidget(cb_size,5,1)
layout.addWidget(cb_locx,6,1)
layout.addWidget(cb_locy,7,1)
layout.addWidget(cb_locz,8,1)
layout.addWidget(cb_norm,9,1)
layout.addWidget(l_tol,10,0)
layout.addWidget(sb_tol,11,1)
layout.addWidget(okbox,12,1)
dialog.setLayout(layout)
# Conectios
pb_ref_g.clicked.connect(selectGroupRef)
QtCore.QObject.connect(okbox, QtCore.SIGNAL("accepted()"), proceed)
QtCore.QObject.connect(okbox, QtCore.SIGNAL("rejected()"), hide) 
QtCore.QMetaObject.connectSlotsByName(dialog)

# Dialog show
dialog.show()


