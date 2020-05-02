"""
    The main aim of this class allows to bind the main window widget with the chart widgets
"""
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import ctypes


matplotlib.use('Qt5Agg')
myAppId = u'ShaftExploration.Shaftex.version-1.0'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppId)


class MplCanvasTorque(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, domain, image, length,
                 parent=None, width=5, height=4, dpi=100, fontsize=12, labelImage=r'$Torque$', title='Torque'):
        self.title = title
        self.length = length
        self.labelImage = labelImage
        self.domain = domain
        self.image = image
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

class DynamicMplCanvasTorque(MplCanvasTorque):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MplCanvasTorque.__init__(self, *args, **kwargs)

    def compute_initial_figure(self):
        """
        :return: None.
        """
        self.axes.set_ylabel(r'$Torque$ [Nm]', fontsize=self.fontsize)
        self.axes.set_xlabel(r'length [m]', fontsize=self.fontsize)
        self.axes.set_title(self.title)
        self.axes.set_facecolor('#f2f2f2')
        self.axes.plot(self.domain, self.image, color='#000080', label=self.labelImage)
        self.axes.fill_between(self.domain, self.image, np.zeros_like(self.domain),  alpha=0.5)
        if max(abs(np.array(self.image))) != 0:
            self.axes.set(xlim=(0, self.length), ylim=(0, max(self.image)*1.5))
        else:
            self.axes.set(xlim=(0, self.length), ylim=(-200, 200))
        self.axes.legend(loc='best')

        plt.close('all')

    def update_figure(self, domain, image, length):
        """
        :param length:
        :param domain:
        :param image:
        """

        self.axes.cla()
        self.axes.set_ylabel(r'$Torque$ [Nm]', fontsize=self.fontsize)
        self.axes.set_xlabel(r'length [m]', fontsize=self.fontsize)
        self.axes.set_title(self.title)
        self.axes.spines['bottom'].set_position('zero')
        self.axes.spines['right'].set_color('none')
        self.axes.spines['top'].set_color('none')
        self.axes.set_facecolor('#f2f2f2')
        self.axes.grid(color='#a6a6a6', linestyle='-', linewidth=1)
        self.axes.plot(domain, image, color='#000080', label=self.labelImage)
        if max(abs(np.array(image))) != 0:
            self.axes.set(xlim=(0, length), ylim=(0, max(image)*1.5))
        else:
            self.axes.set(xlim=(0, length), ylim=(-200, 200))
        self.axes.fill_between(domain, image, np.zeros_like(domain),  alpha=0.5)
        self.axes.legend(loc='best')
        self.fig.canvas.draw()
