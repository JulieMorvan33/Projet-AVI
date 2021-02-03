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
    IvySendMsg("GC_AP Time=0 AP_State='HDG'")  # message pas pris en compte
    IvySendMsg("FCULateral Mode=SelectedHeading Val=50")
    time.sleep(1)
    for i in range(50):
        IvySendMsg("Time t="+str(float(i)))
        print("Time t="+str(float(i)))
        x, y = (1861+i*2)*NM2M, (304.5-i)*NM2M  # m

        # if USING_STATE_VECTOR:
        message1 = "StateVector x=" + str(x) + " y=" + str(y) + " z=" + str(30000*FT2M)
        message1 += " Vp=" + str(250*NM2M*3600) + " fpa=" + str(273) + " psi=" + str(0) + " phi=" + str(0)
        #else:
        message2 = "AircraftSetPosition X=" + str(x) + " Y=" + str(y)
        message2 += " Altitude-ft=" + str(30000*FT2M) + " Roll=" + str(0) + " Pitch=" + str(0) + " Yaw=" + str(0)
        message2 += " Heading=" + str(273) + " Airspeed=" + str(250) + " Groundspeed=" + str(265)

        print(message1, message2)
        IvySendMsg(message1)
        IvySendMsg(message2)
        time.sleep(0.5)

    for i in range(50):
        IvySendMsg("Time t=" + str(float(i)))
        x, y = (100 + i * 0.1)*100*NM2M, (75 + i * 1.5/20)*100*NM2M   # m

        #if USING_STATE_VECTOR:
        message1 = "InitStateVector x=" + str(x) + " y=" + str(y) + " z=" + str(30000*FT2M)
        message1 += " Vp=" + str(250*NM2M*3600) + " fpa=" + str(273) + " psi=" + str(0) + " phi=" + str(0)
        #else:
        message2 = "AircraftSetPosition X=" + str(x) + " Y=" + str(y)
        message2 += " Altitude-ft=" + str(30000) + " Roll=" + str(0) + " Pitch=" + str(0) + " Yaw=" + str(0)
        message2 += " Heading=" + str(273) + " Airspeed=" + str(250) + " Groundspeed=" + str(265)
        IvySendMsg(message1)
        IvySendMsg(message2)
        print(message1, message2)
        time.sleep(0.5)

    IvyMainLoop()

