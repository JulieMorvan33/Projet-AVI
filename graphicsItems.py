from PyQt5 import QtWidgets
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QTransform, QFont, QFontMetrics
from PyQt5.QtCore import Qt, QPointF
from PyQt5 import QtGui
import numpy as np
from constantParameters import *
from navigationDisplay import *


# Waypoints width
WP_WIDTH = 5
WP_DP = WP_WIDTH/2.
TP_WIDTH = 10
TP_DP = TP_WIDTH/2.
ASW = 2  # ASW stands for Arc Semi Width

# Aicraft width
AC_WIDTH = 10

# Colors
white = QColor(255, 255, 255)
green = QColor(0, 255, 0)

# Pens
P_PEN = QPen(green, WP_DP)
P_PEN.setCosmetic(True)
TRAJ_PEN = QPen(green, ASW)
TRAJ_PEN.setCosmetic(True)
LEG_PEN = QPen(QColor("lightgrey"), ASW)
LEG_PEN.setCosmetic(True)
ROSE_PEN = QPen(white,ASW)
ROSE_PEN.setCosmetic(True)
AC_PEN = QPen(QColor(255, 255, 0))
AC_PEN.setCosmetic(True)

# Brushes
TP_BRUSH = QBrush(QColor("grey"))
WP_BRUSH = QBrush(QColor("red"))
AC_BRUSH = QBrush(QColor("white"))  # for the aicraft

# Coefficient multiplicateur pour les arc. Un cercle complet = 360*16
SP_ANGLE_COEFF = 16

# ROSE
LARGE_GRAD_LONG = 20
TEXT_SIZE = 10

# to get rid of integers and floats distinction in QGraphicsItem
PRECISION_FACTOR = 100


def resize(x):
    return x*PRECISION_FACTOR


class QGraphicsArcItem(QtWidgets.QGraphicsEllipseItem):
    """Classe graphique qui affiche un arc de cercle,
    comme portion du cercle commençant à start_angle et finissant à
    start_angle + span_angle"""
    def __init__(self, start, centre, alpha, turnRadius, det, parent):
        self.det = det  # déterminant entre les deux segments de la transition
        self.set_XY(centre, turnRadius)
        self.w, self.h = resize(turnRadius*2), resize(turnRadius*2)
        super().__init__(self.x, self.y, self.w, self.h, parent)
        self.set_span_angle(alpha)
        self.start_angle = self.set_start_angle(start, centre)

    def paint(self, painter=QPainter(), style=None, widget=None):
        painter.setPen(TRAJ_PEN)
        if self.det < 0:
            painter.drawArc(self.x, self.y, self.w, self.h, self.start_angle, self.span_angle)
        else:
            painter.drawArc(self.x, self.y, self.w, self.h, self.start_angle, -self.span_angle)

    def set_span_angle(self, alpha):
        self.span_angle = alpha * SP_ANGLE_COEFF

    def set_start_angle(self, start, centre):
        beta = np.arctan((start.y - centre.y) / (start.x - centre.x)) * RAD2DEG
        if start.x < centre.x:
            return -(180 + beta) * SP_ANGLE_COEFF
        else:
            return -beta * SP_ANGLE_COEFF

    def set_XY(self, centre, turnRadius):
        self.x = resize(centre.x - turnRadius)
        self.y = resize(centre.y - turnRadius)


