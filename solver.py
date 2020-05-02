"""build a modolus to bind the py files to solve the problem"""

from dialogFx import DialogFx
from PyQt5 import QtWidgets
from shaft import Shaft
from Shafton.beamSolver import BeamSolver
from solveLib import getChoices
from Shafton.material import MaterialAISI
import keyton as ky
from typing import Union, List
import ctypes

# noinspection PyAttributeOutsideInit
myAppId = u'ShaftExploration.Shaftex.version-1.0'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppId)
class Solver:
    """This class'll be used to build up a solution for the problem """
    def __init__(self,  parent: QtWidgets.QMainWindow,
                 dialog1: DialogFx,
                 dialog2: DialogFx,
                 shaft_material: str,
                 key_material: str,
                 length: float,
                 diameterTrial: float,
                 bearing: List[float],
                 point_of_analyses: float,
                 Temperature: float,
                 reliability: float,
                 notchR: float,
                 notch_type: str,
                 D: str,
                 Kt: float,
                 Kts: float,
                 d: float,
                 safety_factor: Union[None, float],
                 finishing_surface: str,
                 load: str,
                 method: str,
                 keySafetyFactor_shearing: Union[None, float],
                 keyForm: str,
                 keySafetyFactor_compression: Union[None, float]) -> None:

        self.parent = parent
        self.msg = QtWidgets.QMessageBox(self.parent)
        self.diameterTrial = diameterTrial
        self.keySafetyFactor_shearing = keySafetyFactor_shearing
        self.keyForm = keyForm
        self.keySafetyFactor_compression = keySafetyFactor_compression
        self.notchType = notch_type
        self.dUppercase = D
        self.Kt = Kt
        self.Kts = Kts
        self.dLowercase = d
        self.safetyFactor = safety_factor
        self.finishingSurface = finishing_surface
        self.load = load
        self.method = method
        self.bearing = bearing
        self.dialog1 = dialog1
        self.dialog2 = dialog2
        self.parent = parent
        self.length = length
        self.point_of_analyses = point_of_analyses
        self.shaftMaterial = MaterialAISI(shaft_material)
        self.keyMaterial = MaterialAISI(key_material)
        self.Temperature = Temperature
        self.reliability = reliability
        self.notchR = notchR
        self.ambiguousError = QtWidgets.QMessageBox(parent)
        self.Forces1 = getChoices(self.dialog1)
        self.Forces2 = getChoices(self.dialog2)
        self.solutionBeam = BeamSolver(elastic_modulus=self.shaftMaterial.getMaterialModulusOfElasticity(),
                                       length=self.length, bearing=self.bearing,
                                       point_of_analyses=self.point_of_analyses,
                                       Forces1=self.Forces1,
                                       Forces2=self.Forces2)
        self.getInternalForces()
        self.shaft = Shaft(Ma=self.getMa(),
                           Mm=self.getMm(),
                           Ta=self.getTa(),
                           Tm=self.getTm(),
                           Sut=self.shaftMaterial.getMaterialTensileStrengthUltimate(),
                           Sy=self.shaftMaterial.getMaterialTensileStrengthYield(),
                           Temperature=Temperature,
                           reliability=self.reliability,
                           r=self.notchR,
                           notchType=self.notchType,
                           D=self.dUppercase,
                           Kt=self.Kt,
                           Kts=self.Kts,
                           d=self.dLowercase,
                           safetyFactor=self.safetyFactor,
                           methodSurfaceFinish=self.finishingSurface,
                           load=self.load,
                           method=self.method,
                           dTrial=self.diameterTrial)

        if 254e-3 >= self.shaft.getDLowercase() >= 5e-3:
            self.key = ky.Key(diameter=self.shaft.getDLowercase(),
                              Sy=self.keyMaterial.getMaterialTensileStrengthYield(),
                              torque=abs(self.getTm()),
                              safetyFactorCompression=self.keySafetyFactor_compression,
                              safetyFactorShearing=self.keySafetyFactor_shearing)
        elif self.shaft.getDLowercase() <= 5e-3:
            d = 8e-3
            self.shaft = Shaft(Ma=self.getMa(),
                               Mm=self.getMm(),
                               Ta=self.getTa(),
                               Tm=self.getTm(),
                               Sut=self.shaftMaterial.getMaterialTensileStrengthUltimate(),
                               Sy=self.shaftMaterial.getMaterialTensileStrengthYield(),
                               Temperature=Temperature,
                               reliability=self.reliability,
                               r=self.notchR,
                               notchType=self.notchType,
                               D=self.dUppercase,
                               Kt=self.Kt,
                               Kts=self.Kts,
                               d=d,
                               safetyFactor=self.safetyFactor,
                               methodSurfaceFinish=self.finishingSurface,
                               load=self.load,
                               method=self.method,
                               dTrial=self.diameterTrial)
            self.key = ky.Key(diameter=self.shaft.getDLowercase(),
                              Sy=self.keyMaterial.getMaterialTensileStrengthYield(),
                              torque=abs(self.getTm()),
                              safetyFactorCompression=self.keySafetyFactor_compression,
                              safetyFactorShearing=self.keySafetyFactor_shearing)
            informativeText = "The diameter value found is \n" \
                              " outside the borders (5 mm, 254 mm), \n" \
                              " for this reason, the values in \n" \
                              " the table will be projected \n " \
                              "based on the diameter value equal to five."
            self.msg = self.errorMessage(text="The diameter found is outside the borders",
                                         title="Error!",
                                         icon=QtWidgets.QMessageBox.Critical,
                                         informativeText=informativeText)
            self.msg.show()
            # noinspection PyUnusedLocal
            x = self.msg.exec_()
        else:
            d = 254e-3
            self.shaft = Shaft(Ma=self.getMa(),
                               Mm=self.getMm(),
                               Ta=self.getTa(),
                               Tm=self.getTm(),
                               Sut=self.shaftMaterial.getMaterialTensileStrengthUltimate(),
                               Sy=self.shaftMaterial.getMaterialTensileStrengthYield(),
                               Temperature=Temperature,
                               reliability=self.reliability,
                               r=self.notchR,
                               notchType=self.notchType,
                               D=self.dUppercase,
                               Kt=self.Kt,
                               Kts=self.Kts,
                               d=d,
                               safetyFactor=self.safetyFactor,
                               methodSurfaceFinish=self.finishingSurface,
                               load=self.load,
                               method=self.method,
                               dTrial=self.diameterTrial)
            self.key = ky.Key(diameter=self.shaft.getDLowercase(),
                              Sy=self.keyMaterial.getMaterialTensileStrengthYield(),
                              torque=abs(self.getTm()),
                              safetyFactorCompression=self.keySafetyFactor_compression,
                              safetyFactorShearing=self.keySafetyFactor_shearing)
            informativeText = "The diameter value found is \n" \
                              " outside the borders (5 mm, 254 mm), \n" \
                              " for this reason, the values in \n" \
                              " the table will be projected \n " \
                              "based on the diameter value equal to \n" \
                              " two hundred and fifty-four."
            self.msg = self.errorMessage(text="The diameter found is outside the borders",
                                         title="Error!",
                                         icon=QtWidgets.QMessageBox.Critical,
                                         informativeText=informativeText)
            self.msg.show()
            # noinspection PyUnusedLocal
            x = self.msg.exec_()

    def errorMessage(self, text: str, title: str,
                     icon: QtWidgets.QMessageBox.Icon, informativeText: str) -> QtWidgets.QMessageBox:
        """:return"""
        self.msg.setText(text)
        self.msg.setWindowTitle(title)
        self.msg.setIcon(icon)
        self.msg.setInformativeText(informativeText)
        return self.msg

    # noinspection PyAttributeOutsideInit
    def setTa(self, Ta):
        """

        :param Ta:
        """
        self.Ta = Ta

    def setTm(self, Tm):
        """

        :param Tm:
        """
        self.Tm = Tm

    def setMa(self, Ma):
        """

        :param Ma:
        """
        self.Ma = Ma

    def setMm(self, Mm):
        """

        :param Mm:
        """
        self.Mm = Mm

    def getTa(self):
        """

        :return:
        """
        return self.Ta

    def getTm(self):
        """

        :return:
        """
        return self.Tm

    def getMa(self):
        """

        :return:
        """
        return self.Ma

    def getMm(self):
        """

        :return:
        """
        return self.Mm

    def getAmbiguousError(self) -> bool:
        """:return: boolean"""
        self.ambiguousError.setIcon(QtWidgets.QMessageBox.Critical)
        self.ambiguousError.setWindowTitle("Error!")
        self.ambiguousError.setText("Ambiguous information!")
        self.ambiguousError.setInformativeText("Tick the internal forces checkbox only once.")
        self.ambiguousError.setStandardButtons(QtWidgets.QMessageBox.Ok)
        # noinspection PyUnusedLocal
        x = self.ambiguousError.exec_()
        return False

    def getInternalForces(self) -> None:
        """:return: boolean"""
        self.setMa(self.solutionBeam.getBendingMomentAtPoint())
        self.setMm(0)
        self.setTm(self.Forces1['Forces'][0])
        self.setTa(0)

    def getReactions(self) -> None:
        """:return: boolean"""
        self.solutionBeam.getReactionLoads()

