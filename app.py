"""
@Description:
User Interface Dialog, main window
"""
__author__ = "Iaggo Capitanio"
__copyright__ = "Copyright (C) 2020 Iaggo Capitanio"
__license__ = "Public Domain"
__version__ = "1.0"

from typing import Union
import threading
import sys
import ctypes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
from win32api import GetSystemMetrics
import shaft as sh
import keyton as ky
from solveLib import getChoices
from solver import Solver, SolverForManuallyIsChecked
from Shafton.pandasModelKey import PandasModelKey
from Shafton.ModelShaft import ModelShaft
from Shafton.matplotlibChartMoment import DynamicMplCanvas
from Shafton.matplotlibChartTorque import DynamicMplCanvasTorque
from Shafton.itemDelegate import HTMLDelegate
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from slopeDialog import SlopeDialog
from deflectionDialog import DeflectionDialog
from dialogFx import DialogFx
from bearingX import BearingDialog
from notchDialog import NotchDialog
from Shafton.shafton import shaftTorque
import source_images

myAppId = u'ShaftExploration.Shaftex.version-1.0'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppId)


class MainWindow(QtWidgets.QMainWindow):
    """
    @Description:
    This class will be responsible to build the main window of the application.
    """

    def __init__(self) -> None:
        """:return None"""
        super(MainWindow, self).__init__()
        self.backgroundImagePath = ":bg/mainBG.png"
        self.iconPath = ":icons/shaftex.ico"
        self.keyOutPut_dockWidgetContents = QtWidgets.QWidget()
        self.Fx_verticalLayout = QtWidgets.QVBoxLayout()
        self.input_formLayout = QtWidgets.QFormLayout()
        self.inputOptions_horizontalLayout = QtWidgets.QHBoxLayout()
        self.input_verticalLayout = QtWidgets.QVBoxLayout()
        self.scrollArea_widgetContents = QtWidgets.QWidget()
        self.input_dockWidgetContents = QtWidgets.QWidget()
        self.shaftOutPut_dockWidgetContents = QtWidgets.QWidget()
        self.keyOutPut_verticalLayout = QtWidgets.QVBoxLayout()
        self.chart_verticalLayout = QtWidgets.QVBoxLayout()
        self.shatOutPut_verticalLayout = QtWidgets.QVBoxLayout()
        self.reactionsLEFT_formLayout = QtWidgets.QFormLayout()
        self.Fx_horizontalLayout = QtWidgets.QHBoxLayout()
        self.menubar = QtWidgets.QMenuBar(self)
        self.Input_dockWidget = QtWidgets.QDockWidget(self)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuStyle = QtWidgets.QMenu(self.menuFile)
        self.actionQuit = QtWidgets.QAction(self)
        self.centralwidget = QtWidgets.QWidget(self)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.chart_frame = QtWidgets.QFrame(self.centralwidget)
        self.shaftOutput_dockWidget = QtWidgets.QDockWidget(self)
        self.keyOutPut_dockWidget = QtWidgets.QDockWidget(self)
        self.Input_frame = QtWidgets.QFrame(self.scrollArea_widgetContents)
        self.keyOutPut_tableView = QtWidgets.QTableView(self.keyOutPut_dockWidgetContents)
        self.keyOutPut_label = QtWidgets.QLabel(self.keyOutPut_dockWidgetContents)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.keyOutPut_dockWidgetContents)
        self.shaftOutPut_tableView = QtWidgets.QTableView(self.shaftOutPut_dockWidgetContents)
        self.shaftOutPut_label = QtWidgets.QLabel(self.shaftOutPut_dockWidgetContents)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.shaftOutPut_dockWidgetContents)
        self.slope_pushButton = QtWidgets.QPushButton(self.input_dockWidgetContents)
        self.deflection_pushButton = QtWidgets.QPushButton(self.input_dockWidgetContents)
        self.slopeChart_label = QtWidgets.QLabel(self.input_dockWidgetContents)
        self.deflectionChart_label = QtWidgets.QLabel(self.input_dockWidgetContents)
        self.reactionsRIGHT_formLayout = QtWidgets.QFormLayout()
        self.SlopeResult_label = QtWidgets.QLabel(self.input_dockWidgetContents)
        self.Slope_label = QtWidgets.QLabel(self.input_dockWidgetContents)
        self.R2XZResult_label = QtWidgets.QLabel(self.input_dockWidgetContents)
        self.R2XZLabel = QtWidgets.QLabel(self.input_dockWidgetContents)
        self.R1XZResult_label = QtWidgets.QLabel(self.input_dockWidgetContents)
        self.R1XZ_label = QtWidgets.QLabel(self.input_dockWidgetContents)
        self.reactionsCENTER_formLayout = QtWidgets.QFormLayout()
        self.R1XYResult_label = QtWidgets.QLabel(self.input_dockWidgetContents)
        self.deflectionResult_label = QtWidgets.QLabel(self.input_dockWidgetContents)
        self.deflection_label = QtWidgets.QLabel(self.input_dockWidgetContents)
        self.R2XYResult_label = QtWidgets.QLabel(self.input_dockWidgetContents)
        self.R2XY_label = QtWidgets.QLabel(self.input_dockWidgetContents)
        self.R1XY_label = QtWidgets.QLabel(self.input_dockWidgetContents)
        self.solve_pushButton = QtWidgets.QPushButton(self.input_dockWidgetContents)
        # self.resetFx_pushButton = QtWidgets.QPushButton(self.input_dockWidgetContents)
        self.Fx2_pushButton = QtWidgets.QPushButton(self.input_dockWidgetContents)
        self.bearing_pushButton = QtWidgets.QPushButton(self.Input_frame)
        self.Fx1_pushButton = QtWidgets.QPushButton(self.input_dockWidgetContents)
        self.notch_pushButton = QtWidgets.QPushButton(self.Input_frame)
        self.safetyFactorForCompression_doubleSpinBox = QtWidgets.QDoubleSpinBox(self.Input_frame)
        self.safetyFactorForCompression_label = QtWidgets.QLabel(self.Input_frame)
        self.keySafetyFactorForShearing_doubleSpinBox = QtWidgets.QDoubleSpinBox(self.Input_frame)
        self.keySafetyFactorForShearing_label = QtWidgets.QLabel(self.Input_frame)
        self.keyMaterial_comboBox = QtWidgets.QComboBox(self.Input_frame)
        self.keyForm_label = QtWidgets.QLabel(self.Input_frame)
        self.keySolveBasedOn_comboBox = QtWidgets.QComboBox(self.Input_frame)
        self.keySolveBasedOn_label = QtWidgets.QLabel(self.Input_frame)
        self.keyForm_comboBox = QtWidgets.QComboBox(self.Input_frame)
        self.keyMaterial_label = QtWidgets.QLabel(self.Input_frame)
        self.keyTitle_label = QtWidgets.QLabel(self.Input_frame)
        self.shaftFeilureCriteria_comboBox = QtWidgets.QComboBox(self.Input_frame)
        self.shaftFailureCriteria_label = QtWidgets.QLabel(self.Input_frame)
        self.shaftReliability_doubleSpinBox = QtWidgets.QDoubleSpinBox(self.Input_frame)
        self.shaftReliabilityt_label = QtWidgets.QLabel(self.Input_frame)
        self.shaftTemperature_doubleSpinBox = QtWidgets.QDoubleSpinBox(self.Input_frame)
        self.shaftTemperature_label = QtWidgets.QLabel(self.Input_frame)
        self.shaftLoadType_comboBox = QtWidgets.QComboBox(self.Input_frame)
        self.shaftLoadType_label = QtWidgets.QLabel(self.Input_frame)
        self.shaftSurfaceCondition_comboBox = QtWidgets.QComboBox(self.Input_frame)
        self.shaftSurfaceCondition_label = QtWidgets.QLabel(self.Input_frame)
        self.shaftSafetyFactor_doubleSpinBox = QtWidgets.QDoubleSpinBox(self.Input_frame)
        self.shaftSafetyFactor_label = QtWidgets.QLabel(self.Input_frame)
        self.shaftLength_doubleSpinBox = QtWidgets.QDoubleSpinBox(self.Input_frame)
        self.shaftLength_label = QtWidgets.QLabel(self.Input_frame)
        self.shaftDiameter_doubleSpinBox = QtWidgets.QDoubleSpinBox(self.Input_frame)
        self.shaftDiameter_label = QtWidgets.QLabel(self.Input_frame)
        self.shaftAttemptDiameter_doubleSpinBox = QtWidgets.QDoubleSpinBox(self.Input_frame)
        self.shaftAttemptDiameter_label = QtWidgets.QLabel(self.Input_frame)
        self.shaftCriticalPointLocation_doubleSpinBox = QtWidgets.QDoubleSpinBox(self.Input_frame)
        self.shaftCriticalPointLocation_label = QtWidgets.QLabel(self.Input_frame)
        self.shaftMaterialt_comboBox = QtWidgets.QComboBox(self.Input_frame)
        self.shaftMaterial_label = QtWidgets.QLabel(self.Input_frame)
        self.shaftInputTitle_label = QtWidgets.QLabel(self.Input_frame)
        self.solveForTheDiameter_checkBox = QtWidgets.QCheckBox(self.Input_frame)
        self.solveForTheSafetyFactor_checkBox = QtWidgets.QCheckBox(self.Input_frame)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.Input_frame)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.scrollArea_widgetContents)
        self.input_scrollArea = QtWidgets.QScrollArea(self.input_dockWidgetContents)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.input_dockWidgetContents)

        # self.momentChart_widget = QtWidgets.QWidget(self.chart_frame)
        self.momentChart_widget = DynamicMplCanvas(domain=np.linspace(0, 4, 100),
                                                   XY=np.zeros(100),
                                                   XZ=np.zeros(100),
                                                   TOTAL=np.zeros(100),
                                                   dpi=100,
                                                   fontsize=9,
                                                   parent=self.chart_frame)

        self.momentChart_toolbar = NavigationToolbar(self.momentChart_widget, self.chart_frame)
        self.momentChart_label = QtWidgets.QLabel(self.chart_frame)
        # self.torqueChart_widget = QtWidgets.QWidget(self.chart_frame)
        self.torqueChart_widget = DynamicMplCanvasTorque(domain=np.linspace(0, 2, 100),
                                                         length=4,
                                                         image=np.zeros(100),
                                                         dpi=100,
                                                         fontsize=9,
                                                         parent=self.chart_frame)
        threading_bg = threading.Thread(target=self.__threading_action_bg)
        self.torqueChart_toolbar = NavigationToolbar(self.torqueChart_widget, self.chart_frame)
        # self.torqueChart_label = QtWidgets.QLabel(self.chart_frame)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.chart_frame)
        self.mainWindowWidth = 1800  # Height in pixels of the main window.
        self.mainWindowHeight = 900  # Height in pixels of the main window.
        self.stringIcon = str(self.iconPath)
        # noinspection LongLine
        self.stringStyleSheetWindow = " MainWindow { border-image: url(" + str(self.backgroundImagePath) + ")" \
                                                                                                           "0 0 0 0 stretch stretch; }"
        self.notch_var = QtWidgets.QDialog.Rejected
        self.bearing_var = QtWidgets.QDialog.Rejected
        self.fontStyle = QtGui.QFont()  # Create a parameter that's a QFont object.
        self.ScreenWidth = GetSystemMetrics(0)  # This variable takes the width of the user's pc.
        self.ScreenHeight = GetSystemMetrics(1)  # This variable takes the height of the user's pc.
        self.dialogFx1 = DialogFx()
        self.dialogFx1.setWindowTitle("ShaftEx - Force 1")
        self.dialogFx1.setStatusTip("You have to insert the first force here!")
        self.dialogFx2 = DialogFx()
        self.dialogFx2.setWindowTitle("ShaftEx - Force 2")
        self.dialogFx2.setStatusTip("You have to insert the second force here!")
        self.bearingX = BearingDialog()
        self.notchX = NotchDialog()
        self.setUpWindow()

        ################################################################################################################
        #                                                Initial  View
        ################################################################################################################
        Tm = Ma = Mm = Ta = Sut = Sy = Temperature = torque = 100  # dummy values
        error = diameter_attempt = D = d = reliability = r = 0.005  # dummy values
        method_surface_finishing = "Machined or cold-drawn"  # dummy values
        method = "DE-ASME"  # dummy values
        zero = True
        threading_key = threading.Thread(target=self.__threading_action_keyTable,
                                         args=[d,
                                               Sy,
                                               torque,
                                               zero])
        threading_key.start()
        threading_shaft = threading.Thread(target=self.__threading_action_ShaftTable,
                                           args=[Ma,
                                                 Mm,
                                                 Ta,
                                                 Tm,
                                                 Sut,
                                                 Sy,
                                                 r,
                                                 D,
                                                 d,
                                                 Temperature,
                                                 reliability,
                                                 method_surface_finishing,
                                                 diameter_attempt,
                                                 error,
                                                 method,
                                                 zero])
        threading_shaft.start()
        threading_bg.start()
        threading_key.join()
        threading_shaft.join()
        threading_bg.join()
        # noinspection PyTypeChecker
        self.shaftOutPut_tableView.setItemDelegate(HTMLDelegate())

        # noinspection PyTypeChecker
        self.keyOutPut_tableView.setItemDelegate(HTMLDelegate())
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.shaftOutPut_tableView.sizePolicy().hasHeightForWidth())
        self.shaftOutPut_tableView.setAutoFillBackground(True)
        self.shaftOutPut_tableView.setSizePolicy(sizePolicy)
        self.shaftOutPut_tableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.shaftOutPut_tableView.horizontalHeader().setStretchLastSection(True)
        self.shaftOutPut_tableView.resizeColumnsToContents()
        self.shaftOutPut_tableView.resizeRowsToContents()
        self.shaftOutPut_tableView.verticalHeader().hide()
        self.shaftOutPut_tableView.setFocusPolicy(QtCore.Qt.NoFocus)
        self.shaftOutPut_tableView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.keyOutPut_tableView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        hh = self.shaftOutPut_tableView.horizontalHeader()
        hh.setDefaultAlignment(QtCore.Qt.AlignCenter)
        hh.setStretchLastSection(True)
        ###
        self.keyOutPut_tableView.setAutoFillBackground(True)
        self.keyOutPut_tableView.setSizePolicy(sizePolicy)
        self.keyOutPut_tableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.keyOutPut_tableView.horizontalHeader().setStretchLastSection(True)
        self.keyOutPut_tableView.resizeColumnsToContents()
        self.keyOutPut_tableView.resizeRowsToContents()
        self.keyOutPut_tableView.verticalHeader().hide()
        self.keyOutPut_tableView.setFocusPolicy(QtCore.Qt.NoFocus)
        self.keyOutPut_tableView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.keyOutPut_tableView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        hh = self.keyOutPut_tableView.horizontalHeader()
        hh.setDefaultAlignment(QtCore.Qt.AlignCenter)
        hh.setStretchLastSection(True)
        self.keyOutPut_tableView.setShowGrid(True)
        self.shaftOutPut_tableView.setShowGrid(True)
        self.error = False

    def __threading_action_bg(self):

        self.torqueChart_widget.setStyleSheet("border: none; border-image: url(" + self.backgroundImagePath + ")")
        self.momentChart_widget.setStyleSheet("border: none; border-image: url( " + self.backgroundImagePath + ")")
        self.keyOutPut_tableView.setStyleSheet("border: none; border-image: url(" + self.backgroundImagePath + ")")
        self.shaftOutPut_tableView.setStyleSheet("border: none; border-image: url(" + self.backgroundImagePath + ")")

    def __threading_action_ShaftTable(self,
                                      Ma: float,
                                      Mm: float,
                                      Ta: float,
                                      Tm: float,
                                      Sut: float,
                                      Sy: float,
                                      r: float,
                                      D: float,
                                      d: float,
                                      Temperature: float,
                                      reliability: float,
                                      method_surface_finishing: str = "Machined or cold-drawn",
                                      diameter_attempt: float = 8e-3,
                                      error: float = 1e-5,
                                      method: str = "DE-ASME",
                                      zero: bool = False) -> None:
        """
        @Description: This function will help to thread the tables of the program.
        :return: None
        """
        shaft = sh.Shaft(Ma=Ma,
                         Mm=Mm,
                         Ta=Ta,
                         Tm=Tm,
                         Sut=Sut,
                         Sy=Sy,
                         r=r,
                         D=D,
                         d=d,
                         Temperature=Temperature,
                         reliability=reliability,
                         methodSurfaceFinish=method_surface_finishing,
                         dTrial=diameter_attempt,
                         error=error,
                         method=method)

        df = shaft.getWideTable(zero=zero)
        model = ModelShaft(df)
        self.shaftOutPut_tableView.setModel(model)

        return


    def __threading_action_keyTable(self, diameter: float, Sy: float, torque: float, zero=True) -> None:
        """
        @Description: This function will help to thread the tables of the program.
        :return: None
        """
        key = ky.Key(diameter=diameter, Sy=Sy, torque=torque, zero=zero)
        dfKey = key.getTable()[0]
        modelKey = PandasModelKey(dfKey)
        self.keyOutPut_tableView.setModel(modelKey)
        return

    def setChart(self) -> None:
        """
        @Description: here will be set the main window chart section.
        :return: None
        """
        self.chart_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.chart_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.chart_verticalLayout.addWidget(self.torqueChart_label)
        self.chart_verticalLayout.addWidget(self.torqueChart_toolbar)
        self.chart_verticalLayout.addWidget(self.torqueChart_widget)
        # self.chart_verticalLayout.addWidget(self.momentChart_label)
        self.chart_verticalLayout.addWidget(self.momentChart_toolbar)
        self.chart_verticalLayout.addWidget(self.momentChart_widget)
        self.verticalLayout_8.addLayout(self.chart_verticalLayout)
        self.horizontalLayout.addWidget(self.chart_frame)
        self.setCentralWidget(self.centralwidget)

    def setUpWindow(self) -> None:
        """
        This function will set up the main window sittings.
        """
        threading_action = threading.Thread(target=self.setAction)
        threading_font = threading.Thread(target=self.setUpFont)
        threading_icon = threading.Thread(target=self.setUpIcon)
        threading_chart = threading.Thread(target=self.setChart)
        threading_menu = threading.Thread(target=self.setMenu)
        threading_status = threading.Thread(target=self.setStatus)
        self.setInput()
        self.setShaftOutput()
        self.setKeyOutput()
        threading_name = threading.Thread(target=self.setName)
        threading_styleSheet = threading.Thread(target=self.setStyleSheet, args=[self.stringStyleSheetWindow])
        threading_action.start()
        threading_font.start()
        threading_icon.start()
        threading_chart.start()
        threading_menu.start()
        threading_status.start()
        threading_name.start()
        threading_styleSheet.start()
        threading_action.join()
        threading_font.join()
        threading_icon.join()
        threading_chart.join()
        threading_menu.join()
        threading_status.join()
        threading_name.join()
        threading_styleSheet.join()
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.controlSection(False, options=False, shaft=True, key=True, shaftAuxiliaries=True, fx=True)
        self.slope_pushButton.setEnabled(False)
        self.deflection_pushButton.setEnabled(False)
        self.setGeometry(abs(self.ScreenWidth - self.mainWindowWidth) / 2,
                         abs(self.ScreenHeight - self.mainWindowHeight) / 2,
                         self.mainWindowWidth, self.mainWindowHeight)
        self.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.setDockNestingEnabled(True)
        self.setDockOptions(QtWidgets.QMainWindow.AllowNestedDocks
                            | QtWidgets.QMainWindow.AllowTabbedDocks
                            | QtWidgets.QMainWindow.AnimatedDocks)

    def setMenu(self) -> None:
        """
        This function will set up the main window menu.
        """
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1500, 26))
        self.setMenuBar(self.menubar)

    def setStatus(self):
        """
        This function will set up the status bar.
        """
        self.setStatusBar(self.statusbar)

    def setScrollArea(self):
        """
        This function will set up the scroll able area.
        """
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input_scrollArea.sizePolicy().hasHeightForWidth())
        self.input_scrollArea.setSizePolicy(sizePolicy)
        self.input_scrollArea.setMinimumSize(QtCore.QSize(150, 500))
        self.input_scrollArea.setBaseSize(QtCore.QSize(0, 0))
        self.input_scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.input_scrollArea.setWidgetResizable(True)
        self.scrollArea_widgetContents.setGeometry(QtCore.QRect(0, 0, 417, 662))
        self.Input_frame.setMaximumSize(QtCore.QSize(2000, 2000))
        self.Input_frame.setAutoFillBackground(True)
        self.Input_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.Input_frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Input_frame.setLineWidth(1)
        self.Input_frame.setMidLineWidth(0)

    def setInputSettings(self):
        """
        This function will set up the 'input' dockWidget.
        """
        self.Input_dockWidget.setEnabled(True)
        self.Input_dockWidget.setAutoFillBackground(False)
        self.Input_dockWidget.setMaximumSize(QtCore.QSize(900, 50000))
        self.Input_dockWidget.setToolTipDuration(2)
        self.Input_dockWidget.setAccessibleName("")
        self.Input_dockWidget.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.Input_dockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        self.verticalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.input_verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.input_verticalLayout.setSpacing(7)
        self.solveForTheSafetyFactor_checkBox.stateChanged.connect(self.controlSolveForSafetyFactor)
        self.inputOptions_horizontalLayout.addWidget(self.solveForTheSafetyFactor_checkBox)

        self.solveForTheDiameter_checkBox.stateChanged.connect(self.controlSolveForDiameter)
        self.inputOptions_horizontalLayout.addWidget(self.solveForTheDiameter_checkBox)
        self.input_verticalLayout.addLayout(self.inputOptions_horizontalLayout)

    def setInputShaftTitle(self) -> None:
        """
        This function will set up the 'input' dockWidget.
        """
        font = QtGui.QFont()
        font.setFamily("Segoe MDL2 Assets")
        font.setPointSize(8)
        font.setWeight(50)
        font.setBold(True)
        self.shaftInputTitle_label.setFont(font)
        self.input_formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.shaftInputTitle_label)

    def setInputKeyTitle(self) -> None:
        """
        This function will set up the 'input' dockWidget.
        """
        font = QtGui.QFont()
        font.setFamily("Segoe MDL2 Assets")
        font.setPointSize(9)
        font.setWeight(50)
        font.setBold(True)
        self.keyTitle_label.setFont(font)
        self.input_formLayout.setWidget(14, QtWidgets.QFormLayout.LabelRole, self.keyTitle_label)

    def setCriticalPointLocation(self):
        """
        This function will set up the 'input' dockWidget.
        """
        # Critical Point Position
        self.input_formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.shaftCriticalPointLocation_label)
        self.shaftCriticalPointLocation_doubleSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.shaftCriticalPointLocation_doubleSpinBox.setDecimals(2)
        self.shaftCriticalPointLocation_doubleSpinBox.setMinimum(0.0)
        self.shaftCriticalPointLocation_doubleSpinBox.setMaximum(100000.0)
        self.input_formLayout. \
            setWidget(4, QtWidgets.QFormLayout.FieldRole, self.shaftCriticalPointLocation_doubleSpinBox)

    def setAttemptDiameter(self):
        """
        This function will set up the 'input' dockWidget.
        """
        self.input_formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.shaftAttemptDiameter_label)
        self.shaftAttemptDiameter_doubleSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.shaftAttemptDiameter_doubleSpinBox.setDecimals(2)
        self.shaftAttemptDiameter_doubleSpinBox.setMinimum(5.0)
        self.shaftAttemptDiameter_doubleSpinBox.setMaximum(254)
        self.shaftAttemptDiameter_doubleSpinBox.setToolTip("For reasons of technical standards the diameter \n"
                                                           "is limited within the range of 5 mm to 245 mm")
        self.shaftAttemptDiameter_doubleSpinBox.setStyleSheet("""QToolTip { 
                                                              background-color: #f2f2f2; 
                                                              color: black; 
                                                              border: none
                                                              }""")

        self.input_formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.shaftAttemptDiameter_doubleSpinBox)

    def setDiameter(self):
        """
        This function will set up the 'input' dockWidget.
        """
        self.input_formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.shaftDiameter_label)
        self.shaftDiameter_doubleSpinBox.setDecimals(2)
        self.shaftDiameter_doubleSpinBox.setMinimum(5.0)
        self.shaftDiameter_doubleSpinBox.setMaximum(254)
        self.shaftDiameter_doubleSpinBox.setToolTip("For reasons of technical standards the diameter \n"
                                                    "is limited within the range of 5 mm to 245 mm")
        self.shaftDiameter_doubleSpinBox.setStyleSheet("""QToolTip { 
                                                          background-color: #f2f2f2; 
                                                          color: black; 
                                                          border: none
                                                              }""")
        self.shaftDiameter_doubleSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.input_formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.shaftDiameter_doubleSpinBox)

    def setShaftLength(self):
        """
        This function will set up the 'input' dockWidget.
        """
        self.input_formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.shaftLength_label)
        self.shaftLength_doubleSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.shaftLength_doubleSpinBox.setDecimals(2)
        self.shaftLength_doubleSpinBox.setMinimum(5)
        self.shaftLength_doubleSpinBox.setMaximum(1000000.0)
        self.input_formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.shaftLength_doubleSpinBox)
        self.shaftLength_doubleSpinBox.setToolTip("The shaft's length is limited \n"
                                                  "within the range of 5 mm to 100 meters")
        self.shaftLength_doubleSpinBox.setStyleSheet("""QToolTip { 
                                                                 background-color: #f2f2f2; 
                                                                 color: black; 
                                                                border: none
                                                                            }""")

    def setShaftSafetyFactor(self):
        """
        This function will set up the 'input' dockWidget.
        """
        self.input_formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.shaftSafetyFactor_label)
        self.shaftSafetyFactor_doubleSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.shaftSafetyFactor_doubleSpinBox.setRange(0.1, 100)
        self.shaftSafetyFactor_doubleSpinBox.setValue(1)
        self.shaftSafetyFactor_doubleSpinBox.setDecimals(2)
        self.input_formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.shaftSafetyFactor_doubleSpinBox)
        self.shaftSafetyFactor_doubleSpinBox.setToolTip("The shaft's safety factor is limited \n"
                                                        "within the range of 0.1 to 100 ")
        self.shaftSafetyFactor_doubleSpinBox.setStyleSheet("""QToolTip { 
                                                                 background-color: #f2f2f2; 
                                                                 color: black; 
                                                                border: none
                                                                            }""")

    def controlSection(self, state: bool, options: bool, shaft: bool,
                       key: bool, shaftAuxiliaries: bool, fx: bool) -> None:
        """
        This function whelps to control some main window sections.
        """
        if options:
            self.solveForTheDiameter_checkBox.setCheckable(state)
            self.solveForTheSafetyFactor_checkBox.setCheckable(state)

        if shaft:
            self.shaftMaterial_label.setEnabled(state)
            self.shaftMaterialt_comboBox.setEnabled(state)
            self.shaftCriticalPointLocation_label.setEnabled(state)
            self.shaftCriticalPointLocation_doubleSpinBox.setEnabled(state)
            self.shaftAttemptDiameter_label.setEnabled(state)
            self.shaftAttemptDiameter_doubleSpinBox.setEnabled(state)
            self.shaftDiameter_label.setEnabled(state)
            self.shaftDiameter_doubleSpinBox.setEnabled(state)
            self.shaftLength_label.setEnabled(state)
            self.shaftLength_doubleSpinBox.setEnabled(state)
            self.shaftSafetyFactor_label.setEnabled(state)
            self.shaftSafetyFactor_doubleSpinBox.setEnabled(state)
            self.shaftSurfaceCondition_label.setEnabled(state)
            self.shaftSurfaceCondition_comboBox.setEnabled(state)
            self.shaftLoadType_label.setEnabled(state)
            self.shaftLoadType_comboBox.setEnabled(state)
            self.shaftTemperature_label.setEnabled(state)
            self.shaftTemperature_doubleSpinBox.setEnabled(state)
            self.shaftReliabilityt_label.setEnabled(state)
            self.shaftReliability_doubleSpinBox.setEnabled(state)
            self.shaftFailureCriteria_label.setEnabled(state)
            self.shaftFeilureCriteria_comboBox.setEnabled(state)

        if key:
            self.keyMaterial_label.setEnabled(state)
            self.keyMaterial_comboBox.setEnabled(state)
            self.keyForm_label.setEnabled(state)
            self.keyForm_comboBox.setEnabled(state)
            self.keySolveBasedOn_label.setEnabled(state)
            self.keySolveBasedOn_comboBox.setEnabled(state)
            self.keySafetyFactorForShearing_label.setEnabled(state)
            self.keySafetyFactorForShearing_doubleSpinBox.setEnabled(state)
            self.safetyFactorForCompression_label.setEnabled(state)
            self.safetyFactorForCompression_doubleSpinBox.setEnabled(state)

        if shaftAuxiliaries:
            self.bearing_pushButton.setEnabled(state)
            self.notch_pushButton.setEnabled(state)

        if fx:
            self.Fx1_pushButton.setEnabled(state)
            self.Fx2_pushButton.setEnabled(state)
            # self.resetFx_pushButton.setEnabled(state)
            self.solve_pushButton.setEnabled(state)
            self.deflection_pushButton.setEnabled(state)
            self.slope_pushButton.setEnabled(state)

    def controlSolveForDiameter(self, state: QtCore.Qt.CheckState) -> None:
        """
        This function will set up the 'input' dockWidget.
        :param state: QtCore.Qt.CheckState, state caught.
        """

        if state == QtCore.Qt.Checked:

            self.solveForTheSafetyFactor_checkBox.setChecked(False)
            self.solveForTheSafetyFactor_checkBox.setCheckable(False)
            self.controlSection(True, options=False, shaft=True, key=True, shaftAuxiliaries=True, fx=True)
            self.shaftDiameter_label.setEnabled(False)
            self.shaftDiameter_doubleSpinBox.setEnabled(False)
            self.Fx2_pushButton.setEnabled(False)
            self.solve_pushButton.setEnabled(False)
            self.slope_pushButton.setEnabled(False)
            self.deflection_pushButton.setEnabled(False)

        else:
            self.solveForTheSafetyFactor_checkBox.setCheckable(True)
            self.solveForTheSafetyFactor_checkBox.setChecked(True)
            self.controlSection(True, options=False, shaft=True, key=True, shaftAuxiliaries=True, fx=True)
            self.shaftSafetyFactor_label.setEnabled(False)
            self.shaftSafetyFactor_doubleSpinBox.setEnabled(False)
            self.shaftAttemptDiameter_label.setEnabled(False)
            self.shaftAttemptDiameter_doubleSpinBox.setEnabled(False)
            self.Fx2_pushButton.setEnabled(False)
            self.solve_pushButton.setEnabled(False)
            self.slope_pushButton.setEnabled(False)
            self.deflection_pushButton.setEnabled(False)

    def controlSolveForSafetyFactor(self, state: QtCore.Qt.CheckState) -> None:
        """
        This function will set up the 'input' dockWidget.
        :param state: QtCore.Qt.CheckState, state caught.
        """

        if state == QtCore.Qt.Checked:

            self.solveForTheDiameter_checkBox.setChecked(False)
            self.solveForTheDiameter_checkBox.setCheckable(False)
            self.controlSection(True, options=False, shaft=True, key=True, shaftAuxiliaries=True, fx=True)
            self.shaftSafetyFactor_label.setEnabled(False)
            self.shaftSafetyFactor_doubleSpinBox.setEnabled(False)
            self.shaftAttemptDiameter_label.setEnabled(False)
            self.shaftAttemptDiameter_doubleSpinBox.setEnabled(False)
            self.Fx2_pushButton.setEnabled(False)
            self.solve_pushButton.setEnabled(False)
            self.slope_pushButton.setEnabled(False)
            self.deflection_pushButton.setEnabled(False)
        else:
            self.solveForTheDiameter_checkBox.setCheckable(True)
            self.solveForTheDiameter_checkBox.setChecked(True)
            self.controlSection(True, options=False, shaft=True, key=True, shaftAuxiliaries=True, fx=True)
            self.shaftDiameter_label.setEnabled(False)
            self.shaftDiameter_doubleSpinBox.setEnabled(False)
            self.Fx2_pushButton.setEnabled(False)
            self.solve_pushButton.setEnabled(False)
            self.slope_pushButton.setEnabled(False)
            self.deflection_pushButton.setEnabled(False)

    def setShaftTemperature(self):
        """
        This function will set up the 'input' dockWidget.
        """

        self.input_formLayout.setWidget(11, QtWidgets.QFormLayout.LabelRole, self.shaftTemperature_label)
        self.shaftTemperature_doubleSpinBox.setMouseTracking(False)
        self.shaftTemperature_doubleSpinBox.setAcceptDrops(False)
        self.shaftTemperature_doubleSpinBox.setAutoFillBackground(True)
        self.shaftTemperature_doubleSpinBox.setWrapping(False)
        self.shaftTemperature_doubleSpinBox.setFrame(True)
        self.shaftTemperature_doubleSpinBox.setReadOnly(False)
        self.shaftTemperature_doubleSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.shaftTemperature_doubleSpinBox.setMinimum(20.0)
        self.shaftTemperature_doubleSpinBox.setMaximum(600.0)
        self.shaftTemperature_doubleSpinBox.setSingleStep(10.0)
        self.shaftTemperature_doubleSpinBox.setProperty("value", 20.0)
        self.input_formLayout.setWidget(11, QtWidgets.QFormLayout.FieldRole, self.shaftTemperature_doubleSpinBox)

    def setShaftReliability(self):
        """
        This function will set up the 'input' dockWidget.
        """
        self.input_formLayout.setWidget(12, QtWidgets.QFormLayout.LabelRole, self.shaftReliabilityt_label)
        self.shaftReliability_doubleSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.shaftReliability_doubleSpinBox.setDecimals(4)
        self.shaftReliability_doubleSpinBox.setMinimum(0.5)
        self.shaftReliability_doubleSpinBox.setMaximum(1.0)
        self.shaftReliability_doubleSpinBox.setSingleStep(0.0001)
        self.input_formLayout.setWidget(12, QtWidgets.QFormLayout.FieldRole, self.shaftReliability_doubleSpinBox)

    def setKeySafetyFactorForShearing(self):
        """
        This function will set up the 'input' dockWidget.
        """
        self.input_formLayout.setWidget(18, QtWidgets.QFormLayout.LabelRole, self.keySafetyFactorForShearing_label)

        self.keySafetyFactorForShearing_doubleSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.keySafetyFactorForShearing_doubleSpinBox.setRange(0.10, 100)
        self.keySafetyFactorForShearing_doubleSpinBox.setValue(1)
        self.input_formLayout. \
            setWidget(18, QtWidgets.QFormLayout.FieldRole, self.keySafetyFactorForShearing_doubleSpinBox)

    def setKeySafetyFactorForCompression(self):
        """
        This function will set up the 'input' dockWidget.
        """
        self.input_formLayout.setWidget(19, QtWidgets.QFormLayout.LabelRole, self.safetyFactorForCompression_label)

        self.safetyFactorForCompression_doubleSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.safetyFactorForCompression_doubleSpinBox.setRange(0.1, 100)
        self.safetyFactorForCompression_doubleSpinBox.setValue(1)
        self.input_formLayout. \
            setWidget(19, QtWidgets.QFormLayout.FieldRole, self.safetyFactorForCompression_doubleSpinBox)

    def setInput(self) -> None:
        """
        This function will set up the 'input' dockWidget.
        """
        self.setInputSettings()
        self.setScrollArea()
        self.setInputShaftTitle()
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.input_formLayout.setItem(1, QtWidgets.QFormLayout.FieldRole, spacerItem)
        self.setShaftMaterial()
        self.setCriticalPointLocation()
        self.setAttemptDiameter()
        self.setDiameter()
        self.setShaftLength()
        self.setShaftSafetyFactor()
        self.setShaftSurfaceCondition()
        self.setShaftLoadType()
        self.setShaftTemperature()
        self.setShaftReliability()
        self.setFailureCriteria()
        self.setInputKeyTitle()
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.input_formLayout.setItem(14, QtWidgets.QFormLayout.FieldRole, spacerItem1)
        self.setKeyMaterial()
        self.setKeyForm()
        self.setKeyBasedOn()
        self.setKeySafetyFactorForShearing()
        self.setKeySafetyFactorForCompression()
        self.input_verticalLayout.addLayout(self.input_formLayout)
        self.verticalLayout_2.addLayout(self.input_verticalLayout)
        self.notch_pushButton.clicked.connect(self.callNotch)
        self.verticalLayout_2.addWidget(self.notch_pushButton)
        self.bearing_pushButton.clicked.connect(self.callBearing)
        self.verticalLayout_2.addWidget(self.bearing_pushButton)
        self.verticalLayout_10.addWidget(self.Input_frame)
        self.input_scrollArea.setWidget(self.scrollArea_widgetContents)
        self.verticalLayout.addWidget(self.input_scrollArea)
        self.setFx()

    def setKeyBasedOn(self):
        """
        This function will set up the key methods of solution.
        """
        self.input_formLayout.setWidget(17, QtWidgets.QFormLayout.LabelRole, self.keySolveBasedOn_label)
        self.keySolveBasedOn_comboBox.addItem("")
        self.keySolveBasedOn_comboBox.addItem("")
        self.keySolveBasedOn_comboBox.addItem("")
        self.keySolveBasedOn_comboBox.setCurrentIndex(1)
        # noinspection LongLine
        self.keySolveBasedOn_comboBox.setToolTip("The chosen option will define how the data will be shown in \n"
                                                 "the key table. Example: If the option 'Force' is chosen, then \n"
                                                 "the key will show the results of the safety factor for shear \n"
                                                 "and compression based on the force generated in the shaft. \n"
                                                 "If safety factors are chosen, the force required to satisfy \n"
                                                 "the chosen factor will be defined")
        self.keySolveBasedOn_comboBox.setStyleSheet("""QToolTip { background-color: #f2f2f2; 
                                                          color: black; 
                                                          border: none
                                                                            }""")
        self.input_formLayout.setWidget(17, QtWidgets.QFormLayout.FieldRole, self.keySolveBasedOn_comboBox)

    def setKeyForm(self):
        """
        This function will set up the key form.
        """
        self.input_formLayout.setWidget(16, QtWidgets.QFormLayout.LabelRole, self.keyForm_label)
        self.keyForm_comboBox.addItem("")
        self.keyForm_comboBox.addItem("")
        self.keyForm_comboBox.addItem("")
        self.input_formLayout.setWidget(16, QtWidgets.QFormLayout.FieldRole, self.keyForm_comboBox)

    def setFailureCriteria(self):
        """
        This function will set up the shaft criteria failure.
        """
        self.input_formLayout.setWidget(13, QtWidgets.QFormLayout.LabelRole, self.shaftFailureCriteria_label)
        self.shaftFeilureCriteria_comboBox.addItem("")
        self.shaftFeilureCriteria_comboBox.addItem("")
        self.shaftFeilureCriteria_comboBox.addItem("")
        self.shaftFeilureCriteria_comboBox.addItem("")
        self.input_formLayout.setWidget(13, QtWidgets.QFormLayout.FieldRole, self.shaftFeilureCriteria_comboBox)

    def setShaftLoadType(self) -> None:
        """
        This function will set up the shaft load type.
        """
        self.input_formLayout.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.shaftLoadType_label)
        self.shaftLoadType_comboBox.addItem("")
        self.shaftLoadType_comboBox.addItem("")
        self.input_formLayout.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.shaftLoadType_comboBox)

    def setShaftSurfaceCondition(self) -> None:
        """
        This function will set up the shaft surface condition.
        """
        self.input_formLayout.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.shaftSurfaceCondition_label)
        self.shaftSurfaceCondition_comboBox.addItem("")
        self.shaftSurfaceCondition_comboBox.addItem("")
        self.shaftSurfaceCondition_comboBox.addItem("")
        self.shaftSurfaceCondition_comboBox.addItem("")
        self.input_formLayout.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.shaftSurfaceCondition_comboBox)

    def setShaftMaterial(self) -> None:
        """
        This function will set up the shaft material.
        """
        self.input_formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.shaftMaterial_label)
        self.shaftMaterialt_comboBox.setEditable(False)
        self.shaftMaterialt_comboBox.setMaxCount(2147483645)
        self.shaftMaterialt_comboBox.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        self.shaftMaterialt_comboBox.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.shaftMaterialt_comboBox.addItem("")
        self.shaftMaterialt_comboBox.addItem("")
        self.shaftMaterialt_comboBox.addItem("")
        self.shaftMaterialt_comboBox.addItem("")
        self.shaftMaterialt_comboBox.addItem("")
        self.shaftMaterialt_comboBox.addItem("")
        self.shaftMaterialt_comboBox.addItem("")
        self.shaftMaterialt_comboBox.addItem("")
        self.shaftMaterialt_comboBox.addItem("")
        self.shaftMaterialt_comboBox.addItem("")
        self.shaftMaterialt_comboBox.addItem("")
        self.shaftMaterialt_comboBox.addItem("")
        self.shaftMaterialt_comboBox.addItem("")
        self.shaftMaterialt_comboBox.addItem("")
        self.shaftMaterialt_comboBox.addItem("")
        self.shaftMaterialt_comboBox.addItem("")
        self.shaftMaterialt_comboBox.addItem("")
        self.shaftMaterialt_comboBox.addItem("")
        self.shaftMaterialt_comboBox.addItem("")
        self.shaftMaterialt_comboBox.addItem("")
        self.shaftMaterialt_comboBox.addItem("")
        self.shaftMaterialt_comboBox.addItem("")
        self.shaftMaterialt_comboBox.addItem("")
        self.shaftMaterialt_comboBox.addItem("")
        self.shaftMaterialt_comboBox.addItem("")
        self.shaftMaterialt_comboBox.addItem("")
        self.shaftMaterialt_comboBox.addItem("")
        self.shaftMaterialt_comboBox.addItem("")
        self.shaftMaterialt_comboBox.addItem("")
        self.shaftMaterialt_comboBox.addItem("")
        self.shaftMaterialt_comboBox.addItem("")
        self.shaftMaterialt_comboBox.addItem("")
        self.shaftMaterialt_comboBox.addItem("")
        self.shaftMaterialt_comboBox.addItem("")
        self.input_formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.shaftMaterialt_comboBox)

    def setKeyMaterial(self) -> None:
        """
        This function will set up the key material.
        """
        self.input_formLayout.setWidget(15, QtWidgets.QFormLayout.LabelRole, self.keyMaterial_label)
        self.keyMaterial_comboBox.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.keyMaterial_comboBox.addItem("")
        self.keyMaterial_comboBox.addItem("")
        self.keyMaterial_comboBox.addItem("")
        self.keyMaterial_comboBox.addItem("")
        self.keyMaterial_comboBox.addItem("")
        self.keyMaterial_comboBox.addItem("")
        self.keyMaterial_comboBox.addItem("")
        self.keyMaterial_comboBox.addItem("")
        self.keyMaterial_comboBox.addItem("")
        self.keyMaterial_comboBox.addItem("")
        self.keyMaterial_comboBox.addItem("")
        self.keyMaterial_comboBox.addItem("")
        self.keyMaterial_comboBox.addItem("")
        self.keyMaterial_comboBox.addItem("")
        self.keyMaterial_comboBox.addItem("")
        self.keyMaterial_comboBox.addItem("")
        self.keyMaterial_comboBox.addItem("")
        self.keyMaterial_comboBox.addItem("")
        self.keyMaterial_comboBox.addItem("")
        self.keyMaterial_comboBox.addItem("")
        self.keyMaterial_comboBox.addItem("")
        self.keyMaterial_comboBox.addItem("")
        self.keyMaterial_comboBox.addItem("")
        self.keyMaterial_comboBox.addItem("")
        self.keyMaterial_comboBox.addItem("")
        self.keyMaterial_comboBox.addItem("")
        self.keyMaterial_comboBox.addItem("")
        self.keyMaterial_comboBox.addItem("")
        self.keyMaterial_comboBox.addItem("")
        self.keyMaterial_comboBox.addItem("")
        self.keyMaterial_comboBox.addItem("")
        self.keyMaterial_comboBox.addItem("")
        self.keyMaterial_comboBox.addItem("")
        self.keyMaterial_comboBox.addItem("")
        self.keyMaterial_comboBox.setToolTip("The key material")
        self.keyMaterial_comboBox.setStyleSheet("""QToolTip { 
                                                                 background-color: #f2f2f2; 
                                                                 color: black; 
                                                                border: none
                                                                            }""")
        self.input_formLayout.setWidget(15, QtWidgets.QFormLayout.FieldRole, self.keyMaterial_comboBox)

    def setFx(self):
        """
        This function will set up the Fx forces.
        """
        self.Fx_verticalLayout.setContentsMargins(-1, 0, -1, -1)
        self.Fx1_pushButton.clicked.connect(self.callFx1)
        self.Fx_verticalLayout.addWidget(self.Fx1_pushButton)
        self.Fx2_pushButton.clicked.connect(self.callFx2)
        self.Fx_verticalLayout.addWidget(self.Fx2_pushButton)
        # self.Fx_verticalLayout.addWidget(self.resetFx_pushButton)
        self.Fx_verticalLayout.addWidget(self.solve_pushButton)
        self.solve_pushButton.clicked.connect(self.solve)

        self.Fx_horizontalLayout.setContentsMargins(0, -1, -1, -1)
        self.Fx_horizontalLayout.setSpacing(7)
        self.reactionsLEFT_formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.R1XY_label)
        self.reactionsLEFT_formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.R1XYResult_label)
        self.reactionsLEFT_formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.R2XY_label)
        self.reactionsLEFT_formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.R2XYResult_label)
        self.reactionsLEFT_formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.deflection_label)
        self.reactionsLEFT_formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.deflectionResult_label)
        self.Fx_horizontalLayout.addLayout(self.reactionsLEFT_formLayout)
        self.reactionsCENTER_formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.R1XZ_label)
        self.reactionsCENTER_formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.R1XZResult_label)
        self.reactionsCENTER_formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.R2XZLabel)
        self.reactionsCENTER_formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.R2XZResult_label)
        self.reactionsCENTER_formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.Slope_label)
        self.reactionsCENTER_formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.SlopeResult_label)
        self.Fx_horizontalLayout.addLayout(self.reactionsCENTER_formLayout)
        self.reactionsRIGHT_formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.deflectionChart_label)
        self.reactionsRIGHT_formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.deflection_pushButton)
        self.reactionsRIGHT_formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.slopeChart_label)
        self.reactionsRIGHT_formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.slope_pushButton)
        self.Fx_horizontalLayout.addLayout(self.reactionsRIGHT_formLayout)
        self.Fx_verticalLayout.addLayout(self.Fx_horizontalLayout)
        self.verticalLayout.addLayout(self.Fx_verticalLayout)
        self.Input_dockWidget.setWidget(self.input_dockWidgetContents)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.Input_dockWidget)

    def setShaftOutput(self):
        """
        This function will set up the shaft's out put dock widget.
        """
        self.shaftOutput_dockWidget.setMinimumSize(QtCore.QSize(120, 180))
        self.shaftOutput_dockWidget.setMaximumSize(QtCore.QSize(750, 870))
        self.shaftOutput_dockWidget.setFloating(False)
        self.shaftOutput_dockWidget.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable |
                                                QtWidgets.QDockWidget.DockWidgetMovable)
        self.shaftOutput_dockWidget.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.shatOutPut_verticalLayout.addWidget(self.shaftOutPut_label)
        self.shatOutPut_verticalLayout.addWidget(self.shaftOutPut_tableView)
        self.verticalLayout_5.addLayout(self.shatOutPut_verticalLayout)
        self.shaftOutput_dockWidget.setWidget(self.shaftOutPut_dockWidgetContents)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.shaftOutput_dockWidget)

    def setKeyOutput(self):
        """
        This function will set up the key's out put dock widget.
        """
        self.keyOutPut_dockWidget.setMinimumSize(QtCore.QSize(120, 180))
        self.keyOutPut_dockWidget.setMaximumSize(QtCore.QSize(750, 500))
        self.keyOutPut_dockWidget.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable |
                                              QtWidgets.QDockWidget.DockWidgetMovable)
        self.keyOutPut_dockWidget.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.keyOutPut_verticalLayout.addWidget(self.keyOutPut_label)
        self.keyOutPut_verticalLayout.addWidget(self.keyOutPut_tableView)
        self.verticalLayout_4.addLayout(self.keyOutPut_verticalLayout)
        self.keyOutPut_dockWidget.setWidget(self.keyOutPut_dockWidgetContents)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.keyOutPut_dockWidget)

    def callFx1(self) -> bool:
        """:return: None"""
        y = self.dialogFx1
        y.show()
        x = y.exec_()
        if x == QtWidgets.QDialog.Accepted:
            self.Fx2_pushButton.setEnabled(True)
            self.solve_pushButton.setEnabled(True)
            if self.dialogFx2.result() == QtWidgets.QDialog.Accepted:
                try:
                    solve2 = getChoices(self.dialogFx2)
                    torque = solve2['Forces'][0]
                    self.dialogFx1.torqueDoubleSpinBox.setValue(torque)
                    self.dialogFx1.torqueDoubleSpinBox.setToolTip("T<sub>2</sub> = " + str(torque))
                    self.dialogFx1.torqueDoubleSpinBox.setStyleSheet("""QToolTip { background-color: #f2f2f2; 
                                                          color: black; 
                                                          border: none
                                                                            }""")
                    self.error = False
                    if self.dialogFx2.powerCheckBox.isChecked():
                        self.dialogFx1.powerDoubleSpinBox.setValue(-self.dialogFx2.powerDoubleSpinBox.value())
                        self.dialogFx1.rpmDoubleSpinBox.setValue(self.dialogFx2.rpmDoubleSpinBox.value())
                        self.dialogFx1.powerDoubleSpinBox. \
                            setToolTip("Power<sub>2</sub> = " + str(self.dialogFx2.powerDoubleSpinBox.value()))
                        self.dialogFx1.powerDoubleSpinBox.setStyleSheet("""QToolTip { background-color: #f2f2f2; 
                                                          color: black; 
                                                          border: none
                                                                            }""")

                        self.dialogFx1.rpmDoubleSpinBox. \
                            setToolTip("RPM<sub>2</sub> = " + str(self.dialogFx2.rpmDoubleSpinBox.value()))
                        self.dialogFx1.rpmDoubleSpinBox.setStyleSheet("""QToolTip { background-color: #f2f2f2; 
                                                          color: black; 
                                                          border: none
                                                                            }""")
                        if self.dialogFx2.vectorsCheckBox.isChecked():
                            self.dialogFx1.torqueDoubleSpinBox.setValue(-torque)
                            self.dialogFx1.torqueDoubleSpinBox. \
                                setToolTip("T<sub>1</sub> = " + str(torque))
                            self.dialogFx1.torqueDoubleSpinBox.setStyleSheet("""QToolTip { background-color: #f2f2f2; 
                                                              color: black; 
                                                              border: none
                                                                                }""")
                            self.dialogFx1.radiusDoubleSpinBox.setToolTip("r must be equal to"
                                                                          " -T<sub>1</sub> / F<sub>tangential</sub>")
                            self.dialogFx1.radiusDoubleSpinBox.setStyleSheet("""QToolTip { background-color: #f2f2f2; 
                                                              color: black; 
                                                              border: none
                                                                                }""")
                except TypeError:
                    msg = QtWidgets.QMessageBox(self)
                    msg.setWindowTitle('Error!')
                    msg.setText("Information conflict!")
                    msg.setInformativeText("You must complete all options!")
                    msg.setIcon(QtWidgets.QMessageBox.Warning)
                    msg.exec_()
                    self.error = True
                    return False

            if self.dialogFx1.xPositionDoubleSpinBox.value() >= self.shaftLength_doubleSpinBox.value() and not \
                    self.dialogFx1.ManuallyInsertCheckBox.isChecked():
                msg = QtWidgets.QMessageBox(self)
                msg.setWindowTitle('Error!')
                msg.setText("Information conflict!")
                msg.setInformativeText("Force is outside the shaft's \n boundaries!")
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.exec_()
                return False

            return True
        return False

    def callFx2(self) -> bool:
        """:return: None"""

        if self.dialogFx1.ManuallyInsertCheckBox.isChecked():
            msg = QtWidgets.QMessageBox(self)
            msg.setWindowTitle('Error!')
            msg.setText("Information conflict!                                ")
            msg.setInformativeText("Manually insert just can be inserted Once!")
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.exec_()
            return False
        else:

            if self.dialogFx1.result() == QtWidgets.QDialog.Accepted:
                try:
                    solve1 = getChoices(self.dialogFx1)
                    torque = solve1['Forces'][0]
                    self.dialogFx2.torqueDoubleSpinBox.setValue(-torque)
                    self.error = False
                    self.dialogFx2.torqueDoubleSpinBox.setToolTip("T<sub>1</sub> = " + str(torque))
                    self.dialogFx2.torqueDoubleSpinBox.setStyleSheet("""QToolTip { background-color: #f2f2f2; 
                                                          color: black; 
                                                          border: none
                                                                            }""")
                    if self.dialogFx1.powerCheckBox.isChecked():
                        self.dialogFx2.powerDoubleSpinBox.setValue(-self.dialogFx1.powerDoubleSpinBox.value())
                        self.dialogFx2.rpmDoubleSpinBox.setValue(self.dialogFx1.rpmDoubleSpinBox.value())
                        self.dialogFx2.powerDoubleSpinBox. \
                            setToolTip("Power<sub>1</sub> = " + str(self.dialogFx1.powerDoubleSpinBox.value()))
                        self.dialogFx2.powerDoubleSpinBox.setStyleSheet("""QToolTip { background-color: #f2f2f2; 
                                                          color: black; 
                                                          border: none
                                                                            }""")

                        self.dialogFx2.rpmDoubleSpinBox. \
                            setToolTip("RPM<sub>1</sub> = " + str(self.dialogFx1.rpmDoubleSpinBox.value()))
                        self.dialogFx2.rpmDoubleSpinBox.setStyleSheet("""QToolTip { background-color: #f2f2f2; 
                                                          color: black; 
                                                          border: none
                                                                            }""")

                    if self.dialogFx1.vectorsCheckBox.isChecked():
                        self.dialogFx2.torqueDoubleSpinBox.setValue(-torque)
                        self.dialogFx2.torqueDoubleSpinBox. \
                            setToolTip("T<sub>1</sub> = " + str(torque))
                        self.dialogFx2.torqueDoubleSpinBox.setStyleSheet("""QToolTip { background-color: #f2f2f2; 
                                                          color: black; 
                                                          border: none
                                                                            }""")
                        self.dialogFx2.radiusDoubleSpinBox.setToolTip("r must be equal to"
                                                                      " -T<sub>1</sub> / F<sub>tangential</sub> * 10^3")
                        self.dialogFx2.radiusDoubleSpinBox.setStyleSheet("""QToolTip { background-color: #f2f2f2; 
                                                          color: black; 
                                                          border: none
                                                                            }""")



                except TypeError:
                    msg = QtWidgets.QMessageBox(self)
                    msg.setWindowTitle('Error!')
                    msg.setText("Information conflict!")
                    msg.setInformativeText("You must complete all options!")
                    msg.setIcon(QtWidgets.QMessageBox.Warning)
                    msg.exec_()
                    self.error = True
                    return False
            y = self.dialogFx2
            y.show()
            x = y.exec_()
            if x == QtWidgets.QDialog.Accepted:

                try:
                    solve1 = getChoices(self.dialogFx1)
                    solve2 = getChoices(self.dialogFx2)
                    self.error = False
                    if round(solve1['Forces'][0], 1) != -round(solve2['Forces'][0], 1):
                        msg = QtWidgets.QMessageBox(self)
                        msg.setWindowTitle('Error!')
                        msg.setText("Information conflict!                                                  ")
                        msg.setInformativeText("Torques must have the same absolute value. And opposite signs"
                                               "\n The values provided were:"
                                               "\n T1 = " + str(round(solve1['Forces'][0], 2)) +
                                               " [Nm]  \n T2 = " + str(round(solve2['Forces'][0], 2)) + " [Nm]. ")
                        msg.setIcon(QtWidgets.QMessageBox.Warning)
                        msg.exec_()

                        return False
                except TypeError:
                    msg = QtWidgets.QMessageBox(self)
                    msg.setWindowTitle('Error!')
                    msg.setText("Information conflict!")
                    msg.setInformativeText("You must complete all options!")
                    msg.setIcon(QtWidgets.QMessageBox.Warning)
                    msg.exec_()
                    self.error = True
                    return False

                if self.dialogFx2.xPositionDoubleSpinBox.value() >= self.shaftLength_doubleSpinBox.value() and not \
                        self.dialogFx2.ManuallyInsertCheckBox.isChecked():
                    msg = QtWidgets.QMessageBox(self)
                    msg.setWindowTitle('Error!')
                    msg.setText("Information conflict!")
                    msg.setInformativeText("Force is outside the shaft's  boundaries!")
                    msg.setIcon(QtWidgets.QMessageBox.Warning)
                    msg.exec_()
                    return False

                return True

            return False

    def callBearing(self):
        """:return: None"""
        # noinspection PyUnusedLocal
        x = self.bearingX
        x.show()
        self.bearing_var = x.exec_()
        if self.bearing_var == QtWidgets.QDialog.Accepted:
            if self.bearingX.bearingFirstBearingPositionDoubleSpinBox.value() == \
                    self.bearingX.bearingSecondBearingPositionDoubleSpinBox.value():
                msg = QtWidgets.QMessageBox(self)
                msg.setWindowTitle('Error!')
                msg.setText("Information conflict!                            ")
                msg.setInformativeText("Bearing can not overlay same position!")
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.exec_()
                return False

            if self.bearingX.bearingFirstBearingPositionDoubleSpinBox.value() \
                    > self.shaftLength_doubleSpinBox.value() \
                    or self.bearingX.bearingSecondBearingPositionDoubleSpinBox.value() \
                    > self.shaftLength_doubleSpinBox.value():
                msg = QtWidgets.QMessageBox(self)
                msg.setWindowTitle('Error!')
                msg.setText("Information conflict!                            ")
                msg.setInformativeText("Bearing is outside shaft's boundaries!")
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.exec_()
                return False

            return True
        return False

    def callNotch(self):
        """:return: None"""
        # noinspection PyUnusedLocal
        x = self.notchX
        if self.solveForTheSafetyFactor_checkBox.isChecked():
            self.notchX.setShaftDiameter(self.shaftDiameter_doubleSpinBox.value())
        else:
            self.notchX.setShaftDiameter(self.shaftAttemptDiameter_doubleSpinBox.value())
        x.show()
        self.notch_var = x.exec_()
        if self.notch_var == QtWidgets.QDialog.Accepted:
            try:
                float(self.notchX.KtChosenValue_label.text())
            except ValueError:
                msg = QtWidgets.QMessageBox(self)
                msg.setWindowTitle("Error!")
                msg.setText("Information conflict!                    ")
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setStyleSheet("QMessageBox {background-color: #f2f2f2; min-width: 100em} ")
                msg.setText("You must set a value for  Kt and Kts!")
                # noinspection PyUnusedLocal
                x = msg.exec_()
                self.slope_pushButton.setEnabled(False)
                self.deflection_pushButton.setEnabled(False)
                return False
            return True
        return False

    def solve(self):
        """
        This function will set up the main window sittings.
        """
        if self.solveForTheDiameter_checkBox.isChecked():
            safetyFactor = float(self.shaftSafetyFactor_doubleSpinBox.value())
            diameter = None
            diameterTrial = float(self.shaftAttemptDiameter_doubleSpinBox.value()) * 1e-3

        else:
            safetyFactor = None
            diameter = float(self.shaftDiameter_doubleSpinBox.value()) * 1e-3
            diameterTrial = 1e-2
        # material
        keyMaterial = self.keyMaterial_comboBox.currentText()
        shaftMaterial = self.shaftMaterialt_comboBox.currentText()
        # Point od Analyses
        point_of_analyses = float(self.shaftCriticalPointLocation_doubleSpinBox.value()) * 1e-3
        # Length
        length = float(self.shaftLength_doubleSpinBox.value()) * 1e-3
        # Temperature
        Temperature = float(self.shaftTemperature_doubleSpinBox.value())
        # Reliability
        reliability = float(self.shaftReliability_doubleSpinBox.value())
        # Load Type
        loadType = self.shaftLoadType_comboBox.currentText()
        # Finish SurFace
        finishingSurface = self.shaftSurfaceCondition_comboBox.currentText()
        # Method
        method = self.shaftFeilureCriteria_comboBox.currentText()
        keyForm = self.keyForm_comboBox.currentText()

        try:
            float(self.notchX.KtChosenValue_label.text())
        except ValueError:
            msg = QtWidgets.QMessageBox(self)
            msg.setWindowTitle("Error!")
            msg.setText("Information conflict!                    ")
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setStyleSheet("QMessageBox {background-color: #f2f2f2; min-width: 100em} ")
            msg.setText("You must set a value for  Kt and Kts!")
            # noinspection PyUnusedLocal
            x = msg.exec_()
            self.slope_pushButton.setEnabled(False)
            self.deflection_pushButton.setEnabled(False)
            return False



        if self.keySolveBasedOn_comboBox.currentText() == "Safety factor for shearing":
            keySafetyFactor_shearing = float(self.keySafetyFactorForShearing_doubleSpinBox.value())
            keySafetyFactor_compression = None

        elif self.keySolveBasedOn_comboBox.currentText() == "Safety factor for compression":
            keySafetyFactor_shearing = None
            keySafetyFactor_compression = float(self.safetyFactorForCompression_doubleSpinBox.value())

        else:
            keySafetyFactor_shearing = None
            keySafetyFactor_compression = None

        if self.notch_var == QtWidgets.QDialog.Accepted:
            r = self.notchX.r_doubleSpinBox.value() * 1e-3
            notch_type = self.notchX.comboBox.currentText()
            if self.notchX.comboBox.currentText() == "stepped bar" or \
                    self.notchX.comboBox.currentText() == "circumferential groove":
                D = self.notchX.D_doubleSpinBox.value() * 1e-3
                Kt = None
                Kts = None
            else:
                D = None
                Kt = self.notchX.Kt
                Kts = self.notchX.Kts
        else:

            msg = QtWidgets.QMessageBox(self)
            msg.setWindowTitle("Error!")
            msg.setText("Information conflict!                    ")
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setStyleSheet("QMessageBox {background-color: #f2f2f2; min-width: 100em} ")
            msg.setText("You must accept the notch's dialog!")
            # noinspection PyUnusedLocal
            x = msg.exec_()
            self.slope_pushButton.setEnabled(False)
            self.deflection_pushButton.setEnabled(False)
            return False

        ################################################################################################################
        if not self.dialogFx1.ManuallyInsertCheckBox.isChecked():

            A = self.shaftLength_doubleSpinBox.value() <= self.dialogFx1.xPositionDoubleSpinBox.value()
            B = self.shaftLength_doubleSpinBox.value() <= self.dialogFx2.xPositionDoubleSpinBox.value()
            if self.bearing_var == QtWidgets.QDialog.Accepted:
                bearing1 = self.bearingX.bearingFirstBearingPositionDoubleSpinBox.value() * 1e-3
                bearing2 = self.bearingX.bearingSecondBearingPositionDoubleSpinBox.value() * 1e-3


            else:
                msg = QtWidgets.QMessageBox(self)
                msg.setWindowTitle("Error!")
                msg.setText("Information conflict!                    ")
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setStyleSheet("QMessageBox {background-color: #f2f2f2; min-width: 100em} ")
                msg.setText("You must defines the bearings location!")
                # noinspection PyUnusedLocal
                x = msg.exec_()
                self.slope_pushButton.setEnabled(False)
                self.deflection_pushButton.setEnabled(False)
                return False
            if self.dialogFx1.xPositionDoubleSpinBox.value() == self.dialogFx2.xPositionDoubleSpinBox.value():
                msg = QtWidgets.QMessageBox(self)
                msg.setWindowTitle("Error!")
                msg.setText("Information conflict!                    ")
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setStyleSheet("QMessageBox {background-color: #f2f2f2; min-width: 100em} ")
                msg.setText("F<sub>1</sub> position can not be equal to F<sub>2</sub> position!")
                # noinspection PyUnusedLocal
                x = msg.exec_()
                return False

            if self.shaftCriticalPointLocation_doubleSpinBox.value() == 0.0:
                msg = QtWidgets.QMessageBox(self)
                msg.setWindowTitle("Error!")
                msg.setText("Information conflict!                                ")
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setStyleSheet("QMessageBox {background-color: #f2f2f2; min-width: 100em} ")
                msg.setText("Critical Point location can not be in zero position!")
                # noinspection PyUnusedLocal
                x = msg.exec_()
                self.slope_pushButton.setEnabled(False)
                self.deflection_pushButton.setEnabled(False)
                return False

            if self.dialogFx1.xPositionDoubleSpinBox.value() >= self.shaftLength_doubleSpinBox.value() or \
                    self.dialogFx2.xPositionDoubleSpinBox.value() >= self.shaftLength_doubleSpinBox.value():
                msg = QtWidgets.QMessageBox(self)
                msg.setWindowTitle('Error!')
                msg.setText("Information conflict!                       ")
                msg.setInformativeText("The force is outside the borders!")
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.exec_()
                return False

            try:
                solve1 = getChoices(self.dialogFx1)
                solve2 = getChoices(self.dialogFx2)

                if round(solve1['Forces'][0], 1) != -round(solve2['Forces'][0], 1):
                    msg = QtWidgets.QMessageBox(self)
                    msg.setWindowTitle('Error!')
                    msg.setText("Information conflict!                                                   ")
                    msg.setInformativeText("Torques must have the same absolute value. And opposite signs"
                                           "\n The values provided were:"
                                           "\n T1 = " + str(round(solve1['Forces'][0], 2)) +
                                           " [N]  \n T2 = " + str(round(solve2['Forces'][0], 2)) + " [N]. ")
                    msg.setIcon(QtWidgets.QMessageBox.Warning)
                    msg.exec_()
                    return False

            except TypeError:
                msg = QtWidgets.QMessageBox(self)
                msg.setWindowTitle('Error!')
                msg.setText("Information conflict!")
                msg.setInformativeText("You must complete all options!")
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.exec_()
                return False

            if self.bearingX.bearingFirstBearingPositionDoubleSpinBox.value() \
                    > self.shaftLength_doubleSpinBox.value() \
                    or self.bearingX.bearingSecondBearingPositionDoubleSpinBox.value() \
                    > self.shaftLength_doubleSpinBox.value():
                msg = QtWidgets.QMessageBox(self)
                msg.setWindowTitle('Error!')
                msg.setText("Information conflict!                            ")
                msg.setInformativeText("Bearing is outside shaft's boundaries!")
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.exec_()
                return False

            if self.bearingX.bearingFirstBearingPositionDoubleSpinBox.value() == \
                    self.bearingX.bearingSecondBearingPositionDoubleSpinBox.value():
                msg = QtWidgets.QMessageBox(self)
                msg.setWindowTitle('Error!')
                msg.setStyleSheet("QMessageBox {background-color: #f2f2f2; min-width: 100em} ")
                msg.setText("Information conflict!                            ")
                msg.setInformativeText("Bearing can not overlay same position!")
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.exec_()

                return False
            if self.error:
                msg = QtWidgets.QMessageBox(self)
                msg.setWindowTitle("Error!")
                msg.setStyleSheet("QMessageBox {background-color: #f2f2f2; min-width: 100em} ")
                msg.setText("Information missing!                                 ")
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setInformativeText("To proceed, You must complete all options!")
                # noinspection PyUnusedLocal
                x = msg.exec_()
                self.slope_pushButton.setEnabled(False)
                self.deflection_pushButton.setEnabled(False)
                return False

            if A and B:
                msg = QtWidgets.QMessageBox(self)
                msg.setWindowTitle("Error!")
                msg.setText("Information conflict!                                                                   ")
                msg.setStyleSheet("QMessageBox {background-color: #f2f2f2; min-width: 100em} ")
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setInformativeText("To proceed, you must adjust the position of the forces into the shaft length!")
                # noinspection PyUnusedLocal
                x = msg.exec_()
                self.slope_pushButton.setEnabled(False)
                self.deflection_pushButton.setEnabled(False)
                return False

            if self.shaftLength_doubleSpinBox.value() <= self.shaftCriticalPointLocation_doubleSpinBox.value():
                msg = QtWidgets.QMessageBox(self)
                msg.setWindowTitle("Error!")
                msg.setText("Information conflict!                                     ")
                msg.setStyleSheet("QMessageBox {background-color: #f2f2f2; min-width: 100em} ")
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setInformativeText("Critical Point Location is outside the borders!")
                # noinspection PyUnusedLocal
                x = msg.exec_()
                self.slope_pushButton.setEnabled(False)
                self.deflection_pushButton.setEnabled(False)
                return False

            # noinspection PyUnreachableCode

            bearing1 = self.bearingX.bearingFirstBearingPositionDoubleSpinBox.value() * 1e-3
            bearing2 = self.bearingX.bearingSecondBearingPositionDoubleSpinBox.value() * 1e-3
            bearing = [float(bearing1), float(bearing2)]
            solution = Solver(parent=self,
                              dialog1=self.dialogFx1,
                              dialog2=self.dialogFx2,
                              shaft_material=shaftMaterial,
                              key_material=keyMaterial,
                              length=length,
                              bearing=bearing,
                              point_of_analyses=point_of_analyses,
                              Temperature=Temperature,
                              reliability=reliability,
                              notchR=r,
                              D=D,
                              Kt=Kt,
                              Kts=Kts,
                              d=diameter,
                              safety_factor=safetyFactor,
                              finishing_surface=finishingSurface,
                              load=loadType,
                              method=method,
                              notch_type=notch_type,
                              keySafetyFactor_shearing=keySafetyFactor_shearing,
                              keyForm=keyForm,
                              keySafetyFactor_compression=keySafetyFactor_compression,
                              diameterTrial=diameterTrial)
            reactions = solution.solutionBeam.getReactionLoads()
            R1XY = float(reactions[list(reactions.keys())[0]])
            R1XZ = float(reactions[list(reactions.keys())[1]])
            R2XY = float(reactions[list(reactions.keys())[2]])
            R2XZ = float(reactions[list(reactions.keys())[3]])
            deflect = \
                solution.solutionBeam.getTotalDeflection(second_moment_of_area=solution.shaft.getSecondMomentOfArea())
            slope = solution.solutionBeam.getMaxSlope(second_moment_of_area=solution.shaft.getSecondMomentOfArea())
            self.deflectionResult_label.setText("{:.2f} mm".format(deflect * 1e3))
            self.SlopeResult_label.setText("{:.2f} mrad".format(slope * 1e3))
            self.R1XYResult_label.setText("{:.2f}".format(R1XY))
            self.R2XYResult_label.setText("{:.2f}".format(R2XY))
            self.R1XZResult_label.setText("{:.2f}".format(R1XZ))
            self.R2XZResult_label.setText("{:.2f}".format(R2XZ))
            # noinspection LongLine
            threading_torqueChart = threading.Thread(target=self.__threading_action_torqueChart,
                                                     args=[solution, length])
            threading_momentChart = threading.Thread(target=self.__threading_action_momentChart,
                                                     args=[solution])

            threading_torqueChart.start()
            threading_momentChart.start()
            threading_momentChart.join()
            threading_torqueChart.join()


            self.slope_pushButton.setEnabled(True)
            self.deflection_pushButton.setEnabled(True)
            deflection_dialog = DeflectionDialog(beam_var=solution.solutionBeam, shaft_var=solution.shaft)
            self.deflection_pushButton.clicked.connect(self.__makeCallDeflectionChart(deflection_dialog))
            slope_dialog = SlopeDialog(beam_var=solution.solutionBeam, shaft_var=solution.shaft)
            self.slope_pushButton.clicked.connect(self.__makeCallSlopeChart(slope_dialog))



        else:

            Ma = float(self.dialogFx1.Ma_DoubleSpinBox.value())
            Mm = float(self.dialogFx1.Mm_DoubleSpinBox.value())
            Ta = float(self.dialogFx1.Ta_DoubleSpinBox.value())
            Tm = float(self.dialogFx1.Tm_DoubleSpinBox.value())
            R1XY = R1XZ = R2XY = R2XZ = "Not calculated"
            self.R1XYResult_label.setText(str(R1XY))
            self.R2XYResult_label.setText(str(R2XY))
            self.R1XZResult_label.setText(str(R1XZ))
            self.R2XZResult_label.setText(str(R2XZ))

            solution = SolverForManuallyIsChecked(parent=self,
                                                  Ma=Ma,
                                                  Mm=Mm,
                                                  Ta=Ta,
                                                  Tm=Tm,
                                                  shaft_material=shaftMaterial,
                                                  key_material=keyMaterial,
                                                  length=length,
                                                  Temperature=Temperature,
                                                  reliability=reliability,
                                                  notchR=r,
                                                  D=D,
                                                  Kt=Kt,
                                                  Kts=Kts,
                                                  d=diameter,
                                                  safety_factor=safetyFactor,
                                                  finishing_surface=finishingSurface,
                                                  load=loadType,
                                                  method=method,
                                                  notch_type=notch_type,
                                                  keySafetyFactor_shearing=keySafetyFactor_shearing,
                                                  keyForm=keyForm,
                                                  keySafetyFactor_compression=keySafetyFactor_compression,
                                                  diameterTrial=diameterTrial)
            self.slope_pushButton.setEnabled(False)
            self.deflection_pushButton.setEnabled(False)

        ################################################################################################################
        #                         Solve For The Diameter or Solve For The Safety Factor
        ################################################################################################################

        # ##################
        # Solve for the key.
        # ##################
        threading_keyTable_solver = threading.Thread(target=self.__threading_action_keyTable_solver, args=[solution])
        threading_keyTable_solver.start()
        threading_shaftTable_solver = \
            threading.Thread(target=self.__threading_action_shaftTable_solver, args=[solution])
        threading_shaftTable_solver.start()
        threading_keyTable_solver.join()
        threading_shaftTable_solver.join()
        return True



    def __threading_action_momentChart(self, solution: Solver):
        self.momentChart_widget.update_figure(domain=solution.solutionBeam.getPlotBendingMoment()['x'],
                                              XY=solution.solutionBeam.getPlotBendingMoment()['XY'],
                                              XZ=solution.solutionBeam.getPlotBendingMoment()['XZ'],
                                              TOTAL=solution.solutionBeam.getPlotBendingMoment()['TOTAL'])

    def __threading_action_torqueChart(self, solution: Solver, length: float) -> None:
        self.torqueChart_widget.update_figure(domain=solution.solutionBeam.getPlotTorque()['x'],
                                              image=solution.solutionBeam.getPlotTorque()['torque'],
                                              length=length)

    def __threading_action_shaftTable_solver(self, solution: Union[Solver, SolverForManuallyIsChecked]):
        model = ModelShaft(solution.shaft.getWideTable())
        self.shaftOutPut_tableView.setModel(model)
        self.shaftOutPut_tableView.setStyleSheet("border: none; border-image: url(" + self.backgroundImagePath + ")")

    def __threading_action_keyTable_solver(self, solution: Union[Solver, SolverForManuallyIsChecked]):
        keyTable = solution.key.getTable()[0]
        keyTable_info = solution.key.getTable()[1]
        keyModel = PandasModelKey(keyTable, shaft_safety_factor=solution.shaft.getSafetyFactor())
        self.keyOutPut_tableView.setModel(keyModel)
        self.keyOutPut_tableView.setStatusTip("Breite (width) = " + str(keyTable_info.iloc[0, 0]) +
                                              " Höhe (height) = " + str(keyTable_info.iloc[0, 1]) +
                                              " Tiefe (deep) = " + str(keyTable_info.iloc[0, 2]))
        self.keyOutPut_tableView.setToolTip("Breite (width) = " + str(keyTable_info.iloc[0, 0]) +
                                            " Höhe (height) = " + str(keyTable_info.iloc[0, 1]) +
                                            " Tiefe<sub>Eins</sub> (deep<sub>One</sub>) = " +
                                            str(keyTable_info.iloc[0, 2]))

        self.keyOutPut_tableView.setStyleSheet("""QToolTip { 
                                               background-color: #f2f2f2; 
                                               color: black; 
                                               border: none
                                               }""")
        self.keyOutPut_tableView.setStyleSheet("QTableView {border: none; border-image: "
                                               "url(" + self.backgroundImagePath + ")}")

    @staticmethod
    def __makeCallSlopeChart(slope_dialog: SlopeDialog):
        """:return: boolean"""

        def callSlopeChart():
            """
            :return: Dialog
            """
            # noinspection PyUnusedLocal
            x = slope_dialog
            x.show()
            x.exec_()

        return callSlopeChart

    @staticmethod
    def __makeCallDeflectionChart(deflection_dialog: DeflectionDialog):
        """:return: boolean"""

        def callDeflectionChart():
            """
            :return: Dialog
            """
            # noinspection PyUnusedLocal
            x = deflection_dialog
            x.show()
            x.exec_()

        return callDeflectionChart

    def setAction(self) -> None:
        """
        This function will set up the actions in the dialog window.
        :return: None
        """

        self.actionQuit.setText("Quit")
        self.actionQuit.setShortcut('Ctrl+Q')
        self.actionQuit.setStatusTip("Quit the application!")
        self.actionQuit.triggered.connect(self.closeQApp)
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

    def closeQApp(self):
        """
        :return: None.
        """
        choice = QtWidgets.QMessageBox.question(self,
                                                "Quit Application!",
                                                "Are you sure you want to quit the application?",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        if choice == QtWidgets.QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def styleWindow(self):

        styles = QtWidgets.QStyleFactory.keys()

    def setUpFont(self) -> None:
        """
        This function will set up the font to be used in the dialog window.
        :return: None
        """
        self.fontStyle.setFamily("Segoe MDL2 Assets")
        self.fontStyle.setPointSize(8)
        self.setFont(self.fontStyle)

    def setUpIcon(self) -> None:
        """
        This function provides the first two check box of the dialog window.
        :return: None
        """
        icon = QtGui.QIcon(self.iconPath)
        self.setWindowIcon(icon)

    def retranslateUi(self) -> None:
        """:return: None"""

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "ShaftEx"))
        # self.torqueChart_label.setText(_translate("MainWindow", "Torque Chart"))
        # self.momentChart_label.setText(_translate("MainWindow", "Moment chart"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))

        self.Input_dockWidget.setToolTip(_translate("MainWindow", "Input values"))
        self.Input_dockWidget.setStatusTip(_translate("MainWindow", "Input values"))
        self.Input_dockWidget.setWindowTitle(_translate("MainWindow", "Input values"))
        self.solveForTheSafetyFactor_checkBox.setText(_translate("MainWindow", "Solve For the Safety Factor"))
        self.solveForTheDiameter_checkBox.setText(_translate("MainWindow", "Solve For the Diameter"))
        self.shaftInputTitle_label.setText(_translate("MainWindow", "Shaft "))
        self.shaftMaterial_label.setText(_translate("MainWindow", "Material"))
        self.shaftMaterialt_comboBox.setItemText(0, _translate("MainWindow", "AISI 1020 Steel,"
                                                                             " annealed at 870°C (1600°F)"))

        self.shaftMaterialt_comboBox.setItemText(1, _translate("MainWindow", "AISI 1030 Steel, cold drawn,"
                                                                             " 19-32 mm (0.75-1.25 in) round"))

        self.shaftMaterialt_comboBox.setItemText(2, _translate("MainWindow", "AISI 1030 Steel, as rolled"))
        self.shaftMaterialt_comboBox.setItemText(3, _translate("MainWindow", "AISI 1030 Steel,"
                                                                             " normalized 925°C (1700°F)"))

        self.shaftMaterialt_comboBox.setItemText(4, _translate("MainWindow", "AISI 1030 Steel,"
                                                                             " annealed at 845°C (1550°F)"))

        self.shaftMaterialt_comboBox.setItemText(5, _translate("MainWindow", "AISI 1035 Steel,"
                                                                             " as rolled,"
                                                                             " 19-32 mm (0.75-1.25 in) round"))

        self.shaftMaterialt_comboBox.setItemText(6, _translate("MainWindow", "AISI 1035 Steel,"
                                                                             " cold drawn,"
                                                                             " 19-32 mm (0.75-1.25 in) round"))

        self.shaftMaterialt_comboBox.setItemText(7, _translate("MainWindow", "AISI 1037 Steel,"
                                                                             " Hot Rolled Bar (UNS G10370)"))

        self.shaftMaterialt_comboBox.setItemText(8, _translate("MainWindow", "AISI 1037 Steel,"
                                                                             " Cold Drawn Bar (UNS G10370)"))

        self.shaftMaterialt_comboBox.setItemText(9, _translate("MainWindow", "AISI 1040 Steel,"
                                                                             " hot rolled,"
                                                                             " 19-32 mm (0.75-1.25 in) round"))

        self.shaftMaterialt_comboBox.setItemText(10, _translate("MainWindow", "AISI 1040 Steel,"
                                                                              " as cold drawn,"
                                                                              " 16-22 mm (0.625-0.875 in) round"))

        self.shaftMaterialt_comboBox.setItemText(11, _translate("MainWindow", "AISI 1040 Steel,"
                                                                              " as cold drawn,"
                                                                              " 22-32 mm (0.875-1.25 in) round"))

        self.shaftMaterialt_comboBox.setItemText(12, _translate("MainWindow", "AISI 1040 Steel,"
                                                                              " as cold drawn,"
                                                                              " 32-50 mm (1.25-2 in) round"))

        self.shaftMaterialt_comboBox.setItemText(13, _translate("MainWindow", "AISI 1040 Steel,"
                                                                              " as cold drawn, "
                                                                              "50-75 mm (2-3 in) round"))

        self.shaftMaterialt_comboBox.setItemText(14, _translate("MainWindow", "AISI 1040 Steel,"
                                                                              " as rolled"))

        self.shaftMaterialt_comboBox.setItemText(15, _translate("MainWindow", "AISI 1040 Steel,"
                                                                              " normalized at 900°C (1650°F)"))

        self.shaftMaterialt_comboBox.setItemText(16, _translate("MainWindow", "AISI 1040 Steel,"
                                                                              " annealed at 790°C (1450°F)"))

        self.shaftMaterialt_comboBox.setItemText(17, _translate("MainWindow", "AISI 1040 Steel,"
                                                                              " normalized at 900°C (1650°F),"
                                                                              " air cooled, 13 mm (0.5 in.) round"))

        self.shaftMaterialt_comboBox.setItemText(18, _translate("MainWindow", "AISI 1040 Steel,"
                                                                              " normalized at 900°C (1650°F),"
                                                                              " air cooled, 25 mm (1 in.) round"))

        self.shaftMaterialt_comboBox.setItemText(19, _translate("MainWindow", "AISI 1040 Steel,"
                                                                              " normalized at 900°C (1650°F),"
                                                                              " air cooled, 50 mm (2 in.) round"))

        self.shaftMaterialt_comboBox.setItemText(20, _translate("MainWindow", "AISI 1040 Steel,"
                                                                              " normalized at 900°C (1650°F),"
                                                                              " air cooled, 100 mm (4 in.) round"))

        self.shaftMaterialt_comboBox.setItemText(21, _translate("MainWindow", "AISI 1040 Steel,"
                                                                              " oil quenched from 855°C (1570°F),"
                                                                              " 540°C (1000°F) temper,"
                                                                              " 13 mm (0.5 in.) round"))

        self.shaftMaterialt_comboBox.setItemText(22, _translate("MainWindow", "AISI 1040 Steel,"
                                                                              " oil quenched from 855°C (1570°F),"
                                                                              " 540°C (1000°F) temper,"
                                                                              " 25 mm (1 in.) round"))

        self.shaftMaterialt_comboBox.setItemText(23, _translate("MainWindow", "AISI 1040 Steel,"
                                                                              " oil quenched from 855°C (1570°F),"
                                                                              " 540°C (1000°F) temper,"
                                                                              " 50 mm (2 in.) round"))

        self.shaftMaterialt_comboBox.setItemText(24, _translate("MainWindow", "AISI 1040 Steel,"
                                                                              " oil quenched from 855°C (1570°F),"
                                                                              " 540°C (1000°F) temper,"
                                                                              " 100 mm (4 in.) round"))

        self.shaftMaterialt_comboBox.setItemText(25, _translate("MainWindow", "AISI 1042 Steel,"
                                                                              " Hot Rolled Bar (UNS G10420)"))

        self.shaftMaterialt_comboBox.setItemText(26, _translate("MainWindow", "AISI 1042 Steel,"
                                                                              " Cold Drawn Bar (UNS G10420)"))

        self.shaftMaterialt_comboBox.setItemText(27, _translate("MainWindow", "AISI 1050 Steel,"
                                                                              " cold drawn,"
                                                                              " 19-32 mm (0.75-1.25 in) round"))

        self.shaftMaterialt_comboBox.setItemText(28, _translate("MainWindow", "AISI 1050 Steel,"
                                                                              " cold drawn, annealed,"
                                                                              " 19-32 mm (0.75-1.25 in) round"))

        self.shaftMaterialt_comboBox.setItemText(29, _translate("MainWindow", "AISI 1050 Steel,"
                                                                              " cold drawn,"
                                                                              " low temperature,"
                                                                              " stress relieved,"
                                                                              " 16-22 mm (0.625-0.875 in) round"))

        self.shaftMaterialt_comboBox.setItemText(30, _translate("MainWindow", "AISI 1050 Steel,"
                                                                              " cold drawn,"
                                                                              " high temperature,"
                                                                              " stress relieved,"
                                                                              " 16-22 mm (0.625-0.875 in) round"))

        self.shaftMaterialt_comboBox.setItemText(31, _translate("MainWindow", "AISI 1050 Steel,"
                                                                              " as rolled"))

        self.shaftMaterialt_comboBox.setItemText(32, _translate("MainWindow", "AISI 1050 Steel,"
                                                                              " normalized at 900°C (1650°F)"))

        self.shaftMaterialt_comboBox.setItemText(33, _translate("MainWindow", "AISI 1050 Steel,"
                                                                              " annealed at 790°C (1450°F)"))

        self.shaftCriticalPointLocation_label.setText(_translate("MainWindow", "Critical Point Location  [mm]  "))
        self.shaftAttemptDiameter_label.setText(_translate("MainWindow", "Attempt Diameter  [mm]"))
        self.shaftDiameter_label.setText(_translate("MainWindow", "Diameter  [mm]"))
        self.shaftLength_label.setText(_translate("MainWindow", "Shaft Length [mm]"))
        self.shaftSafetyFactor_label.setText(_translate("MainWindow", "Safety Factor"))
        self.shaftSurfaceCondition_label.setText(_translate("MainWindow", "Surface Condition"))
        self.shaftSurfaceCondition_comboBox.setItemText(0, _translate("MainWindow", "As-forged"))
        self.shaftSurfaceCondition_comboBox.setItemText(1, _translate("MainWindow", "Ground"))
        self.shaftSurfaceCondition_comboBox.setItemText(2, _translate("MainWindow", "Hot-rolled"))
        self.shaftSurfaceCondition_comboBox.setItemText(3, _translate("MainWindow", "Machined or cold-drawn"))
        self.shaftLoadType_label.setText(_translate("MainWindow", "Load Type"))
        self.shaftLoadType_comboBox.setItemText(0, _translate("MainWindow", "Bending"))
        self.shaftLoadType_comboBox.setItemText(1, _translate("MainWindow", "Torsion"))
        self.shaftTemperature_label.setText(_translate("MainWindow", "Temperature  [ºC]"))
        self.shaftReliabilityt_label.setText(_translate("MainWindow", "Reliability"))
        self.shaftFailureCriteria_label.setText(_translate("MainWindow", "Failure Criteria"))
        self.shaftFeilureCriteria_comboBox.setItemText(0, _translate("MainWindow", "DE-ASME"))
        self.shaftFeilureCriteria_comboBox.setItemText(1, _translate("MainWindow", "DE-Geber"))
        self.shaftFeilureCriteria_comboBox.setItemText(2, _translate("MainWindow", "DE-Goodman"))
        self.shaftFeilureCriteria_comboBox.setItemText(3, _translate("MainWindow", "DE-Soderberg"))
        self.keyTitle_label.setText(_translate("MainWindow", "Key "))
        self.keyMaterial_label.setText(_translate("MainWindow", "Material"))
        self.keyMaterial_comboBox.setItemText(0, _translate("MainWindow", "AISI 1020 Steel,"
                                                                          " annealed at 870°C (1600°F)"))
        self.keyMaterial_comboBox.setItemText(1, _translate("MainWindow", "AISI 1030 Steel, cold drawn,"
                                                                          " 19-32 mm (0.75-1.25 in) round"))
        self.keyMaterial_comboBox.setItemText(2, _translate("MainWindow", "AISI 1030 Steel, as rolled"))
        self.keyMaterial_comboBox.setItemText(3, _translate("MainWindow", "AISI 1030 Steel, normalized 925°C (1700°F)"))
        self.keyMaterial_comboBox.setItemText(4, _translate("MainWindow", "AISI 1030 Steel,"
                                                                          " annealed at 845°C (1550°F)"))
        self.keyMaterial_comboBox.setItemText(5, _translate("MainWindow", "AISI 1035 Steel,"
                                                                          " as rolled, 19-32 mm (0.75-1.25 in) round"))
        self.keyMaterial_comboBox.setItemText(6, _translate("MainWindow", "AISI 1035 Steel,"
                                                                          " cold drawn, 19-32 mm (0.75-1.25 in) round"))
        self.keyMaterial_comboBox.setItemText(7, _translate("MainWindow", "AISI 1037 Steel,"
                                                                          " Hot Rolled Bar (UNS G10370)"))
        self.keyMaterial_comboBox.setItemText(8, _translate("MainWindow", "AISI 1037 Steel,"
                                                                          " Cold Drawn Bar (UNS G10370)"))
        self.keyMaterial_comboBox.setItemText(9, _translate("MainWindow", "AISI 1040 Steel,"
                                                                          " hot rolled, 19-32 mm (0.75-1.25 in) round"))
        self.keyMaterial_comboBox.setItemText(10, _translate("MainWindow", "AISI 1040 Steel,"
                                                                           " as cold drawn,"
                                                                           " 16-22 mm (0.625-0.875 in) round"))
        self.keyMaterial_comboBox.setItemText(11, _translate("MainWindow", "AISI 1040 Steel,"
                                                                           " as cold drawn,"
                                                                           " 22-32 mm (0.875-1.25 in) round"))
        self.keyMaterial_comboBox.setItemText(12, _translate("MainWindow", "AISI 1040 Steel,"
                                                                           " as cold drawn,"
                                                                           " 32-50 mm (1.25-2 in) round"))
        self.keyMaterial_comboBox.setItemText(13, _translate("MainWindow", "AISI 1040 Steel,"
                                                                           " as cold drawn, 50-75 mm (2-3 in) round"))
        self.keyMaterial_comboBox.setItemText(14, _translate("MainWindow", "AISI 1040 Steel, as rolled"))
        self.keyMaterial_comboBox.setItemText(15, _translate("MainWindow", "AISI 1040 Steel,"
                                                                           " normalized at 900°C (1650°F)"))
        self.keyMaterial_comboBox.setItemText(16, _translate("MainWindow", "AISI 1040 Steel,"
                                                                           " annealed at 790°C (1450°F)"))
        self.keyMaterial_comboBox.setItemText(17, _translate("MainWindow", "AISI 1040 Steel,"
                                                                           " normalized at 900°C (1650°F),"
                                                                           " air cooled, 13 mm (0.5 in.) round"))
        self.keyMaterial_comboBox.setItemText(18, _translate("MainWindow", "AISI 1040 Steel,"
                                                                           " normalized at 900°C (1650°F),"
                                                                           " air cooled, 25 mm (1 in.) round"))
        self.keyMaterial_comboBox.setItemText(19, _translate("MainWindow", "AISI 1040 Steel,"
                                                                           " normalized at 900°C (1650°F),"
                                                                           " air cooled, 50 mm (2 in.) round"))
        self.keyMaterial_comboBox.setItemText(20, _translate("MainWindow", "AISI 1040 Steel,"
                                                                           " normalized at 900°C (1650°F),"
                                                                           " air cooled, 100 mm (4 in.) round"))
        self.keyMaterial_comboBox.setItemText(21, _translate("MainWindow", "AISI 1040 Steel,"
                                                                           " oil quenched from 855°C (1570°F),"
                                                                           " 540°C (1000°F) temper,"
                                                                           " 13 mm (0.5 in.) round"))
        self.keyMaterial_comboBox.setItemText(22, _translate("MainWindow", "AISI 1040 Steel,"
                                                                           " oil quenched from 855°C (1570°F),"
                                                                           " 540°C (1000°F) temper,"
                                                                           " 25 mm (1 in.) round"))
        self.keyMaterial_comboBox.setItemText(23, _translate("MainWindow", "AISI 1040 Steel,"
                                                                           " oil quenched from 855°C (1570°F),"
                                                                           " 540°C (1000°F) temper,"
                                                                           " 50 mm (2 in.) round"))
        self.keyMaterial_comboBox.setItemText(24, _translate("MainWindow", "AISI 1040 Steel,"
                                                                           " oil quenched from 855°C (1570°F),"
                                                                           " 540°C (1000°F) temper,"
                                                                           " 100 mm (4 in.) round"))
        self.keyMaterial_comboBox.setItemText(25, _translate("MainWindow", "AISI 1042 Steel,"
                                                                           " Hot Rolled Bar (UNS G10420)"))
        self.keyMaterial_comboBox.setItemText(26, _translate("MainWindow", "AISI 1042 Steel,"
                                                                           " Cold Drawn Bar (UNS G10420)"))
        self.keyMaterial_comboBox.setItemText(27, _translate("MainWindow", "AISI 1050 Steel,"
                                                                           " cold drawn,"
                                                                           " 19-32 mm (0.75-1.25 in) round"))
        self.keyMaterial_comboBox.setItemText(28, _translate("MainWindow", "AISI 1050 Steel,"
                                                                           " cold drawn,"
                                                                           " annealed, 19-32 mm (0.75-1.25 in) round"))
        self.keyMaterial_comboBox.setItemText(29, _translate("MainWindow", "AISI 1050 Steel,"
                                                                           " cold drawn,"
                                                                           " low temperature,"
                                                                           " stress relieved,"
                                                                           " 16-22 mm (0.625-0.875 in) round"))
        self.keyMaterial_comboBox.setItemText(30, _translate("MainWindow", "AISI 1050 Steel,"
                                                                           " cold drawn,"
                                                                           " high temperature,"
                                                                           " stress relieved,"
                                                                           " 16-22 mm (0.625-0.875 in) round"))
        self.keyMaterial_comboBox.setItemText(31, _translate("MainWindow", "AISI 1050 Steel, as rolled"))
        self.keyMaterial_comboBox.setItemText(32, _translate("MainWindow", "AISI 1050 Steel,"
                                                                           " normalized at 900°C (1650°F)"))
        self.keyMaterial_comboBox.setItemText(33, _translate("MainWindow", "AISI 1050 Steel,"
                                                                           " annealed at 790°C (1450°F)"))
        self.keyForm_label.setText(_translate("MainWindow", "Form"))
        self.keyForm_comboBox.setToolTip("The key forms, based on the DIN 6885 technical standard")
        self.keyForm_comboBox.setStyleSheet("""QToolTip { background-color: #f2f2f2; 
                                                          color: black; 
                                                          border: none
                                                                            }""")
        self.keyForm_comboBox.setItemText(0, _translate("MainWindow", "Form A"))
        self.keyForm_comboBox.setItemText(1, _translate("MainWindow", "Form B"))
        self.keyForm_comboBox.setItemText(2, _translate("MainWindow", "Form AB"))
        self.keySolveBasedOn_label.setText(_translate("MainWindow", "Solve Based on "))
        self.keySolveBasedOn_comboBox.setItemText(0, _translate("MainWindow", "Safety factor for shearing"))
        self.keySolveBasedOn_comboBox.setItemText(1, _translate("MainWindow", "Force"))
        self.keySolveBasedOn_comboBox.setItemText(2, _translate("MainWindow", "Safety factor for compression"))
        self.keySafetyFactorForShearing_label.setText(_translate("MainWindow", "Safety Factor For Shearing"))
        self.safetyFactorForCompression_label.setText(_translate("MainWindow", "Safety Factor For Compression"))
        self.notch_pushButton.setText(_translate("MainWindow", "Notch"))
        self.bearing_pushButton.setText(_translate("MainWindow", "Bearing"))
        self.Fx1_pushButton.setText(_translate("MainWindow", "Insert Force 1"))
        self.Fx2_pushButton.setText(_translate("MainWindow", "Insert Force 2"))
        # self.resetFx_pushButton.setText(_translate("MainWindow", "Reset Forces"))
        self.solve_pushButton.setText(_translate("MainWindow", "SOLVE"))
        self.R1XY_label.setText(_translate("MainWindow", "R1XY  [N]"))
        self.R2XY_label.setText(_translate("MainWindow", "R2XY  [N]"))
        self.R2XYResult_label.setText(_translate("MainWindow", "0"))
        self.deflection_label.setText(_translate("MainWindow", "\u03C5<sub>TOTAL</sub>"))
        self.deflectionResult_label.setText(_translate("MainWindow", "0"))
        self.R1XYResult_label.setText(_translate("MainWindow", "0"))
        self.R1XZ_label.setText(_translate("MainWindow", "R1XZ"))
        self.R1XZResult_label.setText(_translate("MainWindow", "0"))
        self.R2XZLabel.setText(_translate("MainWindow", "R2XZ"))
        self.R2XZResult_label.setText(_translate("MainWindow", "0"))
        self.Slope_label.setText(_translate("MainWindow", "\u03B8<sub>max</sub>"))
        self.SlopeResult_label.setText(_translate("MainWindow", "0"))
        self.deflectionChart_label.setText(_translate("MainWindow", "Deflection chart"))
        self.slopeChart_label.setText(_translate("MainWindow", "Slope chart"))
        self.deflection_pushButton.setText(_translate("MainWindow", "See Chart"))
        self.slope_pushButton.setText(_translate("MainWindow", "See Chart"))
        self.shaftOutput_dockWidget.setWindowTitle(_translate("MainWindow", "Shaft Output"))
        self.shaftOutPut_label.setText(_translate("MainWindow", "Parameters List"))
        self.keyOutPut_dockWidget.setWindowTitle(_translate("MainWindow", "Key Output"))
        self.keyOutPut_label.setText(_translate("MainWindow", "List of Possible Keys"))

    def setName(self):
        """
        This function will set up the objects' name to be used in the dialog window.
        :return: None
        """
        self.setObjectName("MainWindow")
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.chart_frame.setObjectName("chart_frame")
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.chart_verticalLayout.setObjectName("chart_verticalLayout")
        # self.torqueChart_label.setObjectName("torqueChart_label")
        self.torqueChart_widget.setObjectName("torqueChart_widget")
        self.momentChart_label.setObjectName("momentChart_label")
        self.momentChart_widget.setObjectName("momentChart_widget")
        self.menubar.setObjectName("menubar")
        self.menuFile.setObjectName("menuFile")

        self.statusbar.setObjectName("statusbar")
        self.Input_dockWidget.setObjectName("Input_dockWidget")
        self.input_dockWidgetContents.setObjectName("input_dockWidgetContents")
        self.verticalLayout.setObjectName("verticalLayout")
        self.input_scrollArea.setObjectName("input_scrollArea")
        self.scrollArea_widgetContents.setObjectName("scrollArea_widgetContents")
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.Input_frame.setObjectName("Input_frame")
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.input_verticalLayout.setObjectName("input_verticalLayout")
        self.inputOptions_horizontalLayout.setObjectName("inputOptions_horizontalLayout")
        self.solveForTheSafetyFactor_checkBox.setObjectName("solveForTheSafetyFactor_checkBox")
        self.solveForTheDiameter_checkBox.setObjectName("solveForTheDiameter_checkBox")
        self.input_formLayout.setObjectName("input_formLayout")
        self.shaftInputTitle_label.setObjectName("shaftInputTitle_label")
        self.shaftMaterial_label.setObjectName("shaftMaterial_label")
        self.shaftMaterialt_comboBox.setObjectName("shaftMaterialt_comboBox")
        self.shaftCriticalPointLocation_label.setObjectName("shaftCriticalPointLocation_label")
        self.shaftCriticalPointLocation_doubleSpinBox.setObjectName("shaftCriticalPointLocation_doubleSpinBox")
        self.shaftAttemptDiameter_label.setObjectName("shaftAttemptDiameter_label")
        self.shaftAttemptDiameter_doubleSpinBox.setObjectName("shaftAttemptDiameter_doubleSpinBox")
        self.shaftDiameter_label.setObjectName("shaftDiameter_label")
        self.shaftDiameter_doubleSpinBox.setObjectName("shaftDiameter_doubleSpinBox")
        self.shaftLength_label.setObjectName("shaftLength_label")
        self.shaftLength_doubleSpinBox.setObjectName("shaftLength_doubleSpinBox")
        self.shaftSafetyFactor_label.setObjectName("shaftSafetyFactor_label")
        self.shaftSafetyFactor_doubleSpinBox.setObjectName("shaftSafetyFactor_doubleSpinBox")
        self.shaftSurfaceCondition_label.setObjectName("shaftSurfaceCondition_label")
        self.shaftSurfaceCondition_comboBox.setObjectName("shaftSurfaceCondition_comboBox")
        self.shaftLoadType_label.setObjectName("shaftLoadType_label")
        self.shaftLoadType_comboBox.setObjectName("shaftLoadType_comboBox")
        self.shaftTemperature_label.setObjectName("shaftTemperature_label")
        self.shaftTemperature_doubleSpinBox.setObjectName("shaftTemperature_doubleSpinBox")
        self.shaftReliabilityt_label.setObjectName("shaftReliabilityt_label")
        self.shaftReliability_doubleSpinBox.setObjectName("shaftReliability_doubleSpinBox")
        self.shaftFailureCriteria_label.setObjectName("shaftFailureCriteria_label")
        self.shaftFeilureCriteria_comboBox.setObjectName("shaftFeilureCriteria_comboBox")
        self.keyTitle_label.setObjectName("keyTitle_label")
        self.keyMaterial_label.setObjectName("keyMaterial_label")
        self.keyMaterial_comboBox.setObjectName("keyMaterial_comboBox")
        self.keyForm_label.setObjectName("keyForm_label")
        self.keyForm_comboBox.setObjectName("keyForm_comboBox")
        self.keySolveBasedOn_label.setObjectName("keySolveBasedOn_label")
        self.keySolveBasedOn_comboBox.setObjectName("keySolveBasedOn_comboBox")
        self.keySafetyFactorForShearing_label.setObjectName("keySafetyFactorForShearing_label")
        self.keySafetyFactorForShearing_doubleSpinBox.setObjectName("keySafetyFactorForShearing_doubleSpinBox")
        self.safetyFactorForCompression_label.setObjectName("safetyFactorForCompression_label")
        self.safetyFactorForCompression_doubleSpinBox.setObjectName("safetyFactorForCompression_doubleSpinBox")
        self.notch_pushButton.setObjectName("notch_pushButton")
        self.bearing_pushButton.setObjectName("bearing_pushButton")
        self.Fx_verticalLayout.setObjectName("Fx_verticalLayout")
        self.Fx1_pushButton.setObjectName("Fx1_pushButton")
        self.Fx2_pushButton.setObjectName("Fx2_pushButton")
        # self.resetFx_pushButton.setObjectName("resetFx_pushButton")
        self.solve_pushButton.setObjectName("solve_pushButton")
        self.Fx_horizontalLayout.setObjectName("Fx_horizontalLayout")
        self.reactionsLEFT_formLayout.setObjectName("reactionsLEFT_formLayout")
        self.R1XY_label.setObjectName("R1XY_label")
        self.R2XY_label.setObjectName("R2XY_label")
        self.R2XYResult_label.setObjectName("R2XYResult_label")
        self.deflection_label.setObjectName("deflection_label")
        self.deflectionResult_label.setObjectName("deflectionResult_label")
        self.R1XYResult_label.setObjectName("R1XYResult_label")
        self.reactionsCENTER_formLayout.setObjectName("reactionsCENTER_formLayout")
        self.R1XZ_label.setObjectName("R1XZ_label")
        self.R1XZResult_label.setObjectName("R1XZResult_label")
        self.R2XZLabel.setObjectName("R2XZLabel")
        self.R2XZResult_label.setObjectName("R2XZResult_label")
        self.Slope_label.setObjectName("Slope_label")
        self.SlopeResult_label.setObjectName("SlopeResult_label")
        self.reactionsRIGHT_formLayout.setObjectName("reactionsRIGHT_formLayout")
        self.deflectionChart_label.setObjectName("deflectionChart_label")
        self.slopeChart_label.setObjectName("slopeChart_label")
        self.deflection_pushButton.setObjectName("deflection_pushButton")
        self.slope_pushButton.setObjectName("slope_pushButton")
        self.shaftOutput_dockWidget.setObjectName("shaftOutput_dockWidget")
        self.shaftOutPut_dockWidgetContents.setObjectName("shaftOutPut_dockWidgetContents")
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.shatOutPut_verticalLayout.setObjectName("shatOutPut_verticalLayout")
        self.shaftOutPut_label.setObjectName("shaftOutPut_label")
        self.shaftOutPut_tableView.setObjectName("shaftOutPut_tableView")
        self.keyOutPut_dockWidget.setObjectName("keyOutPut_dockWidget")
        self.keyOutPut_dockWidgetContents.setObjectName("keyOutPut_dockWidgetContents")
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.keyOutPut_verticalLayout.setObjectName("keyOutPut_verticalLayout")
        self.keyOutPut_label.setObjectName("keyOutPut_label")
        self.keyOutPut_tableView.setObjectName("keyOutPut_tableView")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = MainWindow()
    dialog.show()
    sys.exit(app.exec_())
