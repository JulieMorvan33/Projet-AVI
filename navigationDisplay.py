"""Navigation Displays visualization.

This module allows the visualization of the aircraft and its
trajectory on a scalable view"""

from graphicsItems import *
from communication import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
import math

TRAJ_Z_VALUE = 0  # afficher la trajectoire sous les autres items

POINT_WIDTH = 130
POINT_BRUSH = QBrush(QColor("grey"))


class PanZoomView(QtWidgets.QGraphicsView):
    """An interactive view that supports Pan and Zoom functions"""

    def __init__(self, scene):
        super().__init__(scene)
        self.scene = scene
        self.setRenderHint(QtGui.QPainter.Antialiasing)  # enable anti-aliasing
        self.setDragMode(self.ScrollHandDrag)  # enable drag and drop of the view

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
    """Vue pour afficher les paramètres"""
    def __init__(self, sim):
        super().__init__()
        self.scene = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.fitInView(self.view.sceneRect(), QtCore.Qt.KeepAspectRatio)
        self.simulation = sim
        self.scene.setBackgroundBrush(QColor('black'))  # modifier le fond de la scène

        # Ajout des textes item
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

        # Ajout du texte "NM"
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
        self.HDGtextitem.setPlainText(str(int(self.simulation.NextWPTParam["COURSE"])))
        self.HDGtextitem.setPos(0, -55)
        self.HDGtextitem.setDefaultTextColor(color3)

        # Ajout du DTWPT
        self.DTWPTtextitem = QtWidgets.QGraphicsTextItem(self.items)
        self.DTWPTtextitem.setFont(font)
        self.DTWPTtextitem.setPlainText(str(int(self.simulation.SEQParam["DTWPT"])))
        self.DTWPTtextitem.setPos(0, -30)
        self.DTWPTtextitem.setDefaultTextColor(color3)

        # Ajout du temps
        self.TTWPTtextitem = QtWidgets.QGraphicsTextItem(self.items)
        self.TTWPTtextitem.setFont(font)
        self.TTWPTtextitem.setPlainText(str(round(self.simulation.NextWPTParam["TTWPT"],1)))
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
        self.DTWPTtextitem.setPlainText(str(int(self.simulation.SEQParam["DTWPT"])))

    def update_wind(self):
        self.WINDtextitem.setPlainText(str(self.simulation.flightParam["WIND"]))

    def update_SEQ_param_display(self):
        print("param ", self.simulation.SEQParam)
        self.NEXTWPTtextitem.setPlainText(str(self.simulation.NextWPTParam["NEXTWPT"]))
        self.HDGtextitem.setPlainText(str(int(self.simulation.NextWPTParam["COURSE"])))
        self.TTWPTtextitem.setPlainText(str(round(self.simulation.NextWPTParam["TTWPT"],1)))

    def update_speed_displays(self):
        self.TAStextitem.setPlainText(str(int(self.simulation.AC_TAS)))
        self.GStextitem.setPlainText(str(int(self.simulation.AC_GS)))


