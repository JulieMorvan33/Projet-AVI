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
        textitem = QtWidgets.QGraphicsTextItem(self.items)
        textitem.setFont(font)
        textitem.setPlainText("GS")
        textitem.setPos(-670, -55)
        textitem.setDefaultTextColor(color2)

        self.GStextitem = QtWidgets.QGraphicsTextItem(self.items)
        self.GStextitem.setFont(font)
        self.GStextitem.setPlainText(str(self.simulation.AC_GS))
        self.GStextitem.setPos(-640, -55)
        self.GStextitem.setDefaultTextColor(color3)

        # Ajout de la TAS
        textitem = QtWidgets.QGraphicsTextItem(self.items)
        textitem.setFont(font)
        textitem.setPlainText("TAS")
        textitem.setPos(-500, -55)
        textitem.setDefaultTextColor(color2)

        self.TAStextitem = QtWidgets.QGraphicsTextItem(self.items)
        self.TAStextitem.setFont(font)
        self.TAStextitem.setPlainText(str(SpeedPredictions().TAS))
        self.TAStextitem.setPos(-460, -55)
        self.TAStextitem.setDefaultTextColor(color3)

        textitem = QtWidgets.QGraphicsTextItem(self.items)
        textitem.setFont(font)
        textitem.setPlainText("NM")
        textitem.setPos(70, -30)
        textitem.setDefaultTextColor(color4)

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
        textitem.setPos(50, -55)
        textitem.setDefaultTextColor(color3)

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

    def update_DTWPT(self):
        self.DTWPTtextitem.setPlainText(str(self.simulation.SEQParam["DTWPT"]))

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

