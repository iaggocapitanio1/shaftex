"""
@Description:
The main aim of this class allows to bind the main window widget with the chart widgets
"""
__author__ = "Iaggo Capitanio"
__copyright__ = "Copyright (C) 2020 Iaggo Capitanio"
__license__ = "Public Domain"
__version__ = "1.0"


import matplotlib
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import ctypes

matplotlib.use('Qt5Agg')

myAppId = u'ShaftExploration.Shaftex.version-1.0'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppId)
class MplCanvasSlope(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, domain, XY, XZ,
                 parent=None, width=5, height=4, dpi=100, fontsize=12,
                 labelImage_One=r'$\theta_{XY} [rads]$', labelImage_Two=r'$\theta_{XZ} [rads]$', title=r"Slope"):
        self.title = title
        self.XZ = XZ
        self.labelImage_One = labelImage_One
        self.labelImage_Two = labelImage_Two
        self.domain = domain
        self.XY = XY
        self.fontsize = fontsize
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.set_facecolor("#f2f2f2")
        self.axes = self.fig.add_subplot(111)
        self.axes.spines['bottom'].set_position('zero')
        self.axes.spines['right'].set_color('none')
        self.axes.spines['top'].set_color('none')
        self.axes.set_facecolor('#f2f2f2')
        self.axes.grid(color='#a6a6a6', linestyle='-', linewidth=1)
        self.compute_initial_figure()
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        """
        :return: None
        """
        pass

class DynamicMplCanvasSlope(MplCanvasSlope):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MplCanvasSlope.__init__(self, *args, **kwargs)

    def compute_initial_figure(self):
        """
        :return: None.
        """
        self.axes.set_ylabel(r'$\theta$ [rads]', fontsize=self.fontsize)
        self.axes.set_xlabel(r'length [m]', fontsize=self.fontsize)
        self.axes.set_title(self.title)
        self.axes.set_facecolor('#f2f2f2')
        self.axes.plot(self.domain, self.XY, color='#000080', label=self.labelImage_One)
        self.axes.plot(self.domain, self.XZ, color='#04E103', label=self.labelImage_Two)
        self.axes.legend(loc='best')

        plt.close('all')

    def update_figure(self, domain, XY, XZ):
        """
        :param domain:
        :param XY:
        :param XZ:
        """

        self.axes.cla()
        self.axes.set_ylabel(r'$\theta$ [rads]', fontsize=self.fontsize)
        self.axes.set_xlabel(r'length [m]', fontsize=self.fontsize)
        self.axes.set_title(self.title)
        self.axes.spines['bottom'].set_position('zero')
        self.axes.spines['right'].set_color('none')
        self.axes.spines['top'].set_color('none')
        self.axes.set_facecolor('#f2f2f2')
        self.axes.grid(color='#a6a6a6', linestyle='-', linewidth=1)
        self.axes.plot(domain, XY, color='#000080', label=self.labelImage_One)
        self.axes.plot(domain, XZ, color='#04E103', label=self.labelImage_Two)
        self.axes.legend(loc='best')
        self.fig.canvas.draw()
