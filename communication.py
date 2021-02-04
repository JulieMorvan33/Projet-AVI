from geometry import *
from PyQt5.QtCore import pyqtSignal, QObject
import time
from predictions import *
from constantParameters import *
import numpy as np
from transitions import *
from ivy.std_api import *

DP = 20  # nb de positions à faire à l'avion sur chaque leg
PRECISION_FACTOR = 100


class Simulation(QObject):
    update_signal = pyqtSignal()  # signal d'update envoyé à radarmotion
    update_display_signal = pyqtSignal()  # signal d'update envoyé à radarview pour l'affichage
    update_param_1 = pyqtSignal()
    update_param_2 = pyqtSignal()
    update_aicraft_signal = pyqtSignal()
    update_flight_param_signal = pyqtSignal()
    AP_mode_signal = pyqtSignal()
    new_active_leg_signal = pyqtSignal()
    update_mode = pyqtSignal()
    new_leg_signal = pyqtSignal()

    def __init__(self, USE_IVY, SIMU_DELAY, AC_SIMULATED, init_time=0):
        super(Simulation, self).__init__()
        self.USE_IVY = USE_IVY
        self.AC_SIMULATED = AC_SIMULATED
        self.SIMU_DELAY = SIMU_DELAY
        self.time = init_time
        self.trajFMS = RefLatPath()
        self.AP_mode = "NAV"  # mode de l'autopilot, peut prendre les valeurs suivantes : "NAV", "HDG" ou "NULL"
        self.mode = "Managed"  # mode latéral, peut prendre les valeurs suivantes : SelectedHeading, SelectedTrack,
        # Managed
        self.HDG_selected = 0
        self.AC_init_HDG = 0
        self.flightParam = dict()  # contient CRZ_ALT, CI et WIND
        self.SEQParam = dict()  # contient XTK, TAE, DTWPT, ALDTWPT
        self.NextWPTParam = dict()  # contient NEXTWPT, COURSE, TTWPT
        self.speedPred = SpeedPredictionsA320()
        self.defineDict()
        self.AC_X, self.AC_Y, self.AC_HDG, self.AC_TAS, self.AC_GS = 0, 0, 0, 0, 0  # initialisation des paramètre de
        # l'avion
        self.AC_X_rel, self.AC_Y_rel = 0, 0  # positions relatives à la position de départ présents dans
        # AircraftSetPosition
        self.flight_started = False
        self.active_leg = None
        self.new_active_leg = False
        self.ZOOM = 0.1
        if not self.USE_IVY:  # pour une simulation sans bus Ivy
            self.create_waypoints_without_Ivy()  # pour les positions des WayPoints
            self.create_AC_positions()  # pour les positions avion

    def defineDict(self):
        self.defineFlightParam(0, 0, (0, 0))
        self.defineSEQParam(0, 0, 0, 0)
        self.defineNextWPTParam(0, 0, 0)

    def defineFlightParam(self, crz_alt, ci, wind):
        """Rempli le dictionnaire flightParam crz_alt en feet, ci entier sans unité, wind chaine de caractère"""
        self.flightParam["CRZ_ALT"] = crz_alt
        self.flightParam["CI"] = ci
        self.flightParam["WIND"] = wind
        self.speedPred.computeSpeeds(ci, crz_alt/100, wind)
        self.update_flight_param_signal.emit()

        if crz_alt != 0 and self.USE_IVY:  # si c'est pas l'initialisation et qu"on utilise le bus IVY
            messageToCOMM = "GT TAS=" + str(round(self.speedPred.TAS*KT2MS, 2)) + " CRZ_ALT=" \
                            + str(round(crz_alt*FT2M, 2))
            IvySendMsg(messageToCOMM)  # Envoi des paramètres au groupe GUID-COMM

    def defineSEQParam(self, xtk, tae, dtwpt, aldtwpt):
        """ Rempli le dictionnaire SEQParam tae en degrés, xtk, dtwpt et aldtwpt en Nm """
        self.SEQParam["XTK"] = xtk
        self.SEQParam["TAE"] = tae
        self.SEQParam["DTWPT"] = dtwpt
        self.SEQParam["ALDTWPT"] = aldtwpt

    def defineNextWPTParam(self, nextwpt, course, ttwpt):
        """ Rempli le dictionnaire NextWPTParam, correspondant aux données du prochain WPT nextwpt string, course en
        degrés, ttwpt en min"""
        self.NextWPTParam["NEXTWPT"] = nextwpt
        self.NextWPTParam["COURSE"] = course
        self.NextWPTParam["TTWPT"] = ttwpt

    def horloge(self, *arg):
        """Réceptionne le signal time
        N'est pas encore opérationnelle en condition réelle"""
        self.time = float(arg[1])
        PRECISION_TIMER = 10 ** -2  # on ne reçoit pas le signal exactement toutes les 5 secondes
        diff_time = int(self.time) - self.time
        if not self.AC_SIMULATED and self.flight_started:
            if int(self.time) % 5 == 0:  # Toutes les 5 secondes : calculer les deux prochaines transitions
                if abs(diff_time) < PRECISION_TIMER:  # Si on est dans l'intervalle de temps souhaité
                    pass
                    # self.compute_two_next_transitions()

    def compute_two_next_transitions(self):
        print("Calcul de la short-term trajectory")
        if self.active_leg != 0:
            for i in range(self.active_leg, self.active_leg + 2):
                if i < (self.trajFMS.nbr_waypoints - 1):
                    a, b, c = self.trajFMS.get_transition(i)  # récupère les trois WPTs de la transition
                    seg_actif = g.Segment(a, b)  # segment d'entrée de la transition
                    seg_next = g.Segment(b, c)  # segment de sortie de la transition
                    if self.USE_IVY:  # Si utilisation du bus IVY
                        transition_type = b.data["FLY"]  # Utilisation des données reçues
                    else:
                        transition_type = "Flyby"

                    if i == 1:  # si première transition
                        if transition_type == "Flyby":  # s'il s'agit d'un flyby
                            transition_list = compute_transition_fly_by(seg_actif, seg_next, self.speedPred.TAS)
                        elif transition_type == "Flyover":  # s'il s'agit d'un flyover
                            transition_list = compute_transition_fly_over(seg_actif, seg_next, self.speedPred.TAS)
                        start_segment = a
                        end_segment = transition_list[0].start

                    else:  # s'il s'agit des autres transitions
                        temp = self.trajFMS.listePaths[i - 1].transition.list_items[-1].end  # récupération du dernier
                        # point de la dernière transition effectuée pour tracer le segment reliant les deux transitions
                        if transition_type == "Flyby":
                            transition_list = compute_transition_fly_by(seg_actif, seg_next, self.speedPred.TAS)

                        elif transition_type == "Flyover":
                            transition_list = compute_transition_fly_over(seg_actif, seg_next, self.speedPred.TAS)

                        start_segment = temp  # point de début du segment
                        end_segment = transition_list[0].start  # point de fin de segment
                    self.trajFMS.listePaths[i] = Path(g.Segment(start_segment, end_segment),
                                                      g.Transition(transition_type, self.speedPred.TAS,
                                                                   transition_list))  # ajout du segment à la
                    # trajectoire
                    print("remplacement de la traj de la transition : ", i)


    def get_AC_current_heading_and_speeds(self, agent, *data):
        """Utilisation de AircraftSetPosition pour avoir le heading courant de l'avion"""
        state = data[0].split(" ")  # message AircraftSetPosition
        self.AC_HDG = float(state[6].strip("Heading="))  # en degrés
        self.AC_TAS, self.AC_GS = float(state[7].strip("Airspeed=")), float(state[8].strip("Groundspeed="))  # en kts
        self.update_aicraft_signal.emit()  # envoi d'un signal sur le bus Ivy

    def get_AC_position(self, agent, *data):
        """Utilisation de StateVector pour avoir la position courante de l'avion
        Attention : le simulateur qui envoie les données interchange les x avec les y"""
        position = data[0].split(" ")  # message StateVector
        self.AC_Y, self.AC_X = float(position[0].strip("x="))/NM2M, float(position[1].strip("y="))/NM2M  # en NM
        # (en m dans le SIMU)
        print("Pos dans SIMU ", self.AC_X, self.AC_Y)

        self.update_aicraft_signal.emit()

    def create_AC_positions(self, n=NB_AC_INTER_POS):
        """Simulation sans bus Ivy, crée les différentes positions de l'avion"""
        self.listeACpositions = []
        self.listeHDG = []
        self.AC_X, self.AC_Y = self.trajFMS.waypoint_list[0].x, self.trajFMS.waypoint_list[0].y
        self.listeACpositions.append(Point(self.AC_X, self.AC_Y))

        for ind in range(self.trajFMS.nbr_waypoints-1):
            a = self.trajFMS.waypoint_list[ind]
            b = self.trajFMS.waypoint_list[ind + 1]
            seg = Segment(a, b)
            hdg = get_track(seg)
            hdg = hdg * RAD2DEG
            if hdg < 0:
                hdg = 360 + hdg
            x1, y1, x2, y2 = a.x, a.y, b.x, b.y
            for i in range(1, n+1):  # entre chaque leg, on prend NB_AC_INTER_POS = 20 positions d'avion (valable juste
                # pour des tests en interne )
                self.AC_X += (x2-x1)/n
                self.AC_Y += (y2-y1)/n
                self.listeACpositions.append(Point(self.AC_X, self.AC_Y))
                self.listeHDG.append(hdg)

    def create_AC_state_without_Ivy(self):
        """Utilisation sans bus Ivy, crée les différents états de l'avion"""
        self.listeHDG = []
        for i in range(50):
            self.AC_HDG = np.arcsin(0.5)*RAD2DEG
            self.AC_TAS, self.AC_GS = self.speedPred.TAS, self.speedPred.GS
            self.listeHDG.append(self.AC_HDG)
        for i in range(50):
            self.HDG = np.arcsin(-0.5)*RAD2DEG
            self.AC_TAS, self.AC_GS = self.speedPred.TAS, self.speedPred.GS
            self.listeHDG.append(self.AC_HDG)

    def from_LEGS(self, *data):
        """Réception de la liste de legs de la part de FPLN-LEGS"""
        print("Agent %r is sending a LEGS message!" % data[0])
        message = data[1].split(" LegList=(")
        time = float(message[0].strip("Time="))
        dataListGlob = message[1].split("; ")
        self.ListeFromLegs = []

        for j, dataList in enumerate(dataListGlob):  # pour chaque élément des la liste
            data = dataList.split(" ")
            seq = int(data[0].strip("SEQ="))  # int numéro de séquencement (ex: 1)
            type = str(data[1].strip("TYPE="))  # type de leg (TF)
            id = data[2].strip("ID=")  # string donnant l'ID du leg (ex : WPT1)

            if j == 0:  # si c'est l'aéroport de départ
                lat = data[3].strip("LAT=")  # string donnant la latitude
                long = data[4].strip("LONG=")  # string donnant la longitude
                self.ListeFromLegs.append([id, seq, lat, long, 0, 'flyby', 0, 0, 0])
            else:
                if j == 1:  # on affiche le premier next waypoint au haut du ND
                    self.defineNextWPTParam(id, 0, 0)
                    self.update_param_2.emit()
                fly = str(data[3].strip("WPT_TYPE="))  # string spécifiant un fly_by ou un fly_over
                lat = data[4].strip("LAT=")  # string donnant la latitude
                long = data[5].strip("LONG=")  # string donnant la longitude
                course = float(data[6].strip("COURSE="))  # float course du leg angle vers le prochain leg (ex: 110°)
                if j == 1:  # s'il s'agit du deuxième waypoint
                    self.AC_init_HDG = course
                distance = float(data[7].strip("DISTANCE="))  # float donnant la longueur du leg en Nm
                fl_min = float(data[8].strip("FLmin=FL"))  # float FL min
                if j == len(dataListGlob) - 1:
                    fl_max = float(data[9][:-1].strip("FLmax=FL"))  # float FL max
                else:
                    fl_max = float(data[9].strip("FLmax=FL"))  # float FL max
                self.ListeFromLegs.append([id, seq, lat, long, course, fly, fl_min, fl_max])
        print(self.ListeFromLegs)
        self.create_WayPoints()

    def create_WayPoints(self):
        """Création des waypoints (utilisation du bus Ivy)"""
        self.trajFMS = RefLatPath()  # on écrase les données de waypoints
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

            if ind == 0:
                self.AC_X, self.AC_Y = wpt.x, wpt.y
                self.waypoint_data = dict()  # contient (course, flyby/flyover, les contraintes de FL et de vitesse)
                self.waypoint_data["COURSE"] = 0
                self.waypoint_data["FLY"] = 'Flyby'
                self.waypoint_data["FLmin"] = 0
                self.waypoint_data["FLmax"] = 0
            else:
                self.waypoint_data = dict()  # contient (course, flyby/flyover, les contraintes de FL et de vitesse)
                self.waypoint_data["COURSE"] = leg[4]
                self.waypoint_data["FLY"] = leg[5]
                self.waypoint_data["FLmin"] = leg[6]
                self.waypoint_data["FLmax"] = leg[7]
            self.waypoint_data["Name"] = leg[0]

            self.trajFMS.add_waypoint(Point(wpt.x, wpt.y, self.waypoint_data))  # ajout du waypoint à la trajectoire

        if self.AC_SIMULATED:  # si on simule nous même l'avion
            self.create_AC_positions()

        self.update_display_signal.emit()  # envoi des signaux
        self.send_AC_init_position_to_SIM_PARAM()

    def create_waypoints_without_Ivy(self):
        """Création de waypoints sans bus Ivy pour des tests en interne"""
        self.trajFMS.add_waypoint(Point(180, 220))
        self.trajFMS.add_waypoint(Point(100, 180))
        self.trajFMS.add_waypoint(Point(200, 150))
        self.trajFMS.add_waypoint(Point(110, -30))
        self.trajFMS.add_waypoint(Point(100, 60))
        self.trajFMS.add_waypoint(Point(20, 100))
        self.trajFMS.add_waypoint(Point(0, 0))
        self.trajFMS.add_waypoint(Point(-60, 0))
        self.trajFMS.add_waypoint(Point(-160, -130))

    def send_AC_init_position_to_SIM_PARAM(self):
        """Fonction d'envoi de la position initiale à SIM_PARAM"""
        time.sleep(0.3)
        mes = "GT Traj_Ready" + " z=" + str(self.flightParam["CRZ_ALT"] * FT2M) + " Vp=" + \
              str(int(self.speedPred.TAS * KT2MS)) + " fpa=0" + " psi=" + str(self.AC_init_HDG / RAD2DEG) \
              + " phi=" + str(0.0)
        print("Message envoyé à SIM_PARAM :", mes)
        IvySendMsg(mes)
        self.flight_started = True  # indication pour indiqué que le vol commence

    def next_wpt_param_without_IVY(self):
        """Création des paramètres du next waypoint sans bus Ivy (pour des tests en interne)"""
        nextwpt = "ABABI"
        course = "150"
        ttwpt = "10:00"
        self.defineNextWPTParam(nextwpt, course, ttwpt)

    def seq_param_without_IVY(self):
        """Création des paramètres du dictionnaire SEQParam sans bus Ivy (pour des tests en interne)"""
        xtk = "15"
        tae = "0"
        dtwpt = "150"
        aldtwpt = "155"
        self.defineSEQParam(xtk, tae, dtwpt, aldtwpt)

    def wind_without_IVY(self):
        """Création du paramètre de vent du dictionnaire flightParam sans bus Ivy (pour des tests en interne)"""
        self.defineFlightParam(400, 30, (163, 10))

    def traj_To_SEQ(self):
        """Trajectoire envoyée à SEQ"""
        mes = []
        wpt0 = self.trajFMS.waypoint_list[0]  # WayPoint de départ
        mes.append("GT WPT_DEPART = WayPoint(" + str(wpt0.x) + ',' + str(wpt0.y) + ')')

        if not self.new_active_leg:
            ind_debut = 0
        else:
            ind_debut = self.active_leg
            self.new_active_leg = False

        # Points
        ListPointsMessage = "GT Liste_Points=["  # message contenant la liste des points
        for point in self.trajFMS.waypoint_list[ind_debut:]:  # pour chaque point dans la liste des waypoints
            ListPointsMessage += "Point(" + str(point.x) + ", " + str(point.y) + "),"
        mes.append(ListPointsMessage[:-1] + "]")  # on enlève la dernière virgule et on rajoute le crochet de la fin

        # Segments
        ListSegmentsMessage = "GT Liste_Segments=["  # message contenant la liste des segments
        for ind in range(ind_debut, self.trajFMS.nbr_waypoints - 1):
            ListSegmentsMessage += "Segment(Liste_Points[" + str(ind) + "], Liste_Points[" + str(ind+1) + "]),"
        mes.append(ListSegmentsMessage[:-1] + "]")

        # Transitions
        ListTransitionsMessage = "GT Liste_Transitions=["
        ListOrthosMessage = "GT Liste_Orthos=["
        ListBankAnglesMessage = "GT Liste_BankAngles=["

        if not self.new_active_leg:
            liste_paths = self.trajFMS.listePaths
        else:
            liste_paths = self.trajFMS.listePaths[self.active_leg:]
            self.new_active_leg = False

        for path in liste_paths:
            ortho, trans = path.segment, path.transition

            if trans is not None:  # si ce n'est pas la dernière transition
                arc1 = trans.list_items[0]  # arc de la transition
                ListTransitionsMessage += 'Transition("'  # message contenant la liste de transition

                if trans.type == 'Flyby':
                    ListTransitionsMessage += 'Flyby"'
                    ListBankAnglesMessage += str(arc1.bank_angle) + ", "
                else:
                    ListTransitionsMessage += 'Flyover"'

                ListTransitionsMessage += ',[Arc(Point(' + str(arc1.centre.x) + ", " + str(arc1.centre.y) + "), "
                ListTransitionsMessage += str(arc1.turn_radius) + ", " + str(arc1.lead_distance) + "), "

                if trans.type == 'Flyby':
                    ListTransitionsMessage = ListTransitionsMessage[:-2] + "]), "
                else:
                    seg = trans.list_items[1]
                    arc2 = trans.list_items[2]
                    ListBankAnglesMessage += "(" + str(arc1.bank_angle) + ", " + str(arc2.bank_angle) + "), "
                    ListTransitionsMessage += "Segment(Point(" + str(seg.start.x) + ", " + str(seg.start.y) + "), "
                    ListTransitionsMessage += "Point(" + str(seg.end.x) + ", " + str(seg.end.y) + ")), "
                    ListTransitionsMessage += 'Arc(Point(' + str(arc2.centre.x) + ", " + str(arc2.centre.y) + "), "
                    ListTransitionsMessage += str(arc2.turn_radius) + ", " + str(arc2.lead_distance) + ")]), "

            else:
                ListTransitionsMessage += ' None]'
                ListBankAnglesMessage += ' None]'

            # Orthos
            s, e = ortho.start, ortho.end
            ListOrthosMessage += "Ortho(Point(" + str(s.x) + ", " + str(s.y) + "), "
            ListOrthosMessage += "Point(" + str(e.x) + ", " + str(e.y) + ")), "

        mes.append(ListTransitionsMessage)
        mes.append(ListOrthosMessage[:-2] + "]")
        mes.append(ListBankAnglesMessage)

        # Paths = ortho + transition
        ListPathMessage = "GT Liste_Paths=["
        for ind in range(len(self.trajFMS.listePaths)):
            if ind == len(self.trajFMS.listePaths)-1:
                ListPathMessage += "Path(Liste_Orthos[" + str(ind) + "], Transition(None, None))]"
            else:
                ListPathMessage += "Path(Liste_Orthos[" + str(ind) + "], Liste_Transitions[" + str(ind) + "]), "
        mes.append(ListPathMessage)

        return mes

    def send_trajectory(self):
        """"Envoi de la trajectoire au groupe SEQ"""
        traj_message = self.traj_To_SEQ()
        print('messageToSEQ : ', traj_message)
        IvySendMsg(traj_message[0])  # envoi de l'aéroport de départ (LAT/LONG) et de la liste des points
        IvySendMsg(traj_message[1])  # envoi de la liste des points
        IvySendMsg(traj_message[2])  # envoi de la liste des segments
        IvySendMsg(traj_message[3])  # envoi de la liste des transitions
        IvySendMsg(traj_message[4])  # envoi de la liste des orthos
        IvySendMsg(traj_message[5])  # envoie la liste des Bank Angles
        IvySendMsg(traj_message[6])  # envoie de la liste des paths

    def receive_SEQ_parameters(self, agent, *data):
        mes = data[0].split(" ")
        time = float(mes[0].strip("Time="))
        xtk = round(float(mes[1].strip("XTK=")), 3)
        tae = round(float(mes[2].strip("TAE="))*RAD2DEG, 3)
        dtwpt = round(float(mes[3].strip("DTWPT=")), 3)
        bank_angle = float(mes[4].strip("BANK_ANGLE_REF="))
        aldtwpt = float(mes[5].strip("ALDTWPT="))
        self.defineSEQParam(xtk, tae, dtwpt, aldtwpt)
        self.update_param_1.emit()

        if self.AC_TAS == 0:
            speed = self.speedPred.TAS
        else:
            speed = self.AC_TAS

        ttwpt = dtwpt * NM2M / (speed * KT2MS) / 60
        self.NextWPTParam["TTWPT"] = ttwpt
        self.update_param_2.emit()
        print("NOUVEAU TTWPT")

    def receive_active_leg(self, agent, *data):
        mes = data[0].split(" ")
        t = float(mes[0].strip("Time="))
        activeLeg = int(mes[1].strip("NumSeqActiveLeg="))
        print("SEQ envoie le séquencement : time=", t, " active leg = ", activeLeg)

        if activeLeg != self.active_leg:
            self.active_leg = activeLeg
            print("Nouveau leg actif :", self.active_leg, " Attente de la liste des legs")
            self.new_active_leg = True
            self.new_leg_signal.emit()

        for i, leg in enumerate(self.ListeFromLegs):
            if activeLeg == leg[1]:
                nextwpt = leg[0]
                course = leg[4]

                if self.AC_TAS == 0:
                    speed = self.speedPred.TAS
                else:
                    speed = self.AC_TAS

                ttwpt = self.SEQParam["DTWPT"] * NM2M / (speed * KT2MS) / 60  # Pour l'instant TAS = 0 donc

                self.defineNextWPTParam(nextwpt, course, ttwpt)
                self.update_param_2.emit()  # envoi du signal

    def get_AP_mode(self, agent, *data):
        """Réception du message du groupe COMM - non utilisée actuellement"""
        mes = data[0].split(" ")
        time = float(mes[0].strip("Time="))
        self.AP_mode = mes[1].strip("AP_State=")
        print("nouveau mode", self.AP_mode)
        self.AP_mode_signal.emit()

    def get_HDG_selected(self, agent, *data):
        """Réception de l'état de l'auto-pilote du simulateur"""
        mes = data[0].split(" ")
        self.mode = mes[0].strip("Mode=")
        self.HDG_selected = mes[1].strip("Val=")
        print("Mode Heading enclenché :", self.mode, self.HDG_selected)
        self.update_mode.emit()
        self.AP_mode_signal.emit()

    def get_depart_airport(self, agent, *data):
        """Réception de l'aéroport de départ"""
        mes = data[0].split(" ")
        lon0, lat0 = mes[0].strip("Lat="), mes[1].strip("Long=")
        print("Aéroport de départ : ", lat0, lon0)
        if False:
            IvySendMsg("GT AC_InitPosition_unknown")