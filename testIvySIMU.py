from ivy.std_api import *
import time


if __name__ == '__main__':
    bus = "192.168.43.255:2010"

    # Initialisation
    IvyInit("SIMU", "Bonjour du simulateur")
    IvyStart()

    time.sleep(5)

    # Envoie du temps
    for i in range(50):
        IvySendMsg("Time t="+str(float(i)))
        x, y = i*2, i*1.5 # Nm
        GS = 700 # knots
        IvySendMsg("StateVector x="+str(x)+" y="+str(y)+" Groundspeed="+str(GS))
        time.sleep(0.2)
    for i in range(50):
        IvySendMsg("Time t=" + str(float(i)))
        x, y = 100 - i * 2, 75 + i * 1.5  # Nm
        GS = 700  # knots
        IvySendMsg("StateVector x=" + str(x) + " y=" + str(y) + " Groundspeed=" + str(GS))
        time.sleep(0.2)

    IvyMainLoop()