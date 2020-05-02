
"""
@Description:
This module has the aim to construct a material class.who will dialog with the UI.
"""
__author__ = "Iaggo Capitanio"
__copyright__ = "Copyright (C) 2020 Iaggo Capitanio"
__license__ = "Public Domain"
__version__ = "1.0"
# from typing import Union
from sympy.physics.continuum_mechanics.beam import Beam
from sympy import symbols
import numpy as np
import matplotlib.pyplot as plt
import ctypes


myAppId = u'ShaftExploration.Shaftex.version-1.0'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppId)


class BeamSolver:
    """
    This class'll define the internal and reactions forces provided by the external forces.
    """
    def __init__(self, elastic_modulus, length, bearing: list, point_of_analyses: float, Forces1: dict, Forces2: dict):
        self.slopeXY = list()
        self.slopeXZ = list()
        self.slopeTOTAL = list()
        self.bendingMomentXY = list()
        self.bendingMomentXZ = list()
        self.bendingMomentTOTAL = list()
        self.deflectionXY = list()
        self.deflectionXZ = list()
        self.deflectionTOTAL = list()
        self.torque_list = list()
        self.secondMomentOfArea = symbols('I')
        self.R1XY, self.R2XY = symbols('R1XY, R2XY')  # XY will be used to axial forces
        self.R1XZ, self.R2XZ = symbols('R1XZ, R2XZ')  # YZ will be used to tangential forces
        self.elasticModulus = elastic_modulus
        self.beamXY = Beam(length=length, elastic_modulus=elastic_modulus, second_moment=self.secondMomentOfArea)
        self.beamXZ = Beam(length=length, elastic_modulus=elastic_modulus, second_moment=self.secondMomentOfArea)
        self.length = length
        self.pointAnalyses = point_of_analyses
        self.bearingPosition = bearing
        self.Forces1 = Forces1
        self.Forces2 = Forces2
        self.torque = None
        self.setBearing()
        self.setExternalLoads()
        self.solveForTheReactions()

    def setBearing(self):
        """
        This function will set the Boundary Condition of the problem.
        :return: numpy.float64"""
        self.beamXY.bc_deflection = [(self.bearingPosition[0], 0), (self.bearingPosition[1], 0)]
        self.beamXZ.bc_deflection = [(self.bearingPosition[0], 0), (self.bearingPosition[1], 0)]

    def setExternalLoads(self):
        """
        set the external loads acting on the shaft
        ;:return: None
        """
        Fr1 = self.Forces1['Forces'][2]
        Ft1 = self.Forces1['Forces'][1]
        Fr2 = self.Forces2['Forces'][2]
        Ft2 = self.Forces2['Forces'][1]
        xPosition1 = self.Forces1['xPosition']
        xPosition2 = self.Forces2['xPosition']

        self.beamXY.apply_load(value=Fr1, start=xPosition1, order=-1)
        self.beamXZ.apply_load(value=Ft1, start=xPosition1, order=-1)
        self.beamXY.apply_load(value=Fr2, start=xPosition2, order=-1)
        self.beamXZ.apply_load(value=Ft2, start=xPosition2, order=-1)
        # Supports loads
        self.beamXY.apply_load(value=self.R1XY, start=self.bearingPosition[0], order=-1)
        self.beamXY.apply_load(value=self.R2XY, start=self.bearingPosition[1], order=-1)
        self.beamXZ.apply_load(value=self.R1XZ, start=self.bearingPosition[0], order=-1)
        self.beamXZ.apply_load(value=self.R2XZ, start=self.bearingPosition[1], order=-1)

    def solveForTheReactions(self):
        """
        This function'll solve for the reactions R1 and R2.
        :return: None
        """
        self.beamXY.solve_for_reaction_loads(self.R1XY, self.R2XY)
        self.beamXZ.solve_for_reaction_loads(self.R1XZ, self.R2XZ)



    def rebuildBeam(self, second_moment_of_area: float) -> None:
        """
        This function permits to create the slope and the deflection charts.
        :param second_moment_of_area: It's the new momentum of inertia obtained by the shaft module.
        :return None
        """
        self.beamXY = Beam(length=self.length, elastic_modulus=self.elasticModulus, second_moment=second_moment_of_area)
        self.beamXZ = Beam(length=self.length, elastic_modulus=self.elasticModulus, second_moment=second_moment_of_area)
        self.setBearing()
        self.setExternalLoads()
        self.solveForTheReactions()

    def getBendingMoment(self) -> tuple:
        """
        :return: tuple
        """

        return self.beamXY.bending_moment(), self.beamXZ.bending_moment()

    def getShearForce(self) -> tuple:
        """
        :return: tuple
        """
        return self.beamXY.shear_force(), self.beamXZ.shear_force()

    def getTotalDeflection(self, second_moment_of_area: float) -> float:
        """
        :param second_moment_of_area: the second moment of area
        :return: float
        """
        self.rebuildBeam(second_moment_of_area=second_moment_of_area)
        a = float(self.beamXY.deflection().subs({'x': self.pointAnalyses}))
        b = float(self.beamXZ.deflection().subs({'x': self.pointAnalyses}))
        return np.sqrt(a**2 + b**2)

    def getDeflection(self, second_moment_of_area: float) -> tuple:
        """
        :param second_moment_of_area: the second moment of area
        :return: tuple
        """
        self.rebuildBeam(second_moment_of_area=second_moment_of_area)
        return self.beamXY.deflection(), self.beamXZ.deflection()

    def getMaxSlope(self, second_moment_of_area: float) -> float:
        """
        :param second_moment_of_area: the second moment of area
        :return: float
        """
        self.rebuildBeam(second_moment_of_area=second_moment_of_area)
        a = float(self.beamXY.slope().subs({'x': self.pointAnalyses}))
        b = float(self.beamXZ.slope().subs({'x': self.pointAnalyses}))
        return max(a, b)

    def getSlope(self, second_moment_of_area: float) -> tuple:
        """
        :param second_moment_of_area: the second moment of area
        :return: tuple
        """
        self.rebuildBeam(second_moment_of_area=second_moment_of_area)
        return self.beamXY.slope(), self.beamXZ.slope()

    def getPlotSlope(self, second_moment_of_area: float,
                     figureWidth=15, figureHeight=7, number_of_points=100, dpi=200, fontsize=15) -> plt.figure:
        """
        :param fontsize:
        :param dpi:
        :param number_of_points: the number of points in the x axis, who will define the 'resolution' of the chart.
        :param figureHeight: the figure's height in pixels
        :param figureWidth: the figure's width in pixels
        :param second_moment_of_area: the second moment of area
        :return: matplotlib.figure.Figure
        """
        x = np.linspace(0, self.length, number_of_points)
        self.slopeXY = \
            np.array([float(self.getSlope(second_moment_of_area=second_moment_of_area)[0].subs({'x': i})) for i in x])
        self.slopeXZ = \
            np.array([float(self.getSlope(second_moment_of_area=second_moment_of_area)[1].subs({'x': i})) for i in x])

        return {'x': x, 'XY': self.slopeXY, 'XZ': self.slopeXZ}

    def getPlotBendingMoment(self,
                             figureWidth=15,
                             figureHeight=7,
                             number_of_points=100,
                             dpi=200,
                             fontsize=15) -> plt.figure:
        """
        :param fontsize:
        :param dpi:
        :param number_of_points: the number of points in the x axis, who will define the 'resolution' of the chart.
        :param figureHeight: the figure's height in pixels.
        :param figureWidth: the figure's width in pixels.
        :return: dictionary,
         {"x": x, "XY": self.bendingMomentXY, "XZ": self.bendingMomentXZ, "TOTAL": self.bendingMomentTOTAL}.
        """
        x = np.linspace(0, self.length, number_of_points)
        self.bendingMomentXY = \
            np.array([float(self.getBendingMoment()[0].subs({'x': i})) for i in x])
        self.bendingMomentXZ = \
            np.array([float(self.getBendingMoment()[1].subs({'x': i})) for i in x])
        self.bendingMomentTOTAL = np.sqrt(self.bendingMomentXY**2 + self.bendingMomentXZ**2)

        return {"x": x, "XY": self.bendingMomentXY, "XZ": self.bendingMomentXZ, "TOTAL": self.bendingMomentTOTAL}

    def getPlotDeflection(self,
                          second_moment_of_area: float,
                          figureWidth=15,
                          figureHeight=7,
                          number_of_points=100,
                          dpi=200,
                          fontsize=15) -> plt.figure:
        """
        :param fontsize:
        :param dpi:
        :param number_of_points: the number of points in the x axis, who will define the 'resolution' of the chart.
        :param figureHeight: the figure's height in pixels
        :param figureWidth: the figure's width in pixels
        :param second_moment_of_area: the second moment of area
        :return: matplotlib.figure.Figure
        """
        x = np.linspace(0, self.length, number_of_points)
        self.deflectionXY = \
            np.array([float(self.getDeflection(second_moment_of_area)[0].subs({'x': i})) for i in x]) * 1e3
        self.deflectionXZ = \
            np.array([float(self.getDeflection(second_moment_of_area)[1].subs({'x': i})) for i in x]) * 1e3
        self.deflectionTOTAL = np.sqrt(self.deflectionXY**2 + self.deflectionXZ**2)

        return {"x": x, "XY": self.deflectionXY, "XZ": self.deflectionXZ, "TOTAL": self.deflectionTOTAL}

    def getPlotTorque(self, figureWidth=15, figureHeight=7, number_of_points=100, dpi=200, fontsize=15) -> dict:
        """
        :param figureWidth:
        :param fontsize:
        :param dpi:
        :param number_of_points: the number of points in the x axis, who will define the 'resolution' of the chart.
        :param figureHeight: the figure's height in pixels
        :return: dictionary, {'x': x, 'torque': self.torque}.
        """
        if self.Forces1['xPosition'] < self.Forces2['xPosition']:
            x = np.linspace(self.Forces1['xPosition'], self.Forces2['xPosition'], number_of_points)
        else:
            x = np.linspace(self.Forces2['xPosition'], self.Forces1['xPosition'], number_of_points)
        self.torque = np.ones_like(x) * self.Forces1['Forces'][0]
        return {'x': x, 'torque': self.torque}

    def getReactionLoads(self):
        """
        :return: tuple
        """
        A = self.beamXY.reaction_loads
        B = self.beamXZ.reaction_loads
        A.update(B)
        return A

    def getBendingMomentAtPoint(self):
        """
        This function returns the bending moment at the critical point of analyses.
        :return float
        """
        A = float(self.getBendingMoment()[0].subs({'x': self.pointAnalyses}))
        B = float(self.getBendingMoment()[0].subs({'x': self.pointAnalyses}))
        C = np.sqrt(A**2 + B**2)
        return C
