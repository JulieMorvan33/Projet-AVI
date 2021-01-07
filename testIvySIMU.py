from ivy.std_api import *
import time
PRECISION_FACTOR = 100

if __name__ == '__main__':
    bus = "192.168.43.255:2010"

    # Initialisation
    IvyInit("SIMU", "Bonjour du simulateur")
    IvyStart(bus)

    time.sleep(2)


    # Envoie du temps
    for i in range(50):
        IvySendMsg("Time t="+str(float(i)))
        x, y = 4.00+i*2, 29.30+i*1.5 # Nm
        message = "AircraftSetPosition X=" + str(x*PRECISION_FACTOR) + " Y=" + str(y*PRECISION_FACTOR)
        message += " Altitude-ft=" + str(30000) + " Roll=" + str(0) + " Pitch=" + str(0) + " Yaw=" + str(0)
        message += " Heading=" + str(273) + " Airspeed=" + str(250) + " Groundspeed=" + str(265)
        print(message)
        IvySendMsg(message)
        time.sleep(0.5)
    for i in range(50):
        IvySendMsg("Time t=" + str(float(i)))
        x, y = 100 - i * 2, 75 + i * 1.5  # Nm
        message = "AircraftSetPosition X=" + str(x*PRECISION_FACTOR) + " Y=" + str(y*PRECISION_FACTOR)
        message += " Altitude-ft=" + str(30000) + " Roll=" + str(0) + " Pitch=" + str(0) + " Yaw=" + str(0)
        message += " Heading=" + str(273) + " Airspeed=" + str(250) + " Groundspeed=" + str(265)
        IvySendMsg(message)
        time.sleep(0.5)

    IvyMainLoop()

