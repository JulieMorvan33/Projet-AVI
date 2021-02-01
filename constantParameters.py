from numpy import pi as PI

# Paramètres généraux
G = 9.807  # m.s^-2
KT2MS = 1852/3600
NM2M = 1852
RAD2DEG = 180/PI
FT2M = 1/3.2808399

# Paramètres de vol
CRZ_ALT = 10000  # en feet
ALTITUDE = 100

# WIND = '110020' # 3 premiers chiffres : direction / trois derniers : vitesse (kts)

CI = 30
FL = 100  # FL100
WIND = 15  # kts

#Constantes de fenêtre
WIDTH = 800  # Largeur initiale de fenêtre (pixels)
HEIGHT = 350  # hauteur initiale de fenêtre (pixels)


#Nombre de positions de l'avion entre 2 waypoints
NB_AC_INTER_POS = 20