class RoseView(QtWidgets.QWidget):
    """Vue qui permet d'afficher la rose"""
    def __init__(self, sim):
        super().__init__()
        self.scene = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.fitInView(self.view.sceneRect(), QtCore.Qt.KeepAspectRatio)
        self.sim = sim

        self.view.scale(1, -1)  # inverser l'axe des y pour la vue

        self.scene.setBackgroundBrush(QColor('black'))  # modifier le fond de la scène

        # Ajout du compas
        self.items = QtWidgets.QGraphicsItemGroup()
        self.scene.addItem(self.items)
        self.rose = QGraphicsRoseItem(self.sim, WIDTH, WIDTH, WIDTH*0.5, self.items, self.view)
        self.items.addToGroup(self.rose)

        # Ajout du heading courant en bas à droite de la rose
        color3 = QColor(0, 255, 0)  # vert
        font = QtGui.QFont()
        font.setWeight(20)
        self.HDGtextitem = QtWidgets.QGraphicsTextItem(self.items)
        self.HDGtextitem.setFont(font)
        self.HDGtextitem.setPlainText(str(int(self.sim.AC_HDG))+"°")
        self.HDGtextitem.setPos(WIDTH, WIDTH)
        self.HDGtextitem.setDefaultTextColor(color3)
        self.HDGtextitem.setTransform(self.view.transform())
        self.items.addToGroup(self.HDGtextitem)

        # Ajout du heading sélecté
        font = QFont()
        font.setWeight(30)
        self.selHDGtextitem = QtWidgets.QGraphicsTextItem(self.items)
        self.selHDGtextitem.setPos(WIDTH + 180, WIDTH + 460)
        self.selHDGtextitem.setPlainText('')
        self.selHDGtextitem.setFont(font)
        self.selHDGtextitem.setDefaultTextColor(green)
        self.selHDGtextitem.setTransform(self.view.transform())
        self.items.addToGroup(self.selHDGtextitem)

        # Affichage du XTK en bas à droite de la rose
        self.XTKtextitem = QtWidgets.QGraphicsTextItem(self.items)
        self.XTKtextitem.setFont(font)
        self.XTKtextitem.setPlainText(str(int(self.sim.SEQParam["XTK"]))+"NM")
        self.XTKtextitem.setPos(WIDTH+11*WIDTH/24, WIDTH)
        self.XTKtextitem.setDefaultTextColor(color3)
        self.XTKtextitem.setTransform(self.view.transform())
        self.items.addToGroup(self.XTKtextitem)

        # Mise à jour du HDG et de la XTK
        self.sim.update_aicraft_signal.connect(self.update_hdg)
        self.sim.update_aicraft_signal.connect(self.update_xtk)

        self.sim.update_mode.connect(self.add_rose)

    def add_rose(self):
        """Ajouter la rose / l'affichage change en fonction du mode de l'auto-pilote"""
        self.items.removeFromGroup(self.rose)
        if self.sim.mode == "SelectedHeading":  # s'il y a un heading sélecté
            self.items.removeFromGroup(self.selHDGtextitem)
            self.selHDGtextitem.setPlainText(str(self.sim.HDG_selected))
            self.items.addToGroup(self.selHDGtextitem)
        else:  # si mode managé
            self.items.removeFromGroup(self.selHDGtextitem)
            self.selHDGtextitem.setPlainText('')
            self.items.addToGroup(self.selHDGtextitem)
        self.rose = QGraphicsRoseItem(self.sim, WIDTH, WIDTH, WIDTH * 0.5, self.items, self.view)
        self.items.addToGroup(self.rose)

    def update_hdg(self):
        """Mise à jour la rotation de la rose"""
        if not self.sim.USE_IVY or self.sim.AC_SIMULATED:  # si tests en interne
            ind = int(self.sim.time / self.sim.SIMU_DELAY)
            hdg = self.sim.listeHDG[ind]
        else:
            hdg = self.sim.AC_HDG
        centre_rot = QtCore.QPointF(WIDTH + (WIDTH * 0.5) / 2, WIDTH + (WIDTH * 0.5) / 2)
        self.rose.setTransformOriginPoint(centre_rot)
        self.rose.setRotation(hdg)
        self.HDGtextitem.setPlainText(str(int(hdg)) + "°")

    def update_xtk(self):
        """Mise à jour du xtk"""
        self.XTKtextitem.setPlainText(str(round(self.sim.SEQParam["XTK"], 1)) + "NM")


class AircraftView(QtWidgets.QWidget):
    """Vue permettant l'affichage de l'avion"""
    def __init__(self, sim):
        super().__init__()
        self.scene = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.sim = sim
        self.view.fitInView(self.view.sceneRect(), QtCore.Qt.KeepAspectRatio)

        self.view.scale(1, -1)  # inverser l'axe des y

        self.aircraft = AircraftItem()
        self.aircraft.update_position(0, 0)
        self.aircraft.setScale(0.01)
        self.scene.addItem(self.aircraft)