########################################################################################################################

########################################################################################################################


# noinspection PyAttributeOutsideInit
class SolverForManuallyIsChecked:
    """This class'll be used to build up a solution for the problem """
    def __init__(self,  parent: QtWidgets.QMainWindow,
                 Ma: float,
                 Mm: float,
                 Ta: float,
                 Tm: float,
                 shaft_material: str,
                 key_material: str,
                 length: float,
                 diameterTrial: float,
                 Temperature: float,
                 reliability: float,
                 notchR: float,
                 notch_type: str,
                 D: str,
                 Kt: float,
                 Kts: float,
                 d: float,
                 safety_factor: Union[None, float],
                 finishing_surface: str,
                 load: str,
                 method: str,
                 keySafetyFactor_shearing: Union[None, float],
                 keyForm: str,
                 keySafetyFactor_compression: Union[None, float]) -> None:
        self.keySafetyFactor_shearing = keySafetyFactor_shearing
        self.keyForm = keyForm
        self.diameterTrial = diameterTrial
        self.keySafetyFactor_compression = keySafetyFactor_compression
        self.notchType = notch_type
        self.dUppercase = D
        self.Kt = Kt
        self.Kts = Kts
        self.dLowercase = d
        self.safetyFactor = safety_factor
        self.finishingSurface = finishing_surface
        self.load = load
        self.method = method
        self.parent = parent
        self.length = length
        self.shaftMaterial = MaterialAISI(shaft_material)
        self.keyMaterial = MaterialAISI(key_material)
        self.Temperature = Temperature
        self.reliability = reliability
        self.notchR = notchR
        self.ambiguousError = QtWidgets.QMessageBox(parent)
        self.setMa(Ma)
        self.setMm(Mm)
        self.setTa(Ta)
        self.setTm(Tm)
        self.shaft = Shaft(Ma=self.getMa(),
                           Mm=self.getMm(),
                           Ta=self.getTa(),
                           Tm=self.getTm(),
                           Sut=self.shaftMaterial.getMaterialTensileStrengthUltimate(),
                           Sy=self.shaftMaterial.getMaterialTensileStrengthYield(),
                           Temperature=Temperature,
                           reliability=self.reliability,
                           r=self.notchR,
                           notchType=self.notchType,
                           D=self.dUppercase,
                           Kt=self.Kt,
                           Kts=self.Kts,
                           d=self.dLowercase,
                           safetyFactor=self.safetyFactor,
                           methodSurfaceFinish=self.finishingSurface,
                           load=self.load,
                           method=self.method,
                           dTrial=diameterTrial)

        self.key = ky.Key(diameter=self.shaft.getDLowercase(),
                          Sy=self.keyMaterial.getMaterialTensileStrengthYield(),
                          torque=abs(self.getTm()),
                          safetyFactorCompression=self.keySafetyFactor_compression,
                          safetyFactorShearing=self.keySafetyFactor_shearing)


    # noinspection PyAttributeOutsideInit
    def setTa(self, Ta):
        """

        :param Ta:
        """
        self.Ta = Ta

    def setTm(self, Tm):
        """

        :param Tm:
        """
        self.Tm = Tm

    def setMa(self, Ma):
        """

        :param Ma:
        """
        self.Ma = Ma

    def setMm(self, Mm):
        """

        :param Mm:
        """
        self.Mm = Mm

    def getTa(self):
        """

        :return:
        """
        return self.Ta

    def getTm(self):
        """

        :return:
        """
        return self.Tm

    def getMa(self):
        """

        :return:
        """
        return self.Ma

    def getMm(self):
        """

        :return:
        """
        return self.Mm

    def getAmbiguousError(self) -> bool:
        """:return: boolean"""
        self.ambiguousError.setIcon(QtWidgets.QMessageBox.Critical)
        self.ambiguousError.setWindowTitle("Error!")
        self.ambiguousError.setText("Ambiguous information!")
        self.ambiguousError.setInformativeText("Tick the internal forces checkbox only once.")
        self.ambiguousError.setStandardButtons(QtWidgets.QMessageBox.Ok)
        # noinspection PyUnusedLocal
        x = self.ambiguousError.exec_()
        return False