class QGraphicsWayPointsItem(QtWidgets.QGraphicsEllipseItem): #QtWidgets.QGraphicsRectItem):
    """Affichage des legs"""
    def __init__(self, x, y, parent):
        super().__init__(resize(x), resize(y), resize(WP_WIDTH), resize(WP_WIDTH), parent)
        self.pen = P_PEN
        self.moveBy(-resize(WP_DP), -resize(WP_DP))

    """Affichage des Way Points
    def __init__(self, x, y, parent):
        self.x, self.y = resize(x), resize(y)
        super().__init__(x, y, WP_WIDTH, WP_WIDTH, parent)
        self.paint(QPainter())

    def paint(self, painter, style=None, widget=None):
        painter.setPen(P_PEN)
        painter.setBrush(WP_BRUSH)

        # copie la transformation due au zoom
        t = painter.transform()
        m11, m22 = t.m11(), t.m22()

        # fixé les coefficients de translation horizontale m11 et verticale m22 à 1
        painter.setTransform(QTransform(1, t.m12(), t.m13(), t.m21(), 1, t.m23(), t.m31(), t.m32(), t.m33()))

        # the item itself will not be scaled, but when the scene is transformed
        # this item still anchor correctly
        painter.translate(-WP_DP, -WP_DP)  # translate de -WP_DP pour s'affranchir de l'épaisseur de l'item
        painter.drawRect(self.x*m11, self.y*m22, WP_WIDTH, WP_WIDTH)

        painter.restore()
    """

class QGraphicsTransitionPoints(QtWidgets.QGraphicsRectItem):
    def __init__(self, x, y, parent):
        super().__init__(x, y, TP_WIDTH, TP_WIDTH, parent)
        self.x, self.y = resize(x), resize(y)
        self.paint(QPainter())

    def paint(self, painter, style=None, widget=None):
        painter.setPen(P_PEN)
        painter.setBrush(TP_BRUSH)
        # copie la transformation due au zoom
        t = painter.transform()
        m11, m22 = t.m11(), t.m22()

        # fixé les coefficients de translation horizontale m11 et verticale m22 à 1
        painter.setTransform(QTransform(1, t.m12(), t.m13(), t.m21(), 1, t.m23(), t.m31(), t.m32(), t.m33()))

        # the item itself will not be scaled, but when the scene is transformed
        # this item still anchor correctly
        painter.translate(-TP_DP, -TP_DP) # translate de -TP_DP pour s'affranchir de l'épaisseur de l'item
        painter.drawRect(self.x * m11, self.y * m22, TP_WIDTH, TP_WIDTH)
        painter.restore()


class QGraphicsImaginaryPoints(QtWidgets.QGraphicsRectItem):
    def __init__(self, x, y, parent):
        super().__init__(x, y, TP_WIDTH, TP_WIDTH, parent)
        self.x, self.y = resize(x), resize(y)

        # self.paint(QPainter())


class QGraphicsLegsItem(QtWidgets.QGraphicsLineItem):
    """Affichage des legs"""
    def __init__(self, x1, y1, x2, y2, parent):
        super().__init__(resize(x1), resize(y1), resize(x2), resize(y2), parent)
        self.pen = LEG_PEN


class AircraftItem(QtWidgets.QGraphicsItemGroup):
    """The view of an aircraft in the GraphicsScene"""

    def __init__(self):
        """AircraftItem constructor, creates the ellipse and adds to the scene"""
        super().__init__(None)
        self.item2 = QtWidgets.QGraphicsEllipseItem()
        image = QtGui.QImage('plane4.png')
        self.pixmap = QtGui.QPixmap.fromImage(image)
        self.item = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap.fromImage(image))
        self.item.setScale(PRECISION_FACTOR)
        self.item2.setBrush(AC_BRUSH)
        self.addToGroup(self.item2)
        self.addToGroup(self.item)

    def update_position(self, x, y):
        # self.item2.setPos(x, y)
        x, y = resize(x), resize(y)
        self.item.setPos(x-51/2, y-51/2)

        # self.item2.setRect(x - AC_WIDTH / 2, y - AC_WIDTH / 2, resize(AC_WIDTH), resize(AC_WIDTH))


