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
    IvyStart() # mettre 'bus' entre parenthèse si utilisation du wifi
    time.sleep(1.0)
    IvyBindMsg(receiveTRAJ, "GT (.*)")

    msg = "FL_LegList Time=0.0 LegList=(SEQ=0 TYPE=IF ID=LFMN LAT=N43395546 LONG=E007125394; SEQ=1 TYPE=TF ID=OKTET WPT_TYPE=Flyby LAT=N44290600 LONG=E006341000 COURSE=327 DISTANCE=63 FLmin=FL000 FLmax=FL195; SEQ=2 TYPE=TF ID=GIPNO WPT_TYPE=Flyby LAT=N45333600 LONG=E005314500 COURSE=325 DISTANCE=76 FLmin=FL195 FLmax=FL460; SEQ=3 TYPE=TF ID=BULOL WPT_TYPE=Flyby LAT=N46024500 LONG=E005053100 COURSE=345 DISTANCE=42 FLmin=FL195 FLmax=FL460; SEQ=4 TYPE=TF ID=MOMIL WPT_TYPE=Flyby LAT=N46324600 LONG=E004324800 COURSE=301 DISTANCE=35 FLmin=FL195 FLmax=FL460; SEQ=5 TYPE=TF ID=ATN WPT_TYPE=Flyby LAT=N46482140 LONG=E004153290 COURSE=323 DISTANCE=11 FLmin=FL000 FLmax=FL460; SEQ=6 TYPE=TF ID=AVLON WPT_TYPE=Flyby LAT=N47333600 LONG=E003484800 COURSE=332 DISTANCE=57 FLmin=FL195 FLmax=FL460; SEQ=7 TYPE=TF ID=OKRIX WPT_TYPE=Flyby LAT=N47575800 LONG=E003340300 COURSE=338 DISTANCE=15 FLmin=FL195 FLmax=FL460; SEQ=8 TYPE=TF ID=TELBO WPT_TYPE=Flyby LAT=N48252700 LONG=E002515300 COURSE=321 DISTANCE=52 FLmin=FL195 FLmax=FL460; SEQ=9 TYPE=TF ID=MLN WPT_TYPE=Flyby LAT=N48272080 LONG=E002484780 COURSE=313 DISTANCE=1 FLmin=FL195 FLmax=FL460; SEQ=10 TYPE=TF ID=AGOGO WPT_TYPE=Flyby LAT=N48311200 LONG=E002423800 COURSE=313 DISTANCE=3 FLmin=FL000 FLmax=FL460; SEQ=11 TYPE=TF ID=LFRG WPT_TYPE=Flyby LAT=N49214822 LONG=E000093599 COURSE=301 DISTANCE=106 FLmin=FL000 FLmax=FL195)"

    IvySendMsg(msg)

    def send_message_previous():
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
