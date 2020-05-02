"""
@Description:
This modulo'll provide some basic functions to project a shaft. This module has the aim to give the main  from the book
Shigley’s Mechanical Engineering Design to handle a shaft
project. The module is built in SI units.
"""
__author__ = "Iaggo Capitanio"
__copyright__ = "Copyright (C) 2020 Iaggo Capitanio"
__license__ = "Public Domain"
__version__ = "1.0"

from typing import Union
import numpy as np
import scipy.stats as st
import ctypes

myAppId = u'ShaftExploration.Shaftex.version-1.0'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppId)

def shaftEnduranceLimitStressRotatingBeam(Sut: float) -> Union[None, float]:
    """
    @Explanation:
    This function returns the endurance threshold for a rotating beam of steel.
    Based on the book: Shigley’s Mechanical Engineering Design, 8th Edition, page 277.

    @Parameters:
    yieldingStress : ultimate strength or tensile strength. (Commonly known as 'Sut')
    """
    if Sut <= 1.4e9:
        return Sut / 2
    elif Sut > 1.4e9:
        return 735e6
    else:
        return None


def shaftVonMissesStress(Ma: float, Mm: float, Ta: float, Tm: float, Kf: float,
                         Kfs: float, d: float) -> float:
    """
    @Explanation:
    This function returns the Von Misses stress for rotating round: (σ'a, σ'm).
    Based on the book: Shigley’s Mechanical Engineering Design, 8th Edition, page 356.

    @Parameters:
    Mm : midrange momentum.
    Ma : alternating momentum.
    Tm : midrange torque.
    Ta : alternating torque.
    Kf : Fatigue stress concentration factor for bending.
    Kfs : Fatigue stress concentration factor for shearing (torsion).
    """
    a = np.sqrt((32 * Kf * Ma / (np.pi * d ** 3)) ** 2 + 3 * (16 * Kfs * Ta / (np.pi * d ** 3)) ** 2)
    m = np.sqrt((32 * Kf * Mm / (np.pi * d ** 3)) ** 2 + 3 * (16 * Kfs * Tm / (np.pi * d ** 3)) ** 2)
    return pow(pow(a, 2) + pow(m, 2), 1 / 2)


def shaftVonMissesSafetyFactor(Ma: float, Mm: float, Ta: float, Tm: float, Kf: float,
                               Kfs: float, d: float, Sy: float) -> float:
    """
    @Explanation:
    This function returns the Von Misses safety factor for rotating round: (σ'a, σ'm).
    Based on the book: Shigley’s Mechanical Engineering Design, 8th Edition, page 356.

    @Parameters:
    Mm : midrange momentum.
    Ma : alternating momentum.
    Tm : midrange torque.
    Ta : alternating torque.
    Sy : Yielding stress.
    Kf : Fatigue stress concentration factor for bending.
    Kfs : Fatigue stress concentration factor for shearing (torsion).
    """
    a = np.sqrt((32 * Kf * Ma / (np.pi * d ** 3)) ** 2 + 3 * (16 * Kfs * Ta / (np.pi * d ** 3)) ** 2)
    m = np.sqrt((32 * Kf * Mm / (np.pi * d ** 3)) ** 2 + 3 * (16 * Kfs * Tm / (np.pi * d ** 3)) ** 2)
    return Sy / (pow(pow(a, 2) + pow(m, 2), 1 / 2))


