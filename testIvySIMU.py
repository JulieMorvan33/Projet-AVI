from ivy.std_api import *
import time
from constantParameters import *
PRECISION_FACTOR = 100

USING_STATE_VECTOR = False

if __name__ == '__main__':
    bus = "192.168.43.255:2010"

    # Initialisation
    IvyInit("SIMU", "Bonjour du simulateur")
    IvyStart()

    time.sleep(2)

    # Envoi de l'identifiant de l'aéroport de départ
    IvySendMsg("SP_AptId Identifier=LFMN")

    # Envoie du temps
    for i in range(50):
        IvySendMsg("Time t="+str(float(i)))
        x, y = (4.33 - i * 0.1)*100*NM2M, (29.30 + i * 1.5/20)*100*NM2M  # m

        if USING_STATE_VECTOR:
            message = "StateVector x=" + str(x) + " y=" + str(y) + " z=" + str(30000*FT2M)
            message += " Vp=" + str(250*NM2M*3600) + " fpa=" + str(273) + " psi=" + str(0) + " phi=" + str(0)
        else:
            message = "AircraftSetPosition X=" + str(x) + " Y=" + str(y)
            message += " Altitude-ft=" + str(30000*FT2M) + " Roll=" + str(0) + " Pitch=" + str(0) + " Yaw=" + str(0)
            message += " Heading=" + str(273) + " Airspeed=" + str(250*NM2M*3600) + " Groundspeed=" + str(265*NM2M*3600)

        print(message)
        IvySendMsg(message)
        time.sleep(0.5)

    for i in range(50):
        IvySendMsg("Time t=" + str(float(i)))
        x, y = (100 + i * 0.1)*100*NM2M , (75 + i * 1.5/20)*100*NM2M   # m
        if USING_STATE_VECTOR:
            message = "InitStateVector x=" + str(x) + " y=" + str(y) + " z=" + str(30000*FT2M)
            message += " Vp=" + str(250*NM2M*3600) + " fpa=" + str(273) + " psi=" + str(0) + " phi=" + str(0)
        else:
            message = "AircraftSetPosition X=" + str(x) + " Y=" + str(y)
            message += " Altitude-ft=" + str(30000) + " Roll=" + str(0) + " Pitch=" + str(0) + " Yaw=" + str(0)
            message += " Heading=" + str(273) + " Airspeed=" + str(250*NM2M*3600) + " Groundspeed=" + str(265*NM2M*3600)
        IvySendMsg(message)
        time.sleep(0.5)

    IvyMainLoop()

