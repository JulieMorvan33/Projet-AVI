from ivy.std_api import *
import time
import random as r

def receiveTRAJ(agent, *data):
    print("Message de TRAJ : ", data[0])


if __name__ == '__main__':
    bus = "192.168.43.255:2010"

    # Initialisation
    IvyInit("LEGS", "Bonjour du groupe SEQ")
    IvyStart()

    t = time.time()
    for i in range(1000):
        dt = time.time() - t

        # Toutes les 100 ms
        time.sleep(0.1)

        # Send SEQ Data message
        xtk = r.randint(5, 50) / 10
        tae = r.randint(1, 10)/10
        dtwpt = r.randint(2, 40)
        bank_angle_ref = r.randint(1, 250)/10
        aldtwpt = dtwpt - r.randint(2, 7)
        seqParamMess = "GS_Data Time="
        seqParamMess += str(round(dt, 1)) + " XTK=" + str(xtk)
        seqParamMess += " TAE=" + str(tae) + " DTWPT=" + str(dtwpt) + " ALDTWPT=" + str(aldtwpt)
        seqParamMess += " BANK_ANGLE_REF=" + str(bank_angle_ref)
        print(seqParamMess)
        IvySendMsg(seqParamMess)

        if i%5==0:
            # Toutes les 500ms
            # Message d'active leg
            actLegMess = "GS_AL Time="
            actLegMess += str(round(dt, 1)) + " NumSeqActiveLeg=" + str(i//5)
            print(actLegMess)
            IvySendMsg(actLegMess)

        time.sleep(1)

    IvyMainLoop()