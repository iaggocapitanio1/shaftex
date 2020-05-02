"""
@Description:
The main aim of this class allows to bind the main window widget with the chart widgets
"""
__author__ = "Iaggo Capitanio"
__copyright__ = "Copyright (C) 2020 Iaggo Capitanio"
__license__ = "Public Domain"
__version__ = "1.0"




from PyQt5 import QtCore, QtGui, QtWidgets
import ctypes
from Shafton.matplotlibChartDeflection import DynamicMplCanvasDeflection
from Shafton.beamSolver import BeamSolver
from shaft import Shaft
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import source_images

myAppId = u'ShaftExploration.Shaftex.version-1.0'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppId)


class DeflectionDialog(QtWidgets.QDialog):
    """
    The aim of this class is to build and dialog and host a chart!
    """
    def __init__(self, beam_var: BeamSolver, shaft_var: Shaft) -> None:
        super(DeflectionDialog, self).__init__()
        self.iconPath = ":icons/shaftex.ico"
        self.beam = beam_var
        self.shaft = shaft_var
        self.canvasQtWidget = DynamicMplCanvasDeflection(
            domain=self.beam.getPlotDeflection(second_moment_of_area=self.shaft.getSecondMomentOfArea())['x'],
            XY=self.beam.getPlotDeflection(second_moment_of_area=self.shaft.getSecondMomentOfArea())['XY'],
            XZ=self.beam.getPlotDeflection(second_moment_of_area=self.shaft.getSecondMomentOfArea())['XZ'],
            TOTAL=self.beam.getPlotDeflection(second_moment_of_area=self.shaft.getSecondMomentOfArea())["TOTAL"])
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint)
        self.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.setSizeGripEnabled(True)
        self.resize(1400, 700)
        self.setWindowIcon(QtGui.QIcon(self.iconPath))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self)
        self.deflection_verticalLayout = QtWidgets.QVBoxLayout()
        self.toolBar = NavigationToolbar(self.canvasQtWidget, self)
        self.deflection_verticalLayout.addWidget(self.toolBar)
        self.deflection_verticalLayout.addWidget(self.canvasQtWidget)
        self.verticalLayout_2.addLayout(self.deflection_verticalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.verticalLayout_2.addWidget(self.buttonBox)
        self.setName()
        self.retranslate()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)



    def setName(self) -> None:
        """
        The aim of this class is to build and dialog and host a chart!
        :return: None.
        """
        self.setObjectName("deflectionDialog")
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.deflection_verticalLayout.setObjectName("deflection_verticalLayout")
        self.buttonBox.setObjectName("buttonBox")

    def retranslate(self) -> None:
        """
        :return: None.
        """
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("deflectionDialog", "Shaftex - Slope Chart"))


