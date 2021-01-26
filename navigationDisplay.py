"""Navigation Displays visualization.

This module allows the visualization of the aircraft and its
trajectory on a scalable view"""

import math
from PyQt5.QtCore import QPoint
from graphicsItems import *
from transitions import *
from constantParameters import WIDTH, HEIGHT, NB_AC_INTER_POS
import time
from predictions import *
from communication import *
from PyQt5 import QtCore


TRAJ_Z_VALUE = 0  # display trajectory items UNDER moving items

POINT_WIDTH = 130
POINT_BRUSH = QBrush(QColor("grey"))


class PanZoomView(QtWidgets.QGraphicsView):
    """An interactive view that supports Pan and Zoom functions"""

    def __init__(self, scene):
        super().__init__(scene)
        self.scene = scene
        # enable anti-aliasing
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        # enable drag and drop of the view
        self.setDragMode(self.ScrollHandDrag)

    def wheelEvent(self, event):
        """Overrides method in QGraphicsView in order to zoom it when mouse scroll occurs"""
        factor = math.pow(1.001, event.angleDelta().y())
        self.zoom_view(factor)

    @QtCore.pyqtSlot(int)
    def zoom_view(self, factor):
        """Updates the zoom factor of the view"""
        self.setTransformationAnchor(self.AnchorUnderMouse)
        super().scale(factor, factor)


