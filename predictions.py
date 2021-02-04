# This file is the Prediction module which is able to calculate altitude
# and speed predictions before and during the flight

from numpy import sqrt
from constantParameters import FT2M

R = 287.053  # Gas constant for air in J/kg/K
GAMMA = 1.4  # Specific heat for air
MU = (GAMMA-1)/GAMMA
P0 = 1013.25  # pressure in ISA condition in hPa
T0 = 288  # temperature in ISA condition in K
RHO_0 = 1.225  # density of air in ISA condition in kg/m^3


class SpeedPredictions():
    def __init__(self):
        self.TAS, self.CAS, self.GS = 0, 0, 0  # true/calibrated air speed, ground speed
        self.MMO, self.VMO = 0, 0  # Maximum Mach Number, Maximum Operating Speed
        self.econMach = 0  # Economic Mach

    def eq3degrees(self, a, b, c, d):
        return lambda x: a*x**3 + b*x**2 + c*x + d

    def compute_average_wind(self, wind):
        return wind[1]

    def computeSpeeds(self, ci, fl, wind):  # wind en chaine de caractère
        wind = self.compute_average_wind(wind)
        temp, p = self.computeFLParam(fl)
        self.compute_ECON_MACH(ci, fl)
        self.wind_correction(wind)
        self.convertMachToTAS(temp)
        self.convertTASToGS(wind)
        self.convertTASToCAS(fl, temp, p)
        return "ECON MACH="+str(self.econMach) + " CAS="+str(self.CAS) + " TAS="+str(self.TAS) + " GS="+str(self.GS)

    def computeFLParam(self, fl):
        altitude = fl * 100 * FT2M  # altitude en mètres
        temp = (15 - 6.5 * altitude / 1000) + 273
        pressure = P0 * (1 - 0.0065 * altitude / 288.15) ** 5.255
        return temp, pressure

    def compute_ECON_MACH(self, ci, fl):
        """Calcul de ECON MACH en fonction du cost index CI, et des FL en entrées (considérés comme entiers)"""
        if ci >= 100:
            ci = 100
        diff_min = 100
        for nom_ci in [0, 20, 40, 60, 100]:
            diff = ci - nom_ci
            if abs(diff) < diff_min:
                diff_min = diff
                ci_used = nom_ci
        if ci_used == 0:
            ratio = (1 + ci/20)
        else:
            ratio = ci/ci_used
        self.econMach = min(self.MMO, round(ratio*eval('self.eq'+str(ci_used)+'('+str(fl)+')'), 3))

    def wind_correction(self, wind):
        """Calcul du ECON Manch avec les corrections du vent (vent en kt). Le vent est considéré négatif pour de
        l'headwind, positif si tailwind.
        On considère +1/2 point de Mach par 50 kts de headind et -1/2 point de Mach par 50 kts de tailwing
        D'après 'Airbus Getting to Grips with Cost Index'"""
        self.econMach = min(self.MMO, round(self.econMach - wind/500*0.5, 3))

    def convertMachToTAS(self, temp):
        # temp est en Kelvin
        a = sqrt(GAMMA*R*temp)  # vitesse du son dans l'air
        self.TAS = int(self.econMach*a)

    def convertTASToGS(self, wind):
        # vent negatif si heading, positif si tailwind
        self.GS = int(self.TAS + wind)

    def convertTASToCAS(self, FL, temp, pressure):
        rho = pressure/R/temp
        r1, r2 = 2*P0/MU/rho, MU*rho/2/pressure
        self.CAS = int(sqrt(r1*((1 + pressure/P0*((1+r2*self.TAS**2)**(1/MU) - 1))**MU - 1)))


class SpeedPredictionsA320(SpeedPredictions):
    """Prédictions de vitesses pour l'A320"""
    def __init__(self):
        super().__init__()
        self.MMO = 0.82  # Maximum Mach Number
        self.VMO = 350  # Maximum Operating Speed (kt)
        self.eq0 = self.eq3degrees(-8.333e-8, 8.3452e-5, -2.7071e-2, 3.5750)
        self.eq20 = self.eq3degrees(-3.5354e-8, 3.1169e-5, -8.3997e-3, 1.4107)
        self.eq40 = self.eq3degrees(-2.5253e-8, 1.7857e-5, -3.2892e-3, 8.3507e-1)
        self.eq60 = self.eq3degrees(5.4714e-8, -5.9286e-5, 2.1181e-2, -1.7028)
        self.eq100 = self.eq3degrees(5.8923e-9, -6.2771e-6, 2.1476e-3, 5.6153e-1)

    def examples(self):
        print("CI=0, FL=350, WIND = -100kt", self.computeSpeeds(0, 350, -20))
        print("CI=0, FL=310, WIND = +20kt", self.computeSpeeds(0, 310, 20))
        print("CI=40, FL=290, WIND = -50kt", self.computeSpeeds(40, 290, -50))
        print("CI=100, FL=370, WIND = -20kt", self.computeSpeeds(100, 370, -20))
        print("CI=200, FL=370, WIND = -20kt", self.computeSpeeds(100, 370, -20))
