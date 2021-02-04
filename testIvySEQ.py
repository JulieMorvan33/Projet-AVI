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
    IvyInit("SEQ", "Bonjour du groupe SEQ", 0, null_cb, null_cb)
    IvyStart()
    time.sleep(1.0)
    t = time.time()
    for i in range(1000):
        dt = time.time() - t

        # Toutes les 100 ms
        time.sleep(0.1)

        # Envoi du SEQ Data message
        xtk = r.randint(5, 50) / 10
        tae = r.randint(1, 10)/10
        dtwpt = r.randint(2, 40)
        bank_angle_ref = r.randint(1, 250)/10
        aldtwpt = dtwpt - r.randint(2, 7)
        seqParamMess = "GS_Data Time="
        seqParamMess += str(round(dt, 1)) + " XTK=" + str(xtk)
        seqParamMess += " TAE=" + str(tae) + " DTWPT=" + str(dtwpt)
        seqParamMess += " BANK_ANGLE_REF=" + str(bank_angle_ref)
        seqParamMess += " ALDTWPT=" + str(aldtwpt)
        print(seqParamMess)
        IvySendMsg(seqParamMess)

        if i % 10 == 0:  # toutes les 100 ms, message d'active leg
            actLegMess = "GS_AL Time="
            actLegMess += str(round(dt, 1)) + " NumSeqActiveLeg=" + str(i//10+1)
            print(actLegMess)
            IvySendMsg(actLegMess)

        time.sleep(1)

    IvyMainLoop()