def shaftSafetyFactor(Ma: float, Mm: float, Ta: float, Tm: float, Kf: float, Kfs: float, Se: float, Sut: float,
                      Sy: float, d: float, method: str = "DE-Goodman"):
    """
    @Explanation:
    This function returns the safety factor, which depends on the case: DE=Goodman, DE-Geber, DE-ASME or
    DE-Soderberg. By default the method is defined as DE-Goodman. But the parameter can be easily changed.
    Based on the book: Shigley’s Mechanical Engineering Design, 8th Edition, page 356-357.

    @Parameters:
    Se : endurance limit in a critic site of a part.
    Sut : ultimate strength or tensile strength.
    Sy : yielding stress.
    Mm : midrange momentum.
    Ma : alternating momentum.
    Tm : midrange torque.
    Ta : alternating torque.
    Kf : Fatigue stress concentration factor for bending.
    Kfs : Fatigue stress concentration factor for shearing (torsion).
    d : shaft's diameter
    method : theory used to solve.
    """
    if method == "DE-Goodman":
        alpha = 1 / Se * np.sqrt(4 * (Kf * Ma) ** 2 + 3 * (Kfs * Ta) ** 2)
        beta = 1 / Sut * np.sqrt(4 * (Kf * Mm) ** 2 + 3 * (Kfs * Tm) ** 2)
        return (16 / (d ** 3 * np.pi) * (alpha + beta)) ** (-1)
    elif method == "DE-Geber":
        A = np.sqrt(4 * (Kf * Ma) ** 2 + 3 * (Kfs * Ta) ** 2)
        B = np.sqrt(4 * (Kf * Mm) ** 2 + 3 * (Kfs * Tm) ** 2)
        C = np.sqrt(1 + (2 * B * Se / (A * Sut)) ** 2) + 1
        return (8 * A / (np.pi * d ** 3 * Se) * C) ** (-1)
    elif method == "DE-ASME":
        a_var = pow(Kf * Ma / Se, 2)
        b_var = pow(Kfs * Ta / Se, 2)
        c_var = pow(Kf * Mm / Sy, 2)
        d_var = pow(Kfs * Tm / Sy, 2)
        exp = 4 * a_var + 3 * b_var + 4 * c_var + 3 * d_var
        return (16 / (np.pi * pow(d, 3)) * np.sqrt(exp)) ** (-1)
    elif method == "DE-Soderberg":
        a = 1 / Se * (4 * (Kf * Ma) ** 2 + 3 * (Kfs * Ta) ** 2) ** (1 / 2)
        m = 1 / Sy * (4 * (Kf * Mm) ** 2 + 3 * (Kfs * Tm) ** 2) ** (1 / 2)
        return (16 / (np.pi * d ** 3) * (a + m)) ** (-1)
    else:
        return 0


def shaftDiameter(Ma, Mm, Ta, Tm, Kf, Kfs, Se, Sut, Sy, n, method="DE-Goodman"):
    """
    @Explanation:
    This function returns the safety factor, which depends on the case: DE=Goodman, DE-Geber, DE-ASME or
    DE-Soderberg. By default the method is defined as DE-Goodman. But the parameter can be easily changed.
    Based on the book: Shigley’s Mechanical Engineering Design, 8th Edition, page 356-357.

    @Parameters:
    Se : endurance limit in a critic site of a part.
    Sut : ultimate strength or tensile strength.
    Sy : yielding stress.
    Mm : midrange momentum.
    Ma : alternating momentum.
    Tm : midrange torque.
    Ta : alternating torque.
    Kf : Fatigue stress concentration factor for bending.
    Kfs : Fatigue stress concentration factor for shearing (torsion).
    """
    if method == "DE-Goodman":
        alpha = 1 / Se * np.sqrt(4 * (Kf * Ma) ** 2 + 3 * (Kfs * Ta) ** 2)
        beta = 1 / Sut * np.sqrt(4 * (Kf * Mm) ** 2 + 3 * (Kfs * Tm) ** 2)
        return (16 * n / np.pi * (alpha + beta)) ** (1 / 3)
    elif method == "DE-Geber":
        A = np.sqrt(4 * (Kf * Ma) ** 2 + 3 * (Kfs * Ta) ** 2)
        B = np.sqrt(4 * (Kf * Mm) ** 2 + 3 * (Kfs * Tm) ** 2)
        C = np.sqrt(1 + (2 * B * Se / (A * Sut)) ** 2) + 1
        return (8 * n * A / (np.pi * Se) * C) ** (1 / 3)
    elif method == "DE-ASME":
        a = (Kf * Ma / Se) ** 2
        b = (Kfs * Ta / Se) ** 2
        c = (Kf * Mm / Sy) ** 2
        d = (Kfs * Tm / Sy) ** 2
        exp = 4 * a + 3 * b + 4 * c + 3 * d
        return (16 * n / np.pi * np.sqrt(exp)) ** (1 / 3)
    elif method == "DE-Soderberg":
        a = 1 / Se * (4 * (Kf * Ma) ** 2 + 3 * (Kfs * Ta) ** 2) ** (1 / 2)
        m = 1 / Sy * (4 * (Kf * Mm) ** 2 + 3 * (Kfs * Tm) ** 2) ** (1 / 2)
        return (16 * n / np.pi * (a + m)) ** (1 / 3)
    else:
        return 0


