from geometry import *
from PyQt5.QtCore import pyqtSignal, QObject
import time
from predictions import SpeedPredictionsA320
from predictions import *
from constantParameters import *
import numpy as np
from transitions import get_track
#from ivy.std_api import *

DP = 20 # nb de positions à faire à l'avion sur chaque leg

class Simulation(QObject):
    update_signal = pyqtSignal() # signal d'update envoyé à radarmotion
    update_display_signal = pyqtSignal()  # signal d'update envoyé à radarview pour l'affichage
    update_param = pyqtSignal()
    heading_update_signal = pyqtSignal()

    def __init__(self, USE_IVY, SIMU_DELAY, init_time=0):
        super(Simulation, self).__init__()
        self.USE_IVY = USE_IVY
        self.SIMU_DELAY = SIMU_DELAY
        self.time = init_time
        self.trajFMS = RefLatPath()
        self.mode = None # mode de l'autopilot ("MAN" ou "SEL")
        self.flightParam = dict() # contient CRZ_ALT, CI et WIND
        self.SEQParam = dict() # contient XTK, TAE, DTWPT, ALDTWPT
        self.NextWPTParam = dict() # contient NEXTWPT, COURSE, TTWPT
        self.defineDict()
        self.speedPred = SpeedPredictionsA320()
        self.defineSpeedsPrediction(CI, FL, WIND)
        self.AC_X, self.AC_Y, self.AC_HDG, self.AC_TAS, self.AC_GS = 0, 0, 0, 0, 0  # initialisation des paramètre de l'avion
        if not(self.USE_IVY): # pour une simulation sans bus Ivy
            self.create_waypoints_without_Ivy()  # pour les positions des WayPoints
            self.create_AC_positions() # pour les positions avion
            self.create_AC_state_without_Ivy()

    def defineDict(self):
        self.defineFlightParam(0, 0, 0)
        self.defineSEQParam(0, 0, 0, 0)
        self.defineNextWPTParam(0, 0, 0)

    def defineFlightParam(self, crz_alt, ci, wind):
        # Rempli le dictionnaire flightParam
        # crz_alt en feet, ci entier sans unité, wind chaine de caractère
        self.flightParam["CRZ_ALT"] = crz_alt
        self.flightParam["CI"] = ci
        self.flightParam["WIND"] = wind

    def defineSEQParam(self, xtk, tae, dtwpt, aldtwpt):
        # Rempli le dictionnaire SEQParam
        # tae en degrés, xtk, dtwpt et aldtwpt en Nm
        self.SEQParam["XTK"] = xtk
        self.SEQParam["TAE"] = tae
        self.SEQParam["DTWPT"] = dtwpt
        self.SEQParam["ALDTWPT"] = aldtwpt

    def defineNextWPTParam(self, nextwpt, course, ttwpt):
        # Rempli le dictionnaire NextWPTParam, correspondant aux données du prochain WPT
        # nextwpt string, course en degrés, ttwpt en min
        self.NextWPTParam["NEXTWPT"] = nextwpt
        self.NextWPTParam["COURSE"] = course
        self.NextWPTParam["TTWPT"] = ttwpt

    def defineSpeedsPrediction(self, ci, fl, wind):
        self.speedPred.computeSpeeds(ci, fl, wind)

    def horloge(self, *arg):
        self.time = float(arg[1])

    #####  Aicraft state ####################################
    def get_AC_state(self, agent, *data):
        state = data[0].split(" ")
        self.AC_X, self.AC_Y = float(state[0].strip("x=")), float(state[1].strip("y="))
        self.AC_HDG = float(state[6].strip("Heading=")) # en degrés
        self.AC_TAS, self.AC_GS = float(state[7].strip("Airspeed=")), float(state[8].strip("Groundspeed=")) # en kts
        print("SIMU, X=", self.AC_X, " Y=", self.AC_Y, " HDG=", self.AC_HDG, " TAS=", self.AC_TAS, " GS=", self.AC_GS)
        self.update_signal.emit()

    def create_AC_positions(self, n=10): # pour une simulation sans bus Ivy
        self.listeACpositions = []
        self.listeHDG = []
        wp0 = self.trajFMS.waypoint_list[0]
        self.AC_X, self.AC_Y = wp0.x, wp0.y
        print("pos de l'avion initiale : ", self.AC_X, self.AC_Y)
        self.listeACpositions.append(Point(self.AC_X, self.AC_Y))

        for ind in range(self.trajFMS.nbr_waypoints-1):
            a = self.trajFMS.waypoint_list[ind]
            b = self.trajFMS.waypoint_list[ind + 1]
            seg = Segment(a,b)
            hdg = get_track(seg)
            hdg = hdg * RAD2DEG
            print(hdg)
            if hdg < 0:
                hdg = 360 + hdg
            x1, y1, x2, y2 = a.x, a.y, b.x, b.y
            for i in range(1, n+1):
                self.AC_X += (x2-x1)/n
                self.AC_Y += (y2-y1)/n
                self.listeACpositions.append(Point(self.AC_X, self.AC_Y))
                self.listeHDG.append(hdg)


        '''
        for i in range(50):
            self.AC_X += float(i * 2) # Nm
            self.AC_Y += i * 1.5  # Nm
            self.listeACpositions.append(Point(self.AC_X, self.AC_Y))
            self.update_signal.emit()
        for i in range(50):
            self.AC_X += float(100 - i * 2)# Nm
            self.AC_Y += 75 + i * 1.5  # Nm
            self.listeACpositions.append(Point(self.AC_X, self.AC_Y))
        '''

    def create_AC_state_without_Ivy(self):
        self.listeHDG = []
        for i in range(50):
            self.AC_HDG = np.arcsin(0.5)*RAD2DEG
            self.AC_TAS, self.AC_GS = self.speedPred.TAS, self.speedPred.GS
            self.listeHDG.append(self.AC_HDG)
        for i in range(50):
            self.HDG = np.arcsin(-0.5)*RAD2DEG
            self.AC_TAS, self.AC_GS = self.speedPred.TAS, self.speedPred.GS
            self.listeHDG.append(self.AC_HDG)

    #### Liste de LEG de la part du groue LEGS ##############
    def from_LEGS(self, *data):
        print("Agent %r is sending a LEGS message!" % data[0])
        message = data[1].split(" LegList=(")
        time = float(message[0].strip("Time="))
        dataListGlob = message[1].split("; ")
        self.ListeFromLegs = []
        for j, dataList in enumerate(dataListGlob):
            data = dataList.split(" ")
            id = data[0].strip("ID=")  # string donnant l'ID du leg (ex : 'WPT1)
            seq = int(data[1].strip("SEQ="))  # int numéro de séquencement (ex: 1)
            lat = data[2].strip("LAT=")  # string donnant la latitude
            long = data[3].strip("LONG=")  # string donnant la longitude
            if j == len(dataListGlob) - 1:
                course = float(data[4][:-1].strip("COURSE="))
            else:
                course = float(
                    data[4].strip("COURSE="))  # float course du leg angle vers le prochain leg (ex: 110°)
            self.ListeFromLegs.append([id, seq, lat, long, course])

        print(self.ListeFromLegs)
        self.create_WayPoints()

    def create_WayPoints(self):
        self.trajFMS = RefLatPath() # on écrase les données de waypoints
        # on pourrait faire mieux en ne rajoutant que les waypoints en plus
        for ind, leg in enumerate(self.ListeFromLegs):
            lat, long = leg[2][1:], leg[3][1:]

            lat = float(lat[0:2]) + float(lat[2:4]) / 60 + float(lat[4:6])/3600
            long = float(long[0:3]) + float(long[3:5]) / 60 + float(long[5:7])/3600

            if leg[2][0] == "S":
                lat = -lat
            if leg[3][0] == "W":
                long = -long

            wpt = WayPoint(lat, long)
            x, y = wpt.convert()
            if ind==0:
                x_airport_depart, y_airport_depart = lat, long
            # on force le premier point (aéroport de départ) à 0,0
            self.trajFMS.add_waypoint(Point(x-x_airport_depart, y-y_airport_depart))
        self.update_display_signal.emit()

    def create_waypoints_without_Ivy(self):
        self.trajFMS.add_waypoint(Point(180, 220))
        self.trajFMS.add_waypoint(Point(100, 180))
        self.trajFMS.add_waypoint(Point(200, 150))
        self.trajFMS.add_waypoint(Point(110, -30))
        self.trajFMS.add_waypoint(Point(100, 60))
        self.trajFMS.add_waypoint(Point(20, 100))
        self.trajFMS.add_waypoint(Point(0, 0))
        self.trajFMS.add_waypoint(Point(-60, 0))
        self.trajFMS.add_waypoint(Point(-160, -130))
        self.update_signal.emit()

    def next_wpt_param_without_IVY(self):
        nextwpt = "ABABI"
        course = "150"
        ttwpt = "10:00"
        self.defineNextWPTParam(nextwpt, course, ttwpt)
        # self.ListeFromLegs.append(["ABABI", "0", "N40451900", "E018383000", "150"])
        # return ["ABABI", "0", "N40451900", "E018383000", "150"]

    def seq_param_without_IVY(self):
        xtk= "15"
        tae = "0"
        dtwpt = "150"
        aldtwpt = "155"
        self.defineSEQParam(xtk, tae, dtwpt, aldtwpt)

    def wind_without_IVY(self):
        self.defineFlightParam("400", "1", "162° / 10")

    #### Trajectoire envoyée à SEQ ##############
    def traj_To_SEQ(self):
        mes = []

        ### Liste des WayPoints
        #if self.ListeFromLegs != []:
            ### Aéroport de départ en LAT/LONG
            #for wpt in self.trajFMS.waypoint_list:


        ### Points
        ListPointsMessage = "GT_TRAJ Liste_Points=["
        for point in self.trajFMS.waypoint_list:
            ListPointsMessage += "Point(" + str(point.x) + ", " + str(point.y) + "),"
        mes.append(ListPointsMessage[:-1] + "]") # on enlève la dernière virgule et on rajoute le crochet de la fin

        ### Segments
        ListSegmentsMessage = "GT_TRAJ Liste_Segments=["
        for ind in range(self.trajFMS.nbr_waypoints - 1):
            ListSegmentsMessage += "Segment(Liste_Points[" + str(ind) + "], Liste_Points[" + str(ind+1) + "]),"
        mes.append(ListSegmentsMessage[:-1] + "]")


        #ListTransitionsMessage = "GT_TRAJ Liste_Transitions=["
        ListOrthosMessage = "GT_TRAJ Liste_Orthos=["
        for path in self.trajFMS.listePaths:
            ortho, trans = path.segment, path.transition

            ### Transitions  A REVOIR CAR trans.centre n'existe plus
            #ListTransitionsMessage += "Transition(Point(" + str(trans.centre.x) + ", " + str(trans.centre.y) + "), "
            #ListTransitionsMessage += str(trans.turn_radius) + ", " + str(trans.lead_distance) + "), "

            ### Orthos
            s, e = ortho.start, ortho.end
            ListOrthosMessage += "Ortho(Point(" + str(s.x) + ", " + str(s.y) + "), "
            ListOrthosMessage += "Point(" + str(e.x) + ", " + str(e.y) + ")), "

        #mes.append(ListTransitionsMessage[:-2] + "]")
        mes.append(ListOrthosMessage[:-2] + "]")

        #Paths
        ListPathMessage = "GT_TRAJ Liste_Paths=["
        for ind in range(len(self.trajFMS.listePaths)):
            if ind==len(self.trajFMS.listePaths)-1:
                ListPathMessage += "Path(Liste_Orthos[" + str(ind) + "], Transition(None, None, None))]"
            else:
                ListPathMessage += "Path(Liste_Orthos[" + str(ind) + "], Liste_Transitions[" + str(ind) + "]), "
        mes.append(ListPathMessage)

        ### Bank angles
        """
        ListBankAnglesMessage = "GT_TRAJ Liste_BankAngles=["
        for bk_angle in self.trajFMS.bankAnglesList:
            ListBankAnglesMessage += str(bk_angle) + ", "
            
        mes.append(ListBankAnglesMessage[:-2] + "]")
        """

        return mes

    def send_trajectory(self):  # Envoi de la trajectoire au groupe SEQ
        print("SIMU ENVOI")
        traj_message = self.traj_To_SEQ()
        print('messageToSEQ : ', traj_message )
        IvySendMsg(traj_message[0])  # envoi de l'aéroport de départ (LAT/LONG) et de la liste des points
        IvySendMsg(traj_message[1])  # envoi de la liste des segments
        #IvySendMsg(traj_message[2])  # envoi de la liste des transitions
        IvySendMsg(traj_message[3])  # envoi de la liste des orthos
        IvySendMsg(traj_message[4])  # envoie de la liste des paths
        IvySendMsg(traj_message[5])  # envoie la liste des Bank Angles


    # Réception des valeurs de XTK, TAE, DTWPT
    #"GS_Data Time=time XTK=xtk TAE=tae DTWPT=dtwpt BANK_ANGLE_REF=ref"
    def receive_SEQ_parameters(self, agent, *data):
        mes = data[0].split(" ")
        time = float(mes[0].strip("Time="))
        xtk = float(mes[1].strip("XTK="))
        tae = float(mes[2].strip("TAE="))
        dtwpt = float(mes[3].strip("DTWPT="))
        aldtwpt = float(mes[4].strip("ALDTWPT="))
        print("SEQ envoie les paramètres : XTK = ", xtk, " TAE = ", tae, " DTWPT = ", dtwpt, " ALDTWPT = ", aldtwpt)
        self.defineSEQParam(xtk, tae, dtwpt, aldtwpt)
        self.update_param.emit()


    # Réception du leg actif
    #"GS_AL Time=time NumSeqActiveLeg=numseq"
    def receive_active_leg(self, agent, *data):
        mes = data[0].split(" ")
        time = float(mes[0].strip("Time="))
        activeLeg = int(mes[1].strip("NumSeqActiveLeg="))
        print("SEQ envoie le séquencement : time=", time, " active leg = ", activeLeg)

        for leg in self.ListeFromLegs:
            if activeLeg==leg[1]:
                nextwpt = leg[0]
                course = leg[4]
                # ttpt = self.SEQParam["DTWPT"] * NM2M / (SpeedPredictions().TAS * KT2MS)  # Pour l'instant TAS = 0 donc

                self.defineNextWPTParam(nextwpt, course, 0) #, ttpt)
                self.update_param.emit()









