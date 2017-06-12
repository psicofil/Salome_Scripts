# -*- coding: utf-8 -*-
# Mesh with GMSH inside of Salome
# License: LGPL v 2.1
# Version: 14/04/2017

# CONFIGURATION - EDIT THE FOLLOWING LINE TO MATCH YOUR GMSH BINARY
gmsh_bin_linux = "/usr/bin/gmsh"
gmsh_bin_windwos = "C:\\Daten\\gmsh-2.10.0-Windows\\gmsh.exe"
gmsh_bin_other = "/usr/bin/gmsh"

# CONFIGURATION - Interactive console
xterm_bin_linux = '/usr/bin/xterm -e '

# END CONFIGURATION

# START OF MACRO
import sys
import salome
from platform import system
import subprocess
import tempfile
try:
    from PyQt4 import QtGui,QtCore
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *
except:
    from PyQt5.QtWidgets import QWidget
    from PyQt5 import QtCore, QtGui
    import PyQt5.QtCore as QtCore
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import Qt

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS
import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

theStudy = salome.myStudy
geompy = geomBuilder.New(theStudy)
salome.salome_init()


if system() == "Linux":
    gmsh_bin = gmsh_bin_linux
    path_sep = "/"
elif system() == "Windows":
    gmsh_bin = gmsh_bin_windwos
    path_sep = "\\"
else:
    gmsh_bin = gmsh_bin_other
    path_sep = "/"