class ParamView(QtWidgets.QWidget):
    def __init__(self, sim):
        super().__init__()
        self.scene = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.fitInView(self.view.sceneRect(), QtCore.Qt.KeepAspectRatio)
        self.simulation = sim


        # modify the scene background
        self.scene.setBackgroundBrush(QColor('black'))

        # ajout des textes item
        self.items = QtWidgets.QGraphicsItemGroup()
        self.scene.addItem(self.items)
        font = QtGui.QFont()
        font.setWeight(20)
        color2 = QColor(255, 255, 255)  # blanc
        color3 = QColor(0, 255, 0)  # vert
        color4 = QColor(0, 200, 255)  # bleu
        font.setWeight(10)  # epaisseur du texte

        # Ajout de la ground speed
        GSunittextitem = QtWidgets.QGraphicsTextItem(self.items)
        GSunittextitem.setFont(font)
        GSunittextitem.setPlainText("GS")
        GSunittextitem.setPos(-670, -55)
        GSunittextitem.setDefaultTextColor(color2)

        self.GStextitem = QtWidgets.QGraphicsTextItem(self.items)
        self.GStextitem.setFont(font)
        self.GStextitem.setPlainText(str(self.simulation.AC_GS))
        self.GStextitem.setPos(-640, -55)
        self.GStextitem.setDefaultTextColor(color3)

        # Ajout de la TAS
        TASunittextitem = QtWidgets.QGraphicsTextItem(self.items)
        TASunittextitem.setFont(font)
        TASunittextitem.setPlainText("TAS")
        TASunittextitem.setPos(-500, -55)
        TASunittextitem.setDefaultTextColor(color2)

        self.TAStextitem = QtWidgets.QGraphicsTextItem(self.items)
        self.TAStextitem.setFont(font)
        self.TAStextitem.setPlainText(str(SpeedPredictions().TAS))
        self.TAStextitem.setPos(-460, -55)
        self.TAStextitem.setDefaultTextColor(color3)

        NMtextitem = QtWidgets.QGraphicsTextItem(self.items)
        NMtextitem.setFont(font)
        NMtextitem.setPlainText("NM")
        NMtextitem.setPos(30, -30)
        NMtextitem.setDefaultTextColor(color4)

        if not self.simulation.USE_IVY:
            self.simulation.seq_param_without_IVY()
            self.simulation.next_wpt_param_without_IVY()
            self.simulation.wind_without_IVY()

        # Ajout du next Waypoint
        self.NEXTWPTtextitem = QtWidgets.QGraphicsTextItem(self.items)
        self.NEXTWPTtextitem.setFont(font)
        self.NEXTWPTtextitem.setPlainText(str(self.simulation.NextWPTParam["NEXTWPT"]))
        self.NEXTWPTtextitem.setPos(-100, -55)
        self.NEXTWPTtextitem.setDefaultTextColor(color2)

        # Ajout du next heading Waypoint
        self.HDGtextitem = QtWidgets.QGraphicsTextItem(self.items)
        self.HDGtextitem.setFont(font)
        self.HDGtextitem.setPlainText(str(self.simulation.NextWPTParam["COURSE"]))

        # textitem.setPlainText(str(self.simulation.create_leg_without_Ivy()[4]))
        #textitem.setPos(50, -55)
        #textitem.setDefaultTextColor(color3)

        # Ajout du DTWPT
        self.DTWPTtextitem = QtWidgets.QGraphicsTextItem(self.items)
        self.DTWPTtextitem.setFont(font)
        self.DTWPTtextitem.setPlainText(str(self.simulation.SEQParam["DTWPT"]))
        self.DTWPTtextitem.setPos(0, -30)
        self.DTWPTtextitem.setDefaultTextColor(color3)

        # Ajout du temps
        self.TTWPTtextitem = QtWidgets.QGraphicsTextItem(self.items)
        self.TTWPTtextitem.setFont(font)
        self.TTWPTtextitem.setPlainText(str(self.simulation.NextWPTParam["TTWPT"]))
        self.TTWPTtextitem.setPos(20, -5)
        self.TTWPTtextitem.setDefaultTextColor(color4)

        # Ajout du vent
        self.WINDtextitem = QtWidgets.QGraphicsTextItem(self.items)
        self.WINDtextitem.setFont(font)
        wind = self.simulation.flightParam["WIND"]
        self.WINDtextitem.setPlainText(str(wind[0]) + "/" + str(wind[1]))
        self.WINDtextitem.setPos(-670, -30)
        self.WINDtextitem.setDefaultTextColor(color3)

        if self.simulation.USE_IVY:
            self.simulation.update_param_1.connect(self.update_DTWPT)
            self.simulation.update_param_2.connect(self.update_SEQ_param_display)
            self.simulation.update_flight_param_signal.connect(self.update_wind)
            self.simulation.update_aicraft_signal.connect(self.update_speed_displays)

    def update_DTWPT(self):
        self.DTWPTtextitem.setPlainText(str(round(self.simulation.SEQParam["DTWPT"], 0)))

    def update_wind(self):
        self.WINDtextitem.setPlainText(str(self.simulation.flightParam["WIND"]))

    def update_SEQ_param_display(self):
        print("param ", self.simulation.SEQParam)
        #print("nextwpt in nddisplay ", str(self.simulation.NextWPTParam["NEXTWPT"], self.simulation.SEQParam["DTWPT"]))
        self.NEXTWPTtextitem.setPlainText(str(self.simulation.NextWPTParam["NEXTWPT"]))
        self.HDGtextitem.setPlainText(str(self.simulation.NextWPTParam["COURSE"]))
        self.TTWPTtextitem.setPlainText(str(self.simulation.NextWPTParam["TTWPT"]))

    def update_speed_displays(self):
        self.TAStextitem.setPlainText(str(int(self.simulation.AC_TAS)))
        self.GStextitem.setPlainText(str(int(self.simulation.AC_GS)))


