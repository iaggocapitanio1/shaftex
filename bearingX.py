"""
@Description:
User Interface Dialog
"""
__author__ = "Iaggo Capitanio"
__copyright__ = "Copyright (C) 2020 Iaggo Capitanio"
__license__ = "Public Domain"
__version__ = "1.0"


from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from win32api import GetSystemMetrics
import ctypes
import source_images

myAppId = u'ShaftExploration.Shaftex.version-1.0'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppId)

class BearingDialog(QtWidgets.QDialog):
    """
    This class will provide the Dialog Window to insert the eternal Forces:
    """
    def __init__(self, *args, **kwargs):
        super(BearingDialog, self).__init__(*args, **kwargs)
        self.iconPath = ":icons/shaftex.ico"
        self.setStyleSheet("QDialog {background-color: #f2f2f2}")
        self.ScreenWidth = GetSystemMetrics(0)
        self.ScreenHeight = GetSystemMetrics(1)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint)
        self.windowHeight = 120
        self.windowWidth = 350
        self.setMaximumHeight(self.windowHeight)
        self.setMinimumHeight(self.windowHeight)
        self.setMaximumWidth(self.windowWidth)
        self.setMaximumWidth(self.windowWidth)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.bearingFormLayout = QtWidgets.QFormLayout()
        self.bearingFirstBearingPositionLabel = QtWidgets.QLabel(self)
        self.bearingFirstBearingPositionDoubleSpinBox = QtWidgets.QDoubleSpinBox(self)
        self.bearingSecondBearingPositionLabel = QtWidgets.QLabel(self)
        self.bearingSecondBearingPositionDoubleSpinBox = QtWidgets.QDoubleSpinBox(self)
        self.bearingbuttonBox = QtWidgets.QDialogButtonBox(self)
        self.bearingbuttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.font = QtGui.QFont()
        self.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.setSizeGripEnabled(True)
        self.setUpWindow()
        self.bearingbuttonBox.accepted.connect(self.accept)
        self.bearingbuttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)

    def frontLayout(self) -> None:
        """
        This function build up the unique program interface.
        :return: None
        """
        self.bearingFormLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.bearingFirstBearingPositionLabel)
        self.bearingFirstBearingPositionDoubleSpinBox.setRange(0, 1e9)
        self.bearingFirstBearingPositionDoubleSpinBox.setDecimals(2)
        self.bearingFirstBearingPositionDoubleSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.bearingFormLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole,
                                         self.bearingFirstBearingPositionDoubleSpinBox)
        self.bearingFormLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole,
                                         self.bearingSecondBearingPositionLabel)

        self.bearingSecondBearingPositionDoubleSpinBox.setRange(0, 1e9)
        self.bearingSecondBearingPositionDoubleSpinBox.setDecimals(2)
        self.bearingSecondBearingPositionDoubleSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.bearingFormLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole,
                                         self.bearingSecondBearingPositionDoubleSpinBox)
        self.verticalLayout.addLayout(self.bearingFormLayout)


    def retranslateUi(self):
        """
        This function translate the name of the object with your value.
        :return: None
        """
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.bearingFirstBearingPositionLabel.setText(_translate("Dialog", "First Bearing Position [mm]"))
        self.bearingSecondBearingPositionLabel.setText(_translate("Dialog", "Second Bearing Position [mm]"))

    def setUpName(self):
        """
        This function will set up the name of some objects.
        """
        self.verticalLayout.setObjectName("verticalLayout")
        self.bearingFormLayout.setObjectName("bearingFormLayout")
        self.bearingFirstBearingPositionLabel.setObjectName("bearingFirstBearingPositionLabel")
        self.bearingFirstBearingPositionDoubleSpinBox.setObjectName("bearingFirstBearingPositionDoubleSpinBox")
        self.bearingSecondBearingPositionLabel.setObjectName("bearingSecondBearingPositionLabel")
        self.bearingSecondBearingPositionDoubleSpinBox.setObjectName("bearingSecondBearingPositionDoubleSpinBox")
        self.bearingbuttonBox.setObjectName("bearingbuttonBox")

    def setUpIcon(self):
        """
        This function provides the first two check box of the dialog window.
        :return: None
        """
        icon = QtGui.QIcon(self.iconPath)
        self.setWindowIcon(icon)

    def setUpFont(self):
        """
        This function will set up the font to be used in the dialog window.
        :return: None
        """
        self.font.setFamily("Segoe UI")

    def setUpButtonBoxDialog(self):
        """
        This function sets the button box of the dialog window.
        :return: None
        """
        self.bearingbuttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.bearingbuttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.bearingbuttonBox)

    def setUpWindow(self):
        """
        :rtype: None
        """

        self.setGeometry(self.ScreenWidth / 2 - self.windowWidth / 2, self.ScreenHeight / 2 - self.windowHeight / 2,
                         self.windowWidth, self.windowHeight)
        self.setUpFont()
        self.setUpName()
        self.frontLayout()
        self.retranslateUi()
        self.setUpButtonBoxDialog()
        self.setUpIcon()
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("DialogExternalForces", "Shaftex-Bearing"))
        self.setToolTip(_translate("DialogExternalForces", "<html><head/><body><p>This window allows the user to"
                                                           " insert external forces acting on "
                                                           "the shaft</p></body></html>"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = BearingDialog()
    dialog.show()
    sys.exit(app.exec_())