def shaftTemperatureFactorFunction(x: float, a0: float, a1: float, a2: float, a3: float) -> float:
    """
    @Explanation:
    Third order function.
    @Parameters:
    x : variable.
    ai : constant of x**(3-i) for i in {0, 1, 2, 3}.
    """
    return + a3 * x ** 3 + a2 * x ** 2 + x * a1 + a0


def shaftForce(torque, radius, degree):
    """
    @Explanation:
    This function returns the tuple: (radial force, tangential force).

    @Parameters:
    torque : torque acting on the shaft.
    radius : distance amid the shaft center and the shaft surface.
    degree : degree of the gear tooth.
    """
    tangentialForce = torque / radius
    degreeInRadian = np.deg2rad(degree)
    return tangentialForce * np.tan(degreeInRadian), tangentialForce


def shaftFactor_Kd(T: float) -> float:
    """
    @Explanation:
    This function returns the temperature factor. The function is an optimum approximation of the points in the
    table 6-4.
    Based on the book: Shigley’s Mechanical Engineering Design, 8th Edition, page 294.

    @Parameters:
    T : Temperature given in °C (Celsius degree).
    """
    coefficient = np.array([9.98585391e-01, 2.51197740e-04, -4.09243589e-07, -2.07245774e-09])
    return shaftTemperatureFactorFunction(T, *coefficient)


def shaftThermalExpansion(a: float, deltaT: float, L: float) -> float:
    """
    @Explanation:
    This function returns the linear thermal expansion.

    @Parameters:
    deltaT : temperature variation given in °C (Celsius degree).
    L : linear length.
    a : coefficient of thermal dilatation.
    """
    return a * deltaT * L


def shaftTorque(power: float, RPM: float) -> float:
    """
    :parameter RPM: The RPM of the shaft.
    :parameter power: The power of the engine that spins the shaft.
    :return: float
    """
    return power * 60 / (2 * np.pi * RPM)


def shaftStress_Se(Ka: float, Kb: float, Kc: int, Kd: float, Ke: float, Kf: float, SeLine: float) -> float:
    """
    @Explanation:
    This function returns the endurance limit in a critic site of a part.
    Based on the book: Shigley’s Mechanical Engineering Design, 8th Edition, page 279.

    @Parameters:
    Ka : surface condition modification factor.
    Kb : size modification factor.
    Kc : load modification factor.
    Kd : temperature modification factor.
    Ke : reliability factor.
    Kf : miscellaneous-effects modification factor
    SeLine : rotary-beam test specimen endurance limit.
    """
    return Ka * Kb * Kc * Kd * Ke * Kf * SeLine


