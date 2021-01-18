from ivy.std_api import *
import time
import random as r


def receiveTRAJ(agent, *data):
    print("Message de TRAJ : ", data[0])


def null_cb(*a):
    pass


if __name__ == '__main__':
    bus = "192.168.43.255:2010"

    # Initialisation
    IvyInit("LEGS", "Bonjour du groupe LEGS", 0, null_cb, null_cb)
    IvyStart()
    time.sleep(1.0)
    IvyBindMsg(receiveTRAJ, "GT (.*)")

    # LAT_list = ["N00000000", "N45000000", "N43000000", "N4600000"]
    # LONG_list = ["E000000000","E005000000", "E030000000", "E040000000"]
    # NAMES = ['ABABI', 'GATEO', 'TIHAG', 'ARIMU']
    #COURSES = [0, 0, 102, 72]

    LAT_list = ["N43400000", "N44290600", "N46024500", "N46482100", "N47575800", "N48251000", "N48340700", "N48472600", "N49214800"]
    LONG_list = ["E007130000", "E006341000", "E005053100", "E004153300", "E003340300", "E002584900", "E002113100", "E000314900", "E000093600"]
    NAMES = ["LFMN", "OKTET", "BULOL", "PIBAT", "OKRIX", "AMODO", "RESMI", "LGL", "LFRG"]
    FLY = ["fly_by", 'fly_by', "fly_by", "fly_over", "fly_by", "fly_by", "fly_by", "fly_by", "fly_by", "fly_by"]
    COURSES = [0, 320, 317, 315, 335, 304, 283, 280, 340]

    deb = time.time()
    time.sleep(1)
    fin = time.time()


    # Envoie de la liste des Legs
    message = "FL_LegList"
    message += " Time="+str(round(fin-deb)) + " LegList=("
    for j, id in enumerate(NAMES):
        message += "ID=" + id + " "
        message += "SEQ=" + str(j) + " "
        message += "LAT=" + str(LAT_list[j]) + " "
        message += "LON=" + str(LONG_list[j]) + " "
        message += "COURSE=" + str(COURSES[j]) + " "
        message += "FLY=" + str(FLY[j]) + " "
        message += "FLmin=" + str(100) + " "
        message += "FLmax=" + str(400) + " "
        message += "SPEEDmax=" + str(350)
        if j == len(NAMES)-1:
            message += ")"  # si c'est le dernier leg
        else:
            message += "; "
    print("Message envoyé : ", message)
    IvySendMsg(message)

    IvyMainLoop()
