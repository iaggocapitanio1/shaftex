"""
        It creates some classes to DIN 6885 keys.
"""
__author__ = "Iaggo Capitanio"
__copyright__ = "Copyright (C) 2020 Iaggo Capitanio"
__license__ = "Public Domain"
__version__ = "1.0"
import ctypes
import numpy as np


myAppId = u'ShaftExploration.Shaftex.version-1.0'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppId)


class FormA:
    """
        It creates a class form the key type: Form B
    """
    def __init__(self, diameter):
        self.diameter = diameter
        self.row = self.keyTableDIN6885()[0]
        self.key = self.keyTableDIN6885()[1]

    def keyAreaShearing(self):
        """:return: float"""
        length = np.array(self.row)
        radius = self.key[0]/2
        sides = np.pi * pow(radius, 2)
        center = (length - 2 * radius) * 2 * radius
        return (sides + center) * 1e-6

    def keyAreaCompression(self):
        """

        :return: float
        """
        length = np.array(self.row)
        radius = self.key[0] / 2
        height = self.key[1]
        t = self.key[2]
        edges = length - 2 * radius + np.pi * radius
        loftiness = height - t
        return loftiness * edges * 1e-6

    def keyTableDIN6885(self):
        """

        :return: tuple
        """
        row_1 = np.array(range(6, 21, 2))
        row_2 = np.array([6, 8, 10, 12, 14, 16, 18, 20, 22, 25, 28, 32, 36])
        row_3 = np.array([8, 10, 12, 14, 16, 18, 20, 22, 25, 28, 32, 36, 40, 45, ])
        row_4 = np.array([10, 12, 14, 16, 18, 20, 22, 25, 28, 32, 36, 40, 45, 50])
        row_5 = np.array([14, 16, 18, 20, 22, 25, 28, 32, 36, 40, 45, 50, 56, 63])
        row_6 = np.array([18, 20, 22, 25, 28, 32, 36, 40, 45, 50, 56, 63, 70, 80, ])
        row_7 = np.array([22, 25, 28, 32, 36, 40, 45, 50, 56, 63, 70, 80, 90, 100])
        row_8 = np.array([28, 32, 36, 40, 45, 50, 56, 63, 70, 80, 90, 100, 110, 125])
        row_9 = np.array([36, 40, 45, 50, 56, 63, 70, 80, 90, 100, 110, 125, 140, 160])
        row_10 = np.array([45, 50, 56, 63, 70, 80, 90, 100, 110, 125, 140, 160, 180])
        row_11 = np.array([50, 56, 63, 70, 80, 90, 100, 110, 125, 140, 160, 180, 200])
        row_12 = np.array([56, 63, 70, 80, 90, 100, 110, 125, 140, 160, 180, 200, 220])
        row_13 = np.array([63, 70, 80, 90, 100, 110, 125, 140, 160, 180, 200, 220, 250])
        row_14 = np.array([70, 80, 90, 100, 110, 125, 140, 160, 180, 200, 220, 250, 280])
        row_15 = np.array([80, 90, 100, 110, 125, 140, 160, 180, 200, 220, 250, 280, 320])
        row_16 = np.array([90, 100, 110, 125, 140, 160, 180, 200, 220, 250, 280, 320, 360])
        row_17 = np.array([100, 110, 125, 140, 160, 180, 200, 220, 250, 280, 320, 360, 400])
        row_18 = np.array([110, 125, 140, 160, 180, 200, 220, 250, 280, 320, 360, 400])
        row_19 = np.array([140, 160, 180, 200, 220, 250, 280, 320, 360, 400])
        row_20 = np.array([125, 140, 160, 180, 200, 220, 250, 280, 320, 360, 400])
        row_21 = np.array([160, 180, 200, 220, 250, 280, 320, 360, 400])
        row_22 = np.array([180, 200, 220, 250, 280, 320, 360, 400])
        row_23 = np.array([200, 220, 250, 280, 320, 360, 400])
        row_24 = np.array([220, 250, 280, 320, 360, 400])
        row_25 = np.array([250, 280, 320, 360, 400])
        row_26 = np.array([280, 320, 360, 400, ])

        ################################################################################################################
        row = [0, row_1, row_2, row_3, row_4, row_5, row_6, row_7, row_8, row_9, row_10, row_11, row_12, row_13, row_14,
               row_15, row_16, row_17, row_18, row_19, row_20, row_21, row_22, row_23, row_24, row_25, row_26]
        ################################################################################################################

        key_1 = np.array([2, 2, 1.2])
        key_2 = np.array([3, 3, 1.8])
        key_3 = np.array([4, 4, 2.5])
        key_4 = np.array([5, 5, 3])
        key_5 = np.array([6, 6, 3.5])
        key_6 = np.array([8, 7, 4])
        key_7 = np.array([10, 8, 5])
        key_8 = np.array([12, 8, 5])
        key_9 = np.array([14, 9, 5.5])
        key_10 = np.array([16, 10, 6])
        key_11 = np.array([18, 11, 7])
        key_12 = np.array([20, 12, 7.5])
        key_13 = np.array([22, 14, 9])
        key_14 = np.array([25, 14, 9])
        key_15 = np.array([28, 16, 10])
        key_16 = np.array([32, 18, 11])
        key_17 = np.array([36, 20, 12])
        key_18 = np.array([40, 22, 13])
        key_19 = np.array([45, 25, 15])
        key_20 = np.array([50, 28, 10])
        key_21 = np.array([56, 32, 20])
        key_22 = np.array([63, 32, 20])
        key_23 = np.array([70, 36, 22])
        key_24 = np.array([80, 40, 25])
        key_25 = np.array([90, 45, 28])
        key_26 = np.array([100, 50, 31])

        ################################################################################################################
        key = [0, key_1, key_2, key_3, key_4, key_5, key_6, key_7, key_8, key_9, key_10, key_11, key_12, key_13, key_14,
               key_15, key_16, key_17, key_18, key_19, key_20, key_21, key_22, key_23, key_24, key_25, key_26]
        ################################################################################################################

        i = 0
        if self.diameter < 1e-3 * 5 or self.diameter > 1e-3 * 500:
            print("The key is out of DIN 6885")
        else:
            if self.diameter <= 1e-3 * 8:
                i = 1
            elif self.diameter <= 1e-3 * 10:
                i = 2
            elif self.diameter <= 1e-3 * 12:
                i = 3
            elif self.diameter <= 1e-3 * 17:
                i = 4
            elif self.diameter <= 1e-3 * 22:
                i = 5
            elif self.diameter <= 1e-3 * 30:
                i = 6
            elif self.diameter <= 1e-3 * 38:
                i = 7
            elif self.diameter <= 1e-3 * 44:
                i = 8
            elif self.diameter <= 1e-3 * 50:
                i = 9
            elif self.diameter <= 1e-3 * 58:
                i = 10
            elif self.diameter <= 1e-3 * 65:
                i = 11
            elif self.diameter <= 1e-3 * 75:
                i = 12
            elif self.diameter <= 1e-3 * 85:
                i = 13
            elif self.diameter <= 1e-3 * 95:
                i = 14
            elif self.diameter <= 1e-3 * 110:
                i = 15
            elif self.diameter <= 1e-3 * 130:
                i = 16
            elif self.diameter <= 1e-3 * 150:
                i = 17
            elif self.diameter <= 1e-3 * 170:
                i = 18
            elif self.diameter <= 1e-3 * 200:
                i = 19
            elif self.diameter <= 1e-3 * 230:
                i = 20
            elif self.diameter <= 1e-3 * 260:
                i = 21
            elif self.diameter <= 1e-3 * 290:
                i = 22
            elif self.diameter <= 1e-3 * 330:
                i = 23
            elif self.diameter <= 1e-3 * 380:
                i = 24
            elif self.diameter <= 1e-3 * 440:
                i = 25
            elif self.diameter <= 1e-3 * 500:
                i = 26
        return row[i], key[i]

