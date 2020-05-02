"""
@Description:
This module has the aim to construct a material class.who will dialog with the UI.
"""
__author__ = "Iaggo Capitanio"
__copyright__ = "Copyright (C) 2020 Iaggo Capitanio"
__license__ = "Public Domain"
__version__ = "1.0"

import pandas as pd
import ctypes
from typing import List, Dict, Union
myAppId = u'ShaftExploration.Shaftex.version-1.0'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppId)


class MaterialDataBaseAISI:
    """
    @Description:
    Creates the material database tobe used in the program.
    """
    def __init__(self):
        self.__Id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
                     27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37]
        self.__Name = ["AISI 1020 Steel, cold rolled",
                        "AISI 1020 Steel, as rolled",
                        "AISI 1020 Steel, normalized at 870°C (1600°F)",
                        "AISI 1020 Steel, annealed at 870°C (1600°F)",
                        "AISI 1030 Steel, cold drawn, 19-32 mm (0.75-1.25 in) round",
                        "AISI 1030 Steel, as rolled",
                        "AISI 1030 Steel, normalized 925°C (1700°F)",
                        "AISI 1030 Steel, annealed at 845°C (1550°F)",
                        "AISI 1035 Steel, as rolled, 19-32 mm (0.75-1.25 in) round",
                        "AISI 1035 Steel, cold drawn, 19-32 mm (0.75-1.25 in) round",
                        "AISI 1037 Steel, Hot Rolled Bar (UNS G10370)",
                        "AISI 1037 Steel, Cold Drawn Bar (UNS G10370)",
                        "AISI 1040 Steel, hot rolled, 19-32 mm (0.75-1.25 in) round",
                        "AISI 1040 Steel, as cold drawn, 16-22 mm (0.625-0.875 in) round",
                        "AISI 1040 Steel, as cold drawn, 22-32 mm (0.875-1.25 in) round",
                        "AISI 1040 Steel, as cold drawn, 32-50 mm (1.25-2 in) round",
                        "AISI 1040 Steel, as cold drawn, 50-75 mm (2-3 in) round",
                        "AISI 1040 Steel, as rolled",
                        "AISI 1040 Steel, normalized at 900°C (1650°F)",
                        "AISI 1040 Steel, annealed at 790°C (1450°F) round",
                        "AISI 1040 Steel, normalized at 900°C (1650°F), air cooled, 13 mm (0.5 in.) round",
                        "AISI 1040 Steel, normalized at 900°C (1650°F), air cooled, 25 mm (1 in.) round",
                        "AISI 1040 Steel, normalized at 900°C (1650°F), air cooled, 50 mm (2 in.) round",
                        "AISI 1040 Steel, normalized at 900°C (1650°F), air cooled, 100 mm (4 in.) round",
                        "AISI 1040 Steel, oil quenched from 855°C (1570°F), 540°C (1000°F)"
                        " temper, 13 mm (0.5 in.) round",
                        "AISI 1040 Steel, oil quenched from 855°C (1570°F), 540°C (1000°F)"
                        " temper, 25 mm (1 in.) round",
                        "AISI 1040 Steel, oil quenched from 855°C (1570°F), 540°C (1000°F) temper, 50 mm (2 in.) round",
                        "AISI 1040 Steel, oil quenched from 855°C (1570°F), 540°C (1000°F)"
                        " temper, 100 mm (4 in.) round",
                        "AISI 1042 Steel, Hot Rolled Bar (UNS G10420)",
                        "AISI 1042 Steel, Cold Drawn Bar (UNS G10420)",
                        'AISI 1050 Steel, cold drawn, 19-32 mm (0.75-1.25 in) round',
                        "AISI 1050 Steel, cold drawn, annealed, 19-32 mm (0.75-1.25 in) round",
                        "AISI 1050 Steel, cold drawn, low temperature, stress relieved,"
                        " 16-22 mm (0.625-0.875 in) round",
                        "AISI 1050 Steel, cold drawn, high temperature, stress relieved,"
                        " 16-22 mm (0.625-0.875 in) round",
                        "AISI 1050 Steel, as rolled",
                        "AISI 1050 Steel, normalized at 900°C (1650°F)",
                        "AISI 1050 Steel, annealed at 790°C (1450°F)"]

        self.__Tensile_Strength_Yielding = [350.0,
                                            330.0,
                                            435.0,
                                            294.74,
                                            440.0,
                                            345.0,
                                            345.0,
                                            345.0,
                                            370.0,
                                            460.0,
                                            279.0,
                                            476.0,
                                            290.0,
                                            550.0,
                                            515.0,
                                            485.0,
                                            450.0,
                                            415.0,
                                            370.0,
                                            350.0,
                                            403.0,
                                            374.0,
                                            365.0,
                                            340.0,
                                            500.0,
                                            469.0,
                                            412.0,
                                            396.0,
                                            303.0,
                                            517.0,
                                            580.0,
                                            550.0,
                                            655.0,
                                            515.0,
                                            414.0,
                                            425.0,
                                            365.0]

        self.__Tensile_Strength_Ultimate = [420.0,
                                            450.0,
                                            440.0,
                                            394.72,
                                            525.0,
                                            550.0,
                                            525.0,
                                            460.0,
                                            585.0,
                                            550.0,
                                            510.0,
                                            565.0,
                                            525.0,
                                            620.0,
                                            585.0,
                                            550.0,
                                            515.0,
                                            620.0,
                                            595.0,
                                            515.0,
                                            608.0,
                                            590.0,
                                            581.0,
                                            583.0,
                                            722.0,
                                            664.0,
                                            635.0,
                                            621.0,
                                            552.0,
                                            614.0,
                                            690.0,
                                            655.0,
                                            725.0,
                                            655.0,
                                            725.0,
                                            752.0,
                                            635.0]
        self.__Modulus_of_Elasticity = [186.0,
                                        186.0,
                                        186.0,
                                        186.0,
                                        206.0,
                                        206.0,
                                        206.0,
                                        206.0,
                                        196.0,
                                        196.0,
                                        200.0,
                                        206.0,
                                        200.0,
                                        200.0,
                                        200.0,
                                        200.0,
                                        200.0,
                                        200.0,
                                        200.0,
                                        200.0,
                                        200.0,
                                        200.0,
                                        200.0,
                                        200.0,
                                        200.0,
                                        200.0,
                                        200.0,
                                        200.0,
                                        200.0,
                                        200.0,
                                        205.0,
                                        205.0,
                                        205.0,
                                        205.0,
                                        205.0,
                                        205.0,
                                        205.0]
        self.__Poisson_ratio = [0.29,
                                0.29,
                                0.29,
                                0.29,
                                0.29,
                                0.29,
                                0.29,
                                0.29,
                                0.29,
                                0.29,
                                0.29,
                                0.29,
                                0.29,
                                0.29,
                                0.29,
                                0.29,
                                0.29,
                                0.29,
                                0.29,
                                0.29,
                                0.29,
                                0.29,
                                0.29,
                                0.29,
                                0.29,
                                0.29,
                                0.29,
                                0.29,
                                0.29,
                                0.29,
                                0.29,
                                0.29,
                                0.29,
                                0.29,
                                0.29,
                                0.29,
                                0.29]

        self.dictionary = {"Id": self.getId(), "Name": self.getName(),
                           "Tensile Strength Ultimate": self.getTensileStrengthUltimate(),
                           "Tensile Strength Yield": self.getTensileStrengthYielding(),
                           "Modulus of Elasticity": self.getModulusOfElasticity(),
                           "Poisson's Ratio": self.getPoissonRatio()}

    def getId(self) -> List[int]:
        """

        :return: list.
        """
        return self.__Id

    def getName(self) -> List[float]:
        """

        :return: list.
        """
        return self.__Name

    def getTensileStrengthUltimate(self) -> List[float]:
        """

        :return: list.
        """
        return self.__Tensile_Strength_Ultimate

    def getTensileStrengthYielding(self) -> List[float]:
        """

        :return: list.
        """
        return self.__Tensile_Strength_Yielding

    def getModulusOfElasticity(self) -> List[float]:
        """

        :return: list.
        """
        return self.__Modulus_of_Elasticity

    def getPoissonRatio(self) -> List[float]:
        """

        :return: list.
        """
        return self.__Poisson_ratio

    def getDictionary(self) -> Dict[str, List[Union[float, int, str]]]:
        """

        :return: dictionary.
        """
        return self.dictionary

    def getFields(self) -> List[str]:
        """

        :return: list.
        """
        return list(self.getDictionary().keys())

    def countRows(self) -> int:
        """

        :return: int.
        """

        return len(self.getDictionary().get(self.getFields()[0]))

    def countColumns(self) -> int:
        """

        :return: int.
        """
        return len(self.getFields())

    def getColumnName(self, column: int) -> str:
        """

        :param column:
        :return: str
        """
        try:
            return self.getFields()[column]
        except IndexError:
            print("The column index is outside the boundaries!")
            raise IndexError

    def getItem(self, row: int, column: int) -> Union[str, int, float]:
        """

        :param row: int.
        :param column: int.
        :return: int, float, str.
        """
        try:
            return list(self.getDictionary().values())[column][row]

        except IndexError:
            print("The index is outside the boundaries!")
            raise IndexError

    def getIdForMaterial(self, material: str) -> int:
        """

        :param material:
        :return:
        """
        k = 0
        for i in self.getDictionary()[self.getColumnName(column=1)]:

            if i == material:
                return self.getItem(row=k, column=0)
            k += 1

            if k >= self.countRows():
                print(material + " not found!")
                raise ValueError

    def getTensileStrengthUltimateForMaterial(self, material: str) -> float:
        """

        :param material:
        :return:
        """
        k = 0
        for i in self.getDictionary()[self.getColumnName(column=1)]:

            if i == material:
                return self.getItem(row=k, column=2)
            k += 1

            if k >= self.countRows():
                print(material + " not found!")
                raise ValueError



    def getTensileStrengthYieldingForMaterial(self, material: str) -> float:
        """

        :param material:
        :return:
        """
        k = 0
        for i in self.getDictionary()[self.getColumnName(column=1)]:

            if i == material:
                return self.getItem(row=k, column=3)
            k += 1

            if k >= self.countRows():
                print(material + " not found!")
                raise ValueError

    def getModulusOfElasticityForMaterial(self, material: str) -> float:
        """

        :param material:
        :return:
        """
        k = 0
        for i in self.getDictionary()[self.getColumnName(column=1)]:

            if i == material:
                return self.getItem(row=k, column=4)
            k += 1

            if k >= self.countRows():
                print(material + " not found!")
                raise ValueError

    def getPoissonRatioForMaterial(self, material: str) -> float:
        """

        :param material:
        :return:
        """
        k = 0
        for i in self.getDictionary()[self.getColumnName(column=1)]:
            if i == material:
                return self.getItem(row=k, column=5)

            k += 1

            if k >= self.countRows():
                print(material + " not found!")
                raise ValueError


    def getMaterialProperties(self, material: str) -> Dict[str, Union[float, int, str]]:
        """

        :param material:
        :return:
        """

        fields = self.getFields()
        Id = self.getIdForMaterial(material)
        Name = material
        Tensile_Strength_Ultimate = self.getTensileStrengthUltimateForMaterial(material)
        Tensile_Strength_Yielding = self.getTensileStrengthYieldingForMaterial(material)
        Modulus_Of_Elasticity = self.getModulusOfElasticityForMaterial(material)
        Poisson_Ratio = self.getPoissonRatioForMaterial(material)
        prop = [Id,
                Name,
                Tensile_Strength_Ultimate,
                Tensile_Strength_Yielding,
                Modulus_Of_Elasticity,
                Poisson_Ratio]

        return {fields[0]: prop[0], fields[1]: prop[1], fields[2]: prop[2],
                fields[3]: prop[3], fields[4]: prop[4], fields[5]: prop[5]}



