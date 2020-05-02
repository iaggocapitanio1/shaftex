"""
@Description:
User Interface Dialog
"""
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtSvg import QSvgWidget
import ctypes
from Shafton.shafton import shaftKtFactorCircumferentialGrooveInShaft, shaftKtFactorSteppedBarOfCircularCrossSection
from Shafton.shafton import shaftKtsFactorCircumferentialGrooveInShaft, shaftKtsFactorSteppedBarOfCircularCrossSection
import source_images

myAppId = u'ShaftExploration.Shaftex.version-1.0'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppId)


class NotchDialog(QtWidgets.QDialog):
    """
    This class'll define the notch dialog.
    """

    def __init__(self):
        super(NotchDialog, self).__init__()
        self.svgKts_flatBottomPath = u":notch/Kts_flatBottom.svg"
        self.svgKt_flatBottomPath = u":notch/Kt_flatBottom.svg"
        self.svgKt_UPath = u":notch/Kt_U.svg"
        self.svgKts_UPath = u":notch/Kts_U.svg"
        self.iconPath = ":icons/shaftex.ico"
        self.svgKt_steppedPath = u":notch/Kt_stepped.svg"
        self.svgKts_steppedPath = u":notch/Kts_stepped.svg"
        self.fontStyle = QtGui.QFont()
        self.shaftDiameter = 8
        self.msg = QtWidgets.QMessageBox(self)
        self.fontStyle.setFamily("Segoe MDL2 Assets")
        self.fontStyle.setPointSize(8)
        self.fontStyle.setWeight(50)
        self.fontStyle.setBold(False)
        self.setFont(self.fontStyle)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint)
        self.Kt = None
        self.Kts = None
        self.resize(1000, 800)
        self.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.setSizeGripEnabled(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.Left_formLayout = QtWidgets.QFormLayout()
        self.d_label = QtWidgets.QLabel(self)
        self.d_doubleSpinBox = QtWidgets.QDoubleSpinBox(self)
        self.Kt_label = QtWidgets.QLabel(self)
        self.r_label = QtWidgets.QLabel(self)
        self.r_doubleSpinBox = QtWidgets.QDoubleSpinBox(self)
        self.set_pushButton = QtWidgets.QPushButton("Set", self)
        self.set_pushButton.clicked.connect(self.setSVG)
        self.Kt_doubleSpinBox = QtWidgets.QDoubleSpinBox(self)
        self.Kts_label = QtWidgets.QLabel(self)
        self.Kts_doubleSpinBox = QtWidgets.QDoubleSpinBox(self)
        self.D_label = QtWidgets.QLabel(self)
        self.D_doubleSpinBox = QtWidgets.QDoubleSpinBox(self)
        self.Right_formLayout = QtWidgets.QFormLayout()
        self.comboBox = QtWidgets.QComboBox(self)
        self.notch_label = QtWidgets.QLabel(self)
        self.KtChosenValue_label = QtWidgets.QLabel(self)
        self.KtsChosenValue_label = QtWidgets.QLabel(self)
        self.btn_label = QtWidgets.QLabel("Set values", self)
        self.KtChosen_label = QtWidgets.QLabel(self)
        self.KtsChosen_label = QtWidgets.QLabel(self)
        self.images_horizontalLayout = QtWidgets.QHBoxLayout()
        self.imageOne_svg = QSvgWidget()  # QtWidgets.QLabel(self)
        self.imageTwo_svg = QSvgWidget()  # QtWidgets.QLabel(self)
        self.imageOne_svg.setBackgroundRole(QtGui.QPalette.Dark)
        self.imageTwo_svg.setBackgroundRole(QtGui.QPalette.Dark)
        self.imageOne_svg.setMinimumWidth(700)
        self.imageTwo_svg.setMinimumWidth(700)
        self.imageOne_svg.setMinimumHeight(700)
        self.imageTwo_svg.setMinimumHeight(700)
        self.setStyleSheet("QDialog {background-color: #f2f2f2}")
        self.setWindowIcon(QtGui.QIcon(self.iconPath))
        self.imageOne_svg.load(self.svgKt_steppedPath)
        self.imageTwo_svg.load(self.svgKts_steppedPath)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel(self)
        self.label_2 = QtWidgets.QLabel(self)
        self.setRight()
        self.setLeft()
        self.setBottom()
        self.retranslate()
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.control()

        self.comboBox.currentTextChanged.connect(self.setSVG)
        self.set_pushButton.clicked.connect(self.getStressFactor)

    def setShaftDiameter(self, diameter: float) -> None:
        """

        :param diameter:
        """
        self.shaftDiameter = diameter
        self.d_doubleSpinBox.setValue(self.getShaftDiameter())

    def getShaftDiameter(self) -> float:
        """

        :return: float
        """
        return self.shaftDiameter

    def getStressFactor(self) -> bool:
        """

        :return: bool
        """
        D = self.D_doubleSpinBox.value()
        d = self.d_doubleSpinBox.value()
        r = self.r_doubleSpinBox.value()

        if self.r_doubleSpinBox.value() == 0.0:
            self.msg.setText("Not divisible by zero!")
            self.msg.setWindowIcon(QtGui.QIcon(self.iconPath))
            self.msg.setInformativeText("Please try again!")
            self.msg.setWindowTitle("Error!")
            self.msg.setIcon(QtWidgets.QMessageBox.Critical)

            # noinspection PyUnusedLocal
            x = self.msg.exec_()

            return False

        if self.comboBox.currentText() == "stepped bar":
            if not (0.5 * r < (D-d) < 8 * r):
                self.msg.setText("Value outside borders!")
                self.msg.setWindowIcon(QtGui.QIcon(self.iconPath))
                self.msg.setInformativeText("Please try again!")
                self.msg.setWindowTitle("Error!")
                self.msg.setIcon(QtWidgets.QMessageBox.Critical)
                # noinspection PyUnusedLocal
                x = self.msg.exec_()
                return False
        if self.comboBox.currentText() == "circumferential groove":
            if not (0.5 * r < (D-d) < 100 * r):
                self.msg.setText("Value outside borders!")
                self.msg.setWindowIcon(QtGui.QIcon(self.iconPath))
                self.msg.setInformativeText("Please try again!")
                self.msg.setWindowTitle("Error!")
                self.msg.setIcon(QtWidgets.QMessageBox.Critical)
                # noinspection PyUnusedLocal
                x = self.msg.exec_()
                return False

        self.fontStyle.setBold(True)



        self.KtChosenValue_label.setFont(self.fontStyle)
        self.KtsChosenValue_label.setFont(self.fontStyle)
        name = self.comboBox.currentText()
        if name == "circumferential groove":

            D = float(self.D_doubleSpinBox.value()) * 1e-3
            r = float(self.r_doubleSpinBox.value()) * 1e-3
            d = float(self.d_doubleSpinBox.value()) * 1e-3
            self.Kt = shaftKtFactorCircumferentialGrooveInShaft(D=D, d=d, r=r)
            self.Kts = shaftKtsFactorCircumferentialGrooveInShaft(D=D, d=d, r=r)
            self.KtChosenValue_label.setText(str(self.Kt))
            self.KtsChosenValue_label.setText(str(self.Kts))
            return True

        elif name == "stepped bar":
            D = float(self.D_doubleSpinBox.value()) * 1e-3
            r = float(self.r_doubleSpinBox.value()) * 1e-3
            d = float(self.d_doubleSpinBox.value()) * 1e-3
            self.Kt = shaftKtFactorSteppedBarOfCircularCrossSection(D=D, d=d, r=r)
            self.Kts = shaftKtsFactorSteppedBarOfCircularCrossSection(D=D, d=d, r=r)
            self.KtChosenValue_label.setText(str(self.Kt))
            self.KtsChosenValue_label.setText(str(self.Kts))
            return True

        else:
            self.Kt = float(self.Kt_doubleSpinBox.value())
            self.Kts = float(self.Kts_doubleSpinBox.value())
            self.KtChosenValue_label.setText(str(self.Kt))
            self.KtsChosenValue_label.setText(str(self.Kts))
            return True

    def setSVG(self) -> None:
        """
        :return: None
        """
        name = self.comboBox.currentText()
        self.control()
        if name == "circumferential groove":
            self.imageOne_svg.load(self.svgKt_UPath)
            self.imageTwo_svg.load(self.svgKts_UPath)
        if name == "stepped bar":
            self.imageOne_svg.load(self.svgKt_steppedPath)
            self.imageTwo_svg.load(self.svgKts_steppedPath)

        if name == "flat bottom":
            self.imageOne_svg.load(self.svgKt_flatBottomPath)
            self.imageTwo_svg.load(self.svgKts_flatBottomPath)

    def control(self) -> None:
        """
        :return: None
        """
        text = self.comboBox.currentText()
        if text == "circumferential groove" or text == "stepped bar":

            self.Kt_doubleSpinBox.setValue(0)
            self.Kts_doubleSpinBox.setValue(0)
            self.d_label.setEnabled(False)
            self.d_doubleSpinBox.setEnabled(False)
            self.d_doubleSpinBox.setValue(self.getShaftDiameter())
            self.D_label.setEnabled(True)
            self.D_doubleSpinBox.setEnabled(True)
            self.Kt_label.setEnabled(False)
            self.Kt_doubleSpinBox.setEnabled(False)
            self.Kts_label.setEnabled(False)
            self.Kts_doubleSpinBox.setEnabled(False)

        else:
            self.d_label.setEnabled(False)
            self.d_doubleSpinBox.setEnabled(False)
            self.D_label.setEnabled(False)
            self.D_doubleSpinBox.setEnabled(False)
            self.Kt_label.setEnabled(True)
            self.Kt_doubleSpinBox.setEnabled(True)
            self.Kts_label.setEnabled(True)
            self.Kts_doubleSpinBox.setEnabled(True)

    def setLeft(self) -> None:
        """
        :return: None
        """
        # 1-d
        self.d_label.setText("d  [mm]")
        self.d_doubleSpinBox.setRange(0, 500)
        self.d_doubleSpinBox.setDecimals(2)
        self.d_doubleSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.Left_formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.d_doubleSpinBox)
        self.Left_formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.d_label)
        # 2-D
        self.Left_formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.D_label)
        self.D_doubleSpinBox.setMinimum(8.0)
        self.D_doubleSpinBox.setMaximum(1000.0)
        self.D_doubleSpinBox.setSingleStep(10.0)
        self.D_doubleSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.Left_formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.D_doubleSpinBox)
        self.horizontalLayout.addLayout(self.Left_formLayout)
        # 3-r
        self.r_label.setText("Notch radius  [mm]")
        self.r_doubleSpinBox.setDecimals(2)
        self.r_doubleSpinBox.setSingleStep(0.01)
        self.r_doubleSpinBox.setRange(0, 500)
        self.r_doubleSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.Left_formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.r_label)
        self.Left_formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.r_doubleSpinBox)
        # 4-Kts
        self.Left_formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.Kts_label)
        self.Kts_doubleSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.Left_formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.Kts_doubleSpinBox)
        # 5-Kt
        self.Left_formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.Kt_label)
        self.Kt_doubleSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.Left_formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.Kt_doubleSpinBox)

    def setRight(self):
        """
        :return: None
        """
        self.Right_formLayout.setContentsMargins(0, -1, -1, -1)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.Right_formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comboBox)
        self.Right_formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.notch_label)
        self.Right_formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.KtChosenValue_label)
        self.Right_formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.KtsChosenValue_label)
        self.Right_formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.KtChosen_label)
        self.Right_formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.KtsChosen_label)
        self.Right_formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.btn_label)
        self.Right_formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.set_pushButton)

    def setBottom(self) -> None:
        """
        :return: None
        """
        self.horizontalLayout.addLayout(self.Right_formLayout)
        self.verticalLayout.heightForWidth(3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.imageOne_svg.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.imageOne_svg.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        # self.imageOne_label.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.images_horizontalLayout.addWidget(self.imageOne_svg)
        self.images_horizontalLayout.addWidget(self.imageTwo_svg)
        self.verticalLayout.addLayout(self.images_horizontalLayout)



    def setName(self) -> None:
        """
        :return: None
        """
        self.setObjectName("Dialog")
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Left_formLayout.setObjectName("Left_formLayout")
        self.Kt_label.setObjectName("Kt_label")
        self.Kt_doubleSpinBox.setObjectName("Kt_doubleSpinBox")
        self.Kts_label.setObjectName("Kts_label")
        self.Kts_doubleSpinBox.setObjectName("Kts_doubleSpinBox")
        self.D_label.setObjectName("D_label")
        self.D_doubleSpinBox.setObjectName("D_doubleSpinBox")
        self.Right_formLayout.setObjectName("Right_formLayout")
        self.comboBox.setObjectName("comboBox")
        self.notch_label.setObjectName("notch_label")
        self.KtChosenValue_label.setObjectName("KtChosenValue_label")
        self.KtsChosenValue_label.setObjectName("KtsChosenValue_label")
        self.KtChosen_label.setObjectName("KtChosen_label")
        self.KtsChosen_label.setObjectName("KtsChosen_label")
        self.images_horizontalLayout.setObjectName("images_horizontalLayout")
        self.imageOne_label.setObjectName("imageOne_label")
        self.imageTwo_label.setObjectName("imageTwo_label")

    def retranslate(self):
        """
        :return: None
        """
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Shaftex-Notch"))
        self.Kt_label.setText(_translate("Dialog", "kt"))
        self.Kts_label.setText(_translate("Dialog", "Kts"))
        self.D_label.setText(_translate("Dialog", "D [mm]"))
        self.comboBox.setItemText(0, _translate("Dialog", "stepped bar"))
        self.comboBox.setItemText(1, _translate("Dialog", "circumferential groove"))
        self.comboBox.setItemText(2, _translate("Dialog", "flat bottom"))
        self.comboBox.setItemText(3, _translate("Dialog", "Other"))
        self.notch_label.setText(_translate("Dialog", "Notch"))
        self.KtChosenValue_label.setText(_translate("Dialog", "Not computed yet!"))
        self.KtsChosenValue_label.setText(_translate("Dialog", "Not computed yet!"))
        self.KtChosen_label.setText(_translate("Dialog", "Kt"))
        self.KtsChosen_label.setText(_translate("Dialog", "Kts"))
        # self.imageOne_label.setText(_translate("Dialog", "TextLabel"))
        # self.imageTwo_label.setText(_translate("Dialog", "TextLabel"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Dialog = NotchDialog()
    Dialog.show()
    sys.exit(app.exec_())
