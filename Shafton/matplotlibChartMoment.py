"""
    The main aim of this class allows to bind the main window widget with the chart widgets
"""
import matplotlib
import ctypes
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

matplotlib.use('Qt5Agg')
myAppId = u'ShaftExploration.Shaftex.version-1.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppId)

class MplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, domain, XY, XZ, TOTAL,
                 parent=None, width=5, height=4, dpi=100, fontsize=12,
                 labelXY=r'$M_{XY}$', labelXZ=r'$M_{XZ}$', labelTOTAL=r'$M_{TOTAL}$', title='Moment'):
        self.title = title
        self.labelXY = labelXY
        self.labelXZ = labelXZ
        self.labelTotal = labelTOTAL
        self.domain = domain
        self.XY = XY
        self.XZ = XZ
        self.TOTAL = TOTAL
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

class DynamicMplCanvas(MplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MplCanvas.__init__(self, *args, **kwargs)

    def compute_initial_figure(self):
        """
        :return: None.
        """

        self.axes.set_ylabel(r'$M$   [Nm]', fontsize=self.fontsize)
        self.axes.set_xlabel(r'length [m]', fontsize=self.fontsize)
        self.axes.set_title(self.title)
        self.axes.plot(self.domain, self.XY, color='#000080', label=self.labelXY)
        self.axes.plot(self.domain, self.XZ, color='#04E103', label=self.labelXZ)
        self.axes.plot(self.domain, self.TOTAL, color='#BA0000', label=self.labelTotal)
        self.axes.legend(loc='best')

        plt.close('all')

    def update_figure(self, domain, XY, XZ, TOTAL):
        """

        :param domain:
        :param XY:
        :param XZ:
        :param TOTAL:
        """
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        self.axes.cla()
        self.axes.set_ylabel(r'$M$   [Nm]', fontsize=self.fontsize)
        self.axes.set_xlabel(r'length [m]', fontsize=self.fontsize)
        self.axes.set_title('Moment')
        self.axes.spines['bottom'].set_position('zero')
        self.axes.spines['right'].set_color('none')
        self.axes.spines['top'].set_color('none')
        self.axes.set_facecolor('#f2f2f2')
        self.axes.grid(color='#a6a6a6', linestyle='-', linewidth=1)
        self.axes.plot(domain, XY, color='#000080', label=r'$M_{XY}$')
        self.axes.plot(domain, XZ, color='#04E103', label=r'$M_{XZ}$')
        self.axes.plot(domain, TOTAL, color='#BA0000', label=r'$M_{TOTAL}$')
        self.axes.legend(loc='best')
        self.fig.canvas.draw()
        self.fig.tight_layout()
