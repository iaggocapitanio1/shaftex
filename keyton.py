"""
This mode defines the key's methods and attributes.
@Description:
This module has the aim to give the main methods and attributes  to handle a shaft project.
The module is built in SI units. Based on the book Shigley’s Mechanical Engineering Design.
"""
__author__ = "Iaggo Capitanio"
__copyright__ = "Copyright (C) 2020 Iaggo Capitanio"
__license__ = "Public Domain"
__version__ = "1.0"

from Shafton.keysDIN6885 import *
import numpy as np
import pandas as pd
import ctypes
import source_images


myAppId = u'ShaftExploration.Shaftex.version-1.0'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppId)


class Key:
    """This class will define a key.
    """
    def __init__(self, diameter, Sy, torque, safetyFactorCompression=None, safetyFactorShearing=None, Form=FormA,
                 style=False, zero=False):
        """
        @Explanation:
        This class defines a parallel key. Based on the norm DIN(Deutsches Institut für Normung) 6885.

        @methods:
            @Public:
            - setKeyType : defines the type of the key. It can be Form A or Form B or another one attached to the
            module KeysDIN6885.

            - forceKey : returns the force acting on the key, according withe the type of entry.

            - getTable : returns two pandas' table. The first has the main table with all properties of interest and the
            other one has the key's attributes: width(breite), height(Höhe), t1(Tiefe Eins).

            @Private:
            - stressShearing : it gives the stress caused by shearing.

            - stressCompression : it gives the stress caused by compression.

            - safetyFactorShearing : it gives the safety factor of the stress Shearing.

            - safetyFactorCompression : it gives the safety factor of the stress Compression.

            @Static:
            - setTableStyle:  it simply defines the style of one pandas' table.

        @parameters:
        :parameter diameter : shaft diameter.
        :parameter Sy : yielding stress.
        :parameter torque : torque.
        :parameter safetyFactorCompression : safety factor for compression
        :parameter safetyFactorShearing : safety factor for shearing
        :parameter style: Enable or disable stylized presentation mode of the table.
        """
        self.diameter = diameter
        self.Sy = Sy
        self.torque = torque
        self.zero = zero
        self.safetyFactorCompression = safetyFactorCompression
        self.safetyFactorShearing = safetyFactorShearing
        self.SyShearing = self.Sy/np.sqrt(3)
        self.msgError = ""
        self.keyType = Form(self.diameter)
        self.__styleMode = style

    def forceKey(self):
        """
        @Explanation:
        This function returns the forces acting on the key.
        :return: float
        """
        if self.safetyFactorCompression is None and self.safetyFactorShearing is None:
            return 2 * self.torque / self.diameter
        elif self.safetyFactorShearing is not None and self.safetyFactorCompression is None:
            return self.SyShearing * self.keyType.keyAreaShearing() / self.safetyFactorShearing
        elif self.safetyFactorShearing is None and self.safetyFactorCompression is not None:
            return self.Sy * self.keyType.keyAreaCompression() / self.safetyFactorCompression
        else:
            self.msgError = "One safety factor must be None and the other not None or None. please try again!"
            return ValueError

    def __stressShearing(self):
        """
        @Explanation:
        This function returns the shearing stress.
        :return: float
        """
        return self.forceKey() / self.keyType.keyAreaShearing()

    def __stressCompression(self):
        """
        @Explanation:
        This function returns the compression stress.
        :return: float
        """
        return self.forceKey() / self.keyType.keyAreaCompression()

    def __safetyFactorShearing(self):
        """
        @Explanation:
        This function returns the safety factor of shearing.
        :return: float
        """
        return self.SyShearing / self.__stressShearing()

    def __safetyFactorCompression(self):
        """
        @Explanation:
        This function returns the safety factor of compression.
        """
        return self.Sy / self.__stressCompression()

    def getTable(self):
        """
        @Explanation:
        This function returns two pandas' table, the main table and the key table respectively.
        :return: pandas.DataFrame
        """
        dic1 = dict()
        if not self.zero:
            if all([i == 0 for i in self.keyType.row]) and all([i == 0 for i in self.keyType.key]):
                self.msgError = "There is some error! Try again!"
                return self.msgError
            if self.safetyFactorCompression is None and self.safetyFactorShearing is None:
                dic1 = {"Length [mm]": self.keyType.row,
                        "Shearing area [cm²]": self.keyType.keyAreaShearing() * 1e5,
                        "Compressing area [cm²]": self.keyType.keyAreaShearing() * 1e5,
                        "Force [N]": self.forceKey() * np.ones_like(self.__safetyFactorCompression()),
                        "η compress": self.__safetyFactorCompression(),
                        "η shearing": self.__safetyFactorShearing()}
            elif self.safetyFactorShearing is not None and self.safetyFactorCompression is None:
                dic1 = {"Length [mm]": self.keyType.row,
                        "Shearing area [cm²]": self.keyType.keyAreaShearing() * 1e5,
                        "Compressing area [cm²]": self.keyType.keyAreaCompression() * 1e5,
                        "Force [N]": self.forceKey(),
                        "η compress": self.__safetyFactorCompression(),
                        "η shearing": np.ones_like(self.forceKey()) * self.__safetyFactorShearing()}
            elif self.safetyFactorShearing is None and self.safetyFactorCompression is not None:
                dic1 = {"Length [mm]": self.keyType.row,
                        "Shearing area [cm²]": self.keyType.keyAreaShearing() * 1e6,
                        "Compressing area [cm²]": self.keyType.keyAreaCompression() * 1e6,
                        "Force [N]": self.forceKey(),
                        "η compress": np.ones_like(self.forceKey()) * self.safetyFactorCompression,
                        "η shearing": self.__safetyFactorShearing()}
            df1 = pd.DataFrame(dic1)
            df2 = pd.DataFrame([{"b": self.keyType.key[0], "h": self.keyType.key[1], "$t_1$": self.keyType.key[2]}])
            if self.__styleMode:
                msg = "Key's table "
                df1 = self.__setTableStyle(df1, msg)
                msg = "(Breite, Höhe, Tiefe Eins) @DIN6885"
                df2 = self.__setTableStyle(df2, msg)
            return df1, df2
        else:
            dic1 = {"Length [mm]": self.keyType.row,
                    "Shearing area [cm²]": np.zeros(len(self.keyType.row)),
                    "Compressing area [cm²]": np.zeros(len(self.keyType.row)),
                    "Force [N]": np.zeros(len(self.keyType.row)),
                    "η compress": np.zeros(len(self.keyType.row)),
                    "η shearing": np.zeros(len(self.keyType.row))}
            df1 = pd.DataFrame(dic1)
            df2 = pd.DataFrame([{"b": self.keyType.key[0], "h": self.keyType.key[1], "$t_1$": self.keyType.key[2]}])
            return df1, df2

    @staticmethod
    def __setTableStyle(table, msg):
        """
            @Explanation:
            This function set the Style of one pandas' table.

            @Parameters:
            :parameter table : pandas object table.
            :parameter msg : a string to show underneath the table.
            :return: pandas.DataFrame
            """
        table = table.style.set_properties(**{'background-color': 'black',
                                              'color': 'lawngreen',
                                              'border-color': 'white'}
                                           ).set_table_styles([dict(selector="th",
                                                                    props=[("font-size", "110%"),
                                                                           ("text-align", "center")]),
                                                               dict(selector="caption",
                                                                    props=[("caption-side", "bottom")])
                                                               ]).set_caption(msg)
        return table
