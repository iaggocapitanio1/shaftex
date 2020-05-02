"""
This class'll extract the data from the dialog of the forces and convert it in an standard list with the values
torque, tangential force and radial force
"""
__author__ = "Iaggo Capitanio"
__copyright__ = "Copyright (C) 2020 Iaggo Capitanio"
__license__ = "Public Domain"
__version__ = "1.0"


from Shafton.shafton import *
from dialogFx import DialogFx
import ctypes

myAppId = u'ShaftExploration.Shaftex.version-1.0'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppId)

def solveEngine(dialogX: DialogFx) -> list:
    """:return: list: [torque, tangential_force, radial_force]"""
    if dialogX.powerCheckBox.isChecked():
        power = float(dialogX.powerDoubleSpinBox.value())
        rpm = float(dialogX.rpmDoubleSpinBox.value())
        torque = shaftTorque(power=power, RPM=rpm)
        F_t = 0
        F_r = 0
    elif dialogX.vectorsCheckBox.isChecked():
        F_t = float(dialogX.tangentialForcedoubleSpinBox.value())
        F_r = float(dialogX.radialForceDoubleSpinBox.value())
        radius = float(dialogX.radiusDoubleSpinBox.value()) * 1e-3
        torque = F_t * radius
    else:
        torque = float(dialogX.torqueDoubleSpinBox.value())
        F_t = 0
        F_r = 0
    return [torque, F_t, F_r]


def solveGear(dialogX: DialogFx) -> list:
    """:return: list: [torque, tangential_force, radial_force]"""
    radius = float(dialogX.radiusDoubleSpinBox.value()) * 1e-3
    theta = float(dialogX.angleObliquityDoubleSpinBox.value())
    if dialogX.powerCheckBox.isChecked():

        power = float(dialogX.powerDoubleSpinBox.value())
        rpm = float(dialogX.rpmDoubleSpinBox.value())
        torque = shaftTorque(power=power, RPM=rpm)
        F_r, F_t = shaftForce(torque=torque, radius=radius, degree=theta)
    elif dialogX.vectorsCheckBox.isChecked():
        F_t = float(dialogX.tangentialForcedoubleSpinBox.value())
        F_r = float(dialogX.radialForceDoubleSpinBox.value())
        radius = float(dialogX.radiusDoubleSpinBox.value()) * 1e-3
        torque = F_t * radius
    else:
        torque = float(dialogX.torqueDoubleSpinBox.value())
        F_r, F_t = shaftForce(torque=torque, radius=radius, degree=theta)
    return [torque, F_t, F_r]


def solvePulley(dialogX: DialogFx) -> list:
    """:return: list: [torque, tangential_force, radial_force]"""
    diameter = 2 * float(dialogX.radiusDoubleSpinBox.value()) * 1e-3

    if dialogX.powerCheckBox.isChecked():
        power = float(dialogX.powerDoubleSpinBox.value())
        rpm = float(dialogX.rpmDoubleSpinBox.value())
        torque = shaftTorque(power=power, RPM=rpm)
        F_r = shaftPulleyForce(power=power, RPM=rpm, diameter=diameter)
        F_t = F_r / 1.5
    elif dialogX.vectorsCheckBox.isChecked():
        F_t = float(dialogX.tangentialForcedoubleSpinBox.value())
        F_r = float(dialogX.radialForceDoubleSpinBox.value())
        radius = float(dialogX.radiusDoubleSpinBox.value()) * 1e-3
        torque = F_t * radius
    else:
        torque = float(dialogX.torqueDoubleSpinBox.value())
        F_r = float(3 * torque / diameter)
        F_t = float(F_r / 1.5)

    return [torque, F_t, F_r]


def getChoices(dialogX: DialogFx):
    """:return: list"""

    if dialogX.engineCheckBox.isChecked():
        return {'Forces': solveEngine(dialogX), 'xPosition': dialogX.xPositionDoubleSpinBox.value() * 1e-3}
    if dialogX.gearCheckBox.isChecked():
        return {'Forces': solveGear(dialogX), 'xPosition': dialogX.xPositionDoubleSpinBox.value() * 1e-3,
                'angle of Obliquity': dialogX.angleObliquityDoubleSpinBox.value()}
    if dialogX.pulleyCheckBox.isChecked():
        return {'Forces': solvePulley(dialogX), 'xPosition': dialogX.xPositionDoubleSpinBox.value() * 1e-3}