class RoseView(QtWidgets.QWidget):
    def __init__(self, sim):
        super().__init__()
        self.scene = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.fitInView(self.view.sceneRect(), QtCore.Qt.KeepAspectRatio)
        self.sim = sim

        # invert y axis for the view
        self.view.scale(1, -1)

        # modify the scene background
        self.scene.setBackgroundBrush(QColor('black'))

        # ajout du compas
        self.items = QtWidgets.QGraphicsItemGroup()
        self.scene.addItem(self.items)
        self.rose = QGraphicsRoseItem(self.sim, WIDTH, WIDTH, WIDTH*0.5, self.items, self.view)
        self.items.addToGroup(self.rose)

        # Ajout du HDG
        color3 = QColor(0, 255, 0)  # vert
        font = QtGui.QFont()
        font.setWeight(20)
        HDGtextitem = QtWidgets.QGraphicsTextItem(self.items)
        HDGtextitem.setFont(font)
        HDGtextitem.setPlainText("Hello")
        HDGtextitem.setPos(WIDTH, WIDTH)
        HDGtextitem.setDefaultTextColor(color3)
        HDGtextitem.setTransform(self.view.transform())
        self.items.addToGroup(HDGtextitem)

        self.sim.update_aicraft_signal.connect(self.update_hdg)
        self.sim.update_mode.connect(self.add_rose)

    def add_rose(self):
        self.items.removeFromGroup(self.rose)
        self.rose = QGraphicsRoseItem(self.sim, WIDTH, WIDTH, WIDTH * 0.5, self.items, self.view)
        self.items.addToGroup(self.rose)

    def update_hdg(self):
        if not self.sim.USE_IVY:
            ind = int(self.sim.time / self.sim.SIMU_DELAY)
            hdg = self.sim.listeHDG[ind]
        else:
            hdg = self.sim.AC_HDG
        centre_rot = QtCore.QPointF(WIDTH + (WIDTH * 0.5) / 2, WIDTH + (WIDTH * 0.5) / 2)
        self.rose.setTransformOriginPoint(centre_rot)
        self.rose.setRotation(hdg)


class AircraftView(QtWidgets.QWidget):
    def __init__(self, sim):
        super().__init__()
        self.scene = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.sim = sim
        self.view.fitInView(self.view.sceneRect(), QtCore.Qt.KeepAspectRatio)

        # invert y axis for the view
        self.view.scale(1, -1)

        self.aircraft = AircraftItem()
        self.aircraft.update_position(0, 0)
        self.aircraft.setScale(0.01)
        self.scene.addItem(self.aircraft)

    def update_position(self):
        if not self.sim.USE_IVY:  # if Ivy Bus isn't used
            pos = self.sim.listeACpositions[int(self.sim.time / self.sim.SIMU_DELAY)]
            self.aircraft.update_position(pos.x, pos.y)
            time.sleep(self.sim.SIMU_DELAY)
        else:
            self.aircraft.update_position(self.sim.AC_Y, self.sim.AC_X)