def shaftFactor_Ka(method: str, Sut: float) -> float:
    """
    @Explanation:
    This function returns the surface condition modification factor.
    According to the author: The surface of a rotating-beam specimen is highly polished, with a final polishing in
    the axial direction to smooth out any circumferential scratches. The surface modification factor depends on the
    quality of the finish of the actual part surface and on the tensile strength of the part material.
    Based on the book: Shigley’s Mechanical Engineering Design, 8th Edition, page 279.

    @Parameters:
    method : method of surface finish. ["Ground", "Machined or cold-drawn", "Hot-rolled", "As-forged"]
    Sut : ultimate stress
    """
    methodChoice = ["Ground", "Machined or cold-drawn", "Hot-rolled", "As-forged"]

    if method == methodChoice[0]:
        a = 1.58
        b = -0.085
    elif method == methodChoice[1]:
        a = 4.51
        b = -0.265
    elif method == methodChoice[2]:
        a = 57.7
        b = -0.718
    elif method == methodChoice[3]:
        a = 272
        b = -0.995
    else:
        a = b = 0
    return a * (Sut * 1e-6) ** b


def shaftFactor_Kb(d: float):
    """
    @Explanation:
    This function returns the size factor.
    According to the author this function might be used only when the bar has a circular section and is rotating. Either
    whether the bar doesn't have only axial forces acting on itself. If there is only axial forces, Kb id equal to one.
    Based on the book: Shigley’s Mechanical Engineering Design, 8th Edition, page 281.

    @Parameters:
    d : shaft diameter.
    """
    if 2.79e-3 <= d <= 51e-3:
        return 1.24 * (d * 1e+3) ** (-0.107)
    elif 51e-3 < d <= 254e-3:
        return 1.51 * (d * 1e+3) ** (-0.157)
    else:
        return None


def shaftFactor_Kc(load: str = "Bending") -> Union[float, None]:
    """
    @Explanation:
    This function returns the load factor.
    Based on the book: Shigley’s Mechanical Engineering Design, 8th Edition, page 285.

    @Parameters:
    load : the type of load predominant on the shaft [ "Bending", "Axial", "Torsion"]
    """
    if load == "Bending":
        return 1
    elif load == "Axial":
        return 0.85
    elif load == "Torsion":
        return 0.59
    else:
        return None


def shaftFactor_Ke(reliability: float) -> float:
    """
    @Explanation:
    This function returns the reliability factor.
    Based on the book: Shigley’s Mechanical Engineering Design, 8th Edition, page 287.

    @Parameters:
    :param reliability: the reliability of the data.
    """
    return 1 - 0.08 * shaft_Za(probability=reliability)


def shaft_Za(probability: float) -> np.float64:
    """
    @Explanation:
    This function returns the Z_a number.
    Based on the package scipy.

    @Parameters:
    probability : the probability accumulated.
    """
    return abs(st.norm.ppf(probability))


