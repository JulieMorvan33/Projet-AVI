"""Geometry classes and utilities."""
import numpy as np
from constantParameters import *
from pyproj import Transformer

# Mercator Projection
A = 6378137.0  # Demi grand axe de l'ellipsoide de reference WGS-84 (m)
B = 6356752.3142  # Demi petit axe de l'ellipsoide de reference WGS-84 (m)
F = (A - B) / A  # Aplatissement
E = (F * (2 - F)) ** 0.5  # Excentricite de l'ellipsoide WGS-84


trans = Transformer.from_crs("epsg:4326", "+proj=merc +zone=32 +ellps=WGS84 +lat_ts=45", always_xy=True)

def det(a, b):
    return a[0] * b[1] - a[1] * b[0]


class Point(object):
    """Nm coordinates, with attributes x, y: int"""

    def __init__(self, x, y, data=None):
        self.x = x
        self.y = y
        self.data = data  # dictionnaire de donnée (course, fly, FLmin, FLmax et CASmax)

    def __repr__(self):
        return "({0.x}, {0.y})".format(self)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __rmul__(self, k):
        return Point(k * self.x, k * self.y)

    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def sca(self, other):
        """sca(Point) return float
        returns the scalar product between self and other"""
        return self.x * other.x + self.y * other.y

    def det(self, other):
        """det(Point) return float
        returns the determinant between self and other"""
        return self.x * other.y - self.y * other.x

    def egal(self, other):
        return self.x == other.x and self.y == other.y

    def distance(self, other):
        return abs(self - other)

    def multiplie(self, scalaire):
        """multiplie les coordonnees du point par un scalaire"""
        return Point(self.x * scalaire, self.y * scalaire)

    def det(self, other):
        return self.x*other.y - self.y*other.x

    def milieu(self, other):
        """trouve le milieu de deux points et renvoie ce nouveau point"""
        new_x = (self.x + other.x) / 2
        new_y = (self.y + other.y) / 2
        return Point(new_x, new_y)

    def seg_dist(self, a, b):
        """Distance from point to segment
        @param a,b @e Point: Description of segment
        @return Distance from Point self to segment [a, b]"""
        ab, ap, bp = b - a, self - a, self - b
        if ab.sca(ap) <= 0:
            return abs(ap)
        elif ab.sca(bp) >= 0:
            return abs(bp)
        else:
            return abs(ab.det(ap)) / abs(ab)


class WayPoint(Point):
    def __init__(self, lat, long):
        self.lat = lat
        self.long = long
        self.x, self.y = self.convert()
        #self.x2, self.y2 = self.convert_without_pyproj()
        super().__init__(self.x, self.y)

    def __repr__(self):
        return "({0.x}, {0.y}, {0.lat}, {0.long})".format(self)

    def convert_without_pyproj(self):
        """La latitude et la longitude sont à rentrer en RADIANS (mettre un moins quand coordonnées en S ou W)
        Retourne les coordonnées (x,y) en mde la projection pseudo-Mercator. Pseudo-Mercator par rapport à Mercator
        prend en compte le cote elliptique de la Terre (si jamais on veut juste Mercator, remplacer a par R dans les
        formules) Merator/Pseudo-Mercator OK si base de donnée juste en Europe (pas trop de déformations)
        /!\ formules pas ok quand latitude = 90° (au pole)"""
        R = 6371007  # Rayon de la Terre
        x = A*self.long/RAD2DEG
        y = A*np.log(np.tan(np.pi/4+self.lat/2/RAD2DEG))
        return x/NM2M, y/NM2M

    def convert(self):
        y, x = trans.transform(self.lat, self.long)
        return x/NM2M, y/NM2M


class Segment(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def norm(self):
        return ((self.end.x - self.start.x)**2+(self.end.y - self.start.y)**2)**0.5

    def affix(self):
        return self.end.x-self.start.x,self.end.y-self.start.y

    def scal(self, other):
        return self.affix()[0]*other.affix()[0] + self.affix()[1]*other.affix()[1]

    def det(self, other):
        return self.affix()[0]*other.affix()[1] - self.affix()[1]*other.affix()[0]

    def intersection(self, other):
        xdiff = (self.start.x - self.end.x, other.start.x - other.end.x)
        ydiff = (self.start.y - self.end.y, other.start.y - other.end.y)

        div = det(xdiff, ydiff)
        if div == 0:
            raise Exception('lines do not intersect')

        d = (self.start.det(self.end), other.start.det(other.end))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return Point(x, y)


class Arc(object):
    def __init__(self, centre, start, end, turn_radius, lead_distance, bank_angle, track_change, sens_virage):
        self.centre = centre
        self.start = start
        self.end = end
        self.turn_radius = turn_radius
        self.lead_distance = lead_distance
        self.bank_angle = bank_angle
        self.track_change = track_change
        self.sens_virage = sens_virage  # >0 à gauche


class Transition(object):
    def __init__(self, type, speed, list_items):
        self.type = type
        self.speed = speed
        self.list_items = list_items


class Path(object):
    def __init__(self, segment, transition):
        self.segment = segment
        self.transition = transition

    def get_speed(self):
        pass


class RefLatPath(object):
    def __init__(self):
        self.listePaths = []
        self.waypoint_list = []  # liste des waypoints
        self.nbr_waypoints = 0  # le nombre de waypoints dans le chemin

    def __repr__(self):
        return "RefLatPath = " + str(self.waypoint_list)

    def add_waypoint(self, waypoint):
        """ajoute un point a la fin du chemin"""
        self.waypoint_list.append(waypoint)
        self.nbr_waypoints += 1

    def get_transition(self, ind):
        a = self.waypoint_list[ind - 1]
        b = self.waypoint_list[ind]
        c = self.waypoint_list[ind + 1]
        return a, b, c

    def add_path(self, segment, transition):
        self.listePaths.append(Path(segment, transition))

    def get_bank_angles(self):
        pass


wpt0 = WayPoint(0, 0)
wptOrly = WayPoint(48.726, 2.365)
wptToulouse = WayPoint(43.629, 1.363)


print("Point 0:", round(wpt0.x*NM2M/1000),"km ", round(wpt0.y*NM2M/1000),"km ", end=" \t ")
print("Orly :", round(wptOrly.x*NM2M/1000),"km ", round(wptOrly.y*NM2M/1000),"km ", end=" \t ")
print("Toulouse :", round(wptToulouse.x*NM2M/1000),"km ", round(wptToulouse.y*NM2M/1000),"km ", end=" \t ")
print("Distance Toulouse-Orly :", round(wptToulouse.distance(wptOrly)),"km ")