class RadarView(QtWidgets.QWidget):
    """An interactive view of the items displayed by a ND,
    with the following attributes:
    - scene: QtWidgets.QGraphicsScene (the graphic scene)
    - view: QtWidgets.QGraphicsView (the view of the scene)
    - moving_items: radarmotion.MovingItemsMotionManager  """

    def __init__(self, simu):
        super().__init__()
        self.simulation = simu  # simulation for test purpose of Ivy parameters changing

        # signals connection
        self.simulation.update_display_signal.connect(self.update_ND_items)
        self.simulation.update_display_signal.connect(self.start_timer)
        self.simulation.update_aicraft_signal.connect(self.update_ND_items_position)
        self.simulation.AP_mode_signal.connect(self.mode_heading)

        # Settings
        self.width, self.height = WIDTH, HEIGHT
        self.resize(WIDTH, HEIGHT)

        # create components
        root_layout = QtWidgets.QVBoxLayout(self)
        self.scene = QtWidgets.QGraphicsScene()
        self.view = PanZoomView(self.scene)

        # invert y axis for the view
        self.view.scale(1, -1)

        self.nd_items = QtWidgets.QGraphicsItemGroup()
        self.scene.addItem(self.nd_items)

        # add the ND elements if already existing to the graphic scene and then fit it in the view
        if self.simulation.trajFMS.waypoint_list != []:
            self.add_ND_items()
            self.fit_scene_in_view()

        # add components to the root_layout
        root_layout.addWidget(self.view)

    def start_timer(self):
        if not(self.simulation.USE_IVY) or self.simulation.AC_SIMULATED:  # pour une simulation sans bus Ivy
            # create and setup the timer
            print("Lancement du timer")
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.advance)
            self.timer.start(self.simulation.SIMU_DELAY)

    def add_ND_items(self):
        """ Add the static items to the QGraphicsScene, drawn by the view"""
        self.nd_items = QtWidgets.QGraphicsItemGroup()
        self.nd_items.setZValue(TRAJ_Z_VALUE)
        self.scene.addItem(self.nd_items)

        for i in range(1, self.simulation.trajFMS.nbr_waypoints - 1):
            a, b, c = self.simulation.trajFMS.get_transition(i)  # récupère les trois WPT de la transition
            seg_actif = g.Segment(a, b)  # segment d'entrée de la transition
            seg_next = g.Segment(b, c)  # segment de sortie de la transition
            if self.simulation.USE_IVY: transition_type = b.data["FLY"]
            else: transition_type = "Flyby"

            ######### TEST ##########
            # if i%2==0:
            #     transition_type = "fly_over"
            # else:
            #     transition_type = "fly_by"
            #########################
            if (i == 1): # si première transition
                if transition_type == "Flyby":
                    transition_list = compute_transition_fly_by(seg_actif, seg_next, self.simulation.speedPred.GS)
                elif transition_type == "Flyover":
                    transition_list = compute_transition_fly_over(seg_actif, seg_next, self.simulation.speedPred.GS)
                start_segment = a
                end_segment = transition_list[0].start
            else:
                temp = transition_list[-1].end
                if transition_type == "Flyby":
                    transition_list = compute_transition_fly_by(seg_actif, seg_next, self.simulation.speedPred.GS)
                elif transition_type == "Flyover":
                    transition_list = compute_transition_fly_over(seg_actif, seg_next, self.simulation.speedPred.GS)
                start_segment = temp
                end_segment = transition_list[0].start

            # ajout des objets transitions et orthos dans la trajectoire pour envoi sur le bus IVY
            self.simulation.trajFMS.add_path(g.Segment(start_segment, end_segment), g.Transition(transition_type, self.simulation.speedPred.GS,
                                                                                                 transition_list))
            # self.simulation.trajFMS.bankAnglesList.append(bank_angle) # list de 2 banks pour un fly over ?

            # track change en degré, turn_radius en Nm, start le point d'entrée de la transition
            # end le point de sortie de la transition, centre le centre de l'arc de cercle

            if transition_list[0].track_change > EPSILON:
                for transition in transition_list:
                    if isinstance(transition, g.Arc):
                        # Affichage des points de start, end, centre (Bi, B0, Bc) pour chaque transition
                        #QGraphicsTransitionPoints(transition.start.x, transition.start.y, self.nd_items)
                        #QGraphicsTransitionPoints(transition.end.x, transition.end.y, self.nd_items)
                        #QGraphicsTransitionPoints(transition.centre.x, transition.centre.y, self.nd_items)

                        # Affiche l'arc associé à la transition
                        # print("Paramètres arc :", start, centre, " alpha = ", track_change, " turn radius = ", turn_
                        # adius)
                        item = QGraphicsArcItem(transition.start, transition.centre, transition.track_change,
                                                transition.turn_radius, transition.sens_virage, self.nd_items)
                        item.paint()
                    elif isinstance(transition, g.Segment):
                        # Affichage segment dans la transition
                        leg_item_transition_segment = QGraphicsLegsItem(transition.start.x, transition.start.y,
                                                                        transition.end.x, transition.end.y,
                                                                        self.nd_items)
                        leg_item_transition_segment.setPen(TRAJ_PEN)

            # Affiche le leg (pas quand la ligne est commentée
            leg_item = QGraphicsLegsItem(a.x, a.y, b.x, b.y, self.nd_items)
            # leg_item.setPen(leg_item.pen)

            # Affiche l'ortho
            leg_item_path = QGraphicsLegsItem(start_segment.x, start_segment.y, end_segment.x, end_segment.y,
                                              self.nd_items)

            leg_item_path.setPen(TRAJ_PEN)

            if self.simulation.AP_mode == "Selected":
                TRAJ_PEN.setStyle(Qt.DashLine)
            # Affichage de la trajectoire en pointillé si mode heading

        # Affiche le dernier leg après la dernière transition
        leg_item = QGraphicsLegsItem(b.x, b.y, c.x, c.y, self.nd_items)
        #leg_item.setPen(leg_item.pen)

        # Affiche la dernière ortho après la dernière transition
        leg_item_path = QGraphicsLegsItem(transition.end.x, transition.end.y, c.x, c.y, self.nd_items)
        leg_item_path.setPen(TRAJ_PEN)
        self.simulation.trajFMS.add_path(g.Segment(transition.end, c), None)  # ajout de la dernière ortho, None pour
        # la dernière transition

        # Affiche tous les WayPoints
        for point in self.simulation.trajFMS.waypoint_list:
            point = QGraphicsWayPointsItem(point.x, point.y, self.nd_items)
            point.setPen(point.pen)

    def mode_heading(self):
        if self.simulation.AP_mode == "'Selected'":
            TRAJ_PEN.setStyle(Qt.DashLine)
            self.scene.removeItem(self.nd_items)
            self.add_ND_items()
            print('mode heading')

    def fit_scene_in_view(self):
        global first_pos_x, first_pos_y
        self.item = QtWidgets.QGraphicsItemGroup()
        if not self.simulation.USE_IVY or self.simulation.AC_SIMULATED:
            pos = self.simulation.listeACpositions[int(self.simulation.time / self.simulation.SIMU_DELAY)]
            pos_x, pos_y = pos.x, pos.y
            ind = int(self.simulation.time / self.simulation.SIMU_DELAY)
        else:
            pos_x, pos_y = self.simulation.AC_X, self.simulation.AC_Y

        print("POSITION DE L'AVION sur le ND: ", pos_x, pos_y)

        self.point = QGraphicsImaginaryPoints(pos_x, pos_y, self.nd_items)
        self.nd_items.addToGroup(self.point)

        first_pos_x, first_pos_y = pos_x * PRECISION_FACTOR, pos_y * PRECISION_FACTOR
        self.nd_items.setTransformOriginPoint(first_pos_x, first_pos_y)

        if not self.simulation.USE_IVY or self.simulation.AC_SIMULATED:
            self.nd_items.setRotation(self.simulation.listeHDG[int(self.simulation.time / self.simulation.SIMU_DELAY)])
        else:
            self.nd_items.setRotation(self.simulation.AC_HDG)

        w, h = WIDTH*PRECISION_FACTOR, HEIGHT*PRECISION_FACTOR
        self.scene.setSceneRect(self.point.x-w/20, self.point.y-h/20, w, h)
        self.view.fitInView(self.view.sceneRect(), QtCore.Qt.KeepAspectRatio)

    def update_ND_items_position(self):
        self.fit_scene_in_view()
        if not(self.simulation.USE_IVY) or self.simulation.AC_SIMULATED:
            print("ON sleep")
            time.sleep(self.simulation.SIMU_DELAY)

    def update_ND_items(self):
        # print("UPDATING ITEMS...")
        self.scene.removeItem(self.nd_items)
        self.add_ND_items()
        print("ND ELEMENTS ADDED")
        self.fit_scene_in_view()
        self.simulation.send_trajectory() # émission du signal pour envoyer la trajectoire réactualisée au groupe SEQ

    @QtCore.pyqtSlot()
    def advance(self):
        """this slot computes the new time at each time out
        To be used only if the Ivy bus isn't used"""
        self.simulation.horloge(None, self.simulation.time + self.simulation.SIMU_DELAY)
        self.simulation.update_aicraft_signal.emit()