def __setTableStyle(table, msg):
    """
    @Explanation:
    This function set the Style of one pandas' table.

    @Attributes:
    table : pandas object table.
    msg : a string to show underneath the table.
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


def shaftPulleyForce(power, RPM, diameter):
    """
    @Explanation:
    This function returns the force acting on the shaft caused from the pulley.

    @Attributes:
    power : the power from the engine that spins the shaft.
    RPM : the velocity that the shaft spins.
    diameter : the shaft's diameter.
    """
    return (1.5 / diameter) * 2 * shaftTorque(power, RPM)


def shaftConstantA(Sut: float, method: str = "Bending") -> Union[float, None]:
    """
    @Explanation:
    This function returns the constant a, which is the square of the Neuber constant.

    @Attributes:
    Sut : ultimate strength or tensile strength.
    method : the type of forces prevalent on the shaft.
    """
    Sut *= 1e-6
    if method == "Bending":
        a = pow(0.246 - 3.08 * 1e-3 * Sut + 1.51 * 1e-5 * pow(Sut, 2) - 2.67 * 1e-8 * pow(Sut, 3), 2) * 25.4 * 1e-3
    elif method == "Torsion":
        a = pow(0.19 - 2.51 * 1e-3 * Sut + 1.35 * 1e-5 * pow(Sut, 2) - 2.67 * 1e-8 * pow(Sut, 3), 2) * 25.4 * 1e-3
    else:
        raise ValueError
    return pow(a, 2)


def shaftNotchSensitivity(a: float, r: float) -> np.float64:
    """
    @Explanation:
    This function returns the constant q, which is the notch sensitivity factor.

    @Attributes:
    a : Neuber's constant at the two power.
    r : notch's radius.
    """
    return 1 / (1 + np.sqrt(a / r))


def shaftKtFactorSteppedBarOfCircularCrossSection(D: float, d: float, r: float) -> np.float64:
    """
    @Explanation:
    This function returns the constant Kt for bending, which is the load concentration factor of a stepped bar of a
    circular cross section.
    Based on the book: Peterson’s Stress Concentration Factors, 3th Edition, page 166.

    @Attributes:
    D : the biggest diameter in the section.
    d : the smallest diameter in the section.
    r : notch's radius.
    """
    t = (D - d) / 2
    if 0.1 <= t / r <= 2:
        C1 = 0.947 + 1.206 * np.sqrt(t / r) - 0.131 * t / r
        C2 = 0.022 - 3.405 * np.sqrt(t / r) + 0.915 * t / r
        C3 = 0.869 + 1.777 * np.sqrt(t / r) - 0.555 * t / r
        C4 = - 0.810 + 0.422 * np.sqrt(t / r) - 0.260 * t / r

    elif 2 <= t / r <= 20:
        C1 = 1.232 + 0.832 * np.sqrt(t / r) - 0.008 * t / r
        C2 = - 3.813 + 0.968 * np.sqrt(t / r) - 0.260 * t / r
        C3 = 7.423 - 4.868 * np.sqrt(t / r) + 0.869 * t / r
        C4 = -3.839 + 3.070 * np.sqrt(t / r) - 0.6 * t / r
    else:
        C1 = 0
        C2 = 0
        C3 = 0
        C4 = 0
    a = 2 * t / D
    return C1 + C2 * pow(a, 1) + C3 * pow(a, 2) + C4 * pow(a, 3)


def shaftKtsFactorSteppedBarOfCircularCrossSection(D: float, d: float, r: float) -> np.float64:
    """
    @Explanation:
    This function returns the constant Kts for shearing, which is the load concentration factor of a stepped bar of a
    circular cross section.
    Based on the book: Peterson’s Stress Concentration Factors, 3th Edition, page 167.

    @Attributes:
    D : the biggest diameter in the section.
    d : the smallest diameter in the section.
    r : notch's radius.
    """
    t = (D - d) / 2
    a = (2 * t / D)
    if 0.25 <= t / r <= 4 and (D - d) < 8 * r:
        C1 = 0.905 + 0.783 * np.sqrt(t / r) - 0.075 * t / r
        C2 = - 0.437 - 1.969 * np.sqrt(t / r) + 0.553 * t / r
        C3 = 1.557 + 1.073 * np.sqrt(t / r) - 0.578 * t / r
        C4 = - 1.061 + 0.171 * np.sqrt(t / r) + 0.086 * t / r
    else:
        C1 = 0
        C2 = 0
        C3 = 0
        C4 = 0
    return C1 + C2 * a + C3 * pow(a, 2) + C4 * pow(a, 3)


def shaftKtFactorCircumferentialGrooveInShaft(D, d, r):
    """
    @Explanation:
    This function returns the constant Kt for bending, which is the load concentration factor of a circumferential
    groove in a shaft.
    Based on the book: Peterson’s Stress Concentration Factors, 3th Edition, page 122.
    @Attributes:
    D : the biggest diameter in the section.
    d : the smallest diameter in the section.
    r : notch's radius.
    """
    t = (D - d) / 2
    a = (2 * t) / D
    if 0.25 <= (t / r) <= 2:
        C1 = 0.594 + 2.958 * np.sqrt(t / r) - 0.520 * t / r
        C2 = 0.422 - 10.545 * np.sqrt(t / r) + 2.692 * t / r
        C3 = 0.501 + 14.375 * np.sqrt(t / r) - 4.486 * t / r
        C4 = - 0.613 - 6.573 * np.sqrt(t / r) + 2.177 * t / r
    elif 2 <= (t / r) <= 50:
        C1 = 0.955 + 1.926 * np.sqrt(t / r)
        C2 = - 2.773 - 4.414 * np.sqrt(t / r) - 0.017 * t / r
        C3 = 4.785 + 4.681 * np.sqrt(t / r) + 0.096 * t / r
        C4 = - 1.995 - 2.241 * np.sqrt(t / r) - 0.074 * t / r
    else:
        C1 = C2 = C3 = C4 = 0
    return C1 + C2 * a + C3 * pow(a, 2) + C4 * pow(a, 3)


def shaftKtsFactorCircumferentialGrooveInShaft(D, d, r):
    """
    @Explanation:
    This function returns the constant Kts for bending, which is the load concentration factor of a circumferential
    groove in a shaft.
    Based on the book: Peterson’s Stress Concentration Factors, 3th Edition, page 128.

    @Attributes:
    D : the biggest diameter in the section.
    d : the smallest diameter in the section.
    r : notch's radius.
    """
    t = (D - d) / 2
    a = (2 * t) / D
    if 0.25 <= (t / r) <= 2:
        C1 = 0.966 + 1.056 * np.sqrt(t / r) - 0.022 * t / r
        C2 = 0.192 - 4.037 * np.sqrt(t / r) + 0.674 * t / r
        C3 = 0.808 + 5.321 * np.sqrt(t / r) - 1.231 * t / r
        C4 = - 0.567 - 2.364 * np.sqrt(t / r) + 0.566 * t / r
    elif 2 <= (t / r) <= 50:
        C1 = 1.089 + 0.924 * np.sqrt(t / r) + 0.018 * t / r
        C2 = - 1.504 - 2.141 * np.sqrt(t / r) - 0.047 * t / r
        C3 = 2.486 + 2.289 * np.sqrt(t / r) + 0.091 * t / r
        C4 = - 1.056 - 1.104 * np.sqrt(t / r) - 0.059 * t / r
    else:
        C1 = 0
        C2 = 0
        C3 = 0
        C4 = 0
    return C1 + C2 * a + C3 * pow(a, 2) + C4 * pow(a, 3)


def shaftKtTiptonFactorSteppedBarOfCircularCrossSection(D, d, r):
    """
    @Explanation:
    This function returns the constant Kt for bending, which is the load concentration factor of a circumferential
    groove in a shaft. In this formula, the theory is based in finite element theory.
    Based on the book: Tipton, S. M., Sorem, J. R., and Rolovic, R. D., 1996, Updated stress concentration factors for
    filleted shafts in bending and tension, J. Mech. Des., Vol. 118, p. 321.

    @Attributes:
    D : the biggest diameter in the section.
    d : the smallest diameter in the section.
    r : notch's radius.
    """

    a = - 0.14 - 0.363 * pow(D / d, 2) + 0.503 * pow(D / d, 4)
    b = 1 - 2.39 * pow(D / d, 2) + 3.368 * pow(D / d, 4)
    return 0.632 + 0.377 * pow(D / d, -4.4) + pow(r / d, -0.5) * pow(a / b, 0.5)


def shaftKfFactor(Kt: float, q: float) -> Union[int, float]:
    """
    @Explanation:
    This function returns the constant Kf for bending, which is the fatigue stress concentration factor.
    Based on the book:  Based on the book: Shigley’s Mechanical Engineering Design, 8th Edition, page 313.

    @Attributes:
    Kt : bending factor.
    q : notch factor for bending.
    """
    return 1 + q * (Kt - 1)


def shaftKfsFactor(Kts: float, qs: float) -> Union[int, float]:
    """
    @Explanation:
    This function returns the constant Kfs for shearing, which is the fatigue stress concentration factor.
    Based on the book:  Based on the book: Shigley’s Mechanical Engineering Design, 8th Edition, page 313.

    @Attributes:
    Kts : shearing factor.
    qs : notch factor for shearing.
    """

    return 1 + qs * (Kts - 1)