class MaterialAISI:
    """
    This class gives the materials present in material.db file.
    """
    def __init__(self, materialInput: str):
        self.material_name = materialInput
        self.material_db = MaterialDataBaseAISI()

    def material(self):
        """:return list"""
        prop = self.material_db.getMaterialProperties(self.material_name)
        return list(prop.values())

    def getAllMaterialPandasDataFrame(self):
        """:return pandas DataFrame"""
        return pd.DataFrame(self.material_db.getDictionary())

    def getAllMaterialNameListPandasDataFrame(self):
        """:return pandas DataFrame"""
        return pd.DataFrame(self.material_db.getDictionary()['Name'])

    def getMaterialTensileStrengthUltimate(self):
        """:return pandas DataFrame"""
        return self.material()[2] * 1e6

    def getMaterialTensileStrengthYield(self):
        """:return pandas DataFrame"""
        return self.material()[3] * 1e6

    def getMaterialModulusOfElasticity(self):
        """:return pandas DataFrame"""
        return self.material()[4] * 1e9

    def getMaterialPoissonsRatio(self):
        """:return pandas DataFrame"""
        return self.material()[5]

if __name__ == '__main__':
    a = MaterialAISI(materialInput="AISI 1020 Steel, cold rolled")
    print(a.getAllMaterialNameListPandasDataFrame())
