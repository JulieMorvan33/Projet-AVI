from ivy.std_api import *
import time


def receiveTRAJ(agent, *data):
    print("Message de TRAJ : ", data[0])


def null_cb(*a):
    pass


if __name__ == '__main__':
    bus = "192.168.43.255:2010"

    # Initialisation
    IvyInit("LEGS", "Bonjour du groupe LEGS", 0, null_cb, null_cb)
    IvyStart()  # mettre 'bus' entre les parenthèse si utilisation du wifi
    time.sleep(1.0)
    IvyBindMsg(receiveTRAJ, "GT (.*)")

    msg = "FL_LegList Time=0.0 LegList=(SEQ=0 TYPE=IF ID=LFMN LAT=N43395546 LONG=E007125394; SEQ=1 TYPE=TF ID=OKTET " \
          "WPT_TYPE=Flyby LAT=N44290600 LONG=E006341000 COURSE=327 DISTANCE=63 FLmin=FL000 FLmax=FL195; SEQ=2 " \
          "TYPE=TF ID=GIPNO WPT_TYPE=Flyby LAT=N45333600 LONG=E005314500 COURSE=325 DISTANCE=76 FLmin=FL195 " \
          "FLmax=FL460; SEQ=3 TYPE=TF ID=BULOL WPT_TYPE=Flyby LAT=N46024500 LONG=E005053100 COURSE=345 DISTANCE=42 " \
          "FLmin=FL495 FLmax=FL460; SEQ=4 TYPE=TF ID=MOMIL WPT_TYPE=Flyby LAT=N46324600 LONG=E004324800 COURSE=301 " \
          "DISTANCE=35 FLmin=FL195 FLmax=FL460; SEQ=5 TYPE=TF ID=ATN WPT_TYPE=Flyby LAT=N46482140 LONG=E004153290 " \
          "COURSE=323 DISTANCE=11 FLmin=FL000 FLmax=FL460; SEQ=6 TYPE=TF ID=AVLON WPT_TYPE=Flyby LAT=N47333600 " \
          "LONG=E003484800 COURSE=332 DISTANCE=57 FLmin=FL195 FLmax=FL460; SEQ=7 TYPE=TF ID=OKRIX WPT_TYPE=Flyby " \
          "LAT=N47575800 LONG=E003340300 COURSE=338 DISTANCE=15 FLmin=FL195 FLmax=FL460; SEQ=8 TYPE=TF ID=TELBO " \
          "WPT_TYPE=Flyby LAT=N48252700 LONG=E002515300 COURSE=321 DISTANCE=52 FLmin=FL195 FLmax=FL460; SEQ=9 " \
          "TYPE=TF ID=MLN WPT_TYPE=Flyby LAT=N48272080 LONG=E002484780 COURSE=313 DISTANCE=1 FLmin=FL195 " \
          "FLmax=FL460; SEQ=10 TYPE=TF ID=AGOGO WPT_TYPE=Flyby LAT=N48311200 LONG=E002423800 COURSE=313 DISTANCE=3 " \
          "FLmin=FL000 FLmax=FL460; SEQ=11 TYPE=TF ID=LFRG WPT_TYPE=Flyby LAT=N49214822 LONG=E000093599 COURSE=301 " \
          "DISTANCE=106 FLmin=FL000 FLmax=FL195)"

    IvySendMsg(msg)
    IvyMainLoop()