class RadarView(QtWidgets.QWidget):
    """An interactive view of the items displayed by a ND,
    with the following attributes:
    - scene: QtWidgets.QGraphicsScene (the graphic scene)
    - view: QtWidgets.QGraphicsView (the view of the scene)
    - moving_items: radarmotion.MovingItemsMotionManager  """

    def __init__(self, simu):
        super().__init__()
        self.simulation = simu

        # Connections aux signaux
        self.simulation.update_display_signal.connect(self.update_ND_items)
        self.simulation.update_display_signal.connect(self.start_timer)
        self.simulation.update_aicraft_signal.connect(self.update_ND_items_position)
        self.simulation.AP_mode_signal.connect(self.mode_heading)

        # Paramètres
        self.width, self.height = WIDTH, HEIGHT
        self.resize(WIDTH, HEIGHT)

        # Création des composants
        root_layout = QtWidgets.QVBoxLayout(self)
        self.scene = QtWidgets.QGraphicsScene()
        self.view = PanZoomView(self.scene)

        self.view.scale(1, -1)  # inverser l'axe des y

        self.nd_items = QtWidgets.QGraphicsItemGroup()
        self.waypoint_group = QtWidgets.QGraphicsItemGroup()
        self.list_waypoint_item = []
        self.scene.addItem(self.nd_items)
        self.scene.addItem(self.waypoint_group)

        if self.simulation.trajFMS.waypoint_list != []:  # ajouter les éléments du ND déjà existants à la scène et
            # les ajouter à la vue
            self.add_ND_items()
            self.fit_scene_in_view()

        if not self.simulation.USE_IVY:  # Si utilisation du bus Ivy : nécessité d'un timer
            print("Lancement du timer")
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.advance)
            self.timer.start(self.simulation.SIMU_DELAY)

        root_layout.addWidget(self.view)  # ajouter composants à la root_layer

    def start_timer(self):
        """Lancement du timer sans bus Ivy"""
        if not self.simulation.USE_IVY or self.simulation.AC_SIMULATED:
            print("Lancement du timer")
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.advance)
            self.timer.start(self.simulation.SIMU_DELAY)

    def update_waypoints_items_rotation(self, hdg):
        """Mettre à jour les rotations des items"""
        for item in self.list_waypoint_item:
            item.textitem.setRotation(hdg)

    def display_waypoints(self):
        """Afficher les waypoints"""
        self.waypoint_group = QtWidgets.QGraphicsItemGroup()
        self.scene.addItem(self.waypoint_group)
        for point in self.simulation.trajFMS.waypoint_list:
            pointItem = QGraphicsWayPointsItem(point.x, point.y, self.waypoint_group, point.data['Name'], self.view,
                                               self.simulation.AC_HDG, self.simulation.ZOOM)
            self.list_waypoint_item.append(pointItem)
            pointItem.setPen(pointItem.pen)

    def add_ND_items(self):
        """ Ajouter les items statique à la QGraphicsScene"""
        self.nd_items = QtWidgets.QGraphicsItemGroup()
        self.nd_items.setZValue(TRAJ_Z_VALUE)
        self.scene.addItem(self.nd_items)

        for i in range(1, self.simulation.trajFMS.nbr_waypoints - 1):
            a, b, c = self.simulation.trajFMS.get_transition(i)  # récupère les trois WPTs de la transition
            seg_actif = g.Segment(a, b)  # segment d'entrée de la transition
            seg_next = g.Segment(b, c)  # segment de sortie de la transition
            if self.simulation.USE_IVY: transition_type = b.data["FLY"]
            else:
                transition_type = "Flyby"

            if i == 1:  # si première transition
                if transition_type == "Flyby":
                    transition_list = compute_transition_fly_by(seg_actif, seg_next, self.simulation.speedPred.TAS)
                elif transition_type == "Flyover":
                    transition_list = compute_transition_fly_over(seg_actif, seg_next, self.simulation.speedPred.TAS)
                start_segment = a
                end_segment = transition_list[0].start
            else:
                temp = transition_list[-1].end  # Récupération du point de fin de la dernière transition afin de
                # réaliser la liason sous forme de segment avec la prochaine transition
                if transition_type == "Flyby":
                    transition_list = compute_transition_fly_by(seg_actif, seg_next, self.simulation.speedPred.TAS)
                elif transition_type == "Flyover":
                    transition_list = compute_transition_fly_over(seg_actif, seg_next, self.simulation.speedPred.TAS)
                start_segment = temp
                end_segment = transition_list[0].start

            # Ajout des objets transitions et orthos dans la trajectoire pour envoi sur le bus IVY
            self.simulation.trajFMS.add_path(g.Segment(start_segment, end_segment),
                                             g.Transition(transition_type, self.simulation.speedPred.TAS,
                                                          transition_list))

            if transition_list[0].track_change > EPSILON:  # s'il ne s'agit pas d'une transition en ligne droite
                for transition in transition_list:
                    if isinstance(transition, g.Arc):
                        # Affichage de l'arc dans la transition
                        leg_item_transition_arc = QGraphicsArcItem(transition.start, transition.centre,
                                                                   transition.track_change, transition.turn_radius,
                                                                   transition.sens_virage, self.nd_items)
                        leg_item_transition_arc.paint()
                    elif isinstance(transition, g.Segment):
                        # Affichage segment dans la transition
                        leg_item_transition_segment = QGraphicsLegsItem(transition.start.x, transition.start.y,
                                                                        transition.end.x, transition.end.y,
                                                                        self.nd_items)
                        leg_item_transition_segment.setPen(TRAJ_PEN)

            # Affiche l'ortho
            leg_item_path = QGraphicsLegsItem(start_segment.x, start_segment.y, end_segment.x, end_segment.y,
                                              self.nd_items)

            leg_item_path.setPen(TRAJ_PEN)

            if self.simulation.mode == "SelectedHeading":  # Si l'auto-pilote est en mode sélecté
                TRAJ_PEN.setStyle(Qt.DashLine)  # affichage de la trajectoire en pointillés

        # Affiche le dernier leg après la dernière transition
        leg_item = QGraphicsLegsItem(b.x, b.y, c.x, c.y, self.nd_items)

        # Affiche la dernière ortho après la dernière transition
        leg_item_path = QGraphicsLegsItem(transition_list[-1].end.x,  transition_list[-1].end.y, c.x, c.y, self.nd_items)
        leg_item_path.setPen(TRAJ_PEN)
        self.simulation.trajFMS.add_path(g.Segment(transition_list[-1].end, c), None)  # ajout de la dernière ortho,
        # None pour la dernière transition

    def mode_heading(self):
        """Fonction qui change l'apparence de la trajectoire affichée en fonction du mode de l'AP"""
        if self.simulation.mode == "SelectedHeading":
            TRAJ_PEN.setStyle(Qt.DashLine)
            print('mode heading')
        else:
            TRAJ_PEN.setStyle(Qt.SolidLine)
            print('mode nav')
        self.scene.removeItem(self.nd_items)
        self.add_ND_items()

    def fit_scene_in_view(self):
        """Fait suivre la caméra centrée sur l'avion et permet le zoom"""
        if not self.simulation.USE_IVY or self.simulation.AC_SIMULATED:
            ind = int(self.simulation.time / self.simulation.SIMU_DELAY)
            pos = self.simulation.listeACpositions[ind]
            pos_x, pos_y = pos.x, pos.y
        else:
            pos_x, pos_y = self.simulation.AC_X, self.simulation.AC_Y

        print("POSITION DE L'AVION sur le ND: ", round(pos_x, 1), round(pos_y, 1), round(pos_x*NM2M), round(pos_y)*NM2M)

        self.nd_items.setTransformOriginPoint(pos_x * PRECISION_FACTOR, pos_y * PRECISION_FACTOR)
        self.waypoint_group.setTransformOriginPoint(pos_x * PRECISION_FACTOR, pos_y * PRECISION_FACTOR)

        if not self.simulation.USE_IVY or self.simulation.AC_SIMULATED:
            self.nd_items.setRotation(self.simulation.listeHDG[ind])
            self.waypoint_group.setRotation(self.simulation.listeHDG[ind])
            self.update_waypoints_items_rotation(self.simulation.listeHDG[ind])
        else:
            self.nd_items.setRotation(self.simulation.AC_HDG)
            self.waypoint_group.setRotation(self.simulation.AC_HDG)
            self.update_waypoints_items_rotation(self.simulation.AC_HDG)

        w, h = WIDTH*PRECISION_FACTOR*self.simulation.ZOOM, HEIGHT*PRECISION_FACTOR*self.simulation.ZOOM
        self.scene.setSceneRect(pos_x*PRECISION_FACTOR-w/2, pos_y*PRECISION_FACTOR-h/2, w, h)
        self.view.fitInView(self.view.sceneRect(), QtCore.Qt.KeepAspectRatio)

    def update_ND_items_position(self):
        """Mise à jour de la position des items"""
        self.fit_scene_in_view()
        if not self.simulation.USE_IVY or self.simulation.AC_SIMULATED:
            print("ON sleep")
            time.sleep(self.simulation.SIMU_DELAY)

    def update_ND_items(self):
        """Mettre à jour les items (ajout/suppression d'éléments)"""
        self.scene.removeItem(self.nd_items)
        self.scene.removeItem(self.waypoint_group)
        self.list_waypoint_item = []
        self.add_ND_items()
        self.display_waypoints()
        print("ND ELEMENTS ADDED")
        self.fit_scene_in_view()
        self.simulation.send_trajectory()  # émission du signal pour envoyer la trajectoire réactualisée au groupe SEQ

    @QtCore.pyqtSlot()
    def advance(self):
        """this slot computes the new time at each time out
        To be used only if the Ivy bus isn't used"""
        self.simulation.horloge(None, self.simulation.time + self.simulation.SIMU_DELAY)
        self.simulation.update_aicraft_signal.emit()