class CompassView(QtWidgets.QWidget):
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
        self.compass = QGraphicsCompassItem2(WIDTH, WIDTH, WIDTH*0.5, self.items, self.view)
        self.items.addToGroup(self.compass)

        self.sim.update_aicraft_signal.connect(self.update_hdg)

    def update_hdg(self):
        if not self.sim.USE_IVY:
            ind = int(self.sim.time / self.sim.SIMU_DELAY)
            hdg = self.sim.listeHDG[ind]
        else:
            hdg = self.sim.AC_HDG
        centre_rot = QtCore.QPointF(WIDTH + (WIDTH * 0.5) / 2, WIDTH + (WIDTH * 0.5) / 2)
        self.compass.setTransformOriginPoint(centre_rot)
        self.compass.setRotation(hdg)


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
        self.aircraft.update_position(0,0)
        self.aircraft.setScale(0.01)
        #self.sim.update_signal.connect(self.update_position) # pour visulaiser le mouvement de l'avion
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
        self.simulation.update_aicraft_signal.connect(self.update_ND_items_position)

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

        if not self.simulation.USE_IVY:  # pour une simulation sans bus Ivy
            # create and setup the timer
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.advance)
            self.timer.start(self.simulation.SIMU_DELAY)

        # update the scene anchor in order to be aircarft centered
        # TO DO

    def add_ND_items(self):
        """ Add the static items to the QGraphicsScene, drawn by the view"""
        self.nd_items = QtWidgets.QGraphicsItemGroup()
        self.nd_items.setZValue(TRAJ_Z_VALUE)
        self.scene.addItem(self.nd_items)

        for i in range(1, self.simulation.trajFMS.nbr_waypoints - 1):
            a, b, c = self.simulation.trajFMS.get_transition(i)  # récupère les trois WPT de la transition
            seg_actif = g.Segment(a, b)  # segment d'entrée de la transition
            seg_next = g.Segment(b, c)  # segment de sortie de la transition
            transition_type = b.data["FLY"]

            ######### TEST ##########
            # if i%2==0:
            #     transition_type = "fly_over"
            # else:
            #     transition_type = "fly_by"
            #########################
            if (i == 1): # si première transition
                if transition_type == "fly_by":
                    transition_list = compute_transition_fly_by(seg_actif, seg_next, self.simulation.speedPred.GS)
                elif transition_type == "fly_over":
                    transition_list = compute_transition_fly_over(seg_actif, seg_next, self.simulation.speedPred.GS)
                start_segment = a
                end_segment = transition_list[0].start
            else:
                temp = transition_list[-1].end
                if transition_type == "fly_by":
                    transition_list = compute_transition_fly_by(seg_actif, seg_next, self.simulation.speedPred.GS)
                elif transition_type == "fly_over":
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

            # Affiche le leg
            leg_item = QGraphicsLegsItem(a.x, a.y, b.x, b.y, self.nd_items)
            leg_item.setPen(leg_item.pen)

            # Affiche l'ortho
            leg_item_path = QGraphicsLegsItem(start_segment.x, start_segment.y, end_segment.x, end_segment.y,
                                              self.nd_items)
            leg_item_path.setPen(TRAJ_PEN)

        # Affiche le dernier leg après la dernière transition
        leg_item = QGraphicsLegsItem(b.x, b.y, c.x, c.y, self.nd_items)
        leg_item.setPen(leg_item.pen)

        # Affiche la dernière ortho après la dernière transition
        leg_item_path = QGraphicsLegsItem(transition.end.x, transition.end.y, c.x, c.y, self.nd_items)
        leg_item_path.setPen(TRAJ_PEN)
        self.simulation.trajFMS.add_path(g.Segment(transition.end, c), None)  # ajout de la dernière ortho, None pour
        # la dernière transition

        # Affiche tous les WayPoints
        for point in self.simulation.trajFMS.waypoint_list:
            QGraphicsWayPointsItem(point.x, point.y, self.nd_items)

    def fit_scene_in_view(self):
        #global first_pos_x, first_pos_y
        self.item = QtWidgets.QGraphicsItemGroup()
        print("hello")
        if self.simulation.USE_IVY:
            pos = self.simulation.listeACpositions[int(self.simulation.time / self.simulation.SIMU_DELAY)]
        else:
            pos = self.simulation.AC_X, self.simulation.AC_Y

        self.point = QGraphicsTransitionPoints(pos.x, pos.y, self.nd_items)
        self.nd_items.addToGroup(self.point)
        ind = int(self.simulation.time / self.simulation.SIMU_DELAY)
        first_pos_x, first_pos_y = pos.x*PRECISION_FACTOR, pos.y*PRECISION_FACTOR
        self.nd_items.setTransformOriginPoint(first_pos_x, first_pos_y)
        self.nd_items.setRotation(self.simulation.listeHDG[int(self.simulation.time / self.simulation.SIMU_DELAY)])
        #if first_pos_x != self.point.x and first_pos_y != self.point.y:
        w, h = WIDTH/4*PRECISION_FACTOR, HEIGHT/4*PRECISION_FACTOR
        self.scene.setSceneRect(self.point.x-w/2, self.point.y-h/2, w, h)
        self.view.fitInView(self.view.sceneRect(), QtCore.Qt.KeepAspectRatio)

    def update_ND_items_position(self):
        self.fit_scene_in_view()
        if not self.simulation.USE_IVY :
            time.sleep(self.simulation.SIMU_DELAY)

    def update_ND_items(self):
        # print("UPDATING ITEMS...")
        self.scene.removeItem(self.nd_items)
        print("REMOVE")
        self.add_ND_items()
        print("ELEMENTS ADDED")
        self.fit_scene_in_view()
        print("FIN")
        self.simulation.send_trajectory() # émission du signal pour envoyer la trajectoire réactualisée au groupe SEQ

    @QtCore.pyqtSlot()
    def advance(self):
        """this slot computes the new time at each time out
        To be used only if the Ivy bus isn't used"""
        self.simulation.horloge(None, self.simulation.time + self.simulation.SIMU_DELAY)
        self.simulation.update_signal.emit()


