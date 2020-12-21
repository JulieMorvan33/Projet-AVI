from geometry import *
from PyQt5.QtCore import pyqtSignal, QObject
import time
from ivy.std_api import *

DP = 20 # nb de positions à faire à l'avion sur chaque leg

class Simulation(QObject):
    update_signal = pyqtSignal() # signal d'update envoyé à radarmotion
    update_display_signal = pyqtSignal()  # signal d'update envoyé à radarview pour l'affichage

    def __init__(self, USE_IVY, SIMU_DELAY, init_time=0):
        super(Simulation, self).__init__()
        self.USE_IVY = USE_IVY
        self.SIMU_DELAY = SIMU_DELAY
        self.time = init_time
        self.trajFMS = Trajectoire_brute()
        self.AC_X, self.AC_Y, self.AC_GS = 0, 0, 0  # initialisation des paramètre de l'avion
        if not(self.USE_IVY): # pour une simulation sans bus Ivy
            self.create_AC_positions() # pour les positions avion
            self.create_waypoints_without_Ivy() # pour les positions des WayPoints

    def create_AC_positions(self): # pour une simulation sans bus Ivy
        self.listeACpositions = []
        for i in range(50):
            self.AC_X, self.AC_Y = float(i * 2), i * 1.5  # Nm
            self.listeACpositions.append(Point(self.AC_X, self.AC_Y))
        for i in range(50):
            self.AC_X, self.AC_Y = float(100 - i * 2), 75 + i * 1.5  # Nm
            self.listeACpositions.append(Point(self.AC_X, self.AC_Y))

    def horloge(self, *arg):
        self.time = float(arg[1])

    #####  Aicraft state ####################################
    def get_AC_state(self, agent, *data):
        state = data[0].split(" ")
        self.AC_X, self.AC_Y = float(state[0].strip("x=")), float(state[1].strip("y="))
        print("SIMU, AC X et Y : ", self.AC_X, self.AC_Y)
        self.update_signal.emit()

    def get_AC_state_without_Ivy(self):
        for i in range(50):
            self.AC_X, self.AC_Y = float(i * 2), i * 1.5  # Nm
            self.update_signal.emit()
            time.sleep(self.SIMU_DELAY)
        for i in range(50):
            self.AC_X, self.AC_Y = float(100 - i * 2), 75 + i * 1.5  # Nm
            self.update_signal.emit()
            time.sleep(self.SIMU_DELAY)

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
        self.trajFMS = Trajectoire_brute() # on écrase les données de waypoints
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
        self.trajFMS.add_waypoint(Point(0, 0))
        self.trajFMS.add_waypoint(Point(20, 100))
        self.trajFMS.add_waypoint(Point(100, 60))
        self.trajFMS.add_waypoint(Point(125, 90))
        self.trajFMS.add_waypoint(Point(200, 150))
        self.trajFMS.add_waypoint(Point(100, 180))

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

        ### Transitions
        ListTransitionsMessage = "GT_TRAJ Liste_Transitions=["
        for trans in self.trajFMS.transitions_list:
            ListTransitionsMessage += "Transition(Point(" + str(trans.centre.x) + ", " + str(trans.centre.y) + "), "
            ListTransitionsMessage += str(trans.turn_radius) + ", " + str(trans.lead_distance) + "), "
        mes.append(ListTransitionsMessage[:-2] + "]")

        ### Orthos
        ListOrthosMessage = "GT_TRAJ Liste_Orthos=["
        for ortho in self.trajFMS.orthos_list:
            s, e = ortho.start, ortho.end
            ListOrthosMessage += "Ortho(Point(" + str(s.x) + ", " + str(s.y) + "), "
            ListOrthosMessage += "Point(" + str(e.x) + ", " + str(e.y) + ")), "
        mes.append(ListOrthosMessage[:-2] + "]")

        #Paths
        ListPathMessage = "GT_TRAJ Liste_Paths=["
        for ind in range(len(self.trajFMS.orthos_list)):
            if ind==len(self.trajFMS.orthos_list)-1:
                ListPathMessage += "Path(Liste_Orthos[" + str(ind) + "], Transition(None, None, None))]"
            else:
                ListPathMessage += "Path(Liste_Orthos[" + str(ind) + "], Liste_Transitions[" + str(ind) + "]), "
        mes.append(ListPathMessage)

        ### Bank angles
        ListBankAnglesMessage = "GT_TRAJ Liste_BankAngles=["
        for bk_angle in self.trajFMS.bankAnglesList:
            ListBankAnglesMessage += str(bk_angle) + ", "
            

        mes.append(ListBankAnglesMessage[:-2] + "]")

        return mes

    def send_trajectory(self):  # Envoi de la trajectoire au groupe SEQ
        print("SIMU ENVOI")
        traj_message = self.traj_To_SEQ()
        print('messageToSEQ : ', traj_message )
        IvySendMsg(traj_message[0])  # envoi de l'aéroport de départ (LAT/LONG) et de la liste des points
        IvySendMsg(traj_message[1])  # envoi de la liste des segments
        IvySendMsg(traj_message[2])  # envoi de la liste des transitions
        IvySendMsg(traj_message[3])  # envoi de la liste des orthos
        IvySendMsg(traj_message[4])  # envoie de la liste des paths
        IvySendMsg(traj_message[5])  # envoie la liste des Bank Angles


    # Réception des valeurs de XTK, TAE, DTWPT
    #"GS_Data Time=time XTK=xtk TAE=tae DTWPT=dtwpt BANK_ANGLE_REF=ref"
    def receive_SEQ_parameters(self, agent, *data):
        mes = data[0].split(" ")
        time = float(mes[0].strip("Time="))
        xtk = int(mes[1].strip("XTK="))
        tae = int(mes[1].strip("TAE="))
        dtwpt = int(mes[1].strip("DTWPT="))
        print("SEQ envoie les paramètres : XTK = ", xtk, " TAE = ", tae, " DTWPT = ", dtwpt)

    # Réception du leg actif
    #"GS_AL Time=time NumSeqActiveLeg=numseq"
    def receive_active_leg(self, agent, *data):
        mes = data[0].split(" ")
        time = float(mes[0].strip("Time="))
        activeLeg = int(mes[1].strip("NumSeqActiveLeg="))
        print("SEQ envoie le séquencement : time=", time, " active leg = ", activeLeg)







