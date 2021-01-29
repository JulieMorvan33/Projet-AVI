from PyQt5 import QtWidgets, QtCore
from ivy.std_api import *
import navigationDisplay
import communication
import ndWindowParameters
import time

USE_IVY = True  # use or not use Ivy Bus ?
AC_SIMULATED = False  # use bus IVY with no other groups ?
SIMU_DELAY = 0.1  # increment time for the simulation if Ivy Bus isn't used

def null_cb(*a):
    pass

if __name__ == "__main__":
    # create the simulation for test purpose
    sim = communication.Simulation(USE_IVY, SIMU_DELAY, AC_SIMULATED)

    # Initialisation of Qt
    app = QtWidgets.QApplication([])

    # create the radar view
    rad = navigationDisplay.RadarView(sim)

    ac = navigationDisplay.AircraftView(sim)

    # create the rose view
    rose = navigationDisplay.RoseView(sim)

    # create the parameters view displaying GS, TAS,...
    param = navigationDisplay.ParamView(sim)

    # create the QMainWindow
    win = ndWindowParameters.mywindow(param.view, rad.view, rose.view, ac.view, sim)
    win.setWindowTitle("Navigation Display")
    win.show()

    if USE_IVY:
        # Initialisation du bus Ivy
        bus = "192.168.43.255:2010"
        IvyInit("GUID_TRAJ_APP", "Bonjour de GUID_TRAJ", 0, null_cb, null_cb)
        IvyStart() # mettre 'bus' entre parenthèse si utilisation du wifi
        time.sleep(1.0)  # attente du temps de l'initialisation

        # Abonnement à l'horloge
        IvyBindMsg(sim.horloge, "^Time t=(.*)")

        # Abonnement à l'identifiant de l'aéroport de départ
        IvyBindMsg(sim.get_depart_airport, "SP_InitialCoord (.*)")

        # Abonnement au vecteur d'état pour la récupération du heading
        IvyBindMsg(sim.get_AC_current_heading_and_speeds, "AircraftSetPosition (.*)")

        # Abonnement au vecteur d'état pour la récupération de x et y
        IvyBindMsg(sim.get_AC_position, "StateVector (.*)")

        # Abonnement au message du groupe LEGS (liste des segments)
        IvyBindMsg(sim.from_LEGS, "FL_LegList (.*)")

        # Abonnement au numéro de séquence du leg actif venant de SEQ
        IvyBindMsg(sim.receive_active_leg, "GS_AL (.*)")

        # Abonnement au paramètres envoyés par SEQ (XTK, TAE, DTWPT)
        IvyBindMsg(sim.receive_SEQ_parameters, "GS_Data (.*)")

        # Abonnement au mode de l'autopilot
        IvyBindMsg(sim.get_AP_mode, "GC_AP (.*)")

        # Abonnement au HDG sélecté
        IvyBindMsg(sim.get_HDG_selected, "FCULateral (.*)")

    # enter the main loop
    app.exec_()