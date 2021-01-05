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
        message = "AircraftSetPosition X=" + str(x) + " Y=" + str(y)
        message += " Altitude-ft=" + str(30000) + " Roll=" + str(0) + " Pitch=" + str(0) + " Yaw=" + str(0)
        message += " Heading=" + str(273) + " Airspeed=" + str(250) + " Groundspeed=" + str(265)
        IvySendMsg(message)
        time.sleep(0.5)
    for i in range(50):
        IvySendMsg("Time t=" + str(float(i)))
        x, y = 100 - i * 2, 75 + i * 1.5  # Nm
        message = "AircraftSetPosition X=" + str(x) + " Y=" + str(y)
        message += " Altitude-ft=" + str(30000) + " Roll=" + str(0) + " Pitch=" + str(0) + " Yaw=" + str(0)
        message += " Heading=" + str(273) + " Airspeed=" + str(250) + " Groundspeed=" + str(265)
        IvySendMsg(message)
        time.sleep(0.5)

    IvyMainLoop()

