import geometry as g
import numpy as np

KT2MS = 1852/3600
NM2M = 1852
RAD2DEG = 180/np.pi
GS = 1000*KT2MS #m.s^-1
G = 9.807 #m.s^-2
ALTITUDE = 100 #FL

EPSILON = 5


def compute_transition(seg_actif, seg_next):
	"""Compute track_change, turn radius, seg_actif, seg_next, b_in, b_out, b_center
	associated to the index i transition """

	#Recuperation des points A (debut) et B (fin) du premier segment
	a = seg_actif.start
	b = seg_actif.end

	#calcul du track change entre les deux segments
	track_change = np.arccos((seg_actif.scal(seg_next)) / (seg_actif.norm() * seg_next.norm())) * RAD2DEG  # en degrés
	#print("track_change=", track_change) #en degré

	#calcul bank_angle, turn_radius et lead_distance

	if ALTITUDE>195:
		max_angle = (16 - 25) / (300 - 195) * (ALTITUDE - 195) + 25
		bank_angle = max(5, min(0.5 * track_change, max_angle)) #en DEG
		turn_radius = GS ** 2 / (G * np.tan(bank_angle / RAD2DEG)) / NM2M  # NM
		lead_distance = turn_radius * np.tan(0.5 * track_change / RAD2DEG)  # NM
		if lead_distance > 20:  # NM
			lead_distance = 20  # NM
			turn_radius = lead_distance / np.tan(0.5 * track_change / RAD2DEG)
			bank_angle = max(5, min(np.arctan(GS ** 2) / (G * turn_radius), max_angle))
		#print("lead_distance", lead_distance)
	else :
		max_angle = 25 #DEG
		bank_angle = max(5, min(0.5*track_change,max_angle)) #DEG
		turn_radius = GS**2 / (G*np.tan(bank_angle / RAD2DEG)) / NM2M # NM
		lead_distance = turn_radius * np.tan(0.5 * track_change / RAD2DEG)

	#calcul de b_in et b_out : points de debut et fin de la transition en arc de cercle
	if track_change < EPSILON:
		b_in = b
		b_out = b
		b_center = b

	else:
		norme_act = seg_actif.norm()
		active_track = get_track(seg_actif)  # en RAD
		next_track = get_track(seg_next)
		b_in = calcul_point_de_transition(a, norme_act, lead_distance, active_track)
		b_out = calcul_point_de_transition(b, lead_distance, 0, next_track)

		#calcul de l'angle a_b_bcenter et du point b_center (centre de l'arc de transition)

		d = (turn_radius ** 2 + lead_distance ** 2) ** 0.5
		if seg_actif.det(seg_next) > 0:
			a_b_bc_angle = ((180 + track_change) / 2) / RAD2DEG  # en rad
			b_center = g.Point(b.x + d * np.sin((active_track - a_b_bc_angle)),
						 b.y + d * np.cos((active_track - a_b_bc_angle)))
			bank_angle = - bank_angle

		else:
			a_b_bc_angle = ((180 - track_change) / 2) / RAD2DEG
			b_center = g.Point(b.x - d * np.sin((active_track - a_b_bc_angle)),
						 b.y - d * np.cos((active_track - a_b_bc_angle)))

	return(track_change, turn_radius, b_in, b_out, b_center, lead_distance, bank_angle)


def get_track(segment_courant):
	"""La route est calculee en RAD, entre -pi et pi"""

	# construction segment vertical pour calculer la route.
	seg_calcul = g.Segment(segment_courant.start, g.Point(segment_courant.start.x,segment_courant.start.y + 100))
	track = np.arccos(seg_calcul.scal(segment_courant)/
					  ((seg_calcul.norm())*(segment_courant.norm())))

	#track positive pour un virage a droite
	if seg_calcul.det(segment_courant)>0:
		#print("track=", -track * (RAD2DEG))
		return -track #en RAD
	else :
		#print("track=", track * (RAD2DEG))
		return track #en RAD

def calcul_point_de_transition(origine, dist_segment, lead_dist,track):
	return g.Point(origine.x + (dist_segment - lead_dist) * np.sin(track),
				   origine.y + (dist_segment - lead_dist) * np.cos(track))

