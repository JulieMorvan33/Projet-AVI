from ivy.std_api import *
from simulation import *

#TIME = 0.0 # initialisation du temps de l'horloge
#GROUNDSPEED = 0 # initialisation de la ground speed

def null_cb(*a):
    pass

def stop(agent):
    IvyStop()

def on_COMM(agent, *data):
    """Test : GC_AP Time=time AP_State=selected"""
    mode = str(data[0])
    print("Mode : ", mode)

def trajToSend():
    mes = []
    ListPointsMessage = "GT_TRAJ  Liste_Points=["
    sim = Simulation() # crée des waypoints dans une simulation
    for point in sim.trajFMS.waypoint_list:
        ListPointsMessage += "Point("+str(point.x)+", "+str(point.y)+"),"
    ListPointsMessage = ListPointsMessage[:-1] # la dernière virgule est supprimée
    ListPointsMessage += "]"
    mes.append(ListPointsMessage)
    return mes

def paramVolToSend():
    mes = []


