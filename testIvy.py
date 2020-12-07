from ivy.std_api import *
import time
from ivyFunctions import *

CRZ_ALT = 10000 # en feet
CAS = 800 # en km/h ? en Nm/h ?
MACH = 0.78
WIND = '110020' # 3 premiers chiffres : direction / trois derniers : vitesse (kts)

if __name__ == '__main__':
    bus = "192.168.43.255:2010"

    # Initialisation
    IvyInit("GUID_TRAJ_APP", "Bonjour de GUID_TRAJ", 0, null_cb, null_cb)
    IvyStart()
    # Abonnement à l'horloge
    IvyBindMsg(horloge, "^Time t=(.*)")

    # Abonnement au vecteur d'état
    #IvyBindMsg(getstate, "StateVector (.*)")

    # Abonnement au message du groupe LEGS (liste des segments)
    #IvyBindMsg(on_LEGS, "FL_LegList (.*)")

    # Abonnement au message du groupe COMM (modes manage/selecte)
    #IvyBindMsg(on_COMM, "GC_AP Time=time AP_State=(.*)")

    time.sleep(1.0) #attente le temps de l'initialisation

    # Envoi de la trajectoire au groupe SEQ
    #traj_message = trajToSend()
    #IvySendMsg(traj_message[0])  # envoi de la liste des points
    #IvySendMsg(traj_message[1])  # envoi de la liste des segments
    #IvySendMsg(traj_message[2])  # envoi de la liste des transitions
    #IvySendMsg(traj_message[3])  # envoi de la liste des orthos
    #IvySendMsg(traj_message[4])  # envoie de la liste des paths

    # Envoi des paramètres de vol aux groupe ROUTE
    #IvySendMsg("GT_PARAM_CRZ_ALT="+str(CRZ_ALT)) # envoi de l'altitude de croisière
    #IvySendMsg("GT_PARAM_CAS="+str(CAS)) # envoi de la CAS
    #IvySendMsg("GT_PARAM_MACH=" + str(MACH))  # envoi du MACH
    #IvySendMsg("GT_PARAM_WIND=" + WIND)  # envoi du WIND

    # Abonnement au message de stop
    #IvyBindMsg(stop, "^Stop$")
    #IvyMainLoop()
