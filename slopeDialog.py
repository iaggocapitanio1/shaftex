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
from Shafton.matplotlibChartSlope import DynamicMplCanvasSlope
from Shafton.beamSolver import BeamSolver
from shaft import Shaft
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

myAppId = u'ShaftExploration.Shaftex.version-1.0'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppId)


class SlopeDialog(QtWidgets.QDialog):
    """
    The aim of this class is to build and dialog and host a chart!
    """
    def __init__(self, beam_var: BeamSolver, shaft_var: Shaft) -> None:
        super(SlopeDialog, self).__init__()
        self.iconPath = ":icons/shaftex.ico"
        self.beam = beam_var
        self.shaft = shaft_var
        self.canvasQtWidget = DynamicMplCanvasSlope(
            domain=self.beam.getPlotSlope(second_moment_of_area=self.shaft.getSecondMomentOfArea())['x'],
            XY=self.beam.getPlotSlope(second_moment_of_area=self.shaft.getSecondMomentOfArea())['XY'],
            XZ=self.beam.getPlotSlope(second_moment_of_area=self.shaft.getSecondMomentOfArea())['XZ']
            )
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


if __name__ == "__main__":
    import sys
    from Shafton.TESTE05 import beam, shaft
    app = QtWidgets.QApplication(sys.argv)
    ui = SlopeDialog(beam, shaft)
    ui.show()
    sys.exit(app.exec_())
