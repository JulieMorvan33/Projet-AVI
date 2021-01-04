from numpy import pi as PI

# General parameters
G = 9.807 #m.s^-2
KT2MS = 1852/3600
NM2M = 1852
RAD2DEG = 180/PI
FT2M = 1/3.2808399

# Flight parameters
CRZ_ALT = 10000 # en feet
ALTITUDE = 100 #FL
GS = 500*KT2MS #m.s^-1
CAS = 800 # en km/h ? en Nm/h ?
MACH = 0.78
WIND = '110020' # 3 premiers chiffres : direction / trois derniers : vitesse (kts)

# Window constants
WIDTH = 800  # Initial window width (pixels)
HEIGHT = 350  # Initial window height (pixels)
