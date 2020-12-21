"""Navigation Displays visualization.

This module allows the visualization of the aircraft and its
trajectory on a scalable view"""

import math
from PyQt5 import QtGui, QtCore
from graphicsItems import *
import radarmotion
from calculs import *
import time

# constants
WIDTH = 800  # Initial window width (pixels)
HEIGHT = 350  # Initial window height (pixels)

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
    def __init__(self):
        super().__init__()
        self.scene = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.fitInView(self.view.sceneRect(), QtCore.Qt.KeepAspectRatio)
        # ajout des textes item
        self.items = QtWidgets.QGraphicsItemGroup()
        self.scene.addItem(self.items)
        font = QtGui.QFont()
        color = QColor(255, 255, 0)
        font.setWeight(10)
        name = QtWidgets.QGraphicsTextItem(self.items)
        name.setFont(font)
        name.setPlainText("Navigation Display")
        name.setDefaultTextColor(color)

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

        # Settings
        self.width, self.height = WIDTH, HEIGHT
        self.resize(WIDTH, HEIGHT)

        # create components
        root_layout = QtWidgets.QVBoxLayout(self)
        self.scene = QtWidgets.QGraphicsScene()
        self.view = PanZoomView(self.scene)

        # invert y axis for the view
        self.view.scale(1, -1)

        # modify the scene background
        #self.scene.setBackgroundBrush(QColor('black'))

        self.nd_items = QtWidgets.QGraphicsItemGroup()
        self.scene.addItem(self.nd_items)

        # add the ND elements if already existing  to the graphic scene and then fit it in the view
        if self.simulation.trajFMS.waypoint_list != []:
            self.add_ND_items()
            self.fit_scene_in_view()

        # add the moving items
        #self.moving_items = radarmotion.ItemsMotionManager(self)

        # add components to the root_layout
        root_layout.addWidget(self.view)

        if not (self.simulation.USE_IVY):  # pour une simulation sans bus Ivy
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

            if (i == 1): # si première transition
                #if fly_by / fly_over
                track_change, turn_radius, start_arc, end_arc, centre, lead_distance, bank_angle = compute_transition_fly_over(seg_actif, seg_next)
                start_segment = a
                end_segment = start_arc
            else:
                temp = end_arc
                # if fly_by / fly_over
                track_change, turn_radius, start_arc, end_arc, centre, lead_distance, bank_angle = compute_transition_fly_over(seg_actif, seg_next)
                start_segment = temp
                end_segment = start_arc

            # ajout des objets transitions et orthos dans la trajectoire pour envoi sur le bus IVY
            self.simulation.trajFMS.transitions_list.append(g.Transition(centre, turn_radius, lead_distance))
            self.simulation.trajFMS.bankAnglesList.append(bank_angle) # list de 2 banks pour un fly over ?
            self.simulation.trajFMS.orthos_list.append(g.Ortho(start_segment, end_segment))

            # track change en degré, turn_radius en Nm, start le point d'entrée de la transition
            # end le point de sortie de la transition, centre le centre de l'arc de cercle
            det = seg_actif.det(seg_next)
            if track_change > EPSILON:
                # Affichage des points de start, end, centre (Bi, B0, Bc) pour chaque transition
                QGraphicsTransitionPoints(start_arc.x, start_arc.y, self.nd_items)
                QGraphicsTransitionPoints(end_arc.x, end_arc.y, self.nd_items)
                QGraphicsTransitionPoints(centre.x, centre.y, self.nd_items)

                # Affiche l'arc associé à la transition
                # print("Paramètres arc :", start, centre, " alpha = ", track_change, " turn radius = ", turn_radius)
                item = QGraphicsArcItem(start_arc, centre, track_change, turn_radius, det, self.nd_items)
                item.paint()

            # Affiche le leg
            leg_item = QGraphicsLegsItem(a.x, a.y, b.x, b.y, self.nd_items)
            leg_item.setPen(leg_item.pen)

            # Affiche l'ortho
            leg_item_path = QGraphicsLegsItem(start_segment.x, start_segment.y, end_segment.x, end_segment.y, self.nd_items)
            leg_item_path.setPen(TRAJ_PEN)

        # Affiche le dernier leg après la dernière transition
        leg_item = QGraphicsLegsItem(b.x, b.y, c.x, c.y, self.nd_items)
        leg_item.setPen(leg_item.pen)

        # Affiche la dernière ortho après la dernière transition
        leg_item_path = QGraphicsLegsItem(end_arc.x, end_arc.y, c.x, c.y, self.nd_items)
        leg_item_path.setPen(TRAJ_PEN)
        self.simulation.trajFMS.orthos_list.append(g.Ortho(end_arc, c)) # ajout de la dernière ortho

        # Affiche tous les WayPoints
        for point in self.simulation.trajFMS.waypoint_list:
            QGraphicsWayPointsItem(point.x, point.y, self.nd_items)

    def fit_scene_in_view(self):
        self.view.fitInView(self.view.sceneRect(), QtCore.Qt.KeepAspectRatio)

    def update_ND_items(self):
        print("UPDATING ITEMS...")
        self.scene.removeItem(self.nd_items)
        self.add_ND_items()
        self.fit_scene_in_view()
        time.sleep(0.5)
        self.simulation.send_trajectory() # émission du signal pour envoyer la trajectoire réactualisée au groupe SEQ

    @QtCore.pyqtSlot()
    def advance(self):
        """this slot computes the new time at each time out
        To be used only if the Ivy bus isn't used"""
        self.simulation.horloge(None, self.simulation.time + self.simulation.SIMU_DELAY)
        self.simulation.update_signal.emit()