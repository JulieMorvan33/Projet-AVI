from PyQt5 import QtWidgets, QtCore
#from ivy.std_api import *
import navigationDisplay
import communication
import ndWindowParameters
import time

USE_IVY = False # use or not use Ivy Bus ?
SIMU_DELAY = 0.1 # increment time for the simulation if Ivy Bus isn't used

def null_cb(*a):
    pass

if __name__ == "__main__":
    # create the simulation for test purpose
    sim = communication.Simulation(USE_IVY, SIMU_DELAY)

    # Initialisation of Qt
    app = QtWidgets.QApplication([])

    # create the radar view
    rad = navigationDisplay.RadarView(sim)

    # create the parameters view displaying GS, TAS,...
    param = navigationDisplay.ParamView()

    # create the QMainWindow
    win = ndWindowParameters.mywindow(rad.view, param.view)
    win.setWindowTitle("Navigation Display")
    win.show()

    if USE_IVY:
        # Initialisation du bus Ivy
        bus = "192.168.43.255:2010"
        IvyInit("GUID_TRAJ_APP", "Bonjour de GUID_TRAJ", 0, null_cb, null_cb)
        IvyStart()
        time.sleep(1.0)  # attente du temps de l'initialisation

        # Abonnement à l'horloge
        IvyBindMsg(sim.horloge, "^Time t=(.*)")

        # Abonnement au vecteur d'état pour la récupération de x et y
        IvyBindMsg(sim.get_AC_state, "StateVector (.*)")

        # Abonnement au message du groupe LEGS (liste des segments)
        IvyBindMsg(sim.from_LEGS, "FL_LegList_TEST (.*)")

        # Envoi de la Grounspeed
        IvySendMsg("GT_PARAM_GS=" + str(GS))

        # Abonnement au numéro de séquence du leg actif venant de SEQ
        #IvyBindMsg(sim.receive_active_leg, "GS_AL (.*)")

        # Abonnement au paramètres envoyés par SEQ (XTK, TAE, DTWPT)
        #IvyBindMsg(sim.receive_SEQ_parameters, "GS_Data (.*)")

        # Envoi des paramètres de vol aux groupe ROUTE
        #IvySendMsg("GT_PARAM_CRZ_ALT="+str(CRZ_ALT)) # envoi de l'altitude de croisière
        #IvySendMsg("GT_PARAM_CAS="+str(CAS)) # envoi de la CAS
        #IvySendMsg("GT_PARAM_MACH=" + str(MACH))  # envoi du MACH
        #IvySendMsg("GT_PARAM_WIND=" + WIND)  # envoi du WIND


    # enter the main loop
    app.exec_()