class QGraphicsRoseItem(QtWidgets.QGraphicsItemGroup):  # cette classe groupe tous les items composant le compas
    def __init__(self, sim,  x, y, width, parent, view):
        self.x, self.y, self.w = x, y, width
        self.centre = (self.x + self.w / 2, self.y + self.w / 2)
        super().__init__(None)
        self.view = view
        self.parent = parent
        self.sim = sim
        #self.sim.update_aicraft_signal.connect(self.update_select_hdg)
        font = QFont()
        font_metric = QFontMetrics(font)
        font.setWeight(TEXT_SIZE)
        for i in range(12):
            i = i / RAD2DEG * 30
            a_x = self.centre[0] + np.sin(i) * self.w / 2 + np.sin(i) * (LARGE_GRAD_LONG + 2.3 * TEXT_SIZE)
            a_y = self.centre[1] + np.cos(i) * self.w / 2 + np.cos(i) * (LARGE_GRAD_LONG + 2.3 * TEXT_SIZE)
            hdg = QtWidgets.QGraphicsTextItem(self.parent)
            hdg.setFont(font)
            hdg.setTransform(self.view.transform())
            heading = round(i * RAD2DEG / 10)
            hdg.setPlainText(str(heading))
            hdg.setRotation(heading * 10)
            hdg.setPos(a_x, a_y)
            text_width = font_metric.width(str(round(i * RAD2DEG / 10)))
            hdg.moveBy(-np.cos(i) * text_width / 1.2, np.sin(i) * text_width / 1.2)
            hdg.setDefaultTextColor(white)
            self.addToGroup(hdg)
        if self.sim.AP_mode == "'Selected'":
            font.setWeight(3*TEXT_SIZE)
            self.selHDGtextitem = QtWidgets.QGraphicsTextItem(self.parent)
            self.selHDGtextitem.setPos(WIDTH + 180, WIDTH + 460)
            self.selHDGtextitem.setPlainText(str(self.sim.HDG_selected))
            self.selHDGtextitem.setFont(font)
            self.selHDGtextitem.setDefaultTextColor(green)
            self.selHDGtextitem.setTransform(self.view.transform())
            #self.addToGroup(self.selHDGtextitem)


    def paint(self, painter=QPainter(), style=None, widget=None):
        painter.setPen(ROSE_PEN)

        # Large graduations
        for i in range(36):
            i = i / RAD2DEG * 10
            a_x = self.centre[0] + np.sin(i) * self.w / 2
            a_y = self.centre[1] + np.cos(i) * self.w / 2
            b_x = a_x + np.sin(i) * LARGE_GRAD_LONG
            b_y = a_y + np.cos(i) * LARGE_GRAD_LONG
            l = painter.drawLine(a_x, a_y, b_x, b_y)
            self.addToGroup(l)

        # Small graduations
        for i in range(1, 72, 2):
            i = i / RAD2DEG * 5
            a_x = self.centre[0] + np.sin(i) * self.w / 2
            a_y = self.centre[1] + np.cos(i) * self.w / 2
            b_x = a_x + np.sin(i) * LARGE_GRAD_LONG / 2
            b_y = a_y + np.cos(i) * LARGE_GRAD_LONG / 2
            s = painter.drawLine(a_x, a_y, b_x, b_y)
            self.addToGroup(s)

        e = painter.drawEllipse(self.x, self.y, self.w, self.w)
        self.addToGroup(e)

        if self.sim.AP_mode == "'Selected'":
            a_x2 = self.centre[0] + np.sin(float(self.sim.HDG_selected)/RAD2DEG)*self.w / 2
            a_y2 = self.centre[1] + np.cos(float(self.sim.HDG_selected)/RAD2DEG) * self.w / 2
            b_x2 = self.centre[0] #+ np.sin((float(self.sim.HDG_selected)+180) % 360/RAD2DEG) * self.w / 2
            b_y2 = self.centre[1] #+ np.cos((float(self.sim.HDG_selected)+180) % 360/RAD2DEG) * self.w / 2
            self.line = painter.drawLine(a_x2, a_y2, b_x2, b_y2)
            self.addToGroup(self.line)
