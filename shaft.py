"""
@Description:
This module has the aim to construct a shaft class. Which one will dialog with the UI.
"""
__author__ = "Iaggo Capitanio"
__copyright__ = "Copyright (C) 2020 Iaggo Capitanio"
__license__ = "Public Domain"
__version__ = "1.0"

from typing import List, Union, Dict, Any
import Shafton.shafton as sh
import numpy as np
import ctypes

myAppId = u'ShaftExploration.Shaftex.version-1.0'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppId)

class Shaft:
    """
    This class will be used as the engine behind the user interface.
    """
    def __init__(self, Ma, Mm, Ta, Tm, Sut, Sy, Temperature, reliability, r, dTrial=1e-2, error=1e-3,
                 notchType="stepped bar", D=None, Kt=None, Kts=None, d=None, safetyFactor=None,
                 methodSurfaceFinish="Ground", load="Bending", method="DE-ASME"):
        self.Ma = Ma
        self.Mm = Mm
        self.Ta = Ta
        self.Tm = Tm
        self.Kt = Kt
        self.Kts = Kts
        self.Sut = Sut
        self.Sy = Sy
        self.SeLine = sh.shaftEnduranceLimitStressRotatingBeam(self.Sut)
        self.kf = 1
        self.factorKa = sh.shaftFactor_Ka(methodSurfaceFinish, self.getSy())
        self.factorKc = sh.shaftFactor_Kc(load)
        self.factorKd = sh.shaftFactor_Kd(Temperature)
        self.factorKe = sh.shaftFactor_Ke(reliability)
        self.method = method
        self.__setSafetyFactor(safetyFactor)
        self.__setDLowercase(d)
        self.D = D
        self.r = r
        self.notchType = notchType
        self.__setQ()
        self.__setQs()
        self.dictionary = dict()
        self.static = False
        self.__decisionMakerForDiameterAndSafetyFactor(dTrial, error)

    # setters
    def __setSafetyFactor(self, safetyFactor):
        self.safetyFactor = safetyFactor

    def __setKb(self, d):
        self.kb = sh.shaftFactor_Kb(d)

    def __setDLowercase(self, d):
        self.d = d

    def __setKt(self, D=None, r=None, d=None, Kt=None, Type=None):
        if Kt is None and D is not None:
            if Type == "stepped bar":
                self.Kt = sh.shaftKtFactorSteppedBarOfCircularCrossSection(D, d, r)
                self.static = False

            elif Type == "circumferential groove":
                self.Kt = sh.shaftKtFactorCircumferentialGrooveInShaft(D, d, r)
                self.static = False

            elif Type == "Tipton FEM":

                self.Kt = sh.shaftKtTiptonFactorSteppedBarOfCircularCrossSection(D, d, r)
                self.static = False
            else:
                self.Kt = Kt
                self.static = False

        elif Kt is not None and D is None:
            self.Kt = Kt
            self.static = True

        else:
            raise ValueError

    def __setKts(self, D=None, r=None, d=None, Kts=None, Type=None):
        if Kts is None and D is not None:
            if Type == "stepped bar":
                self.Kts = sh.shaftKtsFactorSteppedBarOfCircularCrossSection(D, d, r)
                self.static = False
            elif Type == "circumferential groove":
                self.Kts = sh.shaftKtsFactorCircumferentialGrooveInShaft(D, d, r)
                self.static = False
            else:
                self.Kts = Kts
                self.static = False
        elif Kts is not None and D is None:
            self.Kts = Kts
            self.static = True
        else:
            raise ValueError

    def __setQ(self):
        a = sh.shaftConstantA(self.Sut)
        self.q = sh.shaftNotchSensitivity(a, self.getR())

    def __setQs(self):
        a = sh.shaftConstantA(self.Sut, method="Torsion")
        self.qs = sh.shaftNotchSensitivity(a, self.getR())

    def __setKf(self):
        self.Kf = sh.shaftKfFactor(self.getKt(), self.getQ())

    def __setKfs(self):
        self.Kfs = sh.shaftKfsFactor(self.getKts(), self.getQs())

    def __setSe(self):
        self.Se = sh.shaftStress_Se(self.getKa(), self.getKb(), self.getKc(), self.getKd(),
                                    self.getKe(), Kf=1, SeLine=self.getSeLine())

    # getters
    def getDictionary(self):
        """
        Get the dictionary parameter.
        :return: dictionary of kb and d.
        """
        return self.dictionary

    def getNotchType(self) -> str:
        """
        Get the Notch Type.
        :return: String.
        """
        return self.notchType

    def getKb(self) -> float:
        """
        Get the kb factor.
        :return: numpy.float.
        """
        return self.kb

    def getKt(self) -> float:
        """
        Get the Kt factor.
        :return: Float.
        """
        return self.Kt

    def getKts(self) -> float:
        """
        Get the Kts factor.
        :return: Float.
        """
        return self.Kts

    def getR(self) -> float:
        """
        Get the notch's radius.
        :return: Float.
        """
        return self.r

    def getShaftStress_Se(self) -> float:
        """
        Get the Se.
         :return: numpy.float64.
        """
        return self.Se

    def getSeLine(self) -> float:
        """
        Get the Se line.
         :return: numpy.float64.
        """
        return self.SeLine

    def getKa(self) -> float:
        """
        Get the ka factor.
         :return: numpy.float64.
        """
        return self.factorKa

    def getKc(self) -> Union[float, int]:
        """
        Get the kc factor.
         :return: numpy.float64.
        """
        return self.factorKc

    def getKd(self) -> float:
        """
        Get the kd factor.
         :return: numpy.float64.
        """
        return self.factorKd

    def getKe(self) -> float:
        """
        Get the ke factor.
        :return: numpy.float64.
        """
        return self.factorKe

    def getMethod(self) -> str:
        """
        Get the failure criteria.
        :return: String.
        """
        return self.method

    def getDLowercase(self) -> float:
        """
        Get the minimum shaft's diameter.
         :return: numpy.float64.
        """
        return self.d

    def getDUppercase(self) -> float:
        """
        Get the shoulder's diameter.
         :return: numpy.float64.
        """
        return self.D

    def getSafetyFactor(self) -> float:
        """
        Get the shaft's diameter.
         :return: numpy.float64.
        """
        return self.safetyFactor

    def getSut(self) -> float:
        """
        Get the ultimate stress.
         :return: numpy.float64.
        """
        return self.Sut

    def getSy(self) -> float:
        """
        Get the yielding stress.
         :return: numpy.float64.
        """
        return self.Sy

    def getKf(self) -> float:
        """
        Get the Kf factor.
         :return: numpy.float64.
        """
        return self.Kf

    def getKfs(self) -> float:
        """
        Get the Kfs factor.
         :return: numpy.float64.
        """
        return self.Kfs

    def getVonMissesStress(self) -> float:
        """
        Get the Von Misses stress.
         :return: numpy.float64.
        """
        vonMisses = sh.shaftVonMissesStress(Ma=self.Ma, Mm=self.Mm, Ta=self.Ta, Tm=self.Tm, Kf=self.getKf(),
                                            Kfs=self.getKfs(), d=self.getDLowercase())
        return vonMisses

    def getSafetyFactorOfVonMisses(self) -> float:
        """
        Get the Von Misses safety factor.
        :return: float.
        """
        return self.Sy / self.getVonMissesStress()

    def getWideTable(self, zero: bool = False) ->\
            Dict[str, Union[List[Union[str, Any]], List[Union[Union[float, int], Any]]]]:
        """
        Get the Von Misses safety factor.
        :return: pandas.DataFrame.
        """
        Diameter_subscript = "<sub>" + self.method + "</sub>"
        Safety_subscript = "<sub>" + self.method + "</sub>"
        units = ["Dimensionless",  # 1
                 "Dimensionless",  # 2
                 "Dimensionless",  # 3
                 "Dimensionless",  # 4
                 "Dimensionless",  # 5
                 "Dimensionless",  # 6
                 "Dimensionless",  # 7
                 "Dimensionless",  # 8
                 "Dimensionless",  # 9
                 "Dimensionless",  # 10
                 "Dimensionless",  # 11
                 "Dimensionless",  # 12
                 "MPa",            # 13
                 "Dimensionless",  # 14
                 "mm",             # 15
                 "Dimensionless",  # 16
                 "mm",             # 17
                 "MPa",            # 18
                 "MPa",            # 19
                 "MPa",            # 20
                 "MPa"]            # 21

        keys = ["<h3>k<sub>a</sub></h3>",                                   # 1
                "<h3>k<sub>b</sub></h3>",                                   # 2
                "<h3>k<sub>c</sub></h3>",                                   # 3
                "<h3>k<sub>d</sub></h3>",                                   # 4
                "<h3>k<sub>c</sub></h3>",                                   # 5
                "<h3>k<sub>f</sub></h3>",                                   # 6
                "<h3>K<sub></sub></h3>",                                    # 7
                "<h3>K<sub>fs</sub></h3>",                                  # 8
                "<h3>q             </h3>",                                    # 9
                "<h3>q<sub>s</sub></h3>",                                   # 10
                "<h3>K<sub>t</sub></h3>",                                   # 11
                "<h3>K<sub>ts</sub></h3>",                                  # 12
                "<h3>\u03C3 <sub>Von Misses</sub></h3>",                    # 13
                "<h3>\u03B7 <sub>Von Misses</sub></h3>",                    # 14
                "<h3>d<sub>" + str(Diameter_subscript) + "</sub></h3>",     # 15
                "<h3>\u03B7<sub>" + str(Safety_subscript) + "</sub></h3>",  # 16
                "<h3>D</h3>",                                               # 17
                "<h3>S<sub>Y</sub></h3>",                                  # 18
                "<h3>S<sub>ut</sub></h3>",                                  # 19
                "<h3>S<sub>e</sub></h3>",                                   # 20
                "<h3>S'<sub>e</sub></h3>"                                   # 21
                ]
        values = [self.getKa(),                           # 1
                  self.getKb(),                           # 2
                  self.getKc(),                           # 3
                  self.getKd(),                           # 4
                  self.getKe(),                           # 5
                  self.kf,                                # 6
                  self.getKf(),                           # 7
                  self.getKfs(),                          # 8
                  self.getQ(),                            # 9
                  self.getQs(),                           # 10
                  self.getKt(),                           # 11
                  self.getKts(),                          # 12
                  self.getVonMissesStress()*1e-6,         # 13
                  self.getSafetyFactorOfVonMisses(),      # 14
                  self.getDLowercase()*1e3,               # 15
                  self.getSafetyFactor(),                 # 16
                  self.getDUppercase()*1e3,                   # 17
                  self.getSy()*1e-6,                      # 18
                  self.getSut()*1e-6,                     # 19
                  self.getShaftStress_Se()*1e-6,          # 20
                  self.getSeLine()*1e-6                   # 21
                  ]
        if zero is False:
            return {"Properties": keys, "Values": values, "Units": units}
        else:
            return {"Properties": keys, "Values": np.zeros(len(keys)), "Units": units}



    def getQ(self) -> float:
        """
        Get the Q factor.
        :return: Float.
        """
        return self.q

    def getQs(self) -> float:
        """
        Get the Qs factor.
        :return: Float.
        """
        return self.qs

    def __getDiameterForSolver(self):
        """
        This function will find the diameter when the safety factor is given.
        :return: Float.
        """
        return sh.shaftDiameter(Ma=self.Ma, Mm=self.Mm, Ta=self.Ta, Tm=self.Tm, Kf=self.getKf(),
                                Kfs=self.getKfs(), Se=self.getShaftStress_Se(), Sut=self.getSut(),
                                Sy=self.getSy(), n=self.getSafetyFactor(), method=self.getMethod())

    def __decisionMakerForDiameterAndSafetyFactor(self, dTrial, error=1e-3):
        if self.getDLowercase() is None and self.getSafetyFactor() is not None:
            self.__setDLowercase(dTrial)
            self.__setKb(dTrial)
            self.__setKt(self.getDUppercase(), self.getR(), self.getDLowercase(), self.getKt(), self.getNotchType())
            self.__setKts(self.getDUppercase(), self.getR(), self.getDLowercase(), self.getKts(), self.getNotchType())
            self.__setKf()
            self.__setKfs()
            self.__setSe()
            self.dictionary = self.solveForKbAndD(dTrial, error)

        elif self.getDLowercase() is not None and self.getSafetyFactor() is None:
            self.__setKt(self.getDUppercase(), self.getR(), self.getDLowercase(), self.getKt(), self.getNotchType())
            self.__setKts(self.getDUppercase(), self.getR(), self.getDLowercase(), self.getKts(), self.getNotchType())
            self.__setKb(self.getDLowercase())
            self.__setKf()
            self.__setKfs()
            self.__setSe()
            self.__setSafetyFactor(sh.shaftSafetyFactor(Ma=self.Ma, Mm=self.Mm, Ta=self.Ta, Tm=self.Tm,
                                                        Kf=self.getKf(), Kfs=self.getKfs(), Se=self.getShaftStress_Se(),
                                                        Sut=self.getSut(), Sy=self.getSy(), d=self.getDLowercase(),
                                                        method=self.getMethod()))

    def solveForKbAndD(self, dTrial, error=1e-3):
        """
        This function will solve for kb and d, when this parameters are not initially defined.
        :param dTrial: the first attempt diameter.
        :param error: the minimum difference between the  n + 1 diameter and the n diameter, that is,
        error = d_(n+1) - d_(n).
        :return: dictionary with d and kb.
        """
        listD = list()
        listKb = list()
        if 2.79e-3 <= dTrial <= 51e-3:
            listD.append(1.2*dTrial)
            listKb.append(sh.shaftFactor_Kb(1.2*dTrial))
        elif 51e-3 < dTrial <= 254e-3:
            listD.append(0.7*dTrial)
            listKb.append(sh.shaftFactor_Kb(0.7*dTrial))
        else:
            listD.append(2.79e-3)
            listKb.append(sh.shaftFactor_Kb(2.79e-3))
        listD.append(dTrial)
        listKb.append(sh.shaftFactor_Kb(dTrial))
        k = 0
        if not self.static:
            while abs(listD[k+1]-listD[k]) > error:
                if 2.79e-3 <= self.getDLowercase() <= 254e-3:
                    self.__setDLowercase(listD[-1])
                    self.__setKb(listD[-1])
                    self.__setKt(D=self.getDUppercase(), r=self.getR(), d=listD[-1], Type=self.getNotchType())
                    self.__setKts(D=self.getDUppercase(), r=self.getR(), d=listD[-1], Type=self.getNotchType())
                    self.__setKfs()
                    self.__setKf()
                    self.__setSe()
                    if 2.79e-3 <= self.getDLowercase() <= 254e-3:
                        listD.append(self.__getDiameterForSolver())
                    elif self.getDLowercase() < 2.79e-3:
                        listD.append(2.8e-3)
                    else:
                        listD.append(253e-3)
                    listKb.append(sh.shaftFactor_Kb(listD[-1]))
                    k += 1
                    if k == 10000:
                        break
                elif self.getDLowercase() < 2.79e-3:
                    listD.append()
        else:
            while abs(listD[k+1]-listD[k]) > error:
                self.__setDLowercase(listD[-1])
                self.__setKb(listD[-1])
                self.__setKt(D=self.getDUppercase(), Kt=self.getKt())
                self.__setKts(D=self.getDUppercase(), Kts=self.getKts())
                self.__setKfs()
                self.__setKf()
                self.__setSe()
                if 2.79e-3 <= self.getDLowercase() <= 254e-3:
                    listD.append(self.__getDiameterForSolver())
                elif self.getDLowercase() < 2.79e-3:
                    listD.append(2.79e-3)
                else:
                    listD.append(254e-3)
                listKb.append(sh.shaftFactor_Kb(listD[-1]))
                k += 1
                if k == 10000:
                    break
        self.__setDLowercase(listD[-1])
        self.__setKb(listD[-1])
        return {r"Diameter:": listD, r"Factor $K_b$": listKb}

    def getSecondMomentOfArea(self):
        """:return float"""
        return pow(self.getDLowercase(), 4) * np.pi / 64