class MeshGmsh(QWidget):
    def __init__(self):
        super(MeshGmsh, self).__init__()
        self.initUI()
    def __del__(self):
        return
    def initUI(self):
        # Mesh dimension
        self.rb_1D = QRadioButton("   1D", self)
        self.rb_2D = QRadioButton("   2D", self)
        self.rb_3D = QRadioButton("   3D", self)
        self.rb_3D.setChecked(Qt.Checked)
        # Optimized:
        self.cb_optimized = QCheckBox("    Optimized", self)
        self.cb_optimized.setChecked(Qt.Checked)
        # Algorithm:
        self.l_algorithm = QLabel("Algorithm ", self)
        self.cmb_algorithm = QComboBox(self)
        self.algorithm_list = [self.tr('iso'), self.tr('netgen'), self.tr('front2d'), self.tr('meshadapt'), self.tr('delquad'), self.tr('del3d'), self.tr('del2d'), self.tr('front3d'), self.tr('mmg3d'), self.tr('pack'), self.tr('tetgen'),]
        self.cmb_algorithm.addItems(self.algorithm_list)
        self.cmb_algorithm.setCurrentIndex(1)
        # Element max size:
        self.cb_max_elme_size = QCheckBox("  Set maximum mesh element size",self)
        self.cb_max_elme_size.setChecked(Qt.Checked)
        self.sb_max_element_size = QDoubleSpinBox(self)
        self.sb_max_element_size.setValue(20.0)
        self.sb_max_element_size.setMaximum(10000000.0)
        self.sb_max_element_size.setMinimum(0.00000001)
        # Element min size:
        self.cb_min_elme_size = QCheckBox("  Set minimum mesh element size",self)
        self.sb_min_element_size = QDoubleSpinBox(self)
        self.sb_min_element_size.setValue(5.0)
        self.sb_min_element_size.setMaximum(10000000.0)
        self.sb_min_element_size.setMinimum(0.00000001)
        self.sb_min_element_size.setEnabled(False)
        # Set Mesh Order:
        self.cb_mesh_order = QCheckBox("  mesh order",self)
        self.sb_mesh_order = QSpinBox(self)
        self.sb_mesh_order.setValue(2)
        self.sb_mesh_order.setMaximum(5)
        self.sb_mesh_order.setMinimum(1)
        # Interactive Follow up:
        self.cb_interact = QCheckBox("    Interactive Follow up", self)
        self.cb_interact.setChecked(Qt.Checked)
        # Other gmsh commands:
        self.l_cmd_line_opt = QLabel("Custom gmsh options ", self)
        self.le_cmd_line_opt = QLineEdit(self)
        self.le_cmd_line_opt.setToolTip("Those option will be appended to gmsh command line call")
        # Ok buttons:
        self.okbox = QDialogButtonBox(self)
        self.okbox.setOrientation(Qt.Horizontal)
        self.okbox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        # Web button
        self.pb_web = QPushButton(self)
        self.pb_web.setText("gmsh options (web)")
        # Layout:
        layout = QGridLayout()
        layout.addWidget(self.rb_1D, 1, 0)
        layout.addWidget(self.rb_2D, 1, 1)
        layout.addWidget(self.rb_3D, 2, 0)
        layout.addWidget(self.cb_optimized, 2, 1)
        layout.addWidget(self.l_algorithm, 3, 0)
        layout.addWidget(self.cmb_algorithm, 3, 1)
        layout.addWidget(self.cb_max_elme_size, 4, 0)
        layout.addWidget(self.sb_max_element_size, 4, 1)
        layout.addWidget(self.cb_min_elme_size, 5, 0)
        layout.addWidget(self.sb_min_element_size, 5, 1)
        layout.addWidget(self.cb_mesh_order, 6, 0)
        layout.addWidget(self.sb_mesh_order, 6, 1)
        layout.addWidget(self.cb_interact, 7, 1)
        layout.addWidget(self.l_cmd_line_opt, 8, 0)
        layout.addWidget(self.le_cmd_line_opt, 8, 1)
        layout.addWidget(self.pb_web, 9, 0)
        layout.addWidget(self.okbox, 9, 1)
        self.setLayout(layout)
        # Connectors:
        self.okbox.accepted.connect(self.proceed)
        self.okbox.rejected.connect(self.cancel)
        self.pb_web.clicked.connect(self.open_gmsh_options)
        self.cb_max_elme_size.stateChanged.connect(self.max_size_state)
        self.cb_min_elme_size.stateChanged.connect(self.min_size_state)
        self.cb_mesh_order.stateChanged.connect(self.mesh_order_state)
        
    def max_size_state(self, state):   
        if state == Qt.Checked:
            self.sb_max_element_size.setEnabled(True)
        else:
            self.sb_max_element_size.setEnabled(False)
            
    def min_size_state(self, state):
        if state == Qt.Checked:
            self.sb_min_element_size.setEnabled(True)
        else:
            self.sb_min_element_size.setEnabled(False)
            
    def mesh_order_state(self, state):   
        if state == Qt.Checked:
            self.sb_mesh_order.setEnabled(True)
        else:
            self.sb_mesh_order.setEnabled(False)
            
    def open_gmsh_options(self):
        import webbrowser
        webbrowser.open('http://www.geuz.org/gmsh/doc/texinfo/gmsh.html#Command_002dline-options')
        
    def cancel(self):
        self.close()
        d.close()
    
    def proceed(self):
        temp_file = tempfile.mkstemp(suffix='.brep')[1]
        selected = salome.sg.getSelected(0)
        selection = salome.myStudy.FindObjectID(selected).GetObject()
        if not selection:
            QMessageBox.critical(None, "GMSHMesh macro", "An object has to be selected to run gmsh!")
        ## Export a part in step format
        geompy.ExportBREP(selection, temp_file)
        selection_name = selection.GetName()
        ## Mesh temporaly file
        file_format = 'med'
        temp_mesh_file = tempfile.tempdir + path_sep + selection_name + '_Mesh.' + file_format
        ## OPTIONS GMSH:
        clmax = self.sb_max_element_size.text()
        clmin = self.sb_min_element_size.text()
        cmd_line_opt = self.le_cmd_line_opt.text()
        algo = self.cmb_algorithm.currentText()
        mesh_order = self.sb_mesh_order.text()
        if self.cb_optimized.isChecked():
            cmd_optimize = ' -optimize'
        else:
            cmd_optimize = ''
        if self.rb_3D.isChecked():
	    dim = ' -3 '
        if self.rb_2D.isChecked():
	    dim = ' -2 '
        if self.rb_1D.isChecked():
	    dim = ' -1 '
	if self.cb_max_elme_size.isChecked():
	  max_size = ' -clmax ' + clmax
        else:
            max_size = ''
        if self.cb_min_elme_size.isChecked():
            min_size = ' -clmin ' + clmin
        else:
            min_size = ''
        if self.cb_mesh_order.isChecked():
            order = ' -order ' + mesh_order
        else:
            order = ''
        options = ' -algo ' + algo + max_size + min_size + cmd_optimize + order + cmd_line_opt
        # RUN GMSH
        command = gmsh_bin + ' ' + temp_file + dim + '-format ' + file_format + ' -o ' + temp_mesh_file  + '' + options
        try:
            if system() == "Linux":
	        if self.cb_interact.isChecked():
		  output = subprocess.check_output([xterm_bin_linux + command, '-1'], shell=True, stderr=subprocess.STDOUT,)
		else:
		  output = subprocess.check_output([command, '-1'], shell=True, stderr=subprocess.STDOUT,)
            elif system() == "Windows":
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT,)
            else:
                output = subprocess.check_output([command, '-1'], shell=True, stderr=subprocess.STDOUT,)
            smesh = smeshBuilder.New(theStudy)
            ([Mesh_1], status) = smesh.CreateMeshesFromMED(temp_mesh_file)
            smesh.SetName(Mesh_1.GetMesh(),selection_name)
            if salome.sg.hasDesktop():
                salome.sg.updateObjBrowser(1)
            #self.close()
            #d.close()
            print "Succefull"
        except:
            QMessageBox.critical(None, "GMSHMesh macro", "Unexpected error in GMSHMesh macro!")
        finally:
            try:
                del temp_file
            except:
		pass
            try:
                del temp_mesh_file
            except:
                pass



d = QDockWidget()
d.setWidget(MeshGmsh())
d.toggleViewAction().setText("Gmsh")
d.setAttribute(Qt.WA_DeleteOnClose)
d.setWindowTitle(" GMSH Mesh Generator ")
d.setGeometry(600, 300, 400, 600)
d.show()

# END OF MACRO
