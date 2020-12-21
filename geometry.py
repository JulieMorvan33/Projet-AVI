"""Geometry classes and utilities."""
import numpy as np
NM2M = 1852
RAD2DEG = 180/np.pi
ALTITUDE = 100 #FL

A = 6378137.0  # Demi grand axe de l'ellipsoide de reference WGS-84 (m)
B = 6356752.3142  # Demi petit axe de l'ellipsoide de reference WGS-84 (m)
F = (A - B) / A  # Aplatissement
E = (F * (2 - F)) ** 0.5  # Excentricite de l'ellipsoide WGS-84

class Point(object):
    """Nm coordinates, with attributes x, y: int"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

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

class WayPoint():
    def __init__(self, lat, long):
        self.lat = lat/RAD2DEG
        self.long = long/RAD2DEG

    def convert(self):
        """La latitude et la longitude sont à rentrer en RADIANS (mettre un moins quand coordonnées en S ou W)
        Retourne les coordonnées (x,y) en mde la projection pseudo-Mercator. Pseudo-Mercator par rapport à Mercator
        prend en compte le cote elliptique de la Terre (si jamais on veut juste Mercator, remplacer a par R dans les
        formules) Merator/Pseudo-Mercator OK si base de donnée juste en Europe (pas trop de déformations)
        /!\ formules pas ok quand latitude = 90° (au pole)"""
        R = 6371007 # Rayon de la Terre
        a = 6378137 # Demi grand axe de l'ellipsoide de reference WGS-84 (m)
        x = a*self.long
        y = a*np.log(np.tan(np.pi/4+self.lat/2))
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

    def det(self,other):
        return self.affix()[0]*other.affix()[1] - self.affix()[1]*other.affix()[0]

class Ortho(Segment): #ça dégage
    """Définit une classe qui hérite de Segment mais qui correspond à la portion
    de segment comprise dans la trajectoire de référence"""
    def __init__(self, start, end):
        super().__init__(start, end)
        self.start = start
        self.end = end

class Transition(object):
    def __init__(self, centre, turnRadius, leadDistance):
        #self.type
        #self.liste objets arcs et segments -> objet arc : center, lead, turn_r, (bi, bo?); segment : les 2 points
        self.centre = centre
        self.turn_radius, self.lead_distance = turnRadius, leadDistance

class Trajectoire_brute(object):
    def __init__(self):
        self.waypoint_list = []  # liste des waypoints
        self.nbr_waypoints = 0  # le nombre de waypoints dans le chemin
        self.transitions_list = [] # liste des objets Transitions
        self.orthos_list = []
        self.bankAnglesList = []

    def __repr__(self):
        return str(self.waypoint_list)

    def add_waypoint(self, waypoint):
        """ajoute un point a la fin du chemin"""
        self.waypoint_list.append(waypoint)
        self.nbr_waypoints += 1

    def distance(self):
        distanceLegsTab = []
        for i in range(len(self.waypoint_list) - 1):
            distanceLegsTab.append(self.waypoint_list[i].distance(self.waypoint_list[i + 1]))
        return distanceLegsTab

    def get_transition(self, ind):
        a = self.waypoint_list[ind - 1]
        b = self.waypoint_list[ind]
        c = self.waypoint_list[ind + 1]
        return a, b, c

class Path(object):
    def __init__(self, segment, transition, speed):
        self.segment = segment
        self.transition = transition
        self.speed = speed
'''
print("wp1 : ", WayPoint(0,1).convert())
print("wp2 : ", WayPoint(0,90).convert())
print("wp3 : ", WayPoint(0,180).convert())
print("wp4 : ", WayPoint(90,0).convert())
print("wp5 : ", WayPoint(180,0).convert())
'''