class FormB:
    """
        It creates a class form the key type: Form B
    """
    def __init__(self, diameter):
        self.diameter = diameter
        self.row = self.keyTableDIN6885()[0]
        self.key = self.keyTableDIN6885()[1]

    def keyAreaShearing(self):
        """
        This function defines the key's area for shearing.
        :return:
        """
        length = np.array(self.row)
        width = self.key[0]
        return length * width * 1e-6

    def keyAreaCompression(self):
        """
        This function defines the key's area for compression.
        :return:
        """
        length = np.array(self.row)
        height = self.key[1]
        t = self.key[2]
        loftiness = height - t
        return loftiness * length * 1e-6

    def keyTableDIN6885(self):
        """
        This function defines the key's properties.
        :return:
        """
        row_1 = np.array(range(6, 21, 2))
        row_2 = np.array([6, 8, 10, 12, 14, 16, 18, 20, 22, 25, 28, 32, 36])
        row_3 = np.array([8, 10, 12, 14, 16, 18, 20, 22, 25, 28, 32, 36, 40, 45])
        row_4 = np.array([10, 12, 14, 16, 18, 20, 22, 25, 28, 32, 36, 40, 45, 50, 56])
        row_5 = np.array([14, 16, 18, 20, 22, 25, 28, 32, 36, 40, 45, 50, 56, 63, 70])
        row_6 = np.array([18, 20, 22, 25, 28, 32, 36, 40, 45, 50, 56, 63, 70, 80, 90])
        row_7 = np.array([22, 25, 28, 32, 36, 40, 45, 50, 56, 63, 70, 80, 90, 100, 110])
        row_8 = np.array([28, 32, 36, 40, 45, 50, 56, 63, 70, 80, 90, 100, 110, 125, 140])
        row_9 = np.array([36, 40, 45, 50, 56, 63, 70, 80, 90, 100, 110, 125, 140, 160])
        row_10 = np.array([45, 50, 56, 63, 70, 80, 90, 100, 110, 125, 140, 160, 180])
        row_11 = np.array([50, 56, 63, 70, 80, 90, 100, 110, 125, 140, 160, 180, 200])
        row_12 = np.array([56, 63, 70, 80, 90, 100, 110, 125, 140, 160, 180, 200, 200])
        row_13 = np.array([63, 70, 80, 90, 100, 110, 125, 140, 160, 180, 200, 220, 250])
        row_14 = np.array([70, 80, 90, 100, 110, 125, 140, 160, 180, 200, 220, 250, 280])
        row_15 = np.array([80, 90, 100, 110, 125, 140, 160, 180, 200, 220, 250, 280, 320])
        row_16 = np.array([90, 100, 110, 125, 140, 160, 180, 200, 220, 250, 280, 320, 360])
        row_17 = np.array([100, 110, 125, 140, 160, 180, 200, 220, 250, 280, 320, 360, 400])
        row_18 = np.array([110, 125, 140, 160, 180, 200, 220, 250, 280, 320, 360, 400])
        row_19 = np.array([140, 160, 180, 200, 220, 250, 280, 320, 360, 400])
        row_20 = np.array([125, 140, 160, 180, 200, 220, 250, 280, 320, 360, 400])
        row_21 = np.array([160, 180, 200, 220, 250, 280, 320, 360, 400])
        row_22 = np.array([180, 200, 220, 250, 280, 320, 360, 400])
        row_23 = np.array([200, 220, 250, 280, 320, 360, 400])
        row_24 = np.array([220, 250, 280, 320, 360, 400])
        row_25 = np.array([250, 280, 320, 360, 400])
        row_26 = np.array([280, 320, 360, 400, ])
        ################################################################################################################
        row = [0, row_1, row_2, row_3, row_4, row_5, row_6, row_7, row_8, row_9, row_10, row_11, row_12, row_13, row_14,
               row_15, row_16, row_17, row_18, row_19, row_20, row_21, row_22, row_23, row_24, row_25, row_26]
        ################################################################################################################
        key_1 = np.array([2, 2, 1.2])
        key_2 = np.array([3, 3, 1.8])
        key_3 = np.array([4, 4, 2.5])
        key_4 = np.array([5, 5, 3])
        key_5 = np.array([6, 6, 3.5])
        key_6 = np.array([8, 7, 4])
        key_7 = np.array([10, 8, 5])
        key_8 = np.array([12, 8, 5])
        key_9 = np.array([14, 9, 5.5])
        key_10 = np.array([16, 10, 6])
        key_11 = np.array([18, 11, 7])
        key_12 = np.array([20, 12, 7.5])
        key_13 = np.array([22, 14, 9])
        key_14 = np.array([25, 14, 9])
        key_15 = np.array([28, 16, 10])
        key_16 = np.array([32, 18, 11])
        key_17 = np.array([36, 20, 12])
        key_18 = np.array([40, 22, 13])
        key_19 = np.array([45, 25, 15])
        key_20 = np.array([50, 28, 10])
        key_21 = np.array([56, 32, 20])
        key_22 = np.array([63, 32, 20])
        key_23 = np.array([70, 36, 22])
        key_24 = np.array([80, 40, 25])
        key_25 = np.array([90, 45, 28])
        key_26 = np.array([100, 50, 31])
        ################################################################################################################
        key = [0, key_1, key_2, key_3, key_4, key_5, key_6, key_7, key_8, key_9, key_10, key_11, key_12, key_13, key_14,
               key_15, key_16, key_17, key_18, key_19, key_20, key_21, key_22, key_23, key_24, key_25, key_26]
        ################################################################################################################
        i = 0
        if self.diameter < 1e-3 * 5 or self.diameter > 1e-3 * 500:
            print("The key is out of DIN 6885")
        else:
            if self.diameter <= 1e-3 * 8:
                i = 1
            elif self.diameter <= 1e-3 * 10:
                i = 2
            elif self.diameter <= 1e-3 * 12:
                i = 3
            elif self.diameter <= 1e-3 * 17:
                i = 4
            elif self.diameter <= 1e-3 * 22:
                i = 5
            elif self.diameter <= 1e-3 * 30:
                i = 6
            elif self.diameter <= 1e-3 * 38:
                i = 7
            elif self.diameter <= 1e-3 * 44:
                i = 8
            elif self.diameter <= 1e-3 * 50:
                i = 9
            elif self.diameter <= 1e-3 * 58:
                i = 10
            elif self.diameter <= 1e-3 * 65:
                i = 11
            elif self.diameter <= 1e-3 * 75:
                i = 12
            elif self.diameter <= 1e-3 * 85:
                i = 13
            elif self.diameter <= 1e-3 * 95:
                i = 14
            elif self.diameter <= 1e-3 * 110:
                i = 15
            elif self.diameter <= 1e-3 * 130:
                i = 16
            elif self.diameter <= 1e-3 * 150:
                i = 17
            elif self.diameter <= 1e-3 * 170:
                i = 18
            elif self.diameter <= 1e-3 * 200:
                i = 19
            elif self.diameter <= 1e-3 * 230:
                i = 20
            elif self.diameter <= 1e-3 * 260:
                i = 21
            elif self.diameter <= 1e-3 * 290:
                i = 22
            elif self.diameter <= 1e-3 * 330:
                i = 23
            elif self.diameter <= 1e-3 * 380:
                i = 24
            elif self.diameter <= 1e-3 * 440:
                i = 25
            elif self.diameter <= 1e-3 * 500:
                i = 26
        return row[i], key[i]
