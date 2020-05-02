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
from PyQt5.QtCore import Qt
from win32api import GetSystemMetrics
import ctypes
import source_images

myAppId = u'ShaftExploration.Shaftex.version-1.0'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppId)


class DialogFx(QtWidgets.QDialog):
    """
    This class will provide the Dialog Window to insert the eternal Forces:
    """

    def __init__(self, *args, **kwargs) -> None:
        super(DialogFx, self).__init__(*args, **kwargs)
        self.iconPath = ":icons/shaftex.ico"
        self.fontForm = QtGui.QFont()
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.dialogVerticalLayout = QtWidgets.QVBoxLayout()
        self.gearPulleyEngineHorizontalLayout = QtWidgets.QHBoxLayout()
        self.engineCheckBox = QtWidgets.QCheckBox(self)
        self.gearCheckBox = QtWidgets.QCheckBox(self)
        self.pulleyCheckBox = QtWidgets.QCheckBox(self)
        self.basicFormLayout = QtWidgets.QFormLayout()
        self.radiusLabel = QtWidgets.QLabel(self)
        self.radiusDoubleSpinBox = QtWidgets.QDoubleSpinBox(self)
        self.radiusDoubleSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.xPositionLabel = QtWidgets.QLabel(self)
        self.xPositionDoubleSpinBox = QtWidgets.QDoubleSpinBox(self)
        self.xPositionDoubleSpinBox.setRange(0, 1e9)
        self.xPositionDoubleSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.angleObliquityAngle = QtWidgets.QLabel(self)
        self.angleObliquityDoubleSpinBox = QtWidgets.QDoubleSpinBox(self)
        self.angleObliquityDoubleSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.torqueLabel = QtWidgets.QLabel(self)
        self.torqueDoubleSpinBox = QtWidgets.QDoubleSpinBox(self)
        self.torqueDoubleSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.AutomaticallyInsertCheckBox = QtWidgets.QCheckBox(self)
        self.automaticallyInsertFormLayout = QtWidgets.QFormLayout()
        self.powerCheckBox = QtWidgets.QCheckBox(self)
        self.powerDoubleSpinBox = QtWidgets.QDoubleSpinBox(self)
        self.powerDoubleSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.rpmLabel = QtWidgets.QLabel(self)
        self.rpmDoubleSpinBox = QtWidgets.QDoubleSpinBox(self)
        self.rpmDoubleSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.radialForceLabel = QtWidgets.QLabel(self)
        self.radialForceDoubleSpinBox = QtWidgets.QDoubleSpinBox(self)
        self.radialForceDoubleSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.tangentialForceLabel = QtWidgets.QLabel(self)
        self.tangentialForcedoubleSpinBox = QtWidgets.QDoubleSpinBox(self)
        self.tangentialForcedoubleSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.vectorsCheckBox = QtWidgets.QCheckBox(self)
        self.ManuallyInsertCheckBox = QtWidgets.QCheckBox(self)
        self.manuallyInsertFormLayout = QtWidgets.QFormLayout()
        self.Ta_Label = QtWidgets.QLabel(self)
        self.Ta_DoubleSpinBox = QtWidgets.QDoubleSpinBox(self)
        self.Ta_DoubleSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.Mm_Label = QtWidgets.QLabel(self)
        self.Mm_DoubleSpinBox = QtWidgets.QDoubleSpinBox(self)
        self.Mm_DoubleSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.Tm_Label = QtWidgets.QLabel(self)
        self.Tm_DoubleSpinBox = QtWidgets.QDoubleSpinBox(self)
        self.Tm_DoubleSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.Ma_Label = QtWidgets.QLabel(self)
        self.Ma_DoubleSpinBox = QtWidgets.QDoubleSpinBox(self)
        self.Ma_DoubleSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.ButtonBox = QtWidgets.QDialogButtonBox(self)
        self.ScreenWidth = GetSystemMetrics(0)
        self.ScreenHeight = GetSystemMetrics(1)
        self.layoutSettings()
        self.setUpEngineGearPulleyBox()
        self.setUpBasicInformationsBox()
        self.setUpAutomaticallyInsertBox()
        self.setUpManuallyInsertBox()
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.dialogVerticalLayout.addItem(spacerItem2)
        self.setUpFont()
        self.setUpIcon(path=self.iconPath)
        self.setUpName()
        self.retranslate()
        self.control()
        self.ButtonBox.accepted.connect(self.accept)
        self.ButtonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.setStyleSheet("QDialog {background-color: #f2f2f2}")
        self.setUpButtonBox()

    def setDialogCheckable(self,
                           state: bool = None,
                           checkBox: bool = None,
                           basic: bool = None,
                           automatically: bool = None,
                           power: bool = None,
                           vector: bool = None,
                           manually: bool = None,
                           reset=False) -> None:
        """
        :param reset: reset the values of the checkboxes.
        :param state: bool, state of the sections.
        :param basic: bool, basic section.
        :param automatically: bool, automatically section.
        :param power: bool, subsection of automatically.
        :param vector: subsection of automatically.
        :param manually: bool, manually section.
        :param checkBox: all checkBoxes in the dialog.
        :return: None.
        """
        if reset:
            self.engineCheckBox.setChecked(state)
            self.pulleyCheckBox.setChecked(state)
            self.gearCheckBox.setChecked(state)
            self.powerCheckBox.setChecked(state)
            self.vectorsCheckBox.setChecked(state)
            self.AutomaticallyInsertCheckBox.setChecked(state)
            self.ManuallyInsertCheckBox.setChecked(state)

        if checkBox:
            self.engineCheckBox.setCheckable(state)
            self.pulleyCheckBox.setCheckable(state)
            self.gearCheckBox.setCheckable(state)


        if basic:
            self.radiusLabel.setEnabled(state)
            self.radiusDoubleSpinBox.setEnabled(state)
            self.xPositionLabel.setEnabled(state)
            self.xPositionDoubleSpinBox.setEnabled(state)
            self.angleObliquityAngle.setEnabled(state)
            self.angleObliquityDoubleSpinBox.setEnabled(state)
            self.torqueLabel.setEnabled(state)
            self.torqueDoubleSpinBox.setEnabled(state)

        if automatically:
            # self.AutomaticallyInsertCheckBox.setCheckable(state)
            self.powerCheckBox.setCheckable(state)
            self.powerDoubleSpinBox.setEnabled(state)
            self.rpmLabel.setEnabled(state)
            self.rpmDoubleSpinBox.setEnabled(state)
            self.vectorsCheckBox.setCheckable(state)
            self.radialForceLabel.setEnabled(state)
            self.radialForceDoubleSpinBox.setEnabled(state)
            self.tangentialForceLabel.setEnabled(state)
            self.tangentialForcedoubleSpinBox.setEnabled(state)

        if power:
            # self.powerCheckBox.setCheckable(state)
            self.powerDoubleSpinBox.setEnabled(state)
            self.rpmLabel.setEnabled(state)
            self.rpmDoubleSpinBox.setEnabled(state)

        if vector:
            # self.vectorsCheckBox.setCheckable(state)
            self.radialForceLabel.setEnabled(state)
            self.radialForceDoubleSpinBox.setEnabled(state)
            self.tangentialForceLabel.setEnabled(state)
            self.tangentialForcedoubleSpinBox.setEnabled(state)

        if manually:
            # self.ManuallyInsertCheckBox.setCheckable(state)
            self.Ma_Label.setEnabled(state)
            self.Ma_DoubleSpinBox.setEnabled(state)
            self.Ta_Label.setEnabled(state)
            self.Ta_DoubleSpinBox.setEnabled(state)
            self.Mm_Label.setEnabled(state)
            self.Mm_DoubleSpinBox.setEnabled(state)
            self.Tm_Label.setEnabled(state)
            self.Tm_DoubleSpinBox.setEnabled(state)
    
    def initialize(self) -> None:
        """:return: None"""
        self.powerCheckBox.setChecked(False)
        self.vectorsCheckBox.setChecked(False)
        self.ManuallyInsertCheckBox.setChecked(False)
        self.AutomaticallyInsertCheckBox.setChecked(False)
        self.ManuallyInsertCheckBox.setCheckable(False)
        self.vectorsCheckBox.setCheckable(False)
        self.powerCheckBox.setCheckable(False)
        self.AutomaticallyInsertCheckBox.setCheckable(False)
        self.setDialogCheckable(state=False, checkBox=False, basic=True, automatically=True, vector=True,
                                power=True, manually=True, reset=True)
        self.setDialogCheckable(state=True, checkBox=True, basic=False, automatically=False, vector=False,
                                power=False, manually=False)



    def control(self) -> None:
        """
        @Description:
        This function'll control the dialog.
        :return: None
        """
        self.initialize()

    def controlAutomatically(self, state: QtCore.Qt.Checked) -> None:
        """
        @Description:
        This function'll enable and disable the labels, check boxes and spin boxes according to user choice
        and checkbox options.
        :param state: QtCore.Qt.Checked.
        :return: None.
        """

        if self.gearCheckBox.isChecked() or self.pulleyCheckBox.isChecked():
            if state == QtCore.Qt.Checked:
                self.ManuallyInsertCheckBox.setChecked(False)
                self.ManuallyInsertCheckBox.setCheckable(False)
            else:
                self.ManuallyInsertCheckBox.setCheckable(True)
                self.ManuallyInsertCheckBox.setChecked(True)
                self.setDialogCheckable(state=True, checkBox=False, basic=False, automatically=False, power=False,
                                        vector=False, manually=True)
        if self.engineCheckBox.isChecked():
            if state == QtCore.Qt.Checked:
                self.ManuallyInsertCheckBox.setChecked(False)
                self.ManuallyInsertCheckBox.setCheckable(False)
            else:
                self.ManuallyInsertCheckBox.setCheckable(True)
                self.ManuallyInsertCheckBox.setChecked(True)
                self.setDialogCheckable(state=True, checkBox=False, basic=False, automatically=False, power=False,
                                        vector=False, manually=True)

    def controlManually(self, state: QtCore.Qt.Checked) -> None:
        """
        @Description:
        This function'll enable and disable the labels, check boxes and spin boxes according to user choice
        and checkbox options.
        :param state: QtCore.Qt.Checked.
        :return: None.
        """
        if self.gearCheckBox.isChecked():
            if state == QtCore.Qt.Checked:

                self.setDialogCheckable(state=False, checkBox=False, basic=True, automatically=True, power=False,
                                        vector=False, manually=False)
                self.setDialogCheckable(state=True, checkBox=False, basic=False, automatically=False, power=False,
                                        vector=False, manually=True)
                self.powerCheckBox.setChecked(False)
                self.vectorsCheckBox.setChecked(False)
                self.powerCheckBox.setCheckable(False)
                self.vectorsCheckBox.setCheckable(False)
                self.AutomaticallyInsertCheckBox.setChecked(False)
                self.AutomaticallyInsertCheckBox.setCheckable(False)


            else:
                self.setDialogCheckable(state=True, checkBox=False, basic=True, automatically=False, power=False,
                                        vector=False, manually=False)
                self.setDialogCheckable(state=False, checkBox=False, basic=False, automatically=False, power=False,
                                        vector=False, manually=True)
                self.AutomaticallyInsertCheckBox.setCheckable(True)
                self.AutomaticallyInsertCheckBox.setChecked(True)
                self.powerCheckBox.setCheckable(True)
                self.vectorsCheckBox.setCheckable(True)
                self.powerCheckBox.setChecked(False)
                self.vectorsCheckBox.setChecked(False)


        if self.pulleyCheckBox.isChecked():
            if state == QtCore.Qt.Checked:
                self.setDialogCheckable(state=False, checkBox=False, basic=True, automatically=True, power=False,
                                        vector=False, manually=False)
                self.setDialogCheckable(state=True, checkBox=False, basic=False, automatically=False, power=False,
                                        vector=False, manually=True)

                self.AutomaticallyInsertCheckBox.setChecked(False)
                self.AutomaticallyInsertCheckBox.setCheckable(False)


            else:
                self.setDialogCheckable(state=True, checkBox=False, basic=True, automatically=False, power=False,
                                        vector=False, manually=False)
                self.angleObliquityAngle.setEnabled(False)
                self.angleObliquityDoubleSpinBox.setEnabled(False)
                self.setDialogCheckable(state=False, checkBox=False, basic=False, automatically=False, power=False,
                                        vector=False, manually=True)
                self.AutomaticallyInsertCheckBox.setCheckable(True)
                self.AutomaticallyInsertCheckBox.setChecked(True)
                self.powerCheckBox.setCheckable(True)
                self.powerCheckBox.setChecked(False)
                self.vectorsCheckBox.setCheckable(True)
                self.vectorsCheckBox.setChecked(False)

        if self.engineCheckBox.isChecked():
            if state == QtCore.Qt.Checked:
                self.setDialogCheckable(state=False, checkBox=False, basic=True, automatically=True, power=False,
                                        vector=True, manually=False)
                self.setDialogCheckable(state=True, checkBox=False, basic=False, automatically=False, power=False,
                                        vector=False, manually=True)
            else:
                self.setDialogCheckable(state=False, checkBox=False, basic=True,
                                        automatically=True, power=True, vector=True, manually=True)
                self.AutomaticallyInsertCheckBox.setCheckable(True)
                self.AutomaticallyInsertCheckBox.setChecked(True)
                self.powerCheckBox.setCheckable(True)
                self.powerCheckBox.setChecked(False)
                self.vectorsCheckBox.setCheckable(True)
                self.vectorsCheckBox.setChecked(False)



    def controlVector(self):
        """
        @Description:
        This function'll enable and disable the labels, check boxes and spin boxes according to user choice
        and checkbox options.
        :return: None.
        """
        if self.gearCheckBox.isChecked():
            self.vectorsCheckBox.setCheckable(True)
            if self.AutomaticallyInsertCheckBox.isChecked():
                if self.vectorsCheckBox.isChecked():
                    self.setDialogCheckable(state=True, checkBox=False, basic=False, automatically=False,
                                            power=False, vector=True, manually=False)
                    self.setDialogCheckable(state=False, checkBox=False, basic=False, automatically=False,
                                            power=True, vector=False, manually=False)
                    self.torqueDoubleSpinBox.setEnabled(False)
                    self.torqueLabel.setEnabled(False)
                    self.angleObliquityDoubleSpinBox.setEnabled(False)
                    self.angleObliquityDoubleSpinBox.setValue(0)
                    self.angleObliquityAngle.setEnabled(False)

                    self.ManuallyInsertCheckBox.setCheckable(False)
                    self.powerCheckBox.setChecked(False)
                else:

                    self.setDialogCheckable(state=False, checkBox=False, basic=False, automatically=False,
                                            power=False, vector=True, manually=False)
                    self.setDialogCheckable(state=True, checkBox=False, basic=False, automatically=False,
                                            power=True, vector=False, manually=False)

                    if not self.ManuallyInsertCheckBox.isChecked():
                        self.angleObliquityDoubleSpinBox.setEnabled(True)
                        self.angleObliquityAngle.setEnabled(True)

                        self.powerCheckBox.setCheckable(True)
                        self.powerCheckBox.setChecked(True)



            else:

                if self.vectorsCheckBox.isChecked():
                    self.AutomaticallyInsertCheckBox.setChecked(True)
                    self.setDialogCheckable(state=True, checkBox=False, basic=False, automatically=False,
                                            power=False, vector=True, manually=False)
                    self.setDialogCheckable(state=False, checkBox=False, basic=False, automatically=False,
                                            power=True, vector=False, manually=False)
                    self.vectorsCheckBox.setCheckable(True)
                    self.powerCheckBox.setChecked(False)
                    self.torqueDoubleSpinBox.setEnabled(False)
                    self.torqueLabel.setEnabled(False)
                    self.angleObliquityDoubleSpinBox.setEnabled(False)
                    self.angleObliquityDoubleSpinBox.setValue(0)
                    self.angleObliquityAngle.setEnabled(False)
                else:
                    if not self.ManuallyInsertCheckBox.isChecked():
                        self.angleObliquityDoubleSpinBox.setEnabled(True)
                        self.angleObliquityAngle.setEnabled(True)
                        self.torqueDoubleSpinBox.setEnabled(True)
                        self.torqueLabel.setEnabled(True)
                        self.vectorsCheckBox.setCheckable(False)
                        self.vectorsCheckBox.setCheckable(True)
                        self.powerCheckBox.setCheckable(True)

        elif self.pulleyCheckBox.isChecked():
            self.vectorsCheckBox.setCheckable(False)



        else:

            self.initialize()



    def controlPower(self, state: QtCore.Qt.CheckState):
        """
        @Description:
        This function'll enable and disable the labels, check boxes and spin boxes according to user choice
        and checkbox options.
        :return: None.
        """
        if self.engineCheckBox.isChecked():
            if self.AutomaticallyInsertCheckBox.isChecked():
                if state == QtCore.Qt.Checked:
                    self.torqueLabel.setEnabled(False)
                    self.torqueDoubleSpinBox.setEnabled(False)
                    self.powerDoubleSpinBox.setEnabled(True)
                    self.setDialogCheckable(state=True, power=True)
                else:
                    self.torqueLabel.setEnabled(True)
                    self.torqueDoubleSpinBox.setEnabled(True)
                    self.setDialogCheckable(state=False, power=False)
            else:
                if state == QtCore.Qt.Checked:
                    self.AutomaticallyInsertCheckBox.setChecked(True)
                    self.torqueLabel.setEnabled(False)
                    self.torqueDoubleSpinBox.setEnabled(False)
                    self.powerDoubleSpinBox.setEnabled(True)
                    self.setDialogCheckable(state=True, power=True)
                else:
                    self.torqueLabel.setEnabled(True)
                    self.torqueDoubleSpinBox.setEnabled(True)
                    self.setDialogCheckable(state=False, power=False)

        if self.gearCheckBox.isChecked():
            if self.AutomaticallyInsertCheckBox.isChecked():
                if state == QtCore.Qt.Checked:
                    self.setDialogCheckable(state=True, checkBox=False, basic=False, automatically=False,
                                            power=True, vector=False, manually=False)
                    self.setDialogCheckable(state=False, checkBox=False, basic=False, automatically=False,
                                            power=False, vector=True, manually=False)
                    self.vectorsCheckBox.setChecked(False)
                    self.vectorsCheckBox.setCheckable(False)
                else:
                    self.setDialogCheckable(state=True, checkBox=False, basic=False, automatically=False,
                                            power=False, vector=True, manually=False)
                    self.setDialogCheckable(state=False, checkBox=False, basic=False, automatically=False,
                                            power=True, vector=False, manually=False)
                    self.vectorsCheckBox.setChecked(True)
                    self.vectorsCheckBox.setCheckable(True)
                    self.powerCheckBox.setChecked(False)
            else:
                if state == QtCore.Qt.Checked:
                    self.AutomaticallyInsertCheckBox.setChecked(True)
                    self.ManuallyInsertCheckBox.setCheckable(False)
                    self.setDialogCheckable(state=True, checkBox=False, basic=False, automatically=False,
                                            power=True, vector=False, manually=False)
                else:
                    self.AutomaticallyInsertCheckBox.setChecked(False)
                    self.ManuallyInsertCheckBox.setCheckable(True)
                    self.vectorsCheckBox.setCheckable(True)
                    self.powerCheckBox.setCheckable(True)

        if self.pulleyCheckBox.isChecked():
            if self.AutomaticallyInsertCheckBox.isChecked():
                if state == QtCore.Qt.Checked:
                    self.setDialogCheckable(state=True, checkBox=False, basic=False, automatically=False,
                                            power=True, vector=False, manually=False)
                    self.setDialogCheckable(state=False, checkBox=False, basic=False, automatically=False,
                                            power=False, vector=True, manually=False)
                    self.vectorsCheckBox.setChecked(False)
                    self.vectorsCheckBox.setCheckable(False)
                else:
                    self.setDialogCheckable(state=False, checkBox=False, basic=False, automatically=False,
                                            power=True, vector=False, manually=False)

                    self.powerCheckBox.setChecked(False)

            else:

                if state == QtCore.Qt.Checked:
                    self.AutomaticallyInsertCheckBox.setChecked(True)
                    self.ManuallyInsertCheckBox.setCheckable(False)
                    self.setDialogCheckable(state=True, checkBox=False, basic=False, automatically=False,
                                            power=True, vector=False, manually=False)
                else:
                    self.AutomaticallyInsertCheckBox.setChecked(False)
                    self.ManuallyInsertCheckBox.setCheckable(True)
                    self.powerCheckBox.setCheckable(True)


    def controlGear(self, state: QtCore.Qt.Checked) -> None:
        """
        @Description:
        This function'll enable and disable the labels, check boxes and spin boxes according to user choice
        and checkbox options.
        :param state: QtCore.Qt.Checked, the checkbox state.
        :return: None.
        """
        if state == QtCore.Qt.Checked:
            self.initialize()
            self.AutomaticallyInsertCheckBox.setCheckable(True)
            self.powerCheckBox.setCheckable(True)
            self.vectorsCheckBox.setCheckable(True)
            self.ManuallyInsertCheckBox.setCheckable(True)
            self.engineCheckBox.setEnabled(False)
            self.pulleyCheckBox.setEnabled(False)
            self.pulleyCheckBox.setChecked(False)
            self.gearCheckBox.setChecked(True)
            self.setDialogCheckable(state=True, checkBox=False, basic=True, automatically=False, power=False,
                                    vector=False, manually=False)
            if self.AutomaticallyInsertCheckBox.isChecked():
                pass

        else:
            self.initialize()
            self.AutomaticallyInsertCheckBox.setCheckable(False)
            self.engineCheckBox.setEnabled(True)
            self.pulleyCheckBox.setEnabled(True)

    def controlPulley(self, state: QtCore.Qt.Checked) -> None:
        """
        @Description:
        This function'll enable and disable the labels, check boxes and spin boxes according to user choice
        and checkbox options.
        :param state: QtCore.Qt.Checked, the checkbox state.
        :return: None.
        """
        if state == QtCore.Qt.Checked:
            self.initialize()
            self.setDialogCheckable(state=False, checkBox=False, basic=True,
                                    automatically=True, power=True, vector=True, manually=True)
            self.setDialogCheckable(state=True, checkBox=False, basic=True, automatically=False, power=False,
                                    vector=False, manually=False)
            self.engineCheckBox.setChecked(False)
            self.gearCheckBox.setChecked(False)
            self.angleObliquityAngle.setEnabled(False)
            self.angleObliquityDoubleSpinBox.setEnabled(False)
            self.AutomaticallyInsertCheckBox.setCheckable(True)
            self.ManuallyInsertCheckBox.setCheckable(True)
            self.powerCheckBox.setCheckable(True)
            self.vectorsCheckBox.setCheckable(True)
            self.pulleyCheckBox.setChecked(True)
            self.gearCheckBox.setEnabled(False)
            self.engineCheckBox.setEnabled(False)

        else:

            self.gearCheckBox.setEnabled(True)
            self.engineCheckBox.setEnabled(True)
            if not (self.engineCheckBox.isChecked() and self.gearCheckBox.isChecked()):
                self.initialize()
                self.setDialogCheckable(state=False, checkBox=False, basic=True,
                                        automatically=True, power=True, vector=True, manually=True)
                self.setDialogCheckable(state=False, checkBox=False, basic=True, automatically=False, power=False,
                                        vector=False, manually=False)
                self.AutomaticallyInsertCheckBox.setCheckable(False)
                self.ManuallyInsertCheckBox.setCheckable(False)
                self.powerCheckBox.setCheckable(False)
                self.vectorsCheckBox.setCheckable(False)

    def controlEngine(self, state: QtCore.Qt.Checked) -> None:
        """
        @Description:
        This function'll enable and disable the labels, check boxes and spin boxes according to user choice
        and checkbox options.
        :param state: QtCore.Qt.Checked, the checkbox state.
        :return: None.
        """

        if state == QtCore.Qt.Checked:
            self.setDialogCheckable(state=False, checkBox=False, basic=True,
                                    automatically=True, power=True, vector=True, manually=True)
            self.AutomaticallyInsertCheckBox.setCheckable(True)
            self.powerCheckBox.setCheckable(True)
            self.gearCheckBox.setEnabled(False)
            self.pulleyCheckBox.setEnabled(False)
            self.radiusLabel.setEnabled(False)
            self.radiusDoubleSpinBox.setEnabled(False)
            self.xPositionLabel.setEnabled(True)
            self.xPositionDoubleSpinBox.setEnabled(True)
            self.torqueLabel.setEnabled(True)
            self.torqueDoubleSpinBox.setEnabled(True)
            self.gearCheckBox.setChecked(False)
            self.pulleyCheckBox.setChecked(False)
            self.ManuallyInsertCheckBox.setCheckable(True)


        else:
            self.setDialogCheckable(state=False, checkBox=False, basic=True,
                                    automatically=True, power=True, vector=True, manually=True)
            self.AutomaticallyInsertCheckBox.setCheckable(False)
            self.powerCheckBox.setCheckable(False)
            self.gearCheckBox.setEnabled(True)
            self.pulleyCheckBox.setEnabled(True)
            self.radiusLabel.setEnabled(False)
            self.radiusDoubleSpinBox.setEnabled(False)
            self.xPositionLabel.setEnabled(False)
            self.xPositionDoubleSpinBox.setEnabled(False)
            self.torqueLabel.setEnabled(False)
            self.torqueDoubleSpinBox.setEnabled(False)

    def setUpManuallyInsertBox(self) -> None:
        """
        @Description:
        This function'll set up the manually insert box.
        :return: None
        """
        # Manually
        self.dialogVerticalLayout.addWidget(self.ManuallyInsertCheckBox)
        self.ManuallyInsertCheckBox.stateChanged.connect(self.controlManually)

        # Ta
        self.manuallyInsertFormLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.Ta_Label)
        self.Ta_DoubleSpinBox.setRange(-1e9, 1e9)
        self.manuallyInsertFormLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.Ta_DoubleSpinBox)

        # Mm
        self.manuallyInsertFormLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.Mm_Label)
        self.Mm_DoubleSpinBox.setRange(-1e9, 1e19)
        self.manuallyInsertFormLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.Mm_DoubleSpinBox)

        # Tm
        self.manuallyInsertFormLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.Tm_Label)
        self.Tm_DoubleSpinBox.setRange(-1e9, 1e19)
        self.manuallyInsertFormLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.Tm_DoubleSpinBox)

        # Ma
        self.manuallyInsertFormLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.Ma_Label)
        self.Ma_DoubleSpinBox.setRange(-1e9, 1e19)
        self.manuallyInsertFormLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.Ma_DoubleSpinBox)

        # Add to layout
        self.dialogVerticalLayout.addLayout(self.manuallyInsertFormLayout)
        self.verticalLayout.addLayout(self.dialogVerticalLayout)

    def setUpAutomaticallyInsertBox(self) -> None:
        """
        @Description:
        This function'll set up the automatically insert box.
        :return: None
        """
        # Automatically
        self.AutomaticallyInsertCheckBox.setEnabled(True)
        self.dialogVerticalLayout.addWidget(self.AutomaticallyInsertCheckBox)
        self.AutomaticallyInsertCheckBox.stateChanged.connect(self.controlAutomatically)

        # Power
        self.automaticallyInsertFormLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.powerCheckBox)
        self.powerDoubleSpinBox.setRange(-1e12, 1e12)
        self.automaticallyInsertFormLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.powerDoubleSpinBox)
        self.powerCheckBox.stateChanged.connect(self.controlPower)

        # RPM
        self.automaticallyInsertFormLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.rpmLabel)
        self.rpmDoubleSpinBox.setRange(-1e9, 1e12)
        self.automaticallyInsertFormLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.rpmDoubleSpinBox)

        # Radial Force
        self.automaticallyInsertFormLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.radialForceLabel)
        self.radialForceDoubleSpinBox.setRange(-1e12, 1e12)
        self.automaticallyInsertFormLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.radialForceDoubleSpinBox)

        # Tangential Force
        self.tangentialForcedoubleSpinBox.setRange(-1e12, 1e12)
        self.automaticallyInsertFormLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.tangentialForceLabel)
        self.tangentialForcedoubleSpinBox.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.tangentialForcedoubleSpinBox.setMouseTracking(True)
        self.tangentialForcedoubleSpinBox.setAcceptDrops(False)
        self.tangentialForcedoubleSpinBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tangentialForcedoubleSpinBox.setAutoFillBackground(False)
        self.automaticallyInsertFormLayout.\
            setWidget(5, QtWidgets.QFormLayout.FieldRole, self.tangentialForcedoubleSpinBox)

        # Vectors
        self.automaticallyInsertFormLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.vectorsCheckBox)
        self.vectorsCheckBox.stateChanged.connect(self.controlVector)

        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.automaticallyInsertFormLayout.setItem(3, QtWidgets.QFormLayout.FieldRole, spacerItem1)
        self.dialogVerticalLayout.addLayout(self.automaticallyInsertFormLayout)

    def setUpBasicInformationsBox(self):
        """
        @Description:
        This function'll set up the box with the basic information contents.
        :return: None
        """
        # Radius
        self.basicFormLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.radiusLabel)
        self.radiusDoubleSpinBox.setRange(2.5, 1e9)
        self.radiusDoubleSpinBox.setValue(50)
        self.basicFormLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.radiusDoubleSpinBox)

        # X Position
        self.basicFormLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.xPositionLabel)
        self.basicFormLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.xPositionDoubleSpinBox)

        # Obliquity angle
        self.basicFormLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.angleObliquityAngle)
        self.angleObliquityDoubleSpinBox.setRange(0, 360)
        self.basicFormLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.angleObliquityDoubleSpinBox)

        # Torque
        self.basicFormLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.torqueLabel)
        self.torqueDoubleSpinBox.setRange(-1e9, 1e9)
        self.basicFormLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.torqueDoubleSpinBox)

        # Add to layout
        self.dialogVerticalLayout.addLayout(self.basicFormLayout)
        # Space item
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.dialogVerticalLayout.addItem(spacerItem)



    def setUpEngineGearPulleyBox(self) -> None:
        """
        @Description:
        This function'll set up the box with the check boxes: Engine, Gear and Pulley.
        :return: None
        """
        # Engine
        self.gearPulleyEngineHorizontalLayout.addWidget(self.engineCheckBox)
        self.engineCheckBox.stateChanged.connect(self.controlEngine)

        # Gear
        self.gearPulleyEngineHorizontalLayout.addWidget(self.gearCheckBox)
        self.gearCheckBox.stateChanged.connect(self.controlGear)

        # Pulley
        self.gearPulleyEngineHorizontalLayout.addWidget(self.pulleyCheckBox)
        self.pulleyCheckBox.stateChanged.connect(self.controlPulley)

        # Add to layout
        self.dialogVerticalLayout.addLayout(self.gearPulleyEngineHorizontalLayout)

    def retranslate(self) -> None:
        """
        @Description:
        This function'll translate the name of the objects.
        :return: None
        """
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Shaftex-Forces"))
        self.setToolTip(_translate("Dialog", "<html><head/><body><p>This window allows the user to insert external "
                                             "forces acting on the shaft</p></body></html>"))
        self.engineCheckBox.setText(_translate("Dialog", "Engine"))
        self.gearCheckBox.setText(_translate("Dialog", "Gear"))
        self.pulleyCheckBox.setText(_translate("Dialog", "Pulley"))
        self.radiusLabel.setText(_translate("Dialog", "Radius  [mm]"))
        self.xPositionLabel.setText(_translate("Dialog", "x position [mm]"))
        self.angleObliquityAngle.setText(_translate("Dialog", "Angle of obliquity  [degree]"))
        self.torqueLabel.setText(_translate("Dialog", "Torque  [Nm]"))
        self.AutomaticallyInsertCheckBox.setText(_translate("Dialog", "Automatically insert"))
        self.powerCheckBox.setText(_translate("Dialog", "Power  [Watts]"))
        self.rpmLabel.setText(_translate("Dialog", "RPM"))
        self.radialForceLabel.setText(_translate("Dialog", "Radial Force [N]"))
        self.tangentialForceLabel.setText(_translate("Dialog", "Tangential Force  [N]"))
        self.tangentialForcedoubleSpinBox.setStatusTip(_translate("Dialog", "Insert here the tangential modolus"))
        self.vectorsCheckBox.setText(_translate("Dialog", "Vectors"))
        self.ManuallyInsertCheckBox.setText(_translate("Dialog", "Manually Insert"))
        self.Ta_Label.setText(_translate("Dialog", "Ta"))
        self.Mm_Label.setText(_translate("Dialog", "Mm"))
        self.Tm_Label.setText(_translate("Dialog", "Tm"))
        self.Ma_Label.setText(_translate("Dialog", "Ma"))

    def setUpButtonBox(self):
        """
        @Description:
        This function'll set up the button box.
        :return: None
        """
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ButtonBox.sizePolicy().hasHeightForWidth())
        self.ButtonBox.setSizePolicy(sizePolicy)
        self.ButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.ButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.ButtonBox)
        self.ButtonBox.accepted.connect(self.accept)
        self.ButtonBox.rejected.connect(self.reject)

    def setUpName(self) -> None:
        """
        @Description:
        This function'll set up the name of the objects.
        :return: None
        """
        self.setObjectName("Dialog")
        self.verticalLayout.setObjectName("verticalLayout")
        self.dialogVerticalLayout.setObjectName("dialogVerticalLayout")
        self.gearPulleyEngineHorizontalLayout.setObjectName("gearPulleyEngineHorizontalLayout")
        self.engineCheckBox.setObjectName("engineCheckBox")
        self.gearCheckBox.setObjectName("gearCheckBox")
        self.pulleyCheckBox.setObjectName("pulleyCheckBox")
        self.basicFormLayout.setObjectName("basicFormLayout")
        self.radiusLabel.setObjectName("radiusLabel")
        self.radiusDoubleSpinBox.setObjectName("radiusDoubleSpinBox")
        self.xPositionLabel.setObjectName("xPositionLabel")
        self.xPositionDoubleSpinBox.setObjectName("xPositionDoubleSpinBox")
        self.angleObliquityAngle.setObjectName("angleObliquityAngle")
        self.angleObliquityDoubleSpinBox.setObjectName("angleObliquityDoubleSpinBox")
        self.torqueLabel.setObjectName("torqueLabel")
        self.torqueDoubleSpinBox.setObjectName("torqueDoubleSpinBox")
        self.AutomaticallyInsertCheckBox.setObjectName("AutomaticallyInsertCheckBox")
        self.automaticallyInsertFormLayout.setObjectName("automaticallyInsertFormLayout")
        self.powerCheckBox.setObjectName("powerCheckBox")
        self.powerDoubleSpinBox.setObjectName("powerDoubleSpinBox")
        self.rpmLabel.setObjectName("rpmLabel")
        self.rpmDoubleSpinBox.setObjectName("rpmDoubleSpinBox")
        self.radialForceLabel.setObjectName("radialForceLabel")
        self.radialForceDoubleSpinBox.setObjectName("radialForceDoubleSpinBox")
        self.tangentialForceLabel.setObjectName("tangentialForceLabel")
        self.tangentialForcedoubleSpinBox.setObjectName("tangentialForcedoubleSpinBox")
        self.vectorsCheckBox.setObjectName("vectorsCheckBox")
        self.ManuallyInsertCheckBox.setObjectName("ManuallyInsertCheckBox")
        self.manuallyInsertFormLayout.setObjectName("manuallyInsertFormLayout")
        self.Ta_Label.setObjectName("Ta_Label")
        self.Ta_DoubleSpinBox.setObjectName("Ta_DoubleSpinBox")
        self.Mm_Label.setObjectName("Mm_Label")
        self.Mm_DoubleSpinBox.setObjectName("Mm_DoubleSpinBox")
        self.Tm_Label.setObjectName("Tm_Label")
        self.Tm_DoubleSpinBox.setObjectName("Tm_DoubleSpinBox")
        self.Ma_Label.setObjectName("Ma_Label")
        self.Ma_DoubleSpinBox.setObjectName("Ma_DoubleSpinBox")

    def setUpFont(self) -> None:
        """
        This function will set up the font to be used in the dialog window.
        :return: None
        """
        self.fontForm.setFamily("Segoe MDL2 Assets")
        self.fontForm.setBold(False)
        self.fontForm.setWeight(50)
        self.setFont(self.fontForm)

    def setUpIcon(self, path: str) -> None:
        """
        This function provides the first two check box of the dialog window.
        :return: None
        """
        icon = QtGui.QIcon(path)
        self.setWindowIcon(icon)

    def layoutSettings(self):
        """
        @Description:
        This function'll the layout's configuration.
        :return: None
        """
        self.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.setAutoFillBackground(True)
        self.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.setSizeGripEnabled(True)
        self.setModal(True)
        self.verticalLayout.setContentsMargins(7, 7, 7, 7)
        self.setWindowFlag(Qt.WindowMinMaxButtonsHint)
        self.setMinimumSize(QtCore.QSize(380, 640))
        self.setMaximumSize(QtCore.QSize(380, 640))
        x, y = self.ScreenWidth / 2 - 380 / 2, self.ScreenHeight / 2 - 640 / 2
        self.setGeometry(x, y, 380, 640)
        self.dialogVerticalLayout.setContentsMargins(7, 7, 7, 7)
        self.dialogVerticalLayout.setSpacing(7)
        self.gearPulleyEngineHorizontalLayout.setContentsMargins(7, 7, 7, 7)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = DialogFx()
    ui.show()
    sys.exit(app.exec_())